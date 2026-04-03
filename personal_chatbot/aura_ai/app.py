import os
import sys
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS # Optional but helpful for web demos

# --- PATH FIX FOR RENDER ---
# This ensures Python finds brain.py and actions.py regardless of where the server starts
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.append(base_dir)

from brain import get_response
from actions import perform_action

# Pointing to templates and static folders relative to this file
app = Flask(__name__, 
            template_folder=os.path.join(base_dir, '../templates'), 
            static_folder=os.path.join(base_dir, '../static'))

CORS(app) # Allows the browser to talk to the server smoothly

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
        return jsonify({"response": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    # Render provides a 'PORT' environment variable. 
    # If it's not found (like on your laptop), it defaults to 5000.
    port = int(os.environ.get("PORT", 10000))
    
    # '0.0.0.0' is REQUIRED for cloud hosting to allow outside traffic
    app.run(host='0.0.0.0', port=port)
