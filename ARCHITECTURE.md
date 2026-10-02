# JARVIS — FINAL APPLICATION ARCHITECTURE

## 1. PROJECT OBJECTIVE

Build JARVIS as a secure, modular, configuration-driven desktop AI agent for Windows.

The application must NOT be designed around hard-coded assumptions such as:

* "JARVIS is always the agent name"
* "Unity always exists at this path"
* "There is only one Gmail account"
* "There is only one Google Calendar"
* "Every agent uses the same AI provider"
* "Every feature is always enabled"
* "Dangerous actions can be decided by the LLM"
* "API keys can be stored in SQLite"
* "Users must edit source code to customize the application"

Everything that can reasonably be customized must be controlled through the application UI and configuration layer.

The system must prioritize:

1. Security
2. Modularity
3. Configurability
4. Reliability
5. Transparency
6. Maintainability
7. Easy addition/removal of capabilities
8. Good desktop UX
9. Minimal hard-coded behavior
10. Graceful failure and recovery

---

# 2. HIGH-LEVEL ARCHITECTURE

Use this architecture:

```text
┌─────────────────────────────────────────────────────────────┐
│                       JARVIS UI                             │
│                                                             │
│ Dashboard | Command Center | Vision | Memory | Agents       │
│ Files | Email | Calendar | Automations | Security           │
│ Integrations | Settings | History | Manual                  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  APPLICATION CONTROLLER                      │
│                                                             │
│ Navigation | UI State | Notifications | Sessions            │
│ Profile Switching | Global Application State                │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    AGENT ORCHESTRATOR                        │
│                                                             │
│ Intent Detection | Planning | Agent Selection               │
│ Tool Selection | Execution | Result Handling                │
│ Cancellation | Retry | Context Management                    │
└─────────────┬──────────────┬──────────────┬─────────────────┘
              │              │              │
              ▼              ▼              ▼
       ┌────────────┐ ┌────────────┐ ┌────────────────┐
       │ AI PROVIDER│ │ TOOL SYSTEM│ │ MEMORY SYSTEM  │
       │   LAYER    │ │            │ │                │
       └────────────┘ └────────────┘ └────────────────┘
              │              │              │
              ▼              ▼              ▼
       Cloud/Local LLM   OS / APIs /   SQLite +
                         Applications   Memory Manager
```

Supporting all layers:

```text
┌─────────────────────────────────────────────────────────────┐
│                  CONFIGURATION ENGINE                        │
├─────────────────────────────────────────────────────────────┤
│ Agent Identity | Hotkeys | Applications | Features          │
│ Integrations | Profiles | AI Providers | UI Preferences     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    SECURITY ENGINE                           │
├─────────────────────────────────────────────────────────────┤
│ Permissions | Face Verification | Confirmations             │
│ Credential Access | Tool Authorization | Audit Logging      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    CREDENTIAL VAULT                          │
├─────────────────────────────────────────────────────────────┤
│ API Keys | OAuth Tokens | Refresh Tokens | Secrets           │
└─────────────────────────────────────────────────────────────┘
```

---

# 3. CORE DESIGN PRINCIPLE

Separate these three things completely:

```text
CONFIGURATION
    ↓
What the application SHOULD do

CREDENTIALS
    ↓
Secrets required to access external services

RUNTIME STATE
    ↓
What the application is doing RIGHT NOW
```

Never mix them.

For example:

```text
Configuration:
Groq
Model: llama-3.1-8b-instant

Credential:
Groq API key

Runtime:
Groq request currently running
```

Do NOT store the API key in normal SQLite configuration tables.

---

# 4. RECOMMENDED PROJECT STRUCTURE

Use a modular Python backend.

