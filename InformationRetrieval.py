import wikipedia

def answer_question(question):
  """
  This function takes a question as input and tries to answer it using Wikipedia.

  Args:
      question: The question to be answered.

  Returns:
      A string containing the answer extracted from Wikipedia, 
      or a message indicating the answer couldn't be found.
  """
  try:
    # Lowercase the question for case-insensitive matching
    question = question.lower()
    
    # Search for relevant Wikipedia pages based on keywords in the question
    search_results = wikipedia.search(question, results=5)
    
    # Iterate through search results and try to find an answer
    for title in search_results:
      summary = wikipedia.summary(title, sentences=3)
      if question.lower() in summary.lower():
        return f"According to Wikipedia on {title}:\n {summary}"
    
    # No answer found in search results
    return "Sorry, I couldn't find an answer in Wikipedia."
  except wikipedia.exceptions.DisambiguationError as e:
    # Handle disambiguation errors (multiple possible pages)
    return f"There are multiple Wikipedia pages related to your question: {e}"
  except wikipedia.exceptions.PageError:
    # Handle cases where the search term doesn't match a Wikipedia page
    return "The topic you requested is not available on Wikipedia."

# Get user input
question = input("Ask me a question about anything: ")

# Try to answer the question
answer = answer_question(question)

# Print the answer
print(answer)