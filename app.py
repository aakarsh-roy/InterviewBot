import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import re
import random
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session
import secrets

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
google_api_key = os.getenv("GOOGLE_API_KEY")

# Configure the Gemini API with the API key
genai.configure(api_key=google_api_key)

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # For session management
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

# In-memory storage for session data (use database in production)
active_sessions = {}


def generate_question(tech_stack, difficulty, question_type='technical', previous_questions=None):
    """Generate a question based on tech stack and difficulty level."""
    model = genai.GenerativeModel("gemini-2.5-flash")

    # Enhanced prompts for cleaner, single questions
    if question_type == 'behavioral':
        prompt = f"Generate a single, clear behavioral interview question relevant to {tech_stack} professionals at {difficulty} level. Focus on real-world scenarios, teamwork, or problem-solving. Provide just the question in plain text without formatting."
    elif question_type == 'coding':
        prompt = f"Generate a single {difficulty} level coding challenge for {tech_stack}. State the problem clearly in plain text without any code examples or formatting. Just describe what needs to be implemented."
    elif question_type == 'system_design':
        prompt = f"Generate a single {difficulty} level system design question for {tech_stack}. Focus on architecture, scalability, or design patterns. Provide just the question in plain text."
    else:
        difficulty_prompts = {
            'easy': f"Generate a single, clear beginner-level {tech_stack} interview question. Focus only on basic concepts. Provide just the question without any additional formatting, context, or explanation. Keep it concise and straightforward.",
            'medium': f"Generate a single, clear intermediate-level {tech_stack} interview question that tests practical knowledge. Provide just the question without any additional formatting, context, or explanation. Keep it concise and focused.",
            'hard': f"Generate a single, clear advanced {tech_stack} interview question involving complex concepts or problem-solving. Provide just the question without any additional formatting, context, or explanation. Keep it concise and challenging."
        }
        prompt = difficulty_prompts.get(difficulty, f"Generate a single, clear {difficulty} level {tech_stack} interview question without any formatting or additional context.")
    
    # Avoid duplicate questions
    if previous_questions:
        prompt += f" Do not ask about these topics that were already covered: {', '.join(previous_questions[:3])}"
    
    prompt += " Do not include markdown formatting, asterisks, bold text, or any interviewer context. Just provide the plain question text."
    
    # Generate content based on the prompt
    response = model.generate_content([prompt])

    # Clean up the response to remove any remaining formatting
    question = response.text.strip()
    question = re.sub(r'\*\*|\*|#', '', question)
    question = question.replace('Question:', '').strip()
    
    # If the question starts with a number or bullet point, clean it
    if re.match(r'^[\d•\-]', question):
        question = re.sub(r'^[\d]+\.\s*', '', question).strip()
        question = re.sub(r'^[•\-]\s*', '', question).strip()
    
    return question


def generate_hint(question, answer_so_far):
    """Generate a helpful hint for the current question."""
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    prompt = f"""
    For this interview question: {question}
    
    The candidate has started with: {answer_so_far if answer_so_far else 'nothing yet'}
    
    Provide a subtle hint to guide them in the right direction without giving away the complete answer.
    Keep the hint concise, encouraging, and educational. Use plain text only, no formatting.
    """
    
    response = model.generate_content([prompt])
    hint = response.text.strip()
    hint = re.sub(r'\*\*|\*|#', '', hint)
    
    return hint


def analyze_answer_quality(answer):
    """Analyze answer quality and extract score using AI."""
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    prompt = f"""
    Analyze this interview answer and provide a numerical score from 0-10:
    
    Answer: {answer}
    
    Respond with ONLY a number between 0 and 10. No other text.
    """
    
    try:
        response = model.generate_content([prompt])
        score_text = response.text.strip()
        # Extract first number found
        match = re.search(r'\d+', score_text)
        if match:
            score = int(match.group())
            return min(max(score, 0), 10)  # Ensure between 0-10
    except:
        pass
    
    return 5  # Default score if analysis fails


