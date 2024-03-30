import speech_recognition as sr
import pyttsx3

# Initialize the recognizer
recognizer = sr.Recognizer()

engine = pyttsx3.init()
engine.setProperty('rate', 185)

commands = {
    "play music": ["play music", "start music", "play some tunes"],
    "open file": ["open file", "open document", "show file"],
    "stop":["stop", "pause", "quit", "exit"]
    # ... more commands
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

flag = 1

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
            print("Command Found!", matched_command)
            speak("Yes, I can help you with that.")
            speak(f"Executing command...{matched_command}")
        
        else:
            print("Command not recognized.")
            speak("Command not recognized.")
            speak("Please try again.")
    if text == "quit" or text == "exit"or text == "stop" or text == "bye":
            flag = 0
            speak("Goodbye!")        
    text = ""