```text
jarvis/
│
├── main.py
│
├── core/
│   ├── application.py
│   ├── agent_orchestrator.py
│   ├── event_bus.py
│   ├── command_router.py
│   ├── session_manager.py
│   ├── state_manager.py
│   └── lifecycle_manager.py
│
├── agents/
│   ├── base_agent.py
│   ├── general_agent.py
│   ├── coding_agent.py
│   ├── vision_agent.py
│   ├── automation_agent.py
│   └── agent_manager.py
│
├── ai/
│   ├── provider_interface.py
│   ├── provider_manager.py
│   ├── model_manager.py
│   ├── groq_provider.py
│   ├── openai_provider.py
│   ├── ollama_provider.py
│   └── router.py
│
├── tools/
│   ├── base_tool.py
│   ├── tool_registry.py
│   ├── os_tools.py
│   ├── application_tools.py
│   ├── filesystem_tools.py
│   ├── terminal_tools.py
│   ├── browser_tools.py
│   ├── media_tools.py
│   ├── screenshot_tools.py
│   ├── vision_tools.py
│   ├── email_tools.py
│   ├── calendar_tools.py
│   └── automation_tools.py
│
├── security/
│   ├── security_manager.py
│   ├── permission_manager.py
│   ├── credential_vault.py
│   ├── face_verification.py
│   ├── confirmation_manager.py
│   ├── action_risk.py
│   └── audit_logger.py
│
├── configuration/
│   ├── config_manager.py
│   ├── schema_validator.py
│   ├── defaults.py
│   ├── migration_manager.py
│   ├── profile_manager.py
│   ├── identity_manager.py
│   ├── hotkey_manager.py
│   ├── application_manager.py
│   ├── feature_manager.py
│   └── import_export.py
│
├── integrations/
│   ├── gmail/
│   ├── google_calendar/
│   ├── hacker_news/
│   ├── spotify/
│   ├── youtube/
│   └── integration_manager.py
│
├── voice/
│   ├── speech_to_text.py
│   ├── text_to_speech.py
│   ├── wake_word.py
│   └── voice_manager.py
│
├── vision/
│   ├── screen_analyzer.py
│   ├── ocr.py
│   ├── qr_scanner.py
│   ├── ui_locator.py
│   └── webcam.py
│
├── memory/
│   ├── memory_manager.py
│   ├── sqlite_database.py
│   ├── memory_types.py
│   ├── retention_manager.py
│   └── search.py
│
├── automation/
│   ├── automation_manager.py
│   ├── trigger_engine.py
│   ├── condition_engine.py
│   └── action_engine.py
│
├── background/
│   ├── background_manager.py
│   ├── scheduler.py
│   └── workers/
│
├── ui/
│   ├── dashboard/
│   ├── command_center/
│   ├── agents/
│   ├── vision/
│   ├── memory/
│   ├── files/
│   ├── email/
│   ├── calendar/
│   ├── automation/
│   ├── security/
│   ├── integrations/
│   ├── settings/
│   ├── history/
│   ├── manual/
│   └── hud/
│
├── database/
│   ├── schema.sql
│   ├── migrations/
│   └── repositories/
│
├── models/
│   ├── agent_models.py
│   ├── application_models.py
│   ├── permission_models.py
│   ├── integration_models.py
│   └── automation_models.py
│
├── tests/
│
├── config/
│   ├── defaults/
│   └── schemas/
│
└── resources/
    ├── icons/
    ├── sounds/
    └── manual/
```

---

# 5. AGENT IDENTITY SYSTEM

Never hard-code the displayed agent name.

Use:

```json
{
    "agent_id": "personal_agent",
    "display_name": "JARVIS",
    "wake_words": [
        "jarvis"
    ],
    "enabled": true
}
```

`agent_id` NEVER changes.

`display_name` CAN change at any time.

Example:

```text
JARVIS
↓
FRIDAY
↓
NOVA
↓
ATLAS
```

The new name must automatically propagate to:

* UI
* Dashboard
* TTS
* Notifications
* HUD
* Wake-word configuration
* Manual
* About page
* Agent cards
* System messages
* Logs where appropriate

Do NOT rename Python classes or source-code identifiers when the user changes the display name.

Example:

```python
class GeneralAgent:
    pass
```

is preferable to:

```python
class JarvisAgent:
    pass
```

---

# 6. HOTKEY SYSTEM

Create a centralized Hotkey Manager.

Example:

```json
{
    "wake": "ctrl+space",
    "cancel": "escape",
    "open_dashboard": "ctrl+shift+j",
    "screenshot": "ctrl+shift+s"
}
```

The UI must allow:

* Change hotkey
* Detect conflicts
* Reset individual hotkey
* Reset all hotkeys
* Enable/disable hotkey
* Test hotkey

Support:

* Keyboard keys
* Function keys
* Modifier combinations
* Mouse buttons where supported

Never let two critical actions silently share the same shortcut.

---

# 7. WAKE WORD SYSTEM

Wake words must be configurable.

Support:

```text
Wake word enabled
Primary wake word
Additional wake phrases
Sensitivity
Cooldown
Enable/disable listening
```

Important:

Do not pretend every speech-recognition library supports arbitrary wake words.

Create a `WakeWordProvider` interface so the implementation can later be changed.

```text
WakeWordManager
      ↓
WakeWordProvider
      ↓
Current wake-word engine
```

If custom wake-word training is required, expose that limitation clearly in the UI.

---

# 8. APPLICATION MANAGER

This is one of the most important systems.

Never hard-code:

```python
if app == "unity":
    ...
```

Instead use an application registry.

Example:

```json
{
    "id": "unity",
    "display_name": "Unity",
    "type": "desktop",
    "launch_method": "executable",
    "executable_path": "C:\\Program Files\\Unity\\Hub\\Editor\\...",
    "arguments": [],
    "enabled": true
}
```

The user can add:

* Unity
* Unreal Engine
* Blender
* Visual Studio
* Antigravity
* Minecraft
* Steam
* Spotify
* Any custom application

Each application should support:

```text
Name
Type
Executable path
Arguments
Working directory
Launch method
Enabled/disabled
Icon
Auto-detect
Test launch
Repair path
```

Application types:

```text
Desktop
Web
Steam
Custom Command
File
URL
```

---

# 9. APPLICATION PATH VALIDATION

Reduce failures by validating applications before saving.

When the user selects an executable:

```text
Browse
 ↓
Validate
 ↓
Display executable information
 ↓
Test launch
 ↓
Save
```

If the executable disappears:

```text
Application unavailable

[Locate]
[Auto Detect]
[Disable]
[Remove]
```

Never silently fail.

