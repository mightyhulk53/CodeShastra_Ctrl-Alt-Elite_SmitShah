import spacy

# Load English language model
nlp = spacy.load("en_core_web_sm")

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
    return " ".join(math_tokens)

# Example usage
input_text = "5 plus 3 then multiply by 2"
math_expression = extract_math_expression(input_text)
print("Extracted mathematical expression:", math_expression)

# Evaluate the mathematical expression
result = eval(math_expression)
print("Result:", result)