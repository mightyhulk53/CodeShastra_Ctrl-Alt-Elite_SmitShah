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
import soundfile
from pydub import AudioSegment
from Google import Create_Service
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import datetime
import os.path
import platform
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import spacy
import psutil
import socket

# Load English language model
nlp = spacy.load("en_core_web_sm")

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

def describe_machine():
    """
    Provides information about the machine where the script is running.
    """

    system = platform.system()
    release = platform.release()
    machine = platform.machine()
    
    memory_total = psutil.virtual_memory().total / (1024 ** 3)  # Convert to GB
    memory_available = psutil.virtual_memory().available / (1024 ** 3)  # Convert to GB

    # Disk usage information
    disk_usage = psutil.disk_usage("/")  # Get usage for the root partition
    disk_total = disk_usage.total / (1024 ** 3)  # Convert to GB
    disk_free = disk_usage.free / (1024 ** 3)  # Convert to GB

    return jsonify(
        {
            "system": system,
            "release": release,
            "machine": machine,
            "memory_total": memory_total,
            "memory_available": memory_available,
            "disk_total": disk_total,
            "disk_free": disk_free,
        }
    )
       

def generate_command(question):

    question = "Extract the implied command line command in the following line:" + question + ". Return only an executable version of the command for windows in plaintext. Add no notes or warnings. Your response should consist of nothing else but the command itself, such that your output can be directly executed on a windows machine. Context: " + str(subprocess.run("dir", shell=True, capture_output=True, text=True).stdout)
    
    response = chat.send_message(str(question))
    
    return str(response.text.replace("\n", ""))
    
def classify_type(cmd):

    question = "Classify the following command into one of the following categories: get_news, get_ip, email_sending, email_history, calendar_events, calculations, description_or_explanation, or executable_on_commandline: " + cmd + ". Return only the category of the command in plaintext. Add no notes, warnings, or any other formatting."
    
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
    
def text_from_base64_audio(base64_string):
    decoded_data = base64.b64decode(base64_string)
    with open("temp_audio.wav", "wb") as temp_file:
        temp_file.write(decoded_data)
        
    audio = AudioSegment.from_wav(r"E:\neov_ide\codeshastra\CodeShastra_Ctrl-Alt-Elite_SmitShah\temp_audio.wav")
    audio.export("temp2.wav", format="wav")

    try:
        with sr.AudioFile("temp2.wav") as source:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
    except KeyboardInterrupt:
        return
    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand audio"})      
    except sr.RequestError as e:
        return jsonify({"error": "Could not request results from Google Speech Recognition service; {0}".format(e)})  
    
    return text

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



def send_email(jsonobject):
    CLIENT_SECRET_FILE = r'E:\neov_ide\codeshastra\CodeShastra_Ctrl-Alt-Elite_SmitShah\smit_creds\Credentials.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    
    jsonobj = json.loads(jsonobject)
    print(jsonobj)
    print(list(jsonobj.keys()))
    
    reciever = jsonobj[list(jsonobj.keys())[0]]
    message = jsonobj[list(jsonobj.keys())[1]]
    subject = jsonobj[list(jsonobj.keys())[2]]

    emailMsg = message
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = reciever
    mimeMessage['subject'] = 'You won'
    mimeMessage.attach(MIMEText(emailMsg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    try:
        message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        return jsonify({"message": "Email sent successfully"})
    except Exception as e:
        return 'An error occurred: {}'.format(e)

def get_credentials():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token1.json'):
        creds = Credentials.from_authorized_user_file('token1.json')
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r'E:\neov_ide\codeshastra\CodeShastra_Ctrl-Alt-Elite_SmitShah\smit_creds\Credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token1.json', 'w') as token:
            token.write(creds.to_json())
    return creds
 
def create_event(eventobj):
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    try:    
        creds = get_credentials()
        service = build('calendar', 'v3', credentials=creds)
        if service:
            event = service.events().insert(calendarId='primary', body=eventobj).execute()
            return 'Event created: %s' % (event.get('htmlLink'))
        else:
            return 'Error creating event:{}'.format(service)
    except HttpError as e:
        return 'Error creating event:{}'.format(e)
 
def calendar_events(jsonobject):
    
    jsonobj = json.loads(jsonobject)
    
    sendingobj = {
        "summary": jsonobj['summary'],
        "location": jsonobj['location'],
        "start": {
            "dateTime": jsonobj['start']['dateTime'],
            "timeZone": jsonobj['start']['timeZone']
        },
        "end": {
            "dateTime": jsonobj['end']['dateTime'],
            "timeZone": jsonobj['end']['timeZone']
        }
    }
    

    return create_event(sendingobj)
    
    
def generate_calendar_event(text):
    question = r"Generate a json object in the following format {      'summary': summary,      'location': location,      'start': {        'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),        'timeZone': 'Asia/Kolkata',  # Example: 'America/Los_Angeles'     },      'end': {        'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),        'timeZone': 'Asia/Kolkata',  # Example: 'America/Los_Angeles'      }    } based on the following line:" + text + ". Return only a json object with the populated fieldsmentioned before. Do not include any fields that are unknown. Each field must be in plaintext only, and there should not be any newline characters. Do Not include any notes or warnings. Your response should consist of nothing else but the json object itself."
    
    response = chat.send_message(str(question))
    
    return str(response.text.replace("\n", ""))

def speak_and_save(text):
    print("ASSISTANT -> " + text)
    try:
        engine.save_to_file(text, "output.wav")
        engine.runAndWait()
    except KeyboardInterrupt or RuntimeError:
        return

def generate_email(text):
    question = "Generate the body of an email based on the following line:" + text + ". Return only a json object with the populated fields of reciever, message, and subject. Do not include any fields that are unknown, such as start or end dates, or newline characters. Each field must be in plaintext only. Do Not include any notes or warnings. Your response should consist of nothing else but the json object itself."
    
    response = chat.send_message(str(question))
    
    return str(response.text.replace("\n", ""))

def emailhistory():
    CLIENT_SECRET_FILE = r'E:\neov_ide\codeshastra\CodeShastra_Ctrl-Alt-Elite_SmitShah\smit_creds\Credentials.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    
    try:
        response = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=5).execute()
        messages = response.get('messages', [])
        snippets = []

        if not messages:
            return "No Messages Found in the inbox."
        else:
            print('Last 5 messages in the inbox:')
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                snippets.append('Message snippet: {}'.format(msg['snippet']))
                
        return snippets
    except Exception as e:
        return 'An error occurred: {}'.format(e)