def get_feedback(answer, tech_stack, difficulty, question, time_taken=None):
    """Provide detailed feedback on the user's answer."""
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    time_context = f" The answer was provided in {time_taken:.1f} seconds." if time_taken else ""
    
    prompt = f"""
    As an expert interview coach for {tech_stack} roles, provide comprehensive feedback on this {difficulty} level answer.{time_context}
    
    Question: {question}
    Answer: {answer}
    
    Provide feedback in plain text format with these sections (use exactly these labels):
    
    SCORE: Give a number from 0-10
    
    STRENGTHS: List 2-3 specific things done well
    
    IMPROVEMENTS: List 2-3 specific areas that need work
    
    TECHNICAL_ADVICE: Provide specific technical suggestions with examples
    
    SAMPLE_ANSWER: Provide a brief example of a better answer approach
    
    NEXT_STEPS: Suggest what to study or practice next
    
    Use plain text only, no markdown, asterisks, or special formatting.
    """
    
    response = model.generate_content([prompt])
    feedback = response.text.strip()
    
    # Clean up formatting
    feedback = re.sub(r'\*\*|\*|`|```|#{1,3}', '', feedback)
    
    # Structure the output
    sections = ['SCORE:', 'STRENGTHS:', 'IMPROVEMENTS:', 'TECHNICAL_ADVICE:', 'SAMPLE_ANSWER:', 'NEXT_STEPS:']
    for section in sections:
        feedback = feedback.replace(section, f'\n\n{section}\n')
    
    return feedback.strip()


def suggest_difficulty_adjustment(score, current_difficulty):
    """Suggest difficulty adjustment based on performance."""
    if score >= 8 and current_difficulty != 'hard':
        return 'increase'
    elif score <= 4 and current_difficulty != 'easy':
        return 'decrease'
    return 'maintain'




@app.route("/")
def index():
    # Initialize session if needed
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(8)
        session['questions_asked'] = []
        session['total_score'] = 0
        session['questions_answered'] = 0
    
    return render_template("index.html", 
                         session_progress=len(session.get('questions_asked', [])),
                         avg_score=session.get('total_score', 0) / max(session.get('questions_answered', 1), 1))

@app.route("/ask_question", methods=["POST"])
def ask_question():
    """Handle the form submission to ask a question."""
    data = request.form
    tech_stack = data.get("tech_stack")
    difficulty = data.get("difficulty")
    question_type = data.get("question_type", "technical")

    # Store in session for later use
    session['current_tech_stack'] = tech_stack
    session['current_difficulty'] = difficulty
    session['current_question_type'] = question_type
    session['question_start_time'] = datetime.now().isoformat()
    
    # Get previous questions to avoid repetition
    previous_questions = session.get('questions_asked', [])

    # Generate the interview question based on the tech stack and difficulty level
    question = generate_question(tech_stack, difficulty, question_type, previous_questions)
    session['current_question'] = question
    
    # Track question
    if 'questions_asked' not in session:
        session['questions_asked'] = []
    session['questions_asked'].append(question[:50])  # Store snippet

    # Render the main page with the generated question
    return render_template("index.html", 
                         question=question,
                         tech_stack=tech_stack, 
                         difficulty=difficulty,
                         question_type=question_type,
                         session_progress=len(session.get('questions_asked', [])),
                         avg_score=session.get('total_score', 0) / max(session.get('questions_answered', 1), 1))

@app.route("/give_feedback", methods=["POST"])
def give_feedback_route():
    """Handle the form submission to provide feedback on the user's answer."""
    data = request.form
    answer = data.get("answer")
    tech_stack = session.get('current_tech_stack', data.get("tech_stack"))
    difficulty = session.get('current_difficulty', data.get("difficulty"))
    question = session.get('current_question', data.get("question"))

    # Calculate time taken
    start_time = session.get('question_start_time')
    time_taken = None
    if start_time:
        start_dt = datetime.fromisoformat(start_time)
        time_taken = (datetime.now() - start_dt).total_seconds()

    # Generate feedback based on the user's answer
    feedback = get_feedback(answer, tech_stack, difficulty, question, time_taken)
    
    # Extract score from feedback
    score_match = re.search(r'SCORE:\s*(\d+)', feedback)
    score = int(score_match.group(1)) if score_match else 5
    
    # Update session statistics
    if 'total_score' not in session:
        session['total_score'] = 0
    if 'questions_answered' not in session:
        session['questions_answered'] = 0
    
    session['total_score'] += score
    session['questions_answered'] += 1
    session['last_score'] = score
    
    # Suggest difficulty adjustment
    adjustment = suggest_difficulty_adjustment(score, difficulty)
    suggested_difficulty = difficulty
    if adjustment == 'increase' and difficulty == 'easy':
        suggested_difficulty = 'medium'
    elif adjustment == 'increase' and difficulty == 'medium':
        suggested_difficulty = 'hard'
    elif adjustment == 'decrease' and difficulty == 'hard':
        suggested_difficulty = 'medium'
    elif adjustment == 'decrease' and difficulty == 'medium':
        suggested_difficulty = 'easy'

    # Render the feedback page with the generated feedback
    return render_template("feedback.html", 
                         feedback=feedback,
                         score=score,
                         time_taken=time_taken,
                         tech_stack=tech_stack,
                         difficulty=difficulty,
                         suggested_difficulty=suggested_difficulty if suggested_difficulty != difficulty else None,
                         session_progress=len(session.get('questions_asked', [])),
                         avg_score=session.get('total_score', 0) / session.get('questions_answered', 1))



