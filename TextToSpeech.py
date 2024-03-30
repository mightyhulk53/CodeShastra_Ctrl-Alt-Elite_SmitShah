# import pyttsx3

# def text_to_speech(text):
#     # Initialize the text-to-speech engine
#     engine = pyttsx3.init()
    
#     # Set properties (optional)
#     engine.setProperty('rate', 150)  # Speed of speech
#     engine.setProperty('volume', 1.0) # Volume (0.0 to 1.0)
    
#     # Convert text to speech
#     engine.say(text)
    
#     # Wait for the speech to finish
#     engine.runAndWait()

# # Example usage
# text_to_speech("Hello, how are you?")
from gtts import gTTS 
  
# This module is imported so that we can  
# play the converted audio 
import os 
  
# The text that you want to convert to audio 
mytext = 'Once the installation is complete, you can use the code provided in the previous message to convert text to speech using the gTTS library. If you encounter any issues during installation or usage, feel free to ask for further assistance!'
  
# Language in which you want to convert 
language = 'en'
  
# Passing the text and language to the engine,  
# here we have marked slow=False. Which tells  
# the module that the converted audio should  
# have a high speed 
myobj = gTTS(text=mytext, lang=language, slow=False) 
  
# Saving the converted audio in a mp3 file named 
# welcome  
myobj.save("welcome.mp3") 
  
# Playing the converted file 
os.system(" welcome.mp3")