from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests


app = Flask(__name__)


# Function to scrape content from a website
def scrape_website(url):
    try:
        # Send GET request to the website
        response = requests.get(url)
        # Check if request was successful
        if response.status_code == 200:
            # Parse HTML content
            soup = BeautifulSoup(response.text, "html.parser")
            # Extract relevant content (you might need to customize this based on the structure of your website)
            content = soup.get_text()
            return content
        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None

# Function to get answer from website
def get_answer_from_website(query, websites):
    for website_url in websites:
        content = scrape_website(website_url)
        if content and query.lower() in content.lower():
            return f"Answer from {website_url}: {query}"
    return None

websites = [
    "https://www.linkedin.com/in/gunjan-chakraborty/",
    "https://github.com/Gunjan-007",
    "https://gunjan-007.github.io/Portfolio"
]

# Function to get answer from ChatGPT API
def get_answer_from_chatgpt(query):
    # API endpoint for ChatGPT
    api_endpoint = "https://api.openai.com/v1/completions"
    # Your OpenAI API key
    api_key = "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"
    # Parameters for the API request
    params = {
        "model": "text-davinci-002",
        "prompt": query,
        "max_tokens": 50
    }
    # Headers containing API key
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }
    # Send POST request to ChatGPT API
    response = requests.post(api_endpoint, json=params, headers=headers)
    # Get response from API
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        return "Sorry, I couldn't find an answer for that."

# Main route to handle incoming chatbot requests
@app.route("/chatbot", methods=["POST"])
def chatbot():
    # Get the user's query from the request
    query = request.json["query"]
    
    # Attempt to get answer from website
    answer = get_answer_from_website(query, websites)
    
    # If answer is not found from website, use ChatGPT API
    if not answer:
        answer = get_answer_from_chatgpt(query)
    
    # Return the answer as JSON response
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
