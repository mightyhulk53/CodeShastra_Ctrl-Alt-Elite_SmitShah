import speech_recognition as sr
import pyttsx3
import requests as requests
import re
import os
from newsapi import NewsApiClient
import newsapi
import re
import subprocess
import pandas as pd
import google.generativeai as genai
import shlex

text_file = r"E:\Work\sem5backups\localdata\newkey.txt"

with open(text_file, "r") as f:
    api_key = f.read().strip()
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-pro-latest')
chat = model.start_chat(history=[])

# Initialize the recognizer
recognizer = sr.Recognizer()

engine = pyttsx3.init()
engine.setProperty('rate', 185)


NEWS = "f8545dec6b684508938d0b230b84b626"
news = NewsApiClient(api_key=NEWS)

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

def get_news():
    try:
        print("Getting news") 
        speak("Function Called")
        top_news = news.get_top_headlines(q='India')
       
        return top_news
    except KeyboardInterrupt:
        return None
    except requests.exceptions.RequestException:
        return None

def ask_text(question):

    question = question + ". Explain in short. Answer in plaintext and not markdown."

    response = chat.send_message(str(question))

    
    return jsonify(
        {
            "response": response.text,
            "question": question
        }
    )

def generate_command(question):

    question = "Extract the implied command line command in the following line:" + question + ". Return only an executable version of the command in plaintext. Add no notes or warnings."
    
    response = chat.send_message(str(question))
    
    return jsonify(
        {
            "response": response.text.replace("\n", ""),
            "question": question
        }
    )
    
def classify_type(cmd):

    question = "Classify the following command into one of the following categories: get_news, email_actions, productivity, calculations, description_or_explanation, or executable_on_commandline: " + cmd + ". Return only the category of the command in plaintext. Add no notes, warnings, or any other formatting."
    
    response = chat.send_message(str(question))
    
    return jsonify(
        {
            "response": response.text.replace("\n", ""),
            "question": question
        }
    )

def run_command(cmd: str):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)    
    return jsonify(
        {
            "output": result.stdout,
            "return_code": resultreturncode
        }
    )
    
def is_safe_command(command):
    # Split the command into arguments
    args = shlex.split(command)

    # Check for well-known risky commands (not exhaustive)
    risky_commands = ["cp", "shutdown", "reboot", "fdisk", "mount", "umount"]
    if args[0] in risky_commands:
        return False

    # Check for redirection or piping (can be risky)
    for arg in args:
        if arg in [">", "<", "|"]:
            return False

    # If no risky patterns found, tentatively assume safe
    return True

def speak(text):
    print("ASSISTANT -> " + text)
    try:
        engine.say(text)
        engine.runAndWait()
    except KeyboardInterrupt or RuntimeError:
        return

def determine_intent(request_type,  text):
    allowed_types = ["get_news", "email_actions", "productivity", "calculations", "description_or_explanation", "executable_on_commandline"]
    
    if request_type not in allowed_types:
        return jsonify({"error": "Invalid request type"})
    
    if request_type == "get_news":
        return get_news()
    elif request_type == "description_or_explanation":
        return ask_text(str(text))
    else:
        return "Wait for Support"
    

    
    
@app.route("/ask_in_text", methods=["POST"])
@cross_origin()
def ask_in_text():
    
    question = request.json["question"]
    req_class = classify_type(str(question))
    
    
    
    return 