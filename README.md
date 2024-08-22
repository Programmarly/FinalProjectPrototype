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
- **`static`**: Responsible for static assets rendering like js or css.


## Quickstart

- **`pip install -r requirements.txt`**
- Change the path where you need your detailed reports for each user session id in `main.py` at line 86.

- ### Backend Installation and Setup
1. Start by setting up and running the backend API. This system is responsible for collecting user information during the registration process, including email, roles, and other relevant details.
2. Based on the registration data, a tailored list of interview questions is curated for the user.



### VR Experience

**Download the project folder(.zip) here: ** https://drive.google.com/file/d/19uTuQwFZQIKr6istgSSa16uOr_erdqu9/view?usp=sharing

1. Enter the VR environment to begin your interview preparation.
2. Use the B button on your VR controller to respond to the customized interview questions.
3. The system will capture your audio responses, convert them into text, and then synthesize the responses to generate a comprehensive feedback report.
4. Within a day, you’ll receive a detailed and overview feedback report directly in your file system, where the backend is running.

## Prerequisites for VR file
Before proceeding with the installation, ensure that you have the following:

- **Unreal Engine 5** installed on your machine.
- **Oculus SDK** integrated with Unreal Engine.
- **Visual Studio** with C++ support (for building the project).
- **Python 3.7+** installed (for backend integration).

## Installation Steps

### 1. Extract the Project Files
- Download the VR project `.zip` file.
- Extract the contents to your preferred directory.

### 2. Open the Project in Unreal Engine
- Launch **Unreal Engine 5**.
- In the Unreal Project Browser, click on **Browse**.
- Navigate to the directory where you extracted the project and open the `.uproject` file.

### 3. Install Required Plugins
- Go to **Edit > Plugins** in Unreal Engine.
- Ensure that the following plugins are enabled:
  - **Oculus VR**
  - **Steam VR** (if applicable)
  - **Python Editor Script Plugin** (for running Python scripts within Unreal)

### 4. Setup Backend Integration
- Open the `Config` folder in the Unreal project directory.
- Modify the `DefaultEngine.ini` file to include your backend API endpoint for question generation and feedback processing.

### 5. Run the Backend
- Ensure your backend API is running. Refer to the backend setup guide for installation and startup instructions.
- The backend will handle user registration, question generation, and feedback synthesis.