def extract_math_expression(text):
    # Tokenize the input text
    doc = nlp(text)
    
    # Initialize a list to store tokens of the mathematical expression
    math_tokens = []
    
    # Flag to track if the previous token was a number
    prev_was_num = False
    
    # Iterate through tokens in the text
    for token in doc:
        # Check if the token is a number
        if token.pos_ == "NUM":
            # If the previous token was also a number, add a multiplication operator
            if prev_was_num:
                math_tokens.append("*")
            math_tokens.append(token.text)
            prev_was_num = True
        # Check if the token is an operator
        elif token.text in ("add", "plus"):
            math_tokens.append("+")
            prev_was_num = False
        elif token.text in ("subtract", "minus"):
            math_tokens.append("-")
            prev_was_num = False
        elif token.text in ("multiply", "times"):
            math_tokens.append("*")
            prev_was_num = False
        elif token.text == "divide":
            math_tokens.append("/")
            prev_was_num = False
    
    # Return the tokens as a string
    eval_str = " ".join(math_tokens)
    result = eval(eval_str)
    print(eval_str, result)
    
    return json.dumps({"result": result})

def get_network_info_json():
    """
    Returns a JSON object containing network information.
    """

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    network_info = {
        "hostname": hostname,
        "ip_address": ip_address,
        "interfaces": []
    }

    try:
        import psutil
        net_if_addrs = psutil.net_if_addrs()
        for interface_name, addresses in net_if_addrs.items():
            for address in addresses:
                if address.family == socket.AF_INET:  # Check for IPv4 addresses
                    interface_info = {
                        "name": interface_name,
                        "ip_address": address.address,
                        "netmask": address.netmask,
                        "broadcast": address.broadcast
                    }
                    network_info["interfaces"].append(interface_info)
    except ImportError:
        pass  # No additional information without psutil

    return json.dumps(network_info)

def determine_intent(request_type,  text):
    allowed_types = ["get_news", "get_ip", "email_sending", "email_history", "calendar_events", "calculations", "description_or_explanation", "executable_on_commandline"]
    
    if request_type not in allowed_types:
        return jsonify({
            "error": "Invalid request type",
            "given_type": request_type    
        })
    
    if request_type == "get_news":
        return get_news()
    elif request_type == "description_or_explanation":
        return ask_text(str(text))
    elif request_type == "executable_on_commandline":
        return run_command(generate_command(str(text)))
    elif request_type == "email_sending":
        returnobj =  generate_email(str(text)).replace("\n", "")
        return send_email(jsonobject=returnobj)
    elif request_type == "email_history":
        return emailhistory()
    elif request_type == "calendar_events":
        returnobj = generate_calendar_event(str(text)).replace("\n", "")
        return calendar_events(jsonobject=returnobj)      
    elif request_type == "calculations":
        return extract_math_expression(str(text))
    elif request_type == "get_ip":
        return get_network_info_json()
    else:
        return "Wait for Support"
    
@app.route("/ask_in_audio", methods=["POST"])
@cross_origin()
def ask_in_audio():
    
    base64_string = request.json["b64"]
    
    text = text_from_base64_audio(base64_string)
    
    if not text:
        return jsonify({"error": "Could not understand audio"})    
    
    print("USER -> " + text)
    
    req_class = classify_type(str(text))
    
    ret = determine_intent(req_class, text)
    

    
    return ret

    
@app.route("/ask_in_text", methods=["POST"])
@cross_origin()
def ask_in_text():
    
    question = request.json["question"]
    req_class = classify_type(str(question))
    
    ret = determine_intent(req_class, question)
    

    
    return ret 

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

def text_from_base64_audio(base64_string):
    decoded_data = base64.b64decode(base64_string)
    with open("temp_audio.wav", "wb") as temp_file:
        temp_file.write(decoded_data)
        
    audio = AudioSegment.from_wav(r"E:\neov_ide\codeshastra\CodeShastra_Ctrl-Alt-Elite_SmitShah\temp_audio.wav")
    audio.export("temp2.wav", format="wav")

    try:
        with sr.AudioFile("temp2.wav") as source:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
    except KeyboardInterrupt:
        return
    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand audio"})      
    except sr.RequestError as e:
        return jsonify({"error": "Could not request results from Google Speech Recognition service; {0}".format(e)})  
    
    return text


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5051)