Never execute arbitrary paths without going through the security/tool permission system.

---

# 10. DESKTOP VS WEB LAUNCHING

Every application must have a launch strategy.

Example:

```json
{
    "name": "Unity",
    "type": "desktop",
    "launch_method": "executable"
}
```

Another:

```json
{
    "name": "YouTube",
    "type": "web",
    "launch_method": "browser"
}
```

Another:

```json
{
    "name": "Minecraft",
    "type": "custom",
    "launch_method": "launcher"
}
```

The user controls this.

---

# 11. FEATURE MANAGER

Every major capability should be a feature.

Example:

```json
{
    "screen_vision": {
        "enabled": true
    },
    "gmail": {
        "enabled": true
    },
    "calendar": {
        "enabled": true
    },
    "background_agents": {
        "enabled": false
    }
}
```

Feature states:

```text
ON
OFF
UNAVAILABLE
ERROR
REQUIRES_CONFIGURATION
```

The Feature Manager must understand dependencies.

Example:

```text
Vision
 ├── OCR
 ├── Screen analysis
 ├── UI clicking
 └── QR scanning
```

If Vision is disabled, dependent features should automatically become unavailable rather than crashing.

---

# 12. AGENT SYSTEM

Create multiple specialized agents instead of one massive agent.

Recommended:

```text
General Agent
Coding Agent
Vision Agent
Automation Agent
System Agent
```

Each agent has:

```text
Agent ID
Display name
Enabled
AI provider
Model
Allowed tools
Allowed integrations
Permission profile
System instructions
Memory access
```

Example:

```json
{
    "agent_id": "coding_agent",
    "display_name": "Code Agent",
    "provider": "openai",
    "model": "configured_model",
    "permissions": "developer",
    "tools": [
        "filesystem",
        "terminal",
        "code_editor"
    ]
}
```

---

# 13. AGENT CAPABILITY MODEL

Do not allow agents to access every tool by default.

Use capability-based access.

Example:

```text
General Agent
 ├── Browser
 ├── Gmail Read
 ├── Calendar Read
 ├── Media
 └── Applications

Coding Agent
 ├── Files
 ├── Terminal
 ├── Code Editor
 └── Application Launcher

Vision Agent
 ├── Screenshot
 ├── OCR
 ├── Webcam
 └── UI Locator
```

An agent must explicitly receive a capability before using it.

---

# 14. AI PROVIDER SYSTEM

Create a unified provider interface.

```text
Agent
 ↓
AI Router
 ↓
Provider
 ↓
Model
 ↓
Credential Vault
 ↓
API
```

Supported provider architecture:

```text
Groq
OpenAI
Ollama
Other providers later
```

The user can configure:

```text
Provider
API key
Model
Endpoint
Temperature
Max tokens
Timeout
```

Never let individual agents directly manage API keys.

They request credentials from the Credential Vault.

---

# 15. DIFFERENT AI PROVIDERS PER AGENT

Allow:

```text
General Agent → Groq
Coding Agent → OpenAI
Vision Agent → OpenAI
Local Agent → Ollama
```

This must be configuration-driven.

Do not hard-code provider choices into agents.

---

# 16. CREDENTIAL VAULT

API keys and OAuth tokens must NOT be stored in:

* SQLite memory
* JSON configuration
* Logs
* Git
* Error messages
* Screenshots
* Prompts

Use a secure OS-backed credential mechanism on Windows, preferably Windows Credential Manager / DPAPI-backed storage.

The configuration should store only references such as:

```text
credential_id = groq_main
```

not:

```text
api_key = gsk_XXXXXXXX
```

The UI must provide:

```text
Add credential
Test credential
Replace credential
Revoke/remove credential
Connection status
Last tested
```

Never display the complete secret after saving.

---

# 17. GMAIL ARCHITECTURE

Support multiple Gmail accounts.

Example:

```text
College
Personal
Projects
```

Each account should have:

```text
Account ID
Email address
Display name
Enabled
Read permission
Send permission
Default account
```

Use OAuth.

NEVER ask the user for their Gmail password.

---

# 18. GMAIL PERMISSIONS

Separate:

```text
Read email
Search email
Send email
Reply
Delete
Archive
Modify labels
```

Do not treat Gmail as one permission.

Recommended default:

```text
Read → allowed
Search → allowed
Send → confirmation
Delete → confirmation + stronger authorization
```

---

# 19. GOOGLE CALENDAR ARCHITECTURE

Support multiple calendars.

Example:

```text
Personal
College
Projects
Fitness
```

Use:

```text
Calendar ID
Account ID
Display name
Enabled
Color
Default
```

Agents can be restricted to specific calendars.

---

# 20. CALENDAR PERMISSIONS

Separate:

```text
Read
Create
Modify
Delete
```

Example:

```text
General Agent:
Read → allowed
Create → confirmation
Modify → confirmation
Delete → Face ID + confirmation
```

---

# 21. SECURITY ARCHITECTURE

The LLM must NEVER be the final authority for dangerous actions.

Correct:

```text
User Request
     ↓
LLM interprets intent
     ↓
Tool selected
     ↓
Security Manager
     ↓
Risk Assessment
     ↓
Permission Check
     ↓
Face ID / Confirmation if required
     ↓
Tool Execution
```

