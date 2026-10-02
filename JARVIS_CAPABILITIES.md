# User Manual

This document outlines everything the AI assistant is currently capable of doing.

## 1. Voice & Identity System
*   **Speech-to-Text:** Understands natural language via Whisper AI.
*   **Text-to-Speech:** Responds with a natural voice using Microsoft Edge TTS.
*   **Face ID Security (SFace):** Automatically turns on your webcam to verify your face before executing dangerous or sensitive commands. If unauthorized, access is denied.

## 2. Core OS Control
*   **System Time:** Instantly retrieves the current system time (`"What time is it?"`).
*   **App Navigation:** Open native applications dynamically (`"Open Notepad"`, `"Open Chrome"`, `"Open Calculator"`).
*   **PowerShell Execution:** Can execute PowerShell commands directly on the host machine. If a command fails, the assistant can read the terminal error and adjust. *(Note: This is a high-risk action and requires Face ID verification).*

## 3. Vision & Screen Analysis
*   **Screenshot Management:** Take screenshots of the current display to document the screen state.
*   **Screen Analysis:** Pass screen captures to the vision model to ask questions about what is on your screen (`"What am I looking at?"`, `"Explain this UI"`).

## 4. Personal Life & Schedule
*   **Email Management (Gmail):** Read your most recent unread emails or send emails on your behalf (`"Read my emails"`, `"Send an email to John"`).
*   **Google Calendar:** Fetch upcoming events or schedule new meetings directly on your calendar (`"What's on my schedule today?"`, `"Schedule a meeting for tomorrow at 2 PM"`).
*   **Proactive Automation:** A background worker runs tasks at scheduled intervals to autonomously check for urgent emails or compile morning briefings.

## 5. File System & Coding
*   **File Reading:** Read the contents of local files on the disk (`"Read the contents of script.py"`).
*   **Code Creation:** Create new files and write code or text into them (`"Create a new python script called hello.py"`).
*   **File Management:** Delete files permanently from the file system. *(Note: Deleting files is a dangerous action and strictly requires Face ID verification).*

## 6. Proactive Permanent Memory
*   **Memory Storage:** Has permanent memory backed by SQLite. Tell the assistant a fact (`"My favorite color is blue"`) and it will remember it forever.
*   **Memory Retrieval:** Query the memory database to recall stored facts or preferences (`"What is my favorite color?"`).
