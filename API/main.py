from flask import Flask, jsonify, request, send_file, redirect, render_template
import ollama
import os
import uuid
import gc  # Import garbage collection for memory management
import time  # Optional: Import time for delays between iterations
import unreal
import speech_recognition as sr
import sqlite3
from flask_mail import Mail, Message
from pathlib import Path




# creating a Flask app 
app = Flask(__name__) 

modelfile = '''
FROM llama3.1
SYSTEM You are Mike, a strict, no-nonsense AI interviewer. Begin by asking generating minimalistic but precise and challenging questions focused on machine learning, Data Structures, and Algorithms, Basic Computer Questions, AI algorithms, and VR technologies in the backend. Then ask the user's name. Provide feedback only at the end of the interview. Maintain a professional and stern demeanor throughout, replicating the intensity of a real-life interview. Ask Minimalistic questions, dont give your own tips until the end of the interview.
'''

ollama.create(model='interview', modelfile=modelfile)  # (Done Creation)

modelfile1 = '''
FROM llama3.1
SYSTEM You are Mike, a strict, no-nonsense AI interviewer. Now you have a question list and an answer list. When i ask you for a genralised feedback , you have two tasks- one is to provide a generalised feedback when i ask so and a detailed analysis on question wise improvements and ideal answers for each question when i ask to provide the same.
'''

ollama.create(model='feedback_provider', modelfile=modelfile)  # (Done Creation)

# Configuration for Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'Noah'
app.config['MAIL_PASSWORD'] = 'hack4change'
app.config['MAIL_DEFAULT_SENDER'] = 'noahipynb@gmail.com'

mail = Mail(app)


currddir = ""  # Define the global variable

