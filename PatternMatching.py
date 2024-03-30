import re
import nltk 
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Provided commands
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
    "script_execution": [
        "run the [script name] script",
        "execute the [script name] script"
    ],
    "get_news": [ "get news", "show news", "what is the news"]
}

# Input command
user_input = "What is the third derivative of 25?"

# def remove_phrases(user_input):
#     # Remove phrases like "what is," "summarize," and "tell me about"
#     for command_list in commandsv2.values():
#         for command in command_list:
#             user_input = user_input.replace(command, "")
#     return user_input.strip()

def extract_nouns(user_input):
    print("Cleaned input after removing phrases:", user_input)
    # Tokenize the input sentence
    words = word_tokenize(user_input)
    print("Tokenized words:", words)
    # Part-of-speech tagging
    tagged_words = pos_tag(words)
    print("Tagged words:", tagged_words)
    # Extract nouns and cardinal numbers
    nouns = [word for word, pos in tagged_words if pos.startswith('N') or pos == 'CD' or pos== 'JJ']
    return nouns

# Remove phrases and extract nouns
# cleaned_input = remove_phrases(user_input)
# print("Cleaned input after removing phrases:", cleaned_input)
nouns = extract_nouns(user_input)

print("Extracted Nouns:", ", ".join(nouns))
