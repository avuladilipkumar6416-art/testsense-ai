# agent/analyzer_agent.py
import os
import sys
import io
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
from typing import Optional, Dict, Any

load_dotenv()

# Silence noisy third-party loggers
_NOISY_LOGGERS = [
    "google", "google.genai", "google.auth",
    "google.genai._api_client", "google_genai._api_client",
    "httpx", "httpcore", "tenacity", "urllib3",
]
for _name in _NOISY_LOGGERS:
    logging.getLogger(_name).setLevel(logging.CRITICAL)
    logging.getLogger(_name).propagate = False

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a senior test failure analysis expert with deep knowledge of Selenium automation.
Your goal is to accurately classify test failures and provide actionable fixes.

Use tools ONLY when you genuinely need more information to classify the failure.
Base your verdict on the error message first, log file second.
Never contradict a clear error message based on log content alone.

After investigating, respond ONLY with this exact JSON — no extra text:
{"failure_type":"TEST_ISSUE or REAL_BUG or ENVIRONMENT_ISSUE","root_cause":"one sentence","is_real_bug":true or false,"confidence":0-100,"suggested_fix":"one sentence","severity":"LOW or MEDIUM or HIGH"}

Classification rules:
- TEST_ISSUE: locator changed, stale element, bad test data, timing, wrong assertion value
- REAL_BUG: app logic wrong, API error, feature broken, wrong data from backend
- ENVIRONMENT_ISSUE: DB down, network failure, infrastructure, browser/driver version mismatch
- If ambiguous between categories, pick the most likely and set confidence below 70%"""


class TestFailureAnalyzerAgent:
    """
    ReAct agent that analyzes Selenium test failures.
    Uses Gemini as primary LLM, falls back to Ollama if unavailable.

    Usage:
        agent = TestFailureAnalyzerAgent()
        verdict = agent.analyze({
            "test_name": "LoginTest",
            "error_type": "NoSuchElementException",
            "error_message": "Unable to locate element: #login-btn",
            "log_path": "reports/logs/login.log",
            "screenshot_path": "reports/screenshots/login.png",
            "environment": "staging"
        })
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
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(
                model="gemini-3.6-flash",
                google_api_key=os.getenv("GEMINI_API_KEY"),
                temperature=0.1
            )
            old_stderr, sys.stderr = sys.stderr, io.StringIO()
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

    def _format_input(self, ctx: Dict) -> str:
        """Format failure context dict into agent input text."""
        return f"""
Test Name: {ctx.get('test_name', 'Unknown')}
Error Type: {ctx.get('error_type', 'Unknown')}
Error Message: {ctx.get('error_message', 'Unknown')}
Stack Trace: {ctx.get('stack_trace', 'Not available')}
Log File Path: {ctx.get('log_path', 'Not available')}
Screenshot Path: {ctx.get('screenshot_path', 'Not available')}
Browser: {ctx.get('browser', 'Unknown')}
Environment: {ctx.get('environment', 'Unknown')}
"""

    def _parse_output(self, output: str) -> Optional[Dict]:
        """Extract and parse JSON from agent output."""
        try:
            if "```" in output:
                output = output[output.find("{"):output.rfind("}") + 1]
            start = output.find('{')
            end = output.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = output[start:end]
                result = json.loads(json_str)
                required = ['failure_type', 'root_cause', 'is_real_bug',
                            'confidence', 'suggested_fix', 'severity']
                if all(k in result for k in required):
                    return result
                else:
                    logger.error("Agent response missing required keys")
                    return None
            else:
                logger.error(f"No JSON found in output: {output[:200]}")
                return None
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}")
            return None

    def analyze(self, failure_context: Dict[str, Any]) -> Optional[Dict]:
        """
        Analyze a test failure and return a structured verdict.

        Args:
            failure_context: Dict with test_name, error_type, error_message,
                           stack_trace, log_path, screenshot_path,
                           browser, environment.

        Returns:
            Dict with failure_type, root_cause, is_real_bug,
            confidence, suggested_fix, severity — or None if failed.
        """
        logger.info(f"Analyzing: {failure_context.get('test_name', 'Unknown')}")

        input_text = self._format_input(failure_context)

        try:
            result = self.agent.invoke({
                "messages": [HumanMessage(content=input_text)]
            })
        except Exception as e:
            error_str = str(e)
            if any(code in error_str for code in ["503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED"]):
                self._switch_to_ollama()
                try:
                    result = self.agent.invoke({
                        "messages": [HumanMessage(content=input_text)]
                    })
                except Exception as e2:
                    logger.error(f"Ollama also failed: {e2}")
                    return None
            else:
                logger.error(f"Analysis failed: {e}")
                return None

        last_message = result["messages"][-1]
        if isinstance(last_message.content, list):
            output = " ".join(
                item.get("text", "") if isinstance(item, dict) else str(item)
                for item in last_message.content
            )
        else:
            output = last_message.content

        verdict = self._parse_output(output)
        if verdict:
            logger.info(f"Done — {verdict['failure_type']} (confidence: {verdict['confidence']}%)")
        return verdict


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    agent = TestFailureAnalyzerAgent()

    verdict = agent.analyze({
        "test_name": "LoginTest.testValidLogin",
        "error_type": "NoSuchElementException",
        "error_message": "Unable to locate element: #login-btn",
        "stack_trace": "at LoginPage.clickLoginButton(LoginPage.java:47)",
        "log_path": "test_sample.log",
        "screenshot_path": "fake_screenshot.png",
        "browser": "Chrome 120",
        "environment": "staging"
    })

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