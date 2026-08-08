import os
import json
import logging
import warnings
warnings.filterwarnings("ignore")

import truststore
truststore.inject_into_ssl()

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

load_dotenv()


class _SuppressNoiseFilter(logging.Filter):
    """Filter out noisy third-party log lines."""
    SUPPRESS = ["Retrying", "AFC is enabled", "HTTP Request"]

    def filter(self, record):
        msg = record.getMessage()
        return not any(phrase in msg for phrase in self.SUPPRESS)


# Apply filter to root logger — catches everything
logging.root.addFilter(_SuppressNoiseFilter())

# Also silence by logger name as a second layer
for _name in ["google", "google.genai", "google.auth", "google.genai._api_client",
              "httpx", "httpcore", "tenacity", "urllib3"]:
    logging.getLogger(_name).setLevel(logging.CRITICAL)


logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a senior test failure analysis expert.
Your goal is to classify test failures accurately using available tools.

After investigating, respond ONLY with this exact JSON:
{"failure_type":"TEST_ISSUE or REAL_BUG or ENVIRONMENT_ISSUE","root_cause":"one sentence","is_real_bug":true or false,"confidence":0-100,"suggested_fix":"one sentence","severity":"LOW or MEDIUM or HIGH"}

Classification rules:
- TEST_ISSUE: locator changed, wrong selector, timing, bad test data
- REAL_BUG: application logic wrong, API error, feature broken
- ENVIRONMENT_ISSUE: DB down, network failure, infrastructure problem

Respond ONLY with the JSON. No extra text."""


class TestFailureAnalyzerAgent:
    """
    ReAct agent that analyzes Selenium test failures.
    Uses Gemini as primary LLM, falls back to Ollama if unavailable.
    Create one instance, call analyze() for each failure.
    """

    def __init__(self):
        self.tools = self._build_tools()
        self.llm = self._create_llm()
        self.agent = create_react_agent(
            self.llm,
            self.tools,
            prompt=SYSTEM_PROMPT
        )
        logger.info("TestFailureAnalyzerAgent initialized")

    def _create_llm(self):
        """Try Gemini first, fall back to Ollama if unavailable."""
        import sys
        import io
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(
                model="gemini-3.6-flash",
                google_api_key=os.getenv("GEMINI_API_KEY"),
                temperature=0.1
            )
            # Suppress stderr during the test call
            old_stderr = sys.stderr
            sys.stderr = io.StringIO()
            try:
                llm.invoke("hi")
            finally:
                sys.stderr = old_stderr

            logger.info("LLM: Gemini gemini-3.6-flash (primary)")
            return llm
        except Exception:
            logger.warning("Gemini unavailable — using Ollama (local)")
            from langchain_ollama import ChatOllama
            return ChatOllama(model="llama3.2", temperature=0.1)

    def _switch_to_ollama(self):
        """Switch agent to Ollama mid-run."""
        logger.warning("Gemini unavailable — switching to Ollama (local)")
        from langchain_ollama import ChatOllama
        self.llm = ChatOllama(model="llama3.2", temperature=0.1)
        self.agent = create_react_agent(self.llm, self.tools, prompt=SYSTEM_PROMPT)

    def _build_tools(self) -> list:

        @tool
        def read_log_file(file_path: str) -> str:
            """
            Reads a test execution log file.
            Use when you need to understand what happened during
            test execution — what pages loaded, what errors occurred.
            """
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return content if content.strip() else "Log file is empty."
            except FileNotFoundError:
                return f"Log file not found at: {file_path}"
            except Exception as e:
                return f"Error reading log: {str(e)}"

        @tool
        def read_screenshot(screenshot_path: str) -> str:
            """
            Reads a test failure screenshot.
            Use when you need visual context about what was on
            screen when the test failed.
            """
            from pathlib import Path
            try:
                path = Path(screenshot_path)
                if not path.exists():
                    return f"Screenshot not found: {screenshot_path}"
                size = path.stat().st_size
                return f"Screenshot loaded: {path.name}, {size} bytes."
            except Exception as e:
                return f"Error reading screenshot: {str(e)}"

        return [read_log_file, read_screenshot]

    def analyze(self, failure_text: str) -> dict:
        """
        Analyze a test failure and return a structured verdict.
        Falls back to Ollama automatically if Gemini fails mid-analysis.

        Args:
            failure_text: Full failure description including error type,
                         message, log path, screenshot path, environment.

        Returns:
            Dict with failure_type, root_cause, is_real_bug,
            confidence, suggested_fix, severity — or None if failed.
        """
        logger.info("Analyzing failure...")

        try:
            result = self.agent.invoke({
                "messages": [HumanMessage(content=failure_text)]
            })

        except Exception as e:
            error_str = str(e)
            if any(code in error_str for code in ["503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED"]):
                self._switch_to_ollama()
                try:
                    result = self.agent.invoke({
                        "messages": [HumanMessage(content=failure_text)]
                    })
                except Exception as e2:
                    logger.error(f"Ollama also failed: {e2}")
                    return None
            else:
                logger.error(f"Analysis failed: {e}")
                return None

        try:
            last_message = result["messages"][-1]

            if isinstance(last_message.content, list):
                output = " ".join(
                    item.get("text", "") if isinstance(item, dict) else str(item)
                    for item in last_message.content
                )
            else:
                output = last_message.content

            # Strip markdown code fences if present
            if "```" in output:
                output = output[output.find("{"):output.rfind("}") + 1]

            verdict = json.loads(output)
            logger.info(f"Done — {verdict['failure_type']} (confidence: {verdict['confidence']}%)")
            return verdict

        except json.JSONDecodeError:
            logger.error("Agent returned invalid JSON")
            return None
        except Exception as e:
            logger.error(f"Failed to parse verdict: {e}")
            return None


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    agent = TestFailureAnalyzerAgent()

    failure = """
    Test Name: LoginTest.testValidLogin
    Error Type: NoSuchElementException
    Error Message: Unable to locate element: #login-btn
    Stack Trace:
        at LoginPage.clickLoginButton(LoginPage.java:47)
        at LoginTest.testValidLogin(LoginTest.java:23)
    Log file: test_sample.log
    Screenshot: fake_screenshot.png
    Environment: staging
    """

    verdict = agent.analyze(failure)

    if verdict:
        print("\n--- VERDICT ---")
        print(f"Type:       {verdict['failure_type']}")
        print(f"Cause:      {verdict['root_cause']}")
        print(f"Is bug:     {verdict['is_real_bug']}")
        print(f"Confidence: {verdict['confidence']}%")
        print(f"Fix:        {verdict['suggested_fix']}")
        print(f"Severity:   {verdict['severity']}")
    else:
        print("Analysis failed")