import truststore
truststore.inject_into_ssl()

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.1
)

# Template — structure written once, values filled later
template = ChatPromptTemplate.from_messages([
    ("system", "You are an expert QA analyst with 15 years experience."),
    ("human", "Analyze this test failure in one sentence: {failure_details}")
])

# Fill in the blank
filled_prompt = template.invoke({
    "failure_details": "NoSuchElementException on #login-btn at LoginPage.java:47"
})

print("--- Filled Prompt ---")
print(filled_prompt)
print()

# Send to Gemini
response = llm.invoke(filled_prompt)
print("--- Gemini Response ---")
print(response.content)