from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pandas as pd
import spacy
import google.generativeai as genai

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

text_file = r"E:\Work\sem5backups\localdata\newkey.txt"

with open(text_file, "r") as f:
    api_key = f.read().strip()
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-pro-latest')
chat = model.start_chat(history=[])

@app.route("/ask", methods=["POST"])
@cross_origin()
def ask():

    question = str(request.json["question"]) + ". Explain in short. Answer in plaintext and not markdown."

    response = chat.send_message(str(question))

    
    return jsonify(
        {
            "response": response.text,
            "question": question
        }
    )

@app.route("/ask_for_command", methods=["POST"])
@cross_origin()
def ask_for_command():

    question = "Extract the implied command line command in the following code:" + str(request.json["question"]) + ". Return only an executable version of the command in plaintext. Add no notes or warnings."
    
    response = chat.send_message(str(question))
    
    return jsonify(
        {
            "response": response.text,
            "question": question
        }
    )
    
@app.route("/classify", methods=["POST"])
@cross_origin()
def classify():

    question = "Classify the following command into one of the following categories: get_news, email_actions, productivity, calculations, description_or_explanation, or executable_on_commandline: " + str(request.json["question"]) + ". Return only the category of the command in plaintext. Add no notes, warnings, or any other formatting."
    
    response = chat.send_message(str(question))
    
    return jsonify(
        {
            "response": response.text.replace("\n", ""),
            "question": question
        }
    )

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5051)