import os
import sys

def prewarm():
    """
    This function is run during the Modal image build.
    It downloads all necessary models into the cache.
    """
    
    print("🚀 Pre-warming Hugging Face models...")

    try:
        from transformers import AutoModel, AutoTokenizer
        
        # --- IMPORTANT --- 
        # List of model names to pre-warm
        model_names = [
            "cdli/whisper-small-Swahili_finetuned_small_CV20",
            "cdli/whisper-small_finetuned_kenyan_english_nonstandard_speech_v0.9"
            # "etc/etc"
        ]

        for model_name in model_names:
            print(f"Downloading model: {model_name}")
            # Download the model weights
            AutoModel.from_pretrained(model_name)
            
            print(f"Downloading tokenizer: {model_name}")
            # Download the tokenizer
            AutoTokenizer.from_pretrained(model_name)

    except ImportError:
        print("❌ Error: 'transformers' library not found.")
        print("Please ensure 'transformers' is in your requirements.txt")
        sys.exit(1) # Exit with an error if transformers isn't installed
    except Exception as e:
        print(f"⚠️ Warning: Could not download a model. Error: {e}")
    
    print("✅ Model pre-warming complete.")

if __name__ == "__main__":
    prewarm()