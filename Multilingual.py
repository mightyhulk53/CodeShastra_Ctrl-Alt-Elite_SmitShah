from flask import Flask, request, jsonify
from googletrans import Translator

app = Flask(__name__)

# Function to check if text is in English
def is_english(text):
    try:
        translator = Translator()
        translated = translator.translate(text, dest="en")
        return translated.src == "en"
    except Exception as e:
        print("Error:", e)
        return False

# Function to translate text to English
def translate_to_english(text):
    translator = Translator()
    translated = translator.translate(text, dest="en")
    english_text = translated.text
    return english_text

# Route for processing text input
@app.route("/process_text", methods=["POST"])
def process_text():
    if "text" not in request.form:
        return jsonify({"error": "No text input provided"})
    text = request.form["text"]
    if text.strip() == "":
        return jsonify({"error": "Empty text input provided"})
    
    is_eng = is_english(text)
    if is_eng:
        return jsonify({"text": text, "is_english": True})
    
    english_text = translate_to_english(text)
    return jsonify({"text": english_text, "is_english": False})

if __name__ == "__main__":
    app.run(debug=True)