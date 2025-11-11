# prewarm_models.py - More robust with progress tracking
import os
import sys
import time

def prewarm_essential():
    """Download essential models with better error handling"""
    print("🚀 Pre-warming Hugging Face models...")
    
    # Add timeout for downloads
    import socket
    socket.setdefaulttimeout(300)  # 5 minute timeout
    
    try:
        from transformers import AutoModel, AutoTokenizer
        
        model_names = [
            "cdli/whisper-small_finetuned_kenyan_swahili_nonstandard_speech_v0.9",
            "cdli/whisper-small_finetuned_kenyan_english_nonstandard_speech_v0.9"
        ]

        for i, model_name in enumerate(model_names, 1):
            print(f"\n📥 [{i}/{len(model_names)}] Downloading: {model_name}")
            
            try:
                # Download with progress indication
                start_time = time.time()
                
                # Tokenizer first (usually smaller)
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                print(f"   ✅ Tokenizer downloaded")
                
                # Model with cleanup
                model = AutoModel.from_pretrained(model_name)
                print(f"   ✅ Model downloaded")
                
                # Clean up memory
                del model, tokenizer
                
                download_time = time.time() - start_time
                print(f"   ⏱️  Download completed in {download_time:.1f}s")
                
            except Exception as e:
                print(f"   ⚠️  Failed to download {model_name}: {str(e)[:100]}...")
                # Continue with next model

    except Exception as e:
        print(f"❌ Error in pre-warming: {e}")
    
    print("\n✅ Model pre-warming complete.")

if __name__ == "__main__":
    prewarm_essential()