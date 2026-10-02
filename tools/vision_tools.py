import os
import io
import time
from PIL import ImageGrab
from .base_tool import BaseTool
from security.security_manager import SecurityManager

class TakeScreenshotTool(BaseTool):
    @property
    def name(self) -> str:
        return "take_screenshot"

    @property
    def description(self) -> str:
        return "Takes a screenshot of the main display and saves it to a file."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string", 
                    "description": "Optional custom filepath. If not provided, saves to e:\jarvis\screenshot.png"
                }
            }
        }

    @property
    def risk_level(self) -> int:
        return SecurityManager.RISK_LOW

    def execute(self, filepath: str = None, **kwargs) -> str:
        if not filepath:
            filepath = r"e:\jarvis\screenshot.png"
        try:
            # Add a tiny delay to ensure menus close if triggered by hotkey
            time.sleep(0.5)
            screenshot = ImageGrab.grab()
            screenshot.save(filepath)
            return f"Screenshot saved successfully to {filepath}."
        except Exception as e:
            return f"Failed to take screenshot: {str(e)}"

# A fully implemented AnalyzeScreenTool would instantiate the Gemini Vision API client
# For Phase 3, we will just stub the execution but register the tool
class AnalyzeScreenTool(BaseTool):
    @property
    def name(self) -> str:
        return "analyze_screen"

    @property
    def description(self) -> str:
        return "Takes a screenshot and analyzes its contents using a Vision model. Use this to 'see' what is on the screen."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "What to look for or analyze on the screen."}
            },
            "required": ["prompt"]
        }

    @property
    def risk_level(self) -> int:
        return SecurityManager.RISK_LOW

    def execute(self, prompt: str, **kwargs) -> str:
        # In the future this uses the Gemini API from old vision_tools.py
        # We will fully migrate the vision API call in Phase 4 when integrations are done
        return f"V2 Vision Analysis (Stub): I see the screen. You asked: '{prompt}'. [Vision API call pending migration in Phase 4]"
