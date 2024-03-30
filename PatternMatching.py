import re

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
        "exit"
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

def match_command(user_speech):
    for command, variations in commandsv2.items():
        for variation in variations:
            if all(part in user_speech.lower() for part in variation.split()):
                parts = re.findall(r'\[([^]]+)\]', variation)  # Extract parts inside square brackets
                meaningful_parts = []
                for part in parts:
                    if part == "number":
                        numbers = re.findall(r'\d+', user_speech)
                        meaningful_parts.extend(numbers)
                    elif part == "message":
                        message = re.search(r'\"(.+?)\"', user_speech)
                        if message:
                            meaningful_parts.append(message.group(1))
                    elif part == "time":
                        time = re.search(r'\d{1,2}:\d{2}', user_speech)
                        if time:
                            meaningful_parts.append(time.group())
                    elif part == "date":
                        date = re.search(r'\d{1,2}/\d{1,2}/\d{4}', user_speech)
                        if date:
                            meaningful_parts.append(date.group())
                    elif part == "contact":
                        contact = re.search(r'\b[A-Za-z]+\b', user_speech)
                        if contact:
                            meaningful_parts.append(contact.group())
                    elif part == "script name":
                        script_name = re.search(r'\b[A-Za-z]+\b', user_speech)
                        if script_name:
                            meaningful_parts.append(script_name.group())
                    elif part == "event":
                        event = re.search(r'\"(.+?)\"', user_speech)
                        if event:
                            meaningful_parts.append(event.group(1))
                    elif part == "task":
                        task = re.search(r'\"(.+?)\"', user_speech)
                        if task:
                            meaningful_parts.append(task.group(1))
                    elif part == "operation":
                        operation = re.search(r'square root', user_speech)
                        if operation:
                            meaningful_parts.append(operation.group())
                    else:
                        meaningful_parts.append(part)
                return command, meaningful_parts
    return None, None  # No matching command found

# Example usage:
user_input = "What is the square root of 25?"
matched_command, matched_parts = match_command(user_input)
if matched_command:
    print(f"Matched command: {matched_command}")
    print(f"Meaningful parts: {matched_parts}")
else:
    print("No matching command found.")