NOT:

```text
LLM decides whether something is safe
```

---

# 22. ACTION RISK LEVELS

Create standardized action risk levels.

```text
LEVEL 0 — Safe
```

Examples:

* Read public information
* Open dashboard
* Change volume
* Read calendar

```text
LEVEL 1 — Low Risk
```

Examples:

* Launch application
* Screenshot
* Open website
* Change brightness

```text
LEVEL 2 — Sensitive
```

Examples:

* Read private email
* Access private files
* Read personal calendar

```text
LEVEL 3 — Dangerous
```

Examples:

* Execute PowerShell
* Delete files
* Send email
* Modify important files
* Shut down computer

```text
LEVEL 4 — Critical
```

Examples:

* Bulk deletion
* Destructive automation
* Credential changes
* High-impact system changes

---

# 23. FACE VERIFICATION

Use Face ID as an additional authorization factor for sensitive actions.

Example:

```text
User:
"Delete this folder."

Agent:
Understands request.

Security:
Action = filesystem.delete
Risk = Level 3

Security asks:
Face verification required.

Face verified.

Confirmation:
"Delete C:\example permanently?"

User confirms.

Execute.
```

Never rely solely on facial recognition for every action.

Use it selectively to avoid excessive friction.

---

# 24. CONFIRMATION SYSTEM

Create a centralized confirmation manager.

Actions can require:

```text
No confirmation
Confirmation
Face verification
Face + confirmation
```

This must be configurable.

---

# 25. PERMISSION PROFILES

Provide:

```text
Relaxed
Balanced
Strict
Custom
```

Recommended default:

```text
Balanced
```

Users can create custom profiles.

Example:

```text
Gaming Mode
Study Mode
Developer Mode
Guest Mode
```

Do not duplicate entire configurations unnecessarily.

Profiles should reference shared configuration and override only required settings.

---

# 26. ACTIVITY TIMELINE

Every important agent action should appear in an activity timeline.

Example:

```text
12:32:01
User requested: "Open Unity"

12:32:01
Intent recognized

12:32:01
Application Manager → Unity

12:32:01
Path validated

12:32:02
Unity launched successfully
```

Actions:

```text
Cancel
Retry
View details
Why did you do this?
```

Sensitive information must be redacted.

Never log:

* API keys
* OAuth tokens
* passwords
* full secret contents

---

# 27. COMMAND HISTORY

Store useful command history.

Allow:

```text
Search
Replay
Delete
Clear history
View execution details
```

Automatically redact secrets and sensitive credential information.

---

# 28. MEMORY SYSTEM

Use SQLite for structured memory.

Separate:

```text
Permanent memory
Temporary session memory
Conversation history
Application state
Automation state
```

Do not blindly store everything.

Memory should have:

```text
ID
Category
Content
Created
Updated
Source
Importance
Retention
```

The Memory Center must allow the user to inspect and modify stored memories.

---

# 29. SQLITE ARCHITECTURE

SQLite should store application data such as:

```text
agents
applications
features
profiles
permissions
integrations metadata
calendar metadata
email account metadata
memories
history
automations
background jobs
activity logs
settings
```

Secrets should remain outside normal SQLite storage.

Use repositories rather than allowing every module to directly execute SQL.

```text
UI
 ↓
Service
 ↓
Repository
 ↓
SQLite
```

---

# 30. CONFIGURATION ENGINE

Create one centralized Configuration Manager.

All modules should use it.

Example:

```text
ConfigManager
 ├── Identity
 ├── Hotkeys
 ├── Applications
 ├── Features
 ├── Agents
 ├── Providers
 ├── Integrations
 ├── Permissions
 ├── Profiles
 └── UI
```

Do not allow random modules to maintain their own conflicting configuration.

---

# 31. CONFIGURATION VALIDATION

Every configuration change must be validated.

Flow:

```text
User changes setting
       ↓
Schema validation
       ↓
Dependency validation
       ↓
Security validation
       ↓
Save
       ↓
Emit configuration-changed event
       ↓
Affected modules reload
```

Invalid settings should NOT crash the application.

Show:

```text
What is wrong
Why it matters
How to fix it
```

---

# 32. LIVE CONFIGURATION

Important configuration changes should take effect without restarting JARVIS.

Examples:

```text
Agent name
Hotkeys
Voice
Application paths
Feature enable/disable
Provider/model
UI settings
Permissions
```

For settings that genuinely require restart, explicitly state:

```text
Restart required
```

Do not pretend to support live changes when the underlying dependency cannot safely reload.

---

# 33. EVENT BUS

Use an internal event bus to propagate configuration changes.

Example:

```text
identity.changed
hotkeys.changed
application.updated
feature.changed
provider.changed
permission.changed
profile.changed
integration.connected
```

Example:

```text
User changes agent name
        ↓
ConfigManager
        ↓
identity.changed
        ↓
UI updates
TTS updates
Notification system updates
Wake-word system updates
HUD updates
```

This avoids hard-coded cross-module dependencies.

---

# 34. FIRST-TIME SETUP WIZARD

First launch should provide:

