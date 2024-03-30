import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

commands = {
    "play music": ["play music", "start music", "play some tunes"],
    "open file": ["open file", "open document", "show file"],
    # ... more commands
}    

def match_command(user_speech):
        for command, variations in commands.items():
            if user_speech.lower() in variations:
                return command
        return None  # No matching command found

while True:
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
        else:
            print("Command not recognized.")