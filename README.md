# Kasuku Transcriber 🦜

![In Progress](https://img.shields.io/badge/Status-In%20Progress-green?style=for-the-badge&logo=wrench&logoColor=white)

An ASR project for non standard Kenyan speech that uses finetunned whisper models to understand non standard Kenyan speech 
A simple and powerful speech transcription application designed for non-standard speech patterns. Kasuku Transcriber helps you convert audio recordings into text with support for English and Swahili.

# Technology Stack

| Category | Technologies |
| :--- | :--- |
| **Framework** | [![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org) [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io) [![Hugging Face](https://img.shields.io/badge/Hugging_Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/transformers) |
| **Language** | [![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org) [![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript) [![CSS](https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS) |
| **Infrastructure** | [![CUDA](https://img.shields.io/badge/CUDA-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://developer.nvidia.com/cuda-zone) [![Modal](https://img.shields.io/badge/Modal-22C55E?style=for-the-badge&logo=modal&logoColor=white)](https://modal.com) |


# ✨ Features

* **Audio Recording**: Record yourself directly in the browser
* **Multi-language Support** : Transcribe speech in English and Swahili
* **Real-time Processing**: Get instant transcription results
* **Save & Manage**: Keep track of all your transcriptions with timestamps
* **Search Functionality**: Find specific transcriptions by content
* **Export Options**: Copy or save your transcriptions for later use

# 🚀 How to Use
```mermaid
flowchart TD
   A[🚀 Start Here] --> B[🔐 1. Login]
    
   B --> C[Use Demo Credentials]

   C --> D[🎤 2. Record Audio]

   D --> E[Select Language]
   E --> F[Click Record]
   F --> G[Allow Microphone]
   G --> H[Speak into the Microphone]
   H --> I[Click Stop]

   I --> J[📝 3. Transcribe]

   J --> K[Click Transcribe]
   K --> L[Wait for Processing]
   L --> M[View Results]

   M --> N[💾 4. Manage]

   N --> O[Save]
   N --> P[Copy]
   N --> Q[Speak]
   N --> R[View History]

   R --> S[Search]
   R --> T[Speak Transcribed Text]
   R --> U[Copy Transcribed Text]
   R --> V[Filter by Language]
   R --> X[Delete Saved Item]

   style A fill:#ff9800,color:#000,stroke:#e65100,stroke-width:3px
   style B fill:#4caf50,color:#fff,stroke:#2e7d32,stroke-width:2px
   style D fill:#4caf50,color:#fff,stroke:#2e7d32,stroke-width:2px
   style J fill:#4caf50,color:#fff,stroke:#2e7d32,stroke-width:2px
   style N fill:#4caf50,color:#fff,stroke:#2e7d32,stroke-width:2px
```

# 💬 Supported Languages 
Currently supports transcription for:

* English : Using cdli/whisper-small_finetuned_kenyan_english_nonstandard_speech_v0.9 model
* Swahili : Using cdli/whisper-small-Swahili_finetuned_small_CV20 model

# 🎯 Key Benefits

* Accessibility: Designed specifically for non-standard speech patterns
* User-Friendly: Simple interface that anyone can use
* Organized: Keep all your transcriptions in one place with timestamps
* Flexible: Bilingual language support for English and Swahili

---

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

---

## Contact Details

For any questions or feedback, please feel free to reach out:

[![Linktree](https://img.shields.io/badge/-Linktree-39E09B?style=for-the-badge&logo=linktree&logoColor=white)](https://linktr.ee/mainye)