```text
1. Agent Name
2. Wake Word
3. Voice
4. Hotkeys
5. Face Verification
6. AI Provider
7. API Credentials
8. Gmail
9. Calendar
10. Applications
11. Features
12. Security Profile
13. Finish
```

Every step should have:

```text
Skip
Configure
Test
Back
```

Advanced users can skip the wizard.

---

# 35. APPLICATION MANAGER UI

Create:

```text
Settings
 → Applications
```

Show:

```text
Unity       Desktop   Enabled
Blender     Desktop   Enabled
Chrome      Desktop   Enabled
YouTube     Web       Enabled
```

Each entry:

```text
Edit
Test
Open
Disable
Remove
Repair
```

Add Application:

```text
+ Add Application
```

Wizard:

```text
Name
Application type
Launch method
Executable
Arguments
Working directory
Icon
Test
Save
```

---

# 36. FEATURE MANAGER UI

Create:

```text
Settings
 → Features
```

Display every major capability.

Example:

```text
Voice
[ON]

Screen Vision
[ON]

Gmail
[ON]

Calendar
[ON]

Background Agents
[OFF]

Automation
[ON]

Face Verification
[ON]
```

For each feature:

```text
Status
Dependencies
Permissions
Configuration
```

---

# 37. INTEGRATIONS CENTER

Create:

```text
Settings
 → Integrations
```

Categories:

```text
AI Providers
Email
Calendar
Media
News
Browser
Other
```

Each integration:

```text
Connected
Disconnected
Error
Needs attention
```

Provide:

```text
Connect
Disconnect
Test
Configure
```

---

# 38. AGENT MANAGER UI

Create:

```text
Agents
```

Example:

```text
General Agent
AI: Groq
Tools: 12
Permissions: Balanced

Coding Agent
AI: OpenAI
Tools: 7
Permissions: Developer

Vision Agent
AI: OpenAI
Tools: 5
Permissions: Vision
```

Allow:

```text
Enable/disable
Rename display name
Change model
Change provider
Assign tools
Assign permissions
Assign integrations
Edit instructions
```

---

# 39. COMMAND CENTER

Main interaction interface:

```text
┌───────────────────────────────────────────┐
│              JARVIS                       │
│                                           │
│       ● Listening / Thinking / Idle       │
│                                           │
│ "What would you like me to do?"           │
│                                           │
│ [ Type a command... ]       🎤             │
│                                           │
│ Open App | Email | Calendar | Screenshot  │
└───────────────────────────────────────────┘
```

Show the current operation instead of only displaying chat messages.

---

# 40. DASHBOARD

Dashboard should show:

```text
Agent status
Voice status
Current task
Current agent
Current AI provider/model
CPU
GPU
RAM
Network
Microphone
Camera
Background agents
Security status
Recent actions
```

The dashboard should make JARVIS feel like an actual running system rather than a chatbot.

---

# 41. LIVE AGENT ACTIVITY

Display:

```text
Thinking
Planning
Using tool
Waiting for permission
Executing
Completed
Failed
Cancelled
```

Example:

```text
User request
   ↓
Planning
   ↓
Application Manager
   ↓
Security Check
   ↓
Execution
   ↓
Success
```

---

# 42. VISION SYSTEM

Existing capabilities should be organized as:

```text
Vision
├── Screen Analysis
├── OCR
├── Screen Translation
├── UI Element Detection
├── UI Clicking
├── QR Scanner
├── Barcode Scanner
├── Webcam
└── Screenshot Manager
```

Every vision operation must pass through permissions.

---

# 43. FILE SYSTEM AGENT

File operations must use a dedicated tool layer.

Supported:

```text
Browse
Read
Create
Edit
Rename
Move
Delete
Search
```

Destructive operations must go through Security Manager.

---

# 44. TERMINAL / POWERSHELL AGENT

PowerShell execution must NEVER be unrestricted by default.

Use:

```text
Command
 ↓
Risk classification
 ↓
Security policy
 ↓
Permission
 ↓
Optional Face verification
 ↓
Execution
```

Keep command output and errors in the activity system.

Never blindly execute LLM-generated commands without policy enforcement.

---

# 45. CODING AGENT

The coding agent can:

```text
Read project
Analyze errors
Edit code
Create files
Run tests
Run build commands
Read terminal output
Debug
Suggest fixes
Apply fixes
```

However:

```text
Code modification
+
Terminal execution
+
File deletion
```

must remain controlled by the permission system.

---

# 46. BACKGROUND AGENTS

Background functionality should be managed centrally.

Examples:

```text
Hacker News scraper
Morning briefing
Reminder scheduler
Automation worker
```

Each background process must have:

```text
Enabled
Schedule
Resource limit
Permissions
Allowed tools
Last run
Next run
Failure state
```

Users must be able to stop all background activity.

---

# 47. AUTOMATION BUILDER

Use:

```text
Trigger
 ↓
Conditions
 ↓
Actions
```

Example:

```text
Every weekday at 8:00
        ↓
Get calendar
        ↓
Get unread email
        ↓
Get tech news
        ↓
Create briefing
        ↓
Speak briefing
```

Every automation action must still pass through permission rules.

