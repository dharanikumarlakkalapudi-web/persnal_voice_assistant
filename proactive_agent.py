import threading
import time
import datetime
import urllib.request
import json

def fetch_top_news():
    """Fetches top tech news silently from HackerNews API."""
    try:
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            story_ids = json.loads(response.read().decode())[:5]
            
        news = []
        for sid in story_ids:
            story_url = f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
            sreq = urllib.request.Request(story_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(sreq) as sresponse:
                story = json.loads(sresponse.read().decode())
                news.append(story.get('title', 'Unknown Title'))
        
        if news:
            return "Top Tech News:\n" + "\n".join([f"- {n}" for n in news])
        return "No news found."
    except Exception as e:
        return f"Failed to fetch news: {e}"

def proactive_loop():
    """The main background loop."""
    print("[Proactive Agent] Background thread started. (News fetching)")
    
    while True:
        try:
            # Other background tasks can be added here.
            # We sleep for a long duration since news is only needed daily.
            time.sleep(3600)
        except Exception as e:
            time.sleep(60)

def start_proactive_agent():
    """Starts the proactive agent in a daemon thread."""
    t = threading.Thread(target=proactive_loop, daemon=True)
    t.start()
