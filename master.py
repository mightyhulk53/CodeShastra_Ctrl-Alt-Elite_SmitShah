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
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import base64

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
        # Get the top news headlines from India
        top_news = news.get_top_headlines(q='India')
       
        retlist = []
        for hl in top_news['articles'][0:5]:
            retlist.append(hl['title'])
        return retlist
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

    question = "Extract the implied command line command in the following line:" + question + ". Return only an executable version of the command for windows in plaintext. Add no notes or warnings. Your response should consist of nothing else but the command itself, such that your output can be directly executed on a windows machine."
    
    response = chat.send_message(str(question))
    
    return str(response.text.replace("\n", ""))
    
def classify_type(cmd):

    question = "Classify the following command into one of the following categories: get_news, email_actions, productivity, calculations, description_or_explanation, or executable_on_commandline: " + cmd + ". Return only the category of the command in plaintext. Add no notes, warnings, or any other formatting."
    
    response = chat.send_message(str(question))
    
    return response.text.replace("\n", "")

def run_command(cmd: str):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)    
    return jsonify(
        {
            "output": result.stdout,
            "return_code": result.returncode
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

def speak_and_save(text):
    print("ASSISTANT -> " + text)
    try:
        engine.save_to_file(text, "output.wav")
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
    elif request_type == "executable_on_commandline":
        return "obtained_command"

    else:
        return "Wait for Support"
    
@app.route("/ask_in_audio", methods=["POST"])
@cross_origin()
def ask_in_audio():
    
    decoded_data = base64.b64decode(base64_string)
    with open("temp_audio.wav", "wb") as temp_file:
        temp_file.write(decoded_data)

    try:
        with sr.AudioFile("temp_audio.wav") as source:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
    except KeyboardInterrupt:
        return
    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand audio"})      
    except sr.RequestError as e:
        return jsonify({"error": "Could not request results from Google Speech Recognition service; {0}".format(e)})  
    
    req_class = classify_type(str(text))
    
    ret = determine_intent(req_class, text)
    if ret == "obtained_command":
        cmmd = generate_command(str(text)).replace("\n", "")
        flagger = is_safe_command(cmmd)
        if flagger:
            print("Command is safe")
            retjson =  jsonify({
                "foundCommand": True,
                "Safe": True,
                "SafeCommand": str(cmmd),
            })
        else:
            print("Command is unsafe")
            retjson =  jsonify({
                "foundCommand": True,
                "Safe": False,
                "SafeCommand": None,
                "Command": str(cmmd),
            })
    else:
        retjson = jsonify({
            "Response": ret,
        })

    
    return retjson if retjson else ret

    
@app.route("/ask_in_text", methods=["POST"])
@cross_origin()
def ask_in_text():
    
    question = request.json["question"]
    req_class = classify_type(str(question))
    
    ret = determine_intent(req_class, question)
    if ret == "obtained_command":
        cmmd = generate_command(str(question)).replace("\n", "")
        flagger = is_safe_command(cmmd)
        if flagger:
            print("Command is safe")
            retjson =  jsonify({
                "foundCommand": True,
                "Safe": True,
                "SafeCommand": str(cmmd),
            })
        else:
            print("Command is unsafe")
            retjson =  jsonify({
                "foundCommand": True,
                "Safe": False,
                "SafeCommand": None,
                "Command": str(cmmd),
            })
    else:
        retjson = jsonify({
            "Response": ret,
        })

    
    return retjson if retjson else ret 

@app.route("/verified_command", methods=["POST"])
@cross_origin()
def verified_command():
    
    cmmd = request.json["command"]
    status = request.json["status"]
    
    if status == "Verified":
        results = run_command(cmmd)
    else:
        results = jsonify({"error": "Command not verified"})
    
    return results

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5051)