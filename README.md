# Flask Interview Preparation Tool

This project is a Flask-based web application that facilitates personalized interview preparation. It generates customized interview questions, processes audio responses, and provides detailed AI-driven feedback.

## Features
- User registration with customized interview settings.
- Interview questions tailored to the role, domain, and branch selected.
- Automatic audio-to-text transcription for interview answers.
- Generalized and detailed feedback using AI models.
- Easy download of feedback reports.

## Project Structure

- **`main.py`**: Contains backend routes and controllers.
- **`templates/`**: Responsible for rendering the frontend (HTML files).
- **`qa/`**: Manages question lists, answer lists, and feedback reports for each user.


##Quickstart

- **`pip install -r requirements.txt`**
- Change the path where you need your detailed reports for each user session id in `main.py` at line 86. 
