import speech_recognition as sr
import pyttsx3
import requests as requests
import re
import os
from newsapi import NewsApiClient
import newsapi
import re
import subprocess

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

# commands = {
#     "play music": ["play music", "start music", "play some tunes"],
#     "open file": ["open file", "open document", "show file"],
#     "stop":["stop", "pause", "quit", "exit"],
#     "get_news": [ "get news", "show news", "what is the news"]
#     # ... more commands
# }    

commandsv2 = {
    "information_retrieval": [
        "what is",
        "summarize",
        "tell me about"
    ],
    "calculations": [
        "calculate",
        "[number] percent of [number]",
        "square root of"
    ],
    "stop":[
        "stop", 
        "pause", 
        "quit", 
        "exit"],
    "productivity": [
        "remind me to [task] at [time]",
        "add [event] to my calendar on [date] at [time]",
        "send an email to [contact] saying [message]",
        "text [message] to [contact]"
    ],
    "email_actions": [
        "send an email to [contact] saying [message]",
        "schedule an email to [contact] for [time] saying [message]"
    ],
    "get_news": [ "get news", "show news", "what is the news"],
    "execution": [
        "execute command",
        "list directory",
        "delete file",
        "execute script",
        "create file",
        "execute git command"
    ]
}

def execute_command(speech_text):
    """
    Executes commands related to file and script execution.

    Args:
        speech_text: The text of the user's speech.
    """

    # Extract the specific command from the speech text
    # (you'll need to implement this based on your NLU or pattern matching)
    command = extract_command_from_speech(speech_text)

    if command == "list directory":
        try:
            current_dir = os.getcwd()
            files = os.listdir(current_dir)
            print("Files in the current directory:")
            for file in files:
                print(file)
        except OSError as e:
            print("Error listing directory:", e)

    elif command == "delete file":
        file_name = extract_file_name_from_speech(speech_text)  # Implement this function
        try:
            os.remove(file_name)
            print("File deleted:", file_name)
        except FileNotFoundError:
            print("Error: File not found:", file_name)
        except OSError as e:
            print("Error deleting file:", e)

    elif command == "execute script" or command == "execute git command":
        script_name = extract_script_name_from_speech(speech_text)  # Implement this function
        try:
            # For Git commands, you might need to prepend "git " to the script_name
            if command == "execute git command":
                script_name = "git " + script_name
            subprocess.run(script_name.split(), check=True)
        except FileNotFoundError:
            print("Error: Script not found:", script_name)
        except subprocess.CalledProcessError as e:
            print("Error executing script:", e.output)

    elif command == "create file":
        file_name = extract_file_name_from_speech(speech_text)  # Implement this function
        try:
            with open(file_name, "x") as f:
                print("File created:", file_name)
        except FileExistsError:
            print("Error: File already exists:", file_name)
        except OSError as e:
            print("Error creating file:", e)

    else:
        print("Command not recognized:", command)

def extract_script_name_from_speech(speech_text):
    """
    Extracts the script name from speech text of the format "execute git command git <command>".

    Args:
        speech_text: The text of the user's speech.

    Returns:
        The extracted script name (Git command) if found, otherwise None.
    """

    match = re.search(r"execute git command git (.*)", speech_text.lower())
    if match:
        return match.group(1)  # Extract the captured command
    else:
        return None

def extract_file_name_from_speech(speech_text):
    """
    Extracts the file name from speech text of the form "Create file <filename>" or "Delete file <filename>".

    Args:
        speech_text: The text of the user's speech.

    Returns:
        The extracted file name if found, otherwise None.
    """

    match = re.search(r"(?:create|delete) (.*)", speech_text.lower())
    if match:
        return match.group(1).strip()  # Extract and remove leading/trailing spaces
    else:
        return None

def speak(text):
    print("ASSISTANT -> " + text)
    try:
        engine.say(text)
        engine.runAndWait()
    except KeyboardInterrupt or RuntimeError:
        return

def match_command(user_speech):
        for command, variations in commandsv2.items():
            if user_speech.lower() in variations:
                return command
        return None  # No matching command found


flag = 1

def run_command(matched_command, command_text):
    """
    Runs the given command using subprocess.

    Args:
        command: The command to execute (e.g., "open file").
    """
    if matched_command == "information_retrieval":
        speak("Retrieving information")
    elif matched_command == "calculations":
        speak("Calculating")
    elif matched_command == "stop":
        speak("Stopping")
    elif matched_command == "get_news":
        speak("Getting news from A P I")
        news = get_news()
        print(news)
        for hl in news['articles'][0:5]:
            speak(str(hl['title'])) 

while flag:
    # Use the microphone as the audio source
    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)

    # Try to recognize the speech
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        
    if text:
        matched_command = match_command(text)

        if matched_command:
            run_command(matched_command=matched_command, command_text=text)
        
        else:
            print("Command not recognized.")
            speak("Command not recognized.")
            speak("Please try again.")
    if text == "quit" or text == "exit"or text == "stop" or text == "bye":
            flag = 0 
    text = ""