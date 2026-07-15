import base64
import logging
from pathlib import Path
from langchain_core.tools import tool

logger = logging.getLogger(__name__)

@tool
def read_screenshot(screenshot_path: str) -> str:
    """
    Reads a test failure screenshot and confirms it is available for analysis.
    
    Use this tool when you need visual context about what was on screen 
    when the test failed — for example, to check if the correct page 
    loaded or if an error message was visible.
    
    Args:
        screenshot_path: Path to the .png or .jpg screenshot file
        
    Returns:
        Confirmation that the screenshot was loaded with its file size,
        or an error message if the file is missing or unreadable.
    """

    try:
        path = Path(screenshot_path)
        if not path.exists():
            return f"Screenshot not found at: {screenshot_path}"
        if path.suffix.lower() not in ['.png', '.jpg', '.jpeg']:
            return f"Expected an image file (.png or .jpg), got: {path.suffix}"
        file_size = path.stat().st_size

        if file_size > 10 * 1024 * 1024:
            return f"Screenshot too large ({file_size} bytes). Maximum is 10MB."
        
        with open(screenshot_path, 'rb') as f:
            image_bytes = f.read()
        encoded = base64.b64encode(image_bytes).decode('utf-8')
        logger.info(f"Screenshot read successfully: {path.name} ({file_size} bytes)")

        return (
            f"Screenshot loaded successfully. "
            f"File: {path.name}, "
            f"Size: {file_size} bytes, "
            f"Base64 length: {len(encoded)} chars. "
            f"Screenshot is ready for analysis."
        )
    except Exception as e:
        return f"Error reading screenshot: {str(e)}"
if __name__ == "__main__":
    # Test 1 — file that doesn't exist
    result = read_screenshot.invoke({"screenshot_path": "fake_image.png"})
    print(f"Missing file: {result}")
    print()

    # Test 2 — wrong file type
    with open("test.txt", "w") as f:
        f.write("I am not an image")
    
    result = read_screenshot.invoke({"screenshot_path": "test.txt"})
    print(f"Wrong type: {result}")
    print()

    # Test 3 — real image (use your test_sample.log path just to confirm error handling)
    print("Tests complete.")