@app.route("/api/random_question")
def random_question():
    """API endpoint for getting a random question without form submission."""
    tech_stacks = ["Python", "JavaScript", "Java", "C++", "React", "Node.js", "Web Development", "Data Science", "Machine Learning", "DevOps"]
    difficulties = ["easy", "medium", "hard"]
    question_types = ["technical", "behavioral", "coding", "system_design"]
    
    tech_stack = random.choice(tech_stacks)
    difficulty = random.choice(difficulties)
    question_type = random.choice(question_types)
    
    question = generate_question(tech_stack, difficulty, question_type)
    
    return jsonify({
        'question': question,
        'tech_stack': tech_stack,
        'difficulty': difficulty,
        'question_type': question_type
    })

@app.route("/api/quick_tip")
def quick_tip():
    """API endpoint for interview tips."""
    tips = [
        "Always think out loud during technical interviews to show your problem-solving process.",
        "Don't be afraid to ask clarifying questions about the problem requirements.",
        "Practice explaining complex concepts in simple terms.",
        "When stuck, break the problem down into smaller, manageable pieces.",
        "It's okay to admit when you don't know something, but show willingness to learn.",
        "Always consider edge cases and test your solutions mentally.",
        "Practice coding without an IDE to get comfortable with syntax.",
        "Review common data structures and their time complexities.",
        "Prepare questions to ask the interviewer about the role and company.",
        "Practice system design concepts for senior-level positions.",
        "Use the STAR method for behavioral questions: Situation, Task, Action, Result.",
        "Research the company's tech stack and recent projects before the interview.",
        "Practice whiteboarding without erasing - interviewers want to see your thought process.",
        "Time management is crucial - don't spend too long on one part of the solution.",
        "Always test your code mentally or on paper before declaring it complete."
    ]
    
    return jsonify({'tip': random.choice(tips)})

@app.route("/api/get_hint", methods=["POST"])
def get_hint():
    """API endpoint for getting a hint on the current question."""
    data = request.json
    question = data.get('question', session.get('current_question', ''))
    answer_so_far = data.get('answer_so_far', '')
    
    if not question:
        return jsonify({'error': 'No active question'}), 400
    
    hint = generate_hint(question, answer_so_far)
    
    return jsonify({'hint': hint})

@app.route("/api/session_stats")
def session_stats():
    """API endpoint for getting current session statistics."""
    return jsonify({
        'questions_answered': session.get('questions_answered', 0),
        'total_score': session.get('total_score', 0),
        'average_score': session.get('total_score', 0) / max(session.get('questions_answered', 1), 1),
        'last_score': session.get('last_score', 0),
        'session_progress': len(session.get('questions_asked', []))
    })

@app.route("/reset_session", methods=["POST"])
def reset_session():
    """Reset the current interview session."""
    session.clear()
    session['session_id'] = secrets.token_hex(8)
    session['questions_asked'] = []
    session['total_score'] = 0
    session['questions_answered'] = 0
    return jsonify({'status': 'success', 'message': 'Session reset successfully'})

@app.route("/next_question", methods=["POST"])
def next_question():
    """Generate next question maintaining current settings."""
    tech_stack = session.get('current_tech_stack', 'Python')
    difficulty = session.get('current_difficulty', 'medium')
    question_type = session.get('current_question_type', 'technical')
    
    # Adjust difficulty if needed based on last score
    if session.get('last_score', 5) >= 8 and difficulty != 'hard':
        if difficulty == 'easy':
            difficulty = 'medium'
        elif difficulty == 'medium':
            difficulty = 'hard'
    elif session.get('last_score', 5) <= 4 and difficulty != 'easy':
        if difficulty == 'hard':
            difficulty = 'medium'
        elif difficulty == 'medium':
            difficulty = 'easy'
    
    previous_questions = session.get('questions_asked', [])
    question = generate_question(tech_stack, difficulty, question_type, previous_questions)
    
    session['current_question'] = question
    session['current_difficulty'] = difficulty
    session['question_start_time'] = datetime.now().isoformat()
    
    if 'questions_asked' not in session:
        session['questions_asked'] = []
    session['questions_asked'].append(question[:50])
    
    return jsonify({
        'question': question,
        'difficulty': difficulty,
        'tech_stack': tech_stack,
        'question_type': question_type
    })





if __name__ == "__main__":
    app.run(debug=True)
