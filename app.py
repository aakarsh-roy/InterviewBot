import google.generativeai as genai
from dotenv import load_dotenv
import os
from flask import Flask, render_template, request, jsonify

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
google_api_key = os.getenv("GOOGLE_API_KEY")

# Configure the Gemini API with the API key
genai.configure(api_key=google_api_key)

# Initialize the Flask app
app = Flask(__name__)

def generate_question(tech_stack, difficulty):
    """Generate a question based on tech stack and difficulty level."""
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"You are an interview bot for {tech_stack} developers. Ask a {difficulty} level interview question. "
    
    # Generate content based on the prompt
    response = model.generate_content([prompt])

    # Return the generated question
    return response.text  # Access the generated text result

def get_feedback(answer, tech_stack, difficulty):
    """Provide feedback on the user's answer."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"As an interview coach for {tech_stack} roles, provide constructive feedback on this {difficulty} level answer: '{answer}'"
    
    # Generate content based on the feedback prompt
    response = model.generate_content([prompt])

    # Return the generated feedback
    return response.text  # Access the generated text result

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask_question", methods=["POST"])
def ask_question():
    """Handle the form submission to ask a question."""
    data = request.form
    tech_stack = data.get("tech_stack")
    difficulty = data.get("difficulty")

    # Generate the interview question based on the tech stack and difficulty level
    question = generate_question(tech_stack, difficulty)

    # Render the main page with the generated question
    return render_template("index.html", question=question)

@app.route("/give_feedback", methods=["POST"])
def give_feedback():
    """Handle the form submission to provide feedback on the user's answer."""
    data = request.form
    answer = data.get("answer")
    tech_stack = data.get("tech_stack")
    difficulty = data.get("difficulty")

    # Generate feedback based on the user's answer
    feedback = get_feedback(answer, tech_stack, difficulty)

    # Render the feedback page with the generated feedback
    return render_template("feedback.html", feedback=feedback)

if __name__ == "__main__":
    app.run(debug=True)
