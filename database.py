import sqlite3
import json
import os
import datetime

DB_FILE = "jarvis.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create Memories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fact TEXT NOT NULL,
            category TEXT DEFAULT 'General',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Reminders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    
    # Migrate old JSON reminders if they exist
    if os.path.exists("reminders.json"):
        try:
            with open("reminders.json", "r") as f:
                old_reminders = json.load(f)
            if old_reminders:
                for r in old_reminders:
                    if "date" in r and "message" in r:
                        set_reminder(r["date"], r["message"])
                print("[Database] Migrated reminders.json to SQLite.")
            # Rename file to prevent re-migration
            os.rename("reminders.json", "reminders.json.bak")
        except Exception as e:
            print(f"[Database Error] Could not migrate reminders: {e}")

# ===========================
# MEMORY TOOLS
# ===========================
def remember_fact(fact: str, category: str = "General") -> str:
    """Store a permanent memory or fact about the user."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO memories (fact, category) VALUES (?, ?)", (fact, category))
        conn.commit()
        conn.close()
        return f"Successfully remembered: {fact}"
    except Exception as e:
        return f"Failed to remember fact: {e}"

def recall_fact(query: str = "") -> str:
    """Retrieves all memories/facts, optionally filtering by a keyword query."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        if query:
            cursor.execute("SELECT id, fact, category, timestamp FROM memories WHERE fact LIKE ? OR category LIKE ?", (f"%{query}%", f"%{query}%"))
        else:
            cursor.execute("SELECT id, fact, category, timestamp FROM memories")
            
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return "I don't have any memories matching that."
            
        output = ["Here is what I remember:"]
        for row in rows:
            output.append(f"[{row[0]}] ({row[2]}): {row[1]}")
        return "\n".join(output)
    except Exception as e:
        return f"Failed to recall facts: {e}"

def delete_fact(fact_id: int) -> str:
    """Deletes a fact from memory using its exact ID."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM memories WHERE id = ?", (fact_id,))
        changes = conn.total_changes
        conn.commit()
        conn.close()
        
        if changes > 0:
            return f"Successfully deleted fact ID {fact_id}."
        else:
            return f"Fact ID {fact_id} not found."
    except Exception as e:
        return f"Failed to delete fact: {e}"

# ===========================
# REMINDER TOOLS (Overrides old tools.py json ones)
# ===========================
def set_reminder(date: str, message: str) -> str:
    """Sets a reminder for a specific date (YYYY-MM-DD)."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Prevent duplicates
        cursor.execute("SELECT id FROM reminders WHERE date = ? AND message = ?", (date, message))
        if cursor.fetchone():
            conn.close()
            return f"Reminder already exists for {date}."
            
        cursor.execute("INSERT INTO reminders (date, message) VALUES (?, ?)", (date, message))
        conn.commit()
        conn.close()
        return f"Reminder set for {date}."
    except Exception as e:
        return f"Failed to set reminder: {e}"

def get_all_reminders() -> str:
    """Returns a list of all currently scheduled reminders."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, message FROM reminders ORDER BY date ASC")
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return "You have no reminders set."
            
        output = ["Your scheduled reminders:"]
        for row in rows:
            output.append(f"[{row[0]}] {row[1]}: {row[2]}")
        return "\n".join(output)
    except Exception as e:
        return f"Failed to get reminders: {e}"

def delete_reminder(keyword_or_id: str) -> str:
    """Deletes a reminder by an exact ID or matching keyword."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # If it's just a number, delete by ID
        if keyword_or_id.isdigit():
            cursor.execute("DELETE FROM reminders WHERE id = ?", (int(keyword_or_id),))
        else:
            cursor.execute("DELETE FROM reminders WHERE message LIKE ?", (f"%{keyword_or_id}%",))
            
        changes = conn.total_changes
        conn.commit()
        conn.close()
        
        if changes > 0:
            return f"Successfully deleted {changes} reminder(s)."
        else:
            return f"No reminders found matching '{keyword_or_id}'."
    except Exception as e:
        return f"Failed to delete reminder: {e}"

def check_todays_reminders() -> list:
    """Helper function to read and clear today's (or overdue) reminders. Used at startup."""
    try:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, message FROM reminders WHERE date <= ?", (today,))
        rows = cursor.fetchall()
        
        if not rows:
            conn.close()
            return []
            
        todays_messages = []
        for row in rows:
            todays_messages.append(row[1])
            cursor.execute("DELETE FROM reminders WHERE id = ?", (row[0],))
            
        conn.commit()
        conn.close()
        return todays_messages
    except Exception as e:
        print(f"[Database Error] Checking reminders failed: {e}")
        return []

# Initialize DB on import
init_db()
