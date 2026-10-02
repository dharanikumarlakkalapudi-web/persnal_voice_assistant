import os
import io
import base64
import time
import datetime
import warnings

# We import these inside the functions or carefully at the module level
# to allow the rest of the file to load even if some dependencies fail,
# but since these are core to vision_tools we'll import them globally.
try:
    import pyautogui
    from PIL import Image
    import pytesseract
    import cv2
    import numpy as np
    from pyzbar.pyzbar import decode
    from openai import OpenAI
    import mss
except ImportError as e:
    warnings.warn(f"Missing dependency for vision tools: {e}")

# Try to set tesseract_cmd for Windows users by default if it exists
tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

from dotenv import load_dotenv
load_dotenv()

def _get_openai_vision_client():
    api_key = os.getenv("VISION_OPENAI_API_KEY")
    if api_key:
        base_url = os.getenv("VISION_BASE_URL")
        
        # Auto-detect Gemini API keys and route to Google's OpenAI-compatible endpoint
        if not base_url and api_key.startswith("AIza"):
            base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
            
        # Default to gemini-flash-latest if it's a Google key, otherwise gpt-4o
        default_model = "gemini-flash-latest" if api_key.startswith("AIza") else "gpt-4o"
        model_name = os.getenv("VISION_MODEL_NAME", default_model)
        
        return OpenAI(api_key=api_key, base_url=base_url), model_name
        
    main_api_key = os.getenv("OPENAI_API_KEY")
    main_base = os.getenv("OPENAI_BASE_URL", "")
    
    # If the user is using Groq for the main LLM, we can route Vision to Groq's Llama 3.2 Vision model!
    if "groq" in main_base.lower() and main_api_key:
        return OpenAI(api_key=main_api_key, base_url="https://api.groq.com/openai/v1"), "llama-3.2-11b-vision-preview"
        
    if not main_api_key or main_api_key == "dummy-key-for-local" or main_api_key == "ollama":
        raise ValueError("VISION_OPENAI_API_KEY is not set in .env. You must provide a valid API key for vision.")
    
    return OpenAI(api_key=main_api_key), os.getenv("VISION_MODEL_NAME", "gpt-4o")

def _take_screenshot(screen: str = "all"):
    """Robust screenshot helper with optional screen targeting."""
    try:
        with mss.mss() as sct:
            screen = screen.lower().strip() if screen else "all"
            target_monitor = sct.monitors[0] # Default to all monitors
            
            if screen != "all" and len(sct.monitors) > 1:
                # Sort individual monitors left-to-right by their 'left' coordinate
                monitors = sorted(sct.monitors[1:], key=lambda m: m["left"])
                if screen in ["left", "first", "1", "1st"]:
                    target_monitor = monitors[0]
                elif screen in ["right", "last"]:
                    target_monitor = monitors[-1]
                elif screen in ["second", "2", "2nd"] and len(monitors) > 1:
                    target_monitor = monitors[1]
                
            sct_img = sct.grab(target_monitor)
            return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
    except Exception:
        try:
            return pyautogui.screenshot(allScreens=True)
        except:
            return pyautogui.screenshot()

def analyze_screen(prompt: str, screen: str = "all") -> str:
    """Takes a screenshot of the current screen and uses a Vision LLM to answer the prompt."""
    try:
        print(f"[Analyzing screen '{screen}' for prompt: '{prompt}']")
        client, model_name = _get_openai_vision_client()
        
        # Take screenshot
        screenshot = _take_screenshot(screen)
        
        # Convert to Base64
        buffered = io.BytesIO()
        screenshot.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_str}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Failed to analyze screen: {str(e)}"

def summarize_screen(screen: str = "all") -> str:
    """Takes a screenshot and summarizes the main article or content."""
    return analyze_screen("Please read the main article or content on this screen and provide a concise 2-3 sentence verbal summary of what it is about.", screen)

def translate_screen(screen: str = "all") -> str:
    """Takes a screenshot, finds foreign text, and translates it to English."""
    return analyze_screen("Please find any foreign text on this screen, detect its language, and translate it to English. Just return the translation.", screen)

def extract_screen_text() -> str:
    """Extracts all readable text from the current screen using OCR."""
    try:
        print("[Extracting text from screen...]")
        screenshot = _take_screenshot()
        text = pytesseract.image_to_string(screenshot)
        if not text.strip():
            return "No text was detected on the screen."
        return f"Extracted Text:\n{text.strip()}"
    except Exception as e:
        return f"Failed to extract screen text (Is Tesseract installed?): {str(e)}"

def click_text_on_screen(target_text: str) -> str:
    """Finds the given text on the screen using OCR and clicks it."""
    try:
        print(f"[Looking for text to click: '{target_text}']")
        screenshot = _take_screenshot()
        
        # Get bounding boxes for all detected words
        data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
        
        target_lower = target_text.lower()
        
        for i in range(len(data['text'])):
            word = data['text'][i].strip().lower()
            if target_lower in word and int(data['conf'][i]) > 40: # confidence > 40
                x = data['left'][i]
                y = data['top'][i]
                w = data['width'][i]
                h = data['height'][i]
                
                # Calculate center
                center_x = x + (w / 2)
                center_y = y + (h / 2)
                
                # Move and click
                pyautogui.moveTo(center_x, center_y, duration=0.2)
                pyautogui.click()
                return f"Successfully clicked on the text: '{data['text'][i]}'."
                
        return f"Could not find the text '{target_text}' on the screen."
    except Exception as e:
        return f"Failed to click text: {str(e)}"

def take_organized_screenshot(description: str) -> str:
    """Takes a screenshot and saves it to the Screenshots folder with a descriptive name."""
    try:
        print(f"[Taking screenshot: {description}]")
        folder = "Screenshots"
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        clean_desc = "".join([c if c.isalnum() else "_" for c in description]).strip("_")
        
        filename = f"{timestamp}_{clean_desc}.png"
        filepath = os.path.join(folder, filename)
        
        screenshot = _take_screenshot()
        screenshot.save(filepath)
        
        return f"Screenshot saved successfully at: {filepath}"
    except Exception as e:
        return f"Failed to take screenshot: {str(e)}"

def scan_qr_code(source: str = "screen") -> str:
    """Scans for QR codes or barcodes either on the 'screen' or via the 'webcam'."""
    try:
        source = source.lower()
        if source == "webcam":
            print("[Starting webcam to scan QR code...]")
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()
            if not ret:
                return "Failed to capture image from webcam."
            
            # Convert OpenCV BGR to RGB for pyzbar
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            print("[Scanning screen for QR code...]")
            screenshot = _take_screenshot()
            # Convert PIL image to numpy array
            img = np.array(screenshot)
            
        decoded_objects = decode(img)
        
        if not decoded_objects:
            return "No QR codes or barcodes found."
            
        results = []
        for obj in decoded_objects:
            results.append(obj.data.decode("utf-8"))
            
        formatted = "\n".join(results)
        return f"Found QR Code(s):\n{formatted}"
        
    except Exception as e:
        return f"Failed to scan QR code: {str(e)}"
