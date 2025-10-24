# deploy.py - Updated with min_containers
import modal

# Cache environment
CACHE_ENV_VARS = {
    "TRANSFORMERS_CACHE": "/root/.cache/huggingface",
    "HF_HOME": "/root/.cache/huggingface",
    "PYTHONPATH": "/app/src",
    "TRANSFORMERS_VERBOSITY": "error",
}

# Build image
image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("ffmpeg", "libsndfile1")
    .pip_install_from_requirements("requirements.txt")
    .env(CACHE_ENV_VARS)
    .add_local_file("prewarm_models.py", "/app/prewarm_models.py", copy=True)
    .run_commands("python /app/prewarm_models.py")
    .add_local_dir("src", "/app/src")
)

app = modal.App("kasuku-transcriber", image=image)

@app.function(
    gpu="A10G",
    cpu=2,
    memory=16384,
    timeout=3600,
    scaledown_window=300,
    min_containers=1  # ✅ CHANGED: keep_warm -> min_containers
)
@modal.asgi_app()
def run_streamlit_asgi():
    import os
    import sys
    from streamlit.web.cli import main
    
    os.chdir("/app")
    os.environ.update(CACHE_ENV_VARS)
    
    # Updated Streamlit config without conflicting options
    sys.argv = [
        "streamlit", "run", "src/app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0",
        "--server.headless=true",
        # Removed conflicting CORS/XSRF options
        "--browser.serverAddress=0.0.0.0",
        "--global.developmentMode=false",
        "--server.fileWatcherType=none",
    ]
    
    main()

@app.local_entrypoint()
def main():
    print("🚀 Deploying Kasuku Transcriber...")
    
    # Quick validation
    required = ["requirements.txt", "prewarm_models.py", "src", "src/app.py"]
    for item in required:
        if not os.path.exists(item):
            print(f"❌ Missing: {item}")
            return
    
    print("✅ All files present")
    print("🔨 Building image (this may take a while for model downloads)...")
    
    app.deploy("kasuku-transcriber")
    print("✅ Deployment initiated!")

if __name__ == "__main__":
    main()