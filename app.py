from flask import Flask, render_template, request
import pickle
import os
from datetime import datetime

app = Flask(__name__)

# Load the phishing model
model_path = "phishing.pkl"  # Ensure this file is in the same directory as app.py

# Check if model exists
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at {model_path}")

# Load the trained model
with open(model_path, "rb") as file:
    model = pickle.load(file)

# In-memory storage for scan history (simple list)
scan_history = []

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", history=scan_history)

@app.route("/predict", methods=["POST"])
def predict():
    url = request.form.get("url")
    if not url:
        return render_template("result.html", url="No URL provided", result="Invalid input")

    # Predict using the trained model
    prediction = model.predict([url])[0]  # Convert single URL into list for prediction

    # Map result to a readable format
    result = "Phishing Detected" if prediction == "bad" else "Safe"
    
    # Add to scan history
    scan_history.append({
        'url': url,
        'result': result,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    return render_template("result.html", url=url, result=result)

# New route for viewing history
@app.route("/history")
def history():
    return render_template("history.html", history=scan_history)

if __name__ == "__main__":
    app.run(debug=True)
