import truststore
truststore.inject_into_ssl()
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Check your .env file.")
    return genai.Client(api_key=api_key)

if __name__ == "__main__":
    client = get_gemini_client()
    
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
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"You are a test failure expert. Analyze this failure:\n\n{fake_failure}"
    )
    
    print(response.text)