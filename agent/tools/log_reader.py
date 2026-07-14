import logging
from langchain_core.tools import tool

logger = logging.getLogger(__name__)

@tool
def read_log_file(file_path: str) -> str:
    """
    Reads a test execution log file and returns its contents.
    Use this tool when you need to understand what happened during 
    test execution — what pages loaded, what elements were found, 
    what errors occurred.
    
    Args:
        file_path: The path to the .log file
        
    Returns:
        The complete log file contents as a string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.strip():
            return "Log file exists but is empty."
        
        logger.info(f"Log file read successfully: {file_path}")
        return content
        
    except FileNotFoundError:
        return f"Log file not found at: {file_path}"
    except PermissionError:
        return f"Permission denied reading: {file_path}"
    except Exception as e:
        return f"Error reading log file: {str(e)}"


if __name__ == "__main__":
   # Create a fake log file and test it
    with open("test_sample.log", "w") as f:
        f.write("INFO - Test started\n")
        f.write("INFO - Browser opened: Chrome\n")
        f.write("ERROR - Element #login-btn not found after 10s\n")
    
    result = read_log_file.invoke({"file_path": "test_sample.log"})
    print(f"Real file result:\n{result}")