Do not bypass security simply because the user created an automation.

---

# 48. PROACTIVE NOTIFICATIONS

Notifications should have priority:

```text
Critical
Important
Normal
Background
```

Users can configure:

```text
Desktop notification
Voice
Silent
HUD
```

---

# 49. FOCUS / GAMING MODE

Provide modes such as:

```text
Normal
Gaming
Study
Developer
Silent
Guest
```

Gaming mode can:

```text
Disable unnecessary notifications
Reduce background agents
Disable voice interruptions
Keep HUD minimal
Reduce resource usage
```

Modes should modify settings through overrides rather than copying entire configurations.

---

# 50. USER MANUAL

Build an integrated manual similar to a game's:

```text
Controls / Settings / Tutorials
```

Sections:

```text
Getting Started
Controls
Voice Commands
Wake Words
Applications
Agents
AI Providers
Gmail
Calendar
Vision
Files
Coding Agent
Automation
Memory
Security
Profiles
Troubleshooting
Advanced Settings
```

Make it:

```text
Searchable
Versioned
Context-sensitive
```

For example, clicking:

```text
API Provider
```

should offer:

:```text
What this does
How to configure it
Security information
Troubleshooting
```

---

# 51. SETTINGS ARCHITECTURE

Use:

```text
Settings
│
├── Agent
│   ├── Identity
│   ├── Voice
│   └── Wake Word
│
├── Controls
│   ├── Hotkeys
│   └── Input
│
├── Applications
│
├── Features
│
├── Agents
│
├── AI
│   ├── Providers
│   ├── Models
│   └── Routing
│
├── Integrations
│   ├── Gmail
│   ├── Calendar
│   ├── Media
│   └── News
│
├── Security
│   ├── Face Verification
│   ├── Permissions
│   ├── Confirmations
│   └── Credential Vault
│
├── Memory
│
├── Automation
│
├── Background Agents
│
├── Appearance
│
├── Profiles
│
├── Data
│   ├── Import
│   ├── Export
│   ├── Backup
│   └── Reset
│
└── User Manual
```

---

# 52. IMPORT / EXPORT

Allow users to export:

```text
Application configuration
Agent configuration
Feature settings
Hotkeys
Profiles
Automation definitions
UI preferences
Non-sensitive integration metadata
```

By default DO NOT export:

```text
API keys
OAuth tokens
Refresh tokens
Passwords
Face data
Biometric information
```

Provide a clear warning before exporting.

---

# 53. BACKUP / RECOVERY

Configuration changes should support recovery.

Use:

```text
Automatic backup before major configuration changes
Configuration versioning
Rollback
Reset individual setting
Reset category
Reset all settings
```

Never make "Reset All" irreversible without confirmation.

---

# 54. CONFIGURATION MIGRATIONS

Configuration schemas will change over time.

Implement:

```text
schema_version
```

Example:

```json
{
    "schema_version": 3
}
```

When updating JARVIS:

```text
Old config
 ↓
Migration Manager
 ↓
New config
 ↓
Validation
 ↓
Application
```

This prevents future updates from breaking existing users.

---

# 55. ERROR HANDLING

Every subsystem should fail gracefully.

Instead of:

```text
Traceback...
```

show:

```text
Calendar unavailable

Reason:
Google authorization expired.

Actions:
[Reconnect]
[Retry]
[View Details]
```

Developer Mode may expose the full traceback.

Normal users should see a useful explanation.

---

# 56. DEVELOPER MODE

Provide an advanced developer panel.

Show:

```text
Current agent
LLM provider
Model
Prompt/context status
Tools
Tool calls
Permissions
Memory retrieval
Latency
Token usage where available
Errors
API status
Background workers
Event bus activity
```

This will be extremely useful while developing JARVIS.

---

# 57. SECURITY LOGGING

Create a separate audit log for important security events.

Record:

```text
Timestamp
User action
Agent
Tool
Risk level
Permission decision
Authentication result
Result
```

Never record secrets.

---

# 58. RESOURCE MANAGEMENT

Background processes and vision/LLM workloads should be controllable.

Provide:

```text
CPU usage
RAM usage
GPU usage
Network usage
Worker count
Background task count
```

Users should be able to disable resource-heavy features.

---

# 59. API FAILURE HANDLING

AI providers can fail.

Implement:

```text
Timeout
Retry
Exponential backoff
Provider health status
Fallback provider
Offline/local fallback where configured
```

Example:

```text
Groq unavailable
      ↓
Fallback provider available?
      ↓
Yes → use fallback
No → explain failure
```

Never silently switch providers if doing so could affect privacy or cost.

Provider fallback must be explicitly configured.

---

# 60. INTEGRATION FAILURE HANDLING

For Gmail/Calendar/etc.:

```text
Connected
 ↓
Token expired
 ↓
Refresh
 ↓
If refresh fails:
Needs Reauthorization
```

Do not crash the entire assistant because one integration is unavailable.

---

# 61. PRIVACY ARCHITECTURE

Clearly distinguish:

```text
Local data
Cloud data
Third-party data
```

Example:

```text
Screen image
 → local processing where possible

LLM request
 → cloud provider if configured

Gmail
 → Google API

Memory
 → local SQLite
```

