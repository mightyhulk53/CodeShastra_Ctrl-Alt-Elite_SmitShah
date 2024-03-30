import speech_recognition as sr
import pyttsx3
import requests as requests
import re
import os
from newsapi import NewsApiClient
import newsapi
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
        top_news = news.get_top_headlines(qintitle='India')
       
        return top_news
    except KeyboardInterrupt:
        return None
    except requests.exceptions.RequestException:
        return None

commands = {
    "play music": ["play music", "start music", "play some tunes"],
    "open file": ["open file", "open document", "show file"],
    "stop":["stop", "pause", "quit", "exit"],
    "get_news": [ "get news", "show news", "what is the news"]
    # ... more commands
}    

commandsv2 = {
    "information_retrieval": [
        "what is [query]",
        "summarize [topic]",
        "tell me about [topic]"
    ],
    "calculations": [
        "calculate [expression]",
        "what is [expression]",
        "[number] percent of [number]",
        "square root of [number]"
    ],
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
    "script_execution": [
        "run the [script name] script",
        "execute the [script name] script"
    ],
    "get_news": [ "get news", "show news", "what is the news"]
}

def speak(text):
    print("ASSISTANT -> " + text)
    try:
        engine.say(text)
        engine.runAndWait()
    except KeyboardInterrupt or RuntimeError:
        return

def match_command(user_speech):
        for command, variations in commands.items():
            if user_speech.lower() in variations:
                return command
        return None  # No matching command found

def run_git_command(command):
    """
    Runs the given Git command using subprocess.

    Args:
        command: The Git command to execute (e.g., "git status").
    """

    try:
        # Execute the command using subprocess
        result = subprocess.run(command.split(), capture_output=True, text=True)

        # Print the output of the command
        print(result.stdout)

        # Check for errors
        if result.returncode != 0:
            print("Error:", result.stderr)

    except FileNotFoundError:
        print("Error: Git is not installed or not found in the PATH.")
    except subprocess.CalledProcessError as e:
        print("Error:", e.output)

flag = 1

def run_command(matched_command, command_text):
    """
    Runs the given command using subprocess.

    Args:
        command: The command to execute (e.g., "open file").
    """
    if matched_command == "play music":
        speak("Playing music")
    elif matched_command == "open file":
        speak("Opening file")
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