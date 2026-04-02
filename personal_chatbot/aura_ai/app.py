import os
import sys
from flask import Flask, render_template, request, jsonify

# This line tells Python to look inside the current folder for modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Now these imports will work on Render!
from brain import get_response
from actions import perform_action

app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()
    
    # Logic: Actions first, then Brain
    response = perform_action(user_input) or get_response(user_input)
    
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
