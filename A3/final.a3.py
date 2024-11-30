# Create a dynamic, interactive quiz app using Flask

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import random
import json
import time
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

LEADERBOARD_FILE = 'data/leaderboard.json'

def load_questions():
    # R2: Dynamic Question Loading
    # Used Claude AI for error handling
    try:
        # To find the questions file path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        questions_path = os.path.join(current_dir, 'data', 'questions.json')
        
        with open(questions_path) as f:
            data = json.load(f)
        return data['questions']
    except Exception as e:
        print(f"Error loading questions: {e}")
        return []

def load_leaderboard():
    # R4: Data Management - Retrieve stored scores
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, 'r') as f:
        return json.load(f)

def save_leaderboard(leaderboard):
    # IR2: Leaderboard System - Rank and store top scores
    # Sort leaderboard by score in descending order
    # Used Claude for help with sorting and limiting leaderboard entries
    sorted_leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)
    # Keep top 10 scores
    sorted_leaderboard = sorted_leaderboard[:10]
    
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(sorted_leaderboard, f)
    return sorted_leaderboard

@app.route("/")
def home():
    # IR1: Persistent User Identification
    # Check if user has visited before
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return render_template('home.html')

@app.route('/set_username', methods=['POST'])
def set_username():
    # IR1: User Identification
    username = request.form['username']
    session['username'] = username
    return redirect(url_for('home'))

@app.route('/quiz')
def quiz():
    # R3: Score Tracking Setup
    # Ensure user is logged in
    if 'username' not in session:
        return redirect(url_for('home'))
    
    # Reset score when starting a new quiz and keep track of time taken
    # Used Claude for help structuring this for score tracking
    session['start_time'] = time.time()
    session['score'] = 0
    session['total_questions'] = 0
    session['correct_answers'] = 0
    return render_template('quiz.html', score=0, username=session['username'])

@app.route('/get_questions', methods=['GET'])
def get_questions():
    # R2: Randomize Questions and Answers
    try:
        questions = load_questions()
        if not questions:
            return jsonify({"error": "No questions found"}), 404
        
        random.shuffle(questions)
        for question in questions:
            random.shuffle(question['answers'])
        
        return jsonify(questions)
    except Exception as e:
        print(f"Error in get_questions: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    # R3: Answer Submission and Feedback
    user_answer = request.form['answer']
    correct_answer = request.form['correct_answer']
    
    score = session.get('score', 0)
    total_questions = session.get('total_questions', 0)
    correct_answers = session.get('correct_answers', 0)
    
    total_questions += 1
    if user_answer == correct_answer:
        score += 1
        correct_answers += 1
    
    session['score'] = score
    session['total_questions'] = total_questions
    session['correct_answers'] = correct_answers
    
    return jsonify({
        'score': score, 
        'correct': user_answer == correct_answer
    })

@app.route('/results', methods=['GET', 'POST'])
def results():
    # R6: Score Tracking and Feedback
    # R7: Error Handling
    if 'username' not in session:
        return redirect(url_for('home'))
    
    score = session.get('score', 0)
    total_questions = session.get('total_questions', 0)
    correct_answers = session.get('correct_answers', 0)
    
    start_time = session.get('start_time', time.time())
    time_taken = round(time.time() - start_time, 2)
    
    # If POST request, save to leaderboard
    if request.method == 'POST':
        try:
            os.makedirs('data', exist_ok=True)
            
            leaderboard = load_leaderboard()
            print("Current leaderboard:", leaderboard)  
            
            new_entry = {
                'username': session['username'],
                'score': score,
                'total_questions': total_questions,
                'time_taken': time_taken
            }
            
            leaderboard.append(new_entry)
            print("New entry:", new_entry)  
            
            leaderboard = save_leaderboard(leaderboard)
            print("Updated leaderboard:", leaderboard)  
            
            return redirect(url_for('leaderboard'))
        
        except Exception as e:
            print(f"Error saving leaderboard: {e}")
            return f"An error occurred: {e}", 500
    
    return render_template('results.html', 
                           score=score, 
                           total_questions=total_questions,
                           correct_answers=correct_answers,
                           time_taken=time_taken)

@app.route('/leaderboard')
def leaderboard():
    # IR2: Leaderboard System
    leaderboard = load_leaderboard()
    return render_template('leaderboard.html', leaderboard=leaderboard)

@app.route('/logout')
def logout():
    # R1: User Session Management
    session.clear()
    return redirect(url_for('home'))

# Run the application
if __name__ == "__main__":
    app.run(debug=True)