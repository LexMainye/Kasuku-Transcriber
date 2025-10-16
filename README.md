# Kasuku Transcriber 🦜
An ASR project for non standard Kenyan speech that uses finetunned whisper models to understand non standard Kenyan speech 
A simple and powerful speech transcription application designed for non-standard speech patterns. Kasuku Transcriber helps you convert audio recordings into text with support for English and Swahili.

## 🚀 Technologies Used

This project leverages a powerful stack of modern AI and machine learning technologies to perform accurate and efficient audio transcription.

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org)
[![Hugging Face](https://img.shields.io/badge/Hugging_Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/transformers)
[![CUDA](https://img.shields.io/badge/CUDA-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://developer.nvidia.com/cuda-zone)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Modal](https://img.shields.io/badge/Modal-22C55E?style=for-the-badge&logo=modal&logoColor=white)](https://modal.com)

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
![App Screenshot](https://github.com/LexMainye/Kasuku-Transcriber/blob/a6b4368b8a47c62d70474efe74258fd5e8f20378/Screenshots/Screen%20Shot%202025-09-24%20at%202.09.29%20PM.png)



# 🎤 2. Record Audio

![App Screenshot](https://github.com/LexMainye/Kasuku-Transcriber/blob/a6b4368b8a47c62d70474efe74258fd5e8f20378/Screenshots/Screen%20Shot%202025-09-24%20at%202.10.28%20PM.png)

* Select your preferred language from the dropdown menu
* Click the "Record Yourself" button
* Allow microphone access when prompted
* Speak clearly into your microphone
* Click stop when finished recording

# 📝 3. Transcribe

![App Screenshot](https://github.com/LexMainye/Kasuku-Transcriber/blob/a6b4368b8a47c62d70474efe74258fd5e8f20378/Screenshots/Screen%20Shot%202025-09-24%20at%202.12.31%20PM.png)

* Click "Transcribe Audio" button that appears to process your recording
* Wait for the transcription results to appear

# 💾 4. Manage Transcriptions

* Save: Click the "Save" button to store your transcription
* Copy: Use the "Copy" button to copy text to your clipboard
* View History: Access "Saved Transcriptions" to see all your past recordings
* Search: Use the search bar to find specific transcriptions
* Filter: Filter transcriptions by language
* Delete: Remove unwanted transcriptions

# 💬 Supported Languages 
Currently supports transcription for:

* English : Using cdli/whisper-small_finetuned_kenyan_english_nonstandard_speech_v0.9 model
* Swahili : Using cdli/whisper-small-Swahili_finetuned_small_CV20 model

# 🎯 Key Benefits

* Accessibility: Designed specifically for non-standard speech patterns
* User-Friendly: Simple interface that anyone can use
* Organized: Keep all your transcriptions in one place with timestamps
* Flexible: Bilingual language support for English and Swahili





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


