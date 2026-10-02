from .base_tool import BaseTool
from security.security_manager import SecurityManager
import pywhatkit

class PlayMediaTool(BaseTool):
    @property
    def name(self) -> str:
        return "play_media"

    @property
    def description(self) -> str:
        return "Plays a specific video, song, or movie on the requested platform (e.g., youtube, spotify)."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The name of the video or song to play"},
                "platform": {"type": "string", "description": "The platform to play on (youtube, spotify). Default is youtube."}
            },
            "required": ["query"]
        }

    @property
    def risk_level(self) -> int:
        return SecurityManager.RISK_SAFE

    def execute(self, query: str, platform: str = "youtube", **kwargs) -> str:
        try:
            import os
            import urllib.parse
            import webbrowser
            
            platform = platform.lower()
            
            if platform == "spotify":
                try:
                    os.startfile(f"spotify:search:{urllib.parse.quote(query)}")
                    return f"Playing '{query}' on Spotify."
                except Exception:
                    webbrowser.open(f"https://open.spotify.com/search/{urllib.parse.quote(query)}")
                    return f"Opened '{query}' on Spotify Web."
            else:
                import pywhatkit
                pywhatkit.playonyt(query)
                return f"Playing '{query}' on YouTube."
        except Exception as e:
            return f"Failed to play media: {str(e)}"
