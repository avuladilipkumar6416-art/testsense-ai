import truststore
truststore.inject_into_ssl()

import os
import logging
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from log_reader import read_log_file
from screenshot_reader import read_screenshot

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

def get_llm_with_tools():
    """
    Creates a Gemini LLM instance with tools bound to it.
    
    Returns:
        A ChatGoogleGenerativeAI instance that knows about
        the log reader and screenshot reader tools.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.1
    )
    
    tools = [read_log_file, read_screenshot]
    llm_with_tools = llm.bind_tools(tools)
    
    logger.info(f"LLM created with {len(tools)} tools bound")
    return llm_with_tools

def test_tool_binding():
    """Tests that the LLM knows about its tools."""
    
    llm_with_tools = get_llm_with_tools()
    
    # Ask the LLM something that should trigger tool use
    message = HumanMessage(content="""
        A test failed with this error:
        NoSuchElementException: Unable to locate element #login-btn
        
        The log file is at: reports/logs/test.log
        The screenshot is at: reports/screenshots/test.png
        
        Please investigate this failure using the available tools.
    """)
    
    response = llm_with_tools.invoke([message])
    
    logger.info(f"Response type: {type(response)}")
    logger.info(f"Content: {response.content}")
    
    # Check if the LLM wants to use tools
    if response.tool_calls:
        logger.info(f"Tool calls requested: {len(response.tool_calls)}")
        for call in response.tool_calls:
            logger.info(f"  Tool: {call['name']}")
            logger.info(f"  Input: {call['args']}")
    else:
        logger.info("No tool calls made — LLM responded directly")
    
    return response

if __name__ == "__main__":
    logger.info("Testing tool binding...")
    response = test_tool_binding()
    logger.info("Tool binding test complete")