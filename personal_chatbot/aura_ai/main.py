from voice import listen, speak
from brain import get_response
from actions import perform_action

WAKE_WORD = "aura"

speak("Hello, I am Aura. Say my name to start.")

while True:

    text = listen()

    if WAKE_WORD in text:

        command = text.replace(WAKE_WORD, "").strip()

        if "exit" in command:
            speak("Goodbye!")
            break

        # Try actions first
        action_result = perform_action(command)

        if action_result:
            speak(action_result)
        else:
            # AI response
            response = get_response(command)
            speak(response)
# ... (all your imports and logic above) ...

# THIS BLOCK IS RECURRED TO ACTUALLY RUN THE CODE
if __name__ == "__main__":
    # 1. Boot up message
    speak("Hello, I am Aura. I am now online and listening.")
    
    # 2. Start the Infinite Alexa Loop
    while True:
        text = listen()
        
        if text and WAKE_WORD in text:
            # Remove 'aura' from the command
            command = text.replace(WAKE_WORD, "").strip()
            
            if "exit" in command or "stop" in command:
                speak("Goodbye!")
                break
                
            # Try actions first (Chrome, Time, etc.)
            action_result = perform_action(command)
            
            if action_result:
                speak(action_result)
            else:
                # If no action, use the AI Brain (GPT-2)
                response = get_response(command)
                speak(response)