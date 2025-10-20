import modal
import os
import sys
import subprocess

# Define the path to your src directory
SRC_DIR = "src"
APP_ENTRYPOINT = f"{SRC_DIR}/app.py"
CONFIG_PATH = f"{SRC_DIR}/config.toml"
REQUIREMENTS_PATH = "requirements.txt"  # In root directory
PREWARM_SCRIPT_PATH = "prewarm_models.py" # pre-warming script

# Define the cache environment variables
CACHE_ENV_VARS = {
    "TRANSFORMERS_CACHE": "/root/.cache/huggingface",
    "HF_HOME": "/root/.cache/huggingface",
    "COQUI_TTS_CACHE": "/root/.cache/tts",
    "TTS_HOME": "/root/.cache/tts",
    "PYTHONPATH": "/app/src",
}

# Define the image with all necessary dependencies
image = (
    modal.Image.debian_slim(python_version="3.11")
    # Step 1: Install system dependencies
    .apt_install(
        "git",
        "ffmpeg", 
        "libsndfile1",
        "libsndfile1-dev",
        "build-essential",
        "wget",
        "curl"
    )
    # Step 2: Install Python dependencies
    .pip_install_from_requirements(REQUIREMENTS_PATH)
    # Step 3: Set cache env vars for the build process
    .env(CACHE_ENV_VARS)
    
    # --- THIS IS THE CORRECTED LOGIC ---
    
    # Step 4: Add AND COPY the pre-warming script.
    .add_local_file(PREWARM_SCRIPT_PATH, f"/app/{PREWARM_SCRIPT_PATH}", copy=True)
    
    # Step 5: Run the pre-warming script to download models.
    # This runs *during the build* and saves models to the cache.
    .run_commands([f"python /app/{PREWARM_SCRIPT_PATH}"])
    
    # Step 6: Add application code and config LAST.
    .add_local_dir(SRC_DIR, "/app/src")
    .add_local_file(CONFIG_PATH, "/app/.streamlit/config.toml")
)

app = modal.App("kasuku-transcriber", image=image)

@app.function(
    gpu="L4",
    cpu=4,
    memory=8192,
    timeout=3600,
    container_idle_timeout=300,
    allow_concurrent_inputs=10
)
@modal.asgi_app()
def run_streamlit():
    # Change to the app directory
    os.chdir("/app")
    
    # Set environment variables for optimal performance at *runtime*
    env = os.environ.copy()
    env.update(CACHE_ENV_VARS)
    env.update({
        "STREAMLIT_SERVER_PORT": "8501",
        "STREAMLIT_SERVER_HEADLESS": "true",
        "STREAMLIT_BROWSER_GATHER_USAGE_STATS": "false",
        "STREAMLIT_SERVER_FILE_WATCHER_TYPE": "none",
        "STREAMLIT_SERVER_ENABLE_STATIC_SERVING": "true",
    })
    
    # Start Streamlit from the src directory
    cmd = [
        "streamlit", "run", "src/app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0",
        "--server.headless=true",
        "--server.enableCORS=false",
        "--server.enableXsrfProtection=false",
        "--browser.gatherUsageStats=false",
        "--server.fileWatcherType=none",
        "--server.maxUploadSize=200",
    ]
    
    try:
        print("🚀 Starting Kasuku Transcriber on Modal...")
        process = subprocess.Popen(cmd, env=env)
        process.wait()
    except KeyboardInterrupt:
        print("🛑 Received interrupt signal, shutting down...")
        process.terminate()
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")
        sys.exit(1)

@app.local_entrypoint()
def main():
    """Deploy the Kasuku Transcriber app to Modal"""
    print("🦜 Kasuku Transcriber - Deployment Script")
    print("=" * 50)
    
    # Validate deployment setup
    for path in [SRC_DIR, REQUIREMENTS_PATH, PREWARM_SCRIPT_PATH, f"{SRC_DIR}/app.py"]:
        if not os.path.exists(path):
            print(f"❌ Error: Required file/directory '{path}' not found!")
            return
            
    if not os.path.exists(CONFIG_PATH):
        print(f"⚠️ Warning: Config file '{CONFIG_PATH}' not found. Proceeding without it.")

    print("✅ Deployment setup validated")
    print(f"📁 Source: {SRC_DIR}")
    print(f"📦 Requirements: {REQUIREMENTS_PATH}")
    print(f"🚀 Entrypoint: {APP_ENTRYPOINT}")
    print(f"🔥 Pre-warm Script: {PREWARM_SCRIPT_PATH}")
    
    print("\n🔨 Building and deploying application...")
    print("📦 This may take a few minutes while models are downloaded and baked into the image...")
    
    print("\n✅ Deployment initiated successfully!")
    print("\n📋 Next steps:")
    print("   1. Wait for the build to complete in the Modal dashboard")
    print("   2. Access your app at the URL provided by Modal")
    print("   3. Your app should now start almost instantly! ✨")

if __name__ == "__main__":
    main()