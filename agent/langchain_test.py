import truststore
truststore.inject_into_ssl()
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.1
)

response = llm.invoke("What is a NoSuchElementException in Selenium? One paragraph.")
print(response.content)
print()
print(f"Response type: {type(response)}")

print(f"Model: {response.response_metadata}")
print(f"Content type: {type(response.content)}")
