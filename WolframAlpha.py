
import wolframalpha

def question_answer(question):
  """
  This function takes a question as input and uses the Wolfram Alpha API to find an answer.

  Args:
      question: The question to be answered.

  Returns:
      The answer from Wolfram Alpha, or None if no answer is found.
  """
  app_id = "JY6T4V-LTG6V8956K"  # Replace with your Wolfram Alpha App ID
  client = wolframalpha.Client(app_id)

  try:
    # Send the question to Wolfram Alpha
    res = client.query(question)
    # Extract the answer from the first result
    answer = next(res.results).text
    return answer
  except:
    return None

# Get user input
question = input("Ask me anything: ")

# Find the answer
answer = question_answer(question)

# Print the answer (or a message if no answer found)
if answer:
  print(answer)
else:
  print("Sorry, I couldn't understand your question.")