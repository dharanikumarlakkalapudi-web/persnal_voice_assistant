import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOL_DEFINITIONS, execute_tool

load_dotenv()

# We configure this to easily swap between OpenAI and a local Ollama instance
# If using Ollama, set OPENAI_BASE_URL="http://localhost:11434/v1" in .env
# and set OPENAI_API_KEY="ollama"
# If using OpenAI, just set OPENAI_API_KEY to your actual key
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY", "dummy-key-for-local"),
    # Defaulting to Groq for sub-second latency. Set in .env if using standard OpenAI.
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.groq.com/openai/v1")
)

# Llama-3.1-8b-instant on Groq is incredibly fast for millisecond latency
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.1-8b-instant") 

# Rolling conversation history
conversation_history = [
    {"role": "system", "content": "You are an ADVANCED PERSONAL AI ASSISTANT named Jarvis. Your persona is highly sophisticated, calm, intelligent, and composed. You are a professional and highly capable entity. Speak concisely and directly with clean articulation and minimal filler words. When reporting information, sound precise and analytical. When confirming an instruction, be calm and confident. Avoid excessive enthusiasm. Do NOT use slang, and do NOT sound like a generic text-to-speech system. Never sound excited, childish, or overly emotional. IMPORTANT RULES: 1. You have access to tools, but you must ONLY use them if the user explicitly asks (unless overridden by another rule). 2. NEVER mention your tools, rules, or internal processes out loud. 3. NEVER output raw JSON in your text response. 4. If the user asks you to read their emails, YOU MUST ask them how many they want you to read AND from which account (e.g., 'personal', 'college', or 'all') BEFORE you use the email tool, unless they already specified both. 5. CRITICAL DATA RULE: If a tool returns data (like emails or search results), you MUST read the actual contents to the user. For web searches, SUMMARIZE the results in 1 to 2 sentences max. For emails, you MUST retain a structured format like 'Email from [Sender]. Subject: [Subject]. Summary: [Your 1-2 sentence intelligent summary of the body]'. Do NOT read the entire email body word-for-word unless the user explicitly asks for the full email. 6. ACTION RULE: If an action tool (like opening an app or notepad) returns a success message, do NOT read the technical message out loud. Just give a natural, 2-word confirmation like 'Opening now.' 7. ERROR RULE: If a tool returns an error string (e.g., 'Exception' or 'failed'), do not read the raw technical error. Apologize naturally and briefly explain what went wrong. 8. SMART REMINDERS RULE: When you read the user's emails, if you notice any important deadlines, exams, or meetings, you MUST automatically use the `set_reminder` tool to schedule a reminder for the appropriate date BEFORE you respond to the user. Inform the user that you have automatically scheduled these reminders."}
]

def clean_llm_text(text: str) -> str:
    """Removes raw JSON blocks and unwanted meta-commentary from the LLM's response before speaking."""
    if not text:
        return ""
    # Remove anything that looks like {"name": ...} or raw JSON
    cleaned = re.sub(r'\{.*?\}', '', text, flags=re.DOTALL)
    
    # Remove markdown asterisks (e.g. **bold**, *italic*)
    cleaned = cleaned.replace('*', '')
    
    # Replace exclamation marks with periods to prevent the TTS from sounding overly excited or shouting
    cleaned = cleaned.replace('!', '.')
    
    # Remove hashtags and other random markdown artifacts
    cleaned = cleaned.replace('#', '')
    
    # Remove anything inside angle brackets (e.g. <email>...</email> or <thought>)
    cleaned = re.sub(r'<[^>]+>', '', cleaned)
    # Strip out common Llama 3 hallucinations about its tools
    phrases_to_remove = [
        "There's no specific function",
        "No special tool calls required",
        "I've decided not to use any",
        "Using the provided functions",
        "Based on the functions",
        "No specific info or tools are needed"
    ]
    for phrase in phrases_to_remove:
        # Regex to remove the phrase and the rest of its sentence
        cleaned = re.sub(rf"{phrase}[^\.]*\.?", "", cleaned, flags=re.IGNORECASE)
    
    # Strip any dangling JSON brackets that got left behind
    cleaned = cleaned.replace("{", "").replace("}", "")
    
    return cleaned.strip()

def process_message(user_input: str) -> str:
    """Sends user input to the LLM, handles tool calls iteratively, and returns the final response."""
    
    conversation_history.append({"role": "user", "content": user_input})
    
    max_iterations = 5
    iterations = 0
    
    while iterations < max_iterations:
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=conversation_history,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            
            # Check if the LLM decided to call a tool
            if response_message.tool_calls:
                # We must append the assistant's message with the tool_calls to the history
                conversation_history.append(response_message)
                
                # Execute all tools called by the LLM
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = tool_call.function.arguments
                    
                    # Execute the actual function
                    function_response = execute_tool(function_name, function_args)
                    
                    # Append the tool's response to the history so the LLM knows the result
                    conversation_history.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    })
                    
                iterations += 1
                continue # Loop back and let the LLM evaluate the new history
                
            else:
                # No tools called, just a normal reply
                final_text = clean_llm_text(response_message.content)
                conversation_history.append({"role": "assistant", "content": final_text})
                return final_text
                
        except Exception as e:
            error_msg = f"Error communicating with LLM: {str(e)}"
            print(f"\n[ERROR] {error_msg}")
            return "Sorry, I ran into an error processing that."
            
    return "Sorry, I had to stop thinking because it was taking too long."