# Initialize the database
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    init_db()
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    global currddir  # Declare currddir as global to modify its value

    username = request.form.get('username')
    email = request.form.get('email')
    phone = request.form.get('phone')
    
    # Save or replace the user details in the SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (id, username, email, phone)
        VALUES (
            (SELECT id FROM users WHERE email = ?),
            ?, ?, ?
        )
    ''', (email, username, email, phone))

    # Dynamically create a directory based on the username
    parent_dir = os.path.expanduser("/Users/tejasbajwa/Downloads/Flask API/qa")  # Replace with a valid, writable path
    user_directory = os.path.join(parent_dir, username)

    # Create the directory if it doesn’t exist
    os.makedirs(user_directory, exist_ok=True)

    # Update the global currddir variable
    currddir = user_directory
    print(f"User directory created or updated: {currddir}")

    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/questions', methods=['GET']) 
def questions(): 
    global currddir  # Declare currddir as global to access its value

    try:
        # Verify currddir
        if not currddir:
            return jsonify({'error': 'User directory is not set.'}), 500
        
        print(f"Using directory: {currddir}")

        # Step 1: Generate 2 questions from the LLM
        ques = ollama.chat(model='interview', messages=[{'role': 'user', 'content': 'You are an interviewer. Provide only 2 questions, without any explanations, introductions, or additional words. Ask questions one by one, directly related to machine learning models, AI algorithms, data structures, and VR technologies. Do not include any other text.'}])
        
        question_string = ques['message']['content']
        print(f"Questions received: {question_string}")  # Print the raw content received
        
        # Step 2: Split the questions into a list
        question_list = question_string.strip().split('\n\n')
        print(f"Question list: {question_list}")  # Print the split questions

        # Step 3: Save the questions to a file inside the user's directory
        questions_file_path = os.path.join(currddir, 'questions.txt')
        print(f"Saving questions to: {questions_file_path}")

        with open(questions_file_path, 'w') as file:
            for question in question_list:
                if question:  # Only write non-empty questions
                    file.write(question + '\n\n')
        
        # Verify file content
        with open(questions_file_path, 'r') as file:
            file_content = file.read()
            print(f"Content of the file: {file_content}")
        print("Hio")
        # Step 4: Return questions as JSON
        return jsonify({'questions': question_list})
    except Exception as e:
        # Handle errors gracefully
        return jsonify({'error': str(e)}), 500

#########################################################################

    

############################################################################    
@app.route('/general-feedback', methods=['POST']) 
def generalisedFeedback(): 
	try:
		# Step 1: Get the JSON data from the request body
		data = request.get_json()

		# Step 2: Extract question_list and answer_list from the data
		question_list = data.get('question_list', [])
		answer_list = data.get('answer_list', [])

		# Step 3: Validate the extracted lists
		if not question_list or not answer_list:
			return jsonify({"error": "Both question_list and answer_list must be provided."}), 400


		# Optional: Further processing or validation can go here
		# Step 4: Prepare a combined string of questions and answers
		quets_ans = ""
		for i in range(len(question_list)):
			quets_ans += f"Q{i+1}: {question_list[i]}\nA{i+1}: {answer_list[i]}\n\n"

        # Step 5: Request general feedback from the model
		feedback_response = ollama.chat(model='feedback_provider', messages=[
            {'role': 'user', 'content': f"You are a general feedback provider. Provide general feedback for the following questions and answers:\n\n{quets_ans}"}
        ])

        # Step 6: Extract feedback from the response
		feedback = feedback_response['message']['content']

        # Step 7: Return a success response with the feedback
		return jsonify({
            "questions_and_answers": quets_ans,
            "feedback": feedback
        }), 200

	except Exception as e:
		return jsonify({"error": str(e)}), 500

#################################################################################################






# Mailing detailed feedback document
###################################################################################################
@app.route('/detailed-feedback', methods=['POST'])
def detailedFeedback():
    global currddir 
    try:
        # Extract data from request
        data = request.get_json()
        question_list = data.get('question_list', [])
        answer_list = data.get('answer_list', [])

        # Validation
        if not question_list or not answer_list:
            return jsonify({"error": "Both question_list and answer_list must be provided."}), 400

        # Prepare question and answer string
        quets_ans = ""
        for i in range(len(question_list)):
            quets_ans += f"Q{i+1}: {question_list[i]}\nA{i+1}: {answer_list[i]}\n\n"

        # Generate feedback
        feedback_response = ollama.chat(model='feedback_provider', messages=[
            {'role': 'user', 'content': f"Provide detailed feedback question wise in 250-300 words for the following:\n\n{quets_ans}"}
        ])
        feedback = feedback_response['message']['content']

        # Generate a unique file name and UUID
        unique_id = str(uuid.uuid4())
        feedback_file_path = os.path.join('static', f'feedback_report_{unique_id}.txt')
        
        # Save detailed feedback report
        with open(feedback_file_path, 'w') as file:
            file.write(f"Questions and Answers:\n\n{quets_ans}\n\nFeedback:\n\n{feedback}")

        # Return UUID for downloading the report
        return jsonify({
            "file_id": unique_id,
            "questions_and_answers": quets_ans,
            "feedback": feedback
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

##########################################################################
@app.route('/download-report/<file_id>')
def download_report(file_id):
    try:
        # Path to the feedback report
        feedback_file_path = os.path.join('static', f'feedback_report_{file_id}.txt')

        if os.path.exists(feedback_file_path):
            # Send file for download
            response = send_file(feedback_file_path, as_attachment=True, download_name='feedback_report.txt')
            
            # Optionally: Clean up the file after download
            os.remove(feedback_file_path)
            
            return response
        else:
            return jsonify({"error": "Feedback report not found."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



###############################################################
@app.route('/speechtotext')
def stt():

# Initialize the recognizer
    recognizer = sr.Recognizer()

# Load the audio file
    with sr.AudioFile("/content/harvard.wav") as source:
        audio_data = recognizer.record(source)

# Recognize (convert from speech to text)
    try:
        text = recognizer.recognize_google(audio_data)
        print("Extracted Text: ", text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service")



# @app.route('/detailed-feedback', methods=['POST'])
# def detailedFeedback():
#     try:
#         # Extract data from form
#         #username = request.form.get('username')
#         question_list = request.form.getlist('question_list')
#         answer_list = request.form.getlist('answer_list')


#         # Validation
#         if not question_list or not answer_list:
#             return jsonify({"error": "Both question_list and answer_list must be provided."}), 400

#         # Prepare question and answer string
#         quets_ans = ""
#         for i in range(len(question_list)):
#             quets_ans += f"Q{i+1}: {question_list[i]}\nA{i+1}: {answer_list[i]}\n\n"

#         # Generate feedback
#         feedback_response = ollama.chat(model='feedback_provider', messages=[
#             {'role': 'user', 'content': f"Provide detailed feedback question wise in 250-300 words for the following:\n\n{quets_ans}"}
#         ])
#         feedback = feedback_response['message']['content']

#         # Generate a unique file name and UUID
#         unique_id = str(uuid.uuid4())
#         feedback_file_name = f'{username}_feedback_{unique_id}.txt'
#         feedback_file_path = os.path.join('static', feedback_file_name)
        
#         # Save detailed feedback report
#         with open(feedback_file_path, 'w') as file:
#             file.write(f"Username: {username}\n\nQuestions and Answers:\n\n{quets_ans}\n\nFeedback:\n\n{feedback}")

#         # Return UUID for downloading the report
#         return jsonify({
#             "file_id": unique_id,
#             "questions_and_answers": quets_ans,
#             "feedback": feedback
#         }), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500








##############################################################

# driver function 
if __name__ == '__main__': 
    app.run(debug=True) 