The UI should tell the user when information is being sent to a cloud provider.

---

# 62. PLUGIN / TOOL ARCHITECTURE

All tools should implement a common interface.

Conceptually:

```python
class BaseTool:
    tool_id
    name
    description
    risk_level
    required_permissions
    execute()
```

Tool registry:

```text
Tool
 ↓
Tool Registry
 ↓
Agent Capability Check
 ↓
Security Manager
 ↓
Execution
```

This allows new tools to be added without rewriting the orchestrator.

---

# 63. DO NOT LET THE LLM DIRECTLY CONTROL THE OS

The LLM should output structured intent/tool requests.

Example:

```text
LLM:
launch_application(
    application_id="unity"
)
```

Then:

```text
Tool Registry
 ↓
Application Manager
 ↓
Security Manager
 ↓
Application
```

Never allow raw LLM text to directly become shell commands or filesystem operations.

---

# 64. STRUCTURED TOOL CALLS

Every tool call should have:

```text
tool_id
arguments
request_id
agent_id
session_id
risk_level
timestamp
```

This enables:

```text
Tracing
Cancellation
Auditing
Debugging
Retry
```

---

# 65. CANCELLATION

Long-running tasks must be cancellable.

Examples:

```text
Cancel LLM request
Cancel file operation
Cancel automation
Cancel background job
Cancel terminal execution where safely possible
```

The UI must expose:

```text
Cancel
```

for active operations.

---

# 66. COMMAND LIFECYCLE

Every command follows:

```text
INPUT
 ↓
Speech/Text
 ↓
STT if voice
 ↓
Intent Detection
 ↓
Agent Selection
 ↓
Planning
 ↓
Tool Selection
 ↓
Permission Check
 ↓
Authentication
 ↓
Confirmation if required
 ↓
Tool Execution
 ↓
Result Validation
 ↓
Memory update if appropriate
 ↓
Response
 ↓
TTS/UI
 ↓
Activity Log
```

This should be the central execution pipeline.

---

# 67. CENTRAL STATE MODEL

Maintain a runtime state object:

```text
Agent state
Voice state
Current command
Current task
Current tool
Security state
Connected integrations
Background workers
System metrics
```

UI should subscribe to state changes instead of independently polling every subsystem.

---

# 68. RECOMMENDED DATABASE ENTITIES

At minimum:

```text
agents
applications
features
hotkeys
profiles
permissions
providers
models
integration_accounts
calendars
memories
commands
activity_logs
automations
background_jobs
settings
schema_metadata
```

Credentials remain outside this normal database.

---

# 69. USER CUSTOMIZATION PRIORITY

The following must be editable without source-code modification:

```text
Agent display name
Wake words
Hotkeys
Voice
Applications
Executable paths
Launch methods
Features
AI provider
AI model
AI routing
Gmail accounts
Calendar accounts
Permissions
Security profile
Profiles
Automations
Notifications
Appearance
Memory preferences
```

---

# 70. ANTI-HARDCODING RULE

Before implementing any new feature ask:

```text
"Could a user reasonably want to change this?"
```

If YES:

```text
Put it in configuration.
```

Examples:

BAD:

```python
UNITY_PATH = "C:\\..."
```

GOOD:

```text
ApplicationManager → configured application
```

BAD:

```python
AGENT_NAME = "JARVIS"
```

GOOD:

```text
IdentityManager → display_name
```

BAD:

```python
GROQ_API_KEY = "..."
```

GOOD:

```text
CredentialVault → credential reference
```

---

# 71. REDUCING COMPLEXITY

Do NOT expose every internal option to normal users.

Use:

```text
Basic
Advanced
Developer
```

settings levels.

Normal user sees:

```text
Agent name
Voice
Hotkeys
Applications
Features
AI provider
Security
```

Advanced users can access:

```text
Routing
Tool permissions
Automation
Profiles
Fallback providers
Memory retention
```

Developers can access:

```text
Debugging
Events
Tool schemas
Logs
Agent internals
Provider diagnostics
```

This keeps the powerful architecture from becoming overwhelming.

---

# 72. DEFAULT SECURITY POLICY

Use secure defaults.

Recommended:

```text
Security profile: Balanced

API secrets: secure vault
Gmail read: allowed
Gmail send: confirmation
Calendar read: allowed
Calendar create: confirmation
File read: allowed
File write: confirmation where appropriate
File delete: Face ID + confirmation
PowerShell: Face ID for dangerous commands
Shutdown: confirmation
Credential operations: Face ID
Bulk destructive automation: Face ID + confirmation
```

Users can customize this.

---

# 73. DEFAULT FEATURE POLICY

Start with:

```text
Voice                 ON
Basic OS control      ON
Application manager   ON
Memory                ON
Dashboard             ON
Activity timeline     ON
Security              ON
Gmail                 OFF until connected
Calendar              OFF until connected
Vision                ON if configured
Background agents     OFF initially
Automation            OFF initially
```

This avoids first-launch failures caused by missing credentials or dependencies.

---

# 74. FINAL USER EXPERIENCE

The application should feel like:

