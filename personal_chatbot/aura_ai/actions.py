import os
import webbrowser
import datetime

def perform_action(text):
    # Standardize input
    text = text.lower().strip()
    
    # 1. Action: Open Browser
    if "open chrome" in text or "open google" in text:
        os.system("start chrome")
        return "Opening Google Chrome for you."

    # 2. Action: Tell Current Time
    elif "time" in text:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}."

    # 3. Action: Google Search
    elif "search" in text:
        query = text.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"I am searching Google for {query}."

    # Return None if it's not a system task (so the AI Brain takes over)
    return None