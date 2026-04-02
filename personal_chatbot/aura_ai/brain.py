from ctransformers import AutoModelForCausalLM
import datetime

# Load the model (It downloads once, then works 100% offline)
print("🧠 Loading Aura's Offline Brain...")
try:
    llm = AutoModelForCausalLM.from_pretrained(
        "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF", 
        model_file="tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf", 
        model_type="llama"
    )
except Exception as e:
    print(f"Error loading model: {e}")
    llm = None

def get_response(text):
    text = text.lower().strip()
    
    # 1. Instant System Skills (No AI needed)
    if any(word in text for word in ["time", "clock", "temperature", "weather"]):
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"It's currently {now}. For live weather, I'd need an active API, but it's looking good outside!"

    if any(word in text for word in ["hi", "hello", "hey", "aura"]):
        return "Hey! I'm Aura. I'm running locally on your machine. What's on your mind?"

    # 2. Random Questions (TinyLlama Logic)
    if llm:
        try:
            # We guide the AI to give short, assistant-like answers
            prompt = f"<|system|>\nYou are Aura, a helpful AI assistant. Answer briefly.\n<|user|>\n{text}\n<|assistant|>\n"
            response = llm(prompt, max_new_tokens=60, stop=["<|user|>"])
            return response.strip()
        except:
            return "My local core is busy. Could you repeat that?"
    
    return "I'm having trouble accessing my local brain files."