import os
import sys
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# --- PATH FIX FOR RENDER ---
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

# Print debug info
print(f"=== DEBUG INFO ===", flush=True)
print(f"Base dir: {base_dir}", flush=True)
print(f"Python path: {sys.path}", flush=True)
print(f"PORT env var: {os.environ.get('PORT', 'NOT SET')}", flush=True)

try:
    from brain import get_response
    from actions import perform_action
    print("✓ Successfully imported brain and actions", flush=True)
except Exception as e:
    print(f"✗ Import error: {e}", flush=True)
    # Create dummy functions if imports fail
    def get_response(text):
        return f"Echo: {text}"
    def perform_action(text):
        return None

# Setup Flask
template_path = os.path.join(os.path.dirname(base_dir), 'templates')
static_path = os.path.join(os.path.dirname(base_dir), 'static')

print(f"Template path: {template_path}", flush=True)
print(f"Static path: {static_path}", flush=True)

app = Flask(__name__, 
            template_folder=template_path,
            static_folder=static_path)

CORS(app)

@app.route("/")
def home():
    try:
        return render_template("index.html")
    except Exception as e:
        return f"<h1>Aura AI Chatbot</h1><p>Template error: {e}</p><p>Try <a href='/health'>/health</a></p>"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message", "").strip()
        
        if not user_input:
            return jsonify({"response": "I'm listening..."})
        
        response = perform_action(user_input)
        
        if not response:
            response = get_response(user_input)
        
        return jsonify({"response": response})
    
    except Exception as e:
        print(f"Error in /chat: {str(e)}", flush=True)
        return jsonify({"response": f"Error: {str(e)}"}), 500

@app.route("/health")
def health():
    return "OK", 200

# This is crucial - gunicorn will call this app object directly
# So we DON'T want the if __name__ == '__main__' block to run
print(f"Flask app created successfully!", flush=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"Starting Flask dev server on port {port}...", flush=True)
    app.run(host='0.0.0.0', port=port, debug=False)
