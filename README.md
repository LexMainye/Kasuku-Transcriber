# Kasuku Transcriber 🦜
An ASR project for non standard Kenyan speech that uses finetunned whisper models to understand non standard Kenyan speech 
A simple and powerful speech transcription application designed for non-standard speech patterns. Kasuku Transcriber helps you convert audio recordings into text with support for English and Swahili.



# ✨ Features

* **Audio Recording**: Record yourself directly in the browser
* **Multi-language Support** : Transcribe speech in English and Swahili
* **Real-time Processing**: Get instant transcription results
* **Save & Manage**: Keep track of all your transcriptions with timestamps
* **Search Functionality**: Find specific transcriptions by content
* **Export Options**: Copy or save your transcriptions for later use

# 🚀 How to Use
# 🔐 1. Login

- Use the demo credentials provided on the login page:
![App Screenshot](https://github.com/LexMainye/Parrot-Transcriber/blob/9933c62d0255797a24cf7cc0e5c402eebaca39a9/Screenshots/Screen%20Shot%202025-09-23%20at%201.15.44%20PM.png)



# 🎤 2. Record Audio

![App Screenshot](https://github.com/LexMainye/Parrot-Transcriber/blob/9933c62d0255797a24cf7cc0e5c402eebaca39a9/Screenshots/Screen%20Shot%202025-09-23%20at%201.03.34%20PM.png)

* Select your preferred language from the dropdown menu
* Click the "Record Yourself" button
* Allow microphone access when prompted
* Speak clearly into your microphone
* Click stop when finished recording

# 📝 3. Transcribe

![App Screenshot](https://github.com/LexMainye/Parrot-Transcriber/blob/d5a3a00303341ba5a01740575de96a5301fc7d84/Screenshots/Screen%20Shot%202025-09-23%20at%201.45.53%20PM.png)

* Click "Transcribe Audio" button that appears to process your recording
* Wait for the transcription results to appear

# 💾 4. Manage Transcriptions

* Save: Click the "Save" button to store your transcription
* Copy: Use the "Copy" button to copy text to your clipboard
* View History: Access "Saved Transcriptions" to see all your past recordings
* Search: Use the search bar to find specific transcriptions
* Filter: Filter transcriptions by language
* Delete: Remove unwanted transcriptions

# 🌍 Supported Languages
Currently supports transcription for:

* English 🇬🇧 : Using [open ai/whisper small](https://huggingface.co/openai/whisper-small) -> Currently fine-tunning 
* Swahili 🇹🇿 : Using fine-tuned [smainye/sw_cv_tune_whisper_tiny_best_model](https://huggingface.co/smainye/sw_cv_tune_whisper_tiny_best_model) -> Currently fine-tunning

# 🎯 Key Benefits

* Accessibility: Designed specifically for non-standard speech patterns
* User-Friendly: Simple interface that anyone can use
* Organized: Keep all your transcriptions in one place with timestamps
* Flexible: Bilingual language support 🇬🇧 🇹🇿



# 📥 Clone This Repository

Follow these steps to set up the project on your local machine:

1. Open your terminal (or Git Bash).
   
2. Navigate to the folder where you want to store the project:
   ```
   cd path/to/your/folder
   ```

3. Clone repository
   ```
   git clone https://github.com/LexMainye/Parrot-Transcriber
    ```
   
4.  Navigate to the project directory

    ```
    cd your-repo-name
    ```

5.  Install Dependencies

    ```
    python -m venv venv
    source venv/bin/activate      # On macOS/Linux
    venv\Scripts\activate         # On Windows
    ```
6. Install required packages from `requirements.txt`

   ```
   pip install -r requirements.txt
   ```

7. Run the project
   After installing the dependencies, run the project
   
   ```
   streamlit run src/app.py
   ```

# 💻 Technical Requirements

* Modern web browser with microphone support
* Microphone access permissions


