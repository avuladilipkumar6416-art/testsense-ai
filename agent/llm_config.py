import truststore
truststore.inject_into_ssl()

import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

SYSTEM_INSTRUCTION = """
You are an expert test failure analyzer with 15 years of QA experience.
When given a test failure, respond ONLY in this exact JSON format:
{
  "failure_type": "TEST_ISSUE or REAL_BUG or ENVIRONMENT_ISSUE",
  "root_cause": "one clear sentence explaining the cause",
  "is_real_bug": true or false,
  "confidence": integer from 0 to 100,
  "suggested_fix": "one clear sentence on what to fix",
  "severity": "LOW or MEDIUM or HIGH"
}

Rules:
- TEST_ISSUE: locator changed, wrong selector, bad test data, timing
- REAL_BUG: application logic wrong, API error, feature broken
- ENVIRONMENT_ISSUE: DB down, network failure, infrastructure problem
- Respond ONLY with JSON. No extra text. No markdown.
"""

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Check your .env file.")
    return genai.Client(api_key=api_key)

def analyze_failure(failure_text: str):
    client = get_gemini_client()
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=failure_text,
        config={"system_instruction": SYSTEM_INSTRUCTION}
    )
    
    response_text = response.text
    return json.loads(response_text)

if __name__ == "__main__":
    fake_failure = """
    Test Name: LoginTest.testValidLogin
    Error Type: NoSuchElementException
    Error Message: Unable to locate element: #login-btn
    Stack Trace:
        at LoginPage.clickLoginButton(LoginPage.java:47)
        at LoginTest.testValidLogin(LoginTest.java:23)
    Browser: Chrome 124
    Environment: staging
    """
    
    result = analyze_failure(fake_failure)
    print(result["failure_type"])
    print(result["confidence"])
    print(result["suggested_fix"])
    print(result["root_cause"])
    print(result["is_real_bug"])
    print(result["severity"])