import os
import sys
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

# --- PATH FIX FOR RENDER ---
# Get the directory where THIS file (app.py) lives
base_dir = os.path.dirname(os.path.abspath(__file__))

# Add base_dir to Python path so imports work
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

# Now import your modules
from brain import get_response
from actions import perform_action

# Setup Flask with correct paths
# Templates should be at: personal_chatbot/templates/
# Static should be at: personal_chatbot/static/
template_path = os.path.join(os.path.dirname(base_dir), 'templates')
static_path = os.path.join(os.path.dirname(base_dir), 'static')

app = Flask(__name__, 
            template_folder=template_path,
            static_folder=static_path)

CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message", "").strip()
        
        if not user_input:
            return jsonify({"response": "I'm listening..."})
        
        # Priority Logic: Check for physical actions first
        response = perform_action(user_input)
        
        # If no action was triggered, use the Brain (Intent Engine)
        if not response:
            response = get_response(user_input)
        
        return jsonify({"response": response})
    
    except Exception as e:
        print(f"Error in /chat: {str(e)}")  # This will show in Render logs
        return jsonify({"response": f"Oops! Something went wrong: {str(e)}"}), 500

@app.route("/health")
def health():
    """Health check endpoint for Render"""
    return "OK", 200

if __name__ == "__main__":
    # Render provides PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    
    # 0.0.0.0 allows external connections (required for Render)
    print(f"Starting server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
