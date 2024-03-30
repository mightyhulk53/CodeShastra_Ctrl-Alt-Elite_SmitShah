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

def ask():

    question = str(request.json["question"]) + ". Explain in short. Answer in plaintext and not markdown."

    response = chat.send_message(str(question))

    
    return jsonify(
        {
            "response": response.text,
            "question": question
        }
    )

def ask_for_command():

    question = "Extract the implied command line command in the following line:" + str(request.json["question"]) + ". Return only an executable version of the command in plaintext. Add no notes or warnings."
    
    response = chat.send_message(str(question))
    
    return jsonify(
        {
            "response": response.text.replace("\n", ""),
            "question": question
        }
    )
    
def classify():

    question = "Classify the following command into one of the following categories: get_news, email_actions, productivity, calculations, description_or_explanation, or executable_on_commandline: " + str(request.json["question"]) + ". Return only the category of the command in plaintext. Add no notes, warnings, or any other formatting."
    
    response = chat.send_message(str(question))
    
    return jsonify(
        {
            "response": response.text.replace("\n", ""),
            "question": question
        }
    )

def runcommand(cmd: str):
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
    
