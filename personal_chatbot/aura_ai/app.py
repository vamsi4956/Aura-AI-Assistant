import os
from flask import Flask, render_template, request, jsonify
from brain import get_response
from actions import perform_action

base_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(base_dir)

app = Flask(__name__, 
            template_folder=os.path.join(project_root, "templates"),
            static_folder=os.path.join(project_root, "static"))

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