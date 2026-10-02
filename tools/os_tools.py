import datetime
import subprocess
import os
from .base_tool import BaseTool
from security.security_manager import SecurityManager
from configuration.config_manager import config_manager

class GetSystemTimeTool(BaseTool):
    @property
    def name(self) -> str:
        return "get_system_time"

    @property
    def description(self) -> str:
        return "Gets the current system time."

    @property
    def parameters(self) -> dict:
        return {"type": "object", "properties": {}}

    @property
    def risk_level(self) -> int:
        return SecurityManager.RISK_SAFE

    def execute(self, **kwargs) -> str:
        return f"The current system time is: {datetime.datetime.now().strftime('%I:%M %p on %A, %B %d, %Y')}."

class ExecutePowerShellTool(BaseTool):
    @property
    def name(self) -> str:
        return "execute_powershell"

    @property
    def description(self) -> str:
        return "Executes a PowerShell command on the Windows host machine. DANGEROUS."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The powershell command to run."}
            },
            "required": ["command"]
        }

    @property
    def risk_level(self) -> int:
        return SecurityManager.RISK_DANGEROUS  # Level 3: Needs Face ID

    def execute(self, command: str, **kwargs) -> str:
        print(f"\n[JARVIS] EXECUTING POWERSHELL COMMAND: {command}\n")
        try:
            result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, timeout=30)
            output = result.stdout.strip()
            error = result.stderr.strip()
            
            if result.returncode == 0:
                return f"Command executed successfully.\nOutput:\n{output}"
            else:
                return f"Command failed with exit code {result.returncode}.\nError:\n{error}\nOutput:\n{output}"
        except Exception as e:
            return f"Failed to execute command: {str(e)}"

class OpenApplicationTool(BaseTool):
    @property
    def name(self) -> str:
        return "open_application"

    @property
    def description(self) -> str:
        return "Opens an application by its generic name (e.g., 'notepad', 'chrome', 'calculator')."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "The name of the application to open."}
            },
            "required": ["app_name"]
        }

    @property
    def risk_level(self) -> int:
        return SecurityManager.RISK_LOW

    def execute(self, app_name: str, **kwargs) -> str:
        # Check SQLite ApplicationManager first
        app_data = config_manager.applications.get_application(app_name.lower())
        if app_data and app_data['executable_path']:
            path = app_data['executable_path']
            subprocess.Popen(path)
            return f"Opened {app_data['display_name']} via configured path."
            
        # Fallback to generic shell execute
        try:
            os.startfile(app_name)
            return f"Opened {app_name} via generic shell execute."
        except Exception as e:
            import webbrowser
            query = f"https://www.google.com/search?q={app_name}"
            webbrowser.open(query)
            return f"Could not find local application '{app_name}'. Opened web search instead."
