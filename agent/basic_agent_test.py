# agent/basic_agent_test.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
load_dotenv()

@tool
def read_log_file(file_path: str) -> str:
    """
    Read a test execution log file.
    Use when you need to understand what happened during test execution.
    """
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return f"Log file not found: {file_path}. Simulated content: Test started at 10:30, element #login-btn not found after 10s."

tools = [read_log_file]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.1
)

system_prompt = """You are an expert test failure analyzer. Use the available tools to investigate failures.

Only call tools if you genuinely need more information to make a decision.

When you have enough information, respond with ONLY this JSON format:
{"failure_type": "TEST_ISSUE|REAL_BUG|ENVIRONMENT_ISSUE", "root_cause": "string", "is_real_bug": boolean, "confidence": 0-100, "suggested_fix": "string", "severity": "LOW|MEDIUM|HIGH"}"""

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=system_prompt
)

# Run it
result = agent.invoke({
    "messages": [HumanMessage(content="LoginTest failed with NoSuchElementException on #login-btn. Log is at /reports/logs/login.log. What happened?")]
})

print("\n" + "="*50)
print("FINAL RESULT:")
print(result['messages'][-1].content)