```text
             ┌───────────────────────┐
             │       JARVIS          │
             │                       │
             │      ● ACTIVE         │
             │                       │
             │  "Launching Unity"    │
             │                       │
             │  Agent: General       │
             │  AI: Groq             │
             │                       │
             │  ✓ Permission         │
             │  ✓ Path validated     │
             │  ✓ Application opened │
             └───────────────────────┘
```

Instead of simply:

```text
JARVIS:
Unity opened.
```

The system should expose what it is doing while hiding unnecessary implementation complexity.

---

# 75. FINAL ARCHITECTURAL RULES

MANDATORY:

1. No hard-coded agent display name.
2. No hard-coded application paths.
3. No hard-coded API keys.
4. No direct LLM-to-OS execution.
5. No unrestricted terminal execution.
6. No unrestricted destructive filesystem operations.
7. No passwords stored for Gmail.
8. No credentials stored in normal SQLite.
9. No agent gets every tool by default.
10. No automation bypasses security.
11. No feature should crash the application when disabled.
12. Configuration must be schema validated.
13. Configuration changes should propagate through events.
14. Important configuration should support rollback.
15. Secrets must be redacted from logs.
16. External integrations must fail independently.
17. Provider fallback must be explicitly configured.
18. User-facing settings should have Basic/Advanced/Developer levels.
19. Agent IDs remain stable even when display names change.
20. All dangerous operations pass through Security Manager.

---

# 76. FINAL SYSTEM ARCHITECTURE

The complete architecture is:

```text
                         ┌─────────────────────┐
                         │      JARVIS UI      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Application Control │
                         └──────────┬──────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
     Configuration             Security              Runtime State
       Engine                  Engine                  Manager
             │                      │                      │
             ▼                      ▼                      ▼
     ┌──────────────┐      ┌───────────────┐       ┌──────────────┐
     │ Identity     │      │ Permissions   │       │ Sessions     │
     │ Hotkeys      │      │ Face ID       │       │ Tasks        │
     │ Applications │      │ Confirmation  │       │ Events       │
     │ Features     │      │ Risk Engine   │       │ Metrics      │
     │ Profiles     │      │ Audit Log     │       │ Notifications│
     └──────────────┘      └───────────────┘       └──────────────┘
             │                      │
             └──────────┬───────────┘
                        ▼
                ┌──────────────────┐
                │ Agent Orchestrator│
                └────────┬─────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
     General Agent   Coding Agent   Vision Agent
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                  ┌──────────────┐
                  │  AI Router   │
                  └──────┬───────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
        Groq           OpenAI         Ollama
                         │
                         ▼
                 Credential Vault
                         │
                         ▼
                ┌────────────────┐
                │   Tool System  │
                └───────┬────────┘
                        │
       ┌────────────────┼─────────────────┐
       ▼                ▼                 ▼
   OS Tools        Applications       Integrations
       │                │                 │
       ▼                ▼                 ▼
 PowerShell       Unity/Blender       Gmail
 Filesystem       VS/Antigravity      Calendar
 Media            Custom Apps         News
 Browser                              Spotify
 Vision                              YouTube
       │
       └────────────────┬────────────────┘
                        ▼
                 Result Validation
                        │
                        ▼
                  Memory Manager
                        │
                        ▼
                    SQLite
```

## 77. IMPLEMENTATION PRIORITY

Do NOT attempt to build everything simultaneously.

### PHASE 1 — FOUNDATION

Build first:

```text
Application lifecycle
Configuration Engine
SQLite database
Event Bus
Security Manager
Credential Vault
Agent Identity
Application Manager
Feature Manager
Hotkey Manager
```

### PHASE 2 — CORE AGENT

Then:

```text
Agent Orchestrator
Tool Registry
AI Provider abstraction
General Agent
Command lifecycle
Activity timeline
```

### PHASE 3 — EXISTING JARVIS CAPABILITIES

Integrate:

```text
Whisper
Edge TTS
Face verification
OS controls
Application launching
Filesystem
PowerShell
Vision
Screenshots
QR/barcode
```

### PHASE 4 — INTEGRATIONS

Add:

```text
Gmail
Google Calendar
Hacker News
Spotify
YouTube
```

### PHASE 5 — ADVANCED AGENTS

Add:

```text
Coding Agent
Vision Agent
Automation Agent
Background Agent system
```

### PHASE 6 — POLISH

Add:

```text
Profiles
Gaming Mode
First-run wizard
Embedded manual
Import/export
Backup/rollback
Developer Mode
HUD
Advanced automation
```

---

# 78. MOST IMPORTANT ENGINEERING PRINCIPLE

Build JARVIS as a PLATFORM, not a script.

The desired relationship is:

```text
                    JARVIS CORE
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
 Configuration       Security           Agents
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
                    Tool Registry
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
     OS Tools       Applications      Integrations
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
                    User Experience
```

If this architecture is followed, adding a new application, AI provider, Gmail account, calendar, agent, feature, tool, hotkey, or automation should generally involve **registering/configuring a new component rather than rewriting the JARVIS core**.

The final target is:

**One stable JARVIS core + configurable modules + secure credentials + capability-based agents + centralized permissions + event-driven configuration + polished desktop UI.**
