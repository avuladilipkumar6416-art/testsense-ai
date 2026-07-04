import truststore
truststore.inject_into_ssl()

import logging
import os
import json
from dotenv import load_dotenv
from google import genai

logging.basicConfig(level=logging.INFO,
                    format= '%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("google").setLevel(logging.WARNING)

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
        model="gemini-2.0-flash-lite",
        contents=failure_text,
        config={"system_instruction": SYSTEM_INSTRUCTION}
    )
    
    response_text = response.text
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        logger.error("Gemini returned invalid JSON")
        return None

if __name__ == "__main__":
    failure_1 = """
    Test Name: LoginTest.testValidLogin
    Error Type: NoSuchElementException
    Error Message: Unable to locate element: #login-btn
    Stack Trace:
        at LoginPage.clickLoginButton(LoginPage.java:47)
        at LoginTest.testValidLogin(LoginTest.java:23)
    Browser: Chrome 124
    Environment: staging
    """
    failure_2 = """
    Test Name: PaymentTest.testSuccessfulPayment
    Error Type: AssertionError
    Error message: Expected HTTP 200 but got HTTP 500 Internal Server Error
    Stack Trace: 
        at PaymentTest.verifyPaymentStatus(PaymentTest.java:67)
        at PaymentTest.testSuccessfulPayment(PaymentTest.java:34)
    Browser: Chrome 124
    Environment: Staging
    """
    failure_3 = """
    Test Name: DatabaseTest.testUserDataRetrieval
    Error Type: java.net.ConnectException
    Error Message: Connection refused to localhost:5432
    Stack Trace:
        at DatabaseTest.setUp(DatabaseTest.java:23)
        at DatabaseTest.testUserDataRetrieval(DatabaseTest.java:45)
    Browser: Chrome 124
    Environment: staging
    """
    
    logger.info("--- Failure 1 ---")
    result_1 = analyze_failure(failure_1)
    logger.info(f"Type:       {result_1['failure_type']}")
    logger.info(f"Cause:      {result_1['root_cause']}")
    logger.info(f"Is bug:     {result_1['is_real_bug']}")
    logger.info(f"Confidence: {result_1['confidence']}%")
    logger.info(f"Fix:        {result_1['suggested_fix']}")
    logger.info(f"Severity:   {result_1['severity']}")

    logger.info("---FAILURE 2---")
    result_2 = analyze_failure(failure_2)
    logger.info(f"Type:       {result_2['failure_type']}")
    logger.info(f"Cause:      {result_2['root_cause']}")
    logger.info(f"Is bug:     {result_2['is_real_bug']}")
    logger.info(f"Confidence: {result_2['confidence']}%")
    logger.info(f"Fix:        {result_2['suggested_fix']}")
    logger.info(f"Severity:   {result_2['severity']}")

    logger.info("---FAILURE 3---")
    result_3 = analyze_failure(failure_3)
    logger.info(f"Type:       {result_3['failure_type']}")
    logger.info(f"Cause:      {result_3['root_cause']}")
    logger.info(f"Is bug:     {result_3['is_real_bug']}")
    logger.info(f"Confidence: {result_3['confidence']}%")
    logger.info(f"Fix:        {result_3['suggested_fix']}")
    logger.info(f"Severity:   {result_3['severity']}")