from .tool_registry import tool_registry

# Import all tool classes
from .os_tools import GetSystemTimeTool, ExecutePowerShellTool, OpenApplicationTool
from .filesystem_tools import ReadFileTool, CreateFileTool, DeleteFileTool
from .vision_tools import TakeScreenshotTool, AnalyzeScreenTool
from .memory_tools import StoreMemoryTool, RetrieveMemoryTool
from .email_tools import ReadEmailTool, SendEmailTool
from .calendar_tools import ReadCalendarTool, CreateCalendarEventTool

# Register OS Tools
tool_registry.register(GetSystemTimeTool())
tool_registry.register(ExecutePowerShellTool())
tool_registry.register(OpenApplicationTool())

# Register File Tools
tool_registry.register(ReadFileTool())
tool_registry.register(CreateFileTool())
tool_registry.register(DeleteFileTool())

# Register Vision Tools
tool_registry.register(TakeScreenshotTool())
tool_registry.register(AnalyzeScreenTool())

# Register Memory Tools
tool_registry.register(StoreMemoryTool())
tool_registry.register(RetrieveMemoryTool())

# Register Email Tools
tool_registry.register(ReadEmailTool())
tool_registry.register(SendEmailTool())

# Register Calendar Tools
tool_registry.register(ReadCalendarTool())
tool_registry.register(CreateCalendarEventTool())

from .media_tools import PlayMediaTool
from .system_control_tools import SetBrightnessTool, SetVolumeTool

# Register Media Tools
tool_registry.register(PlayMediaTool())

# Register System Control Tools
tool_registry.register(SetBrightnessTool())
tool_registry.register(SetVolumeTool())
