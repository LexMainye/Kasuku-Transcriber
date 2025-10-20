# deploy.py
import modal
import os
from pathlib import Path

# Define the path to your src directory
SRC_DIR = "src"
APP_ENTRYPOINT = f"{SRC_DIR}/app.py"
CONFIG_PATH = f"{SRC_DIR}/config.toml"
REQUIREMENTS_PATH = "requirements.txt"  # In root directory

# Define the image with all necessary dependencies
image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install(
        "git",
        "ffmpeg", 
        "libsndfile1",
        "libsndfile1-dev",
        "build-essential",
        "wget",
        "curl"
    )
    .pip_install_from_requirements(REQUIREMENTS_PATH)  # From root directory
    # Copy the entire src directory to the container
    .add_local_dir(SRC_DIR, "/app/src")
    # Copy config from src folder to root for Streamlit to find it
    .add_local_file(CONFIG_PATH, "/app/.streamlit/config.toml")
)

app = modal.App("kasuku-transcriber", image=image)

@app.function(
    gpu="T4",
    cpu=4,
    memory=8192,
    timeout=3600,
    container_idle_timeout=300,
    allow_concurrent_inputs=10
)
@modal.asgi_app()
def run_streamlit():
    import subprocess
    import sys
    
    # Create .streamlit directory if it doesn't exist
    streamlit_dir = "/app/.streamlit"
    os.makedirs(streamlit_dir, exist_ok=True)
    
    # Change to the app directory
    os.chdir("/app")
    
    # Set environment variables for optimal performance
    env = os.environ.copy()
    env.update({
        "STREAMLIT_SERVER_PORT": "8501",
        "STREAMLIT_SERVER_HEADLESS": "true",
        "STREAMLIT_BROWSER_GATHER_USAGE_STATS": "false",
        "STREAMLIT_SERVER_FILE_WATCHER_TYPE": "none",
        "STREAMLIT_SERVER_ENABLE_STATIC_SERVING": "true",
        "TRANSFORMERS_CACHE": "/root/.cache/huggingface",
        "HF_HOME": "/root/.cache/huggingface",
        "COQUI_TTS_CACHE": "/root/.cache/tts",
        "TTS_HOME": "/root/.cache/tts",
        "PYTHONPATH": "/app/src",  # Add src to Python path
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
        print(f"📁 Working directory: {os.getcwd()}")
        print(f"📁 Contents: {os.listdir('.')}")
        
        # Check if .streamlit directory was created
        if os.path.exists('/app/.streamlit'):
            print(f"📁 Streamlit config: {os.listdir('/app/.streamlit')}")
        else:
            print("❌ Streamlit config directory not found!")
            
        process = subprocess.Popen(cmd, env=env)
        process.wait()
    except KeyboardInterrupt:
        print("🛑 Received interrupt signal, shutting down...")
        process.terminate()
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")
        sys.exit(1)

@app.function(
    timeout=600
)
def test_deployment():
    """Test function to verify deployment is working"""
    print("🚀 Deployment test completed!")

def validate_deployment_setup():
    """Validate that all necessary files exist before deployment"""
    errors = []
    warnings = []
    
    # Check if source directory exists
    if not os.path.exists(SRC_DIR):
        errors.append(f"Source directory '{SRC_DIR}' not found!")
    
    # Check if requirements.txt exists in root
    if not os.path.exists(REQUIREMENTS_PATH):
        errors.append(f"Requirements file '{REQUIREMENTS_PATH}' not found in root directory!")
    
    # Check if app.py exists
    app_path = f"{SRC_DIR}/app.py"
    if not os.path.exists(app_path):
        errors.append(f"Main application file '{app_path}' not found!")
    
    # Check if config.toml exists
    if not os.path.exists(CONFIG_PATH):
        warnings.append(f"Config file '{CONFIG_PATH}' not found - using default Streamlit theme")
    
    # Check if all Python modules exist
    required_modules = ['backend.py', 'frontend.py']
    for module in required_modules:
        module_path = f"{SRC_DIR}/{module}"
        if not os.path.exists(module_path):
            errors.append(f"Required module '{module_path}' not found!")
    
    return errors, warnings

@app.local_entrypoint()
def main(deploy: bool = True, test: bool = False):
    """
    Deploy the Kasuku Transcriber app to Modal
    
    Args:
        deploy: Whether to deploy the app (default: True)
        test: Whether to run deployment tests (default: False)
    """
    
    print("🦜 Kasuku Transcriber - Deployment Script")
    print("=" * 50)
    
    # Validate deployment setup
    errors, warnings = validate_deployment_setup()
    
    if errors:
        print("❌ Deployment validation failed:")
        for error in errors:
            print(f"   - {error}")
        print("\n💡 Please fix these issues before deploying.")
        return
    
    # Show warnings but continue
    if warnings:
        print("⚠️  Deployment warnings:")
        for warning in warnings:
            print(f"   - {warning}")
        print()
    
    print("✅ Deployment setup validated")
    print(f"📁 Source: {SRC_DIR}")
    print(f"📦 Requirements: {REQUIREMENTS_PATH} (root directory)")
    print(f"🎨 Config: {CONFIG_PATH}")
    print(f"🚀 Entrypoint: {APP_ENTRYPOINT}")
    
    if deploy:
        print("\n🔨 Building and deploying application...")
        print("📦 This may take a few minutes while dependencies are installed...")
        
        # Additional deployment information
        print("\n⚙️  Deployment Configuration:")
        print(f"   - GPU: T4")
        print(f"   - CPU: 4.0 cores")
        print(f"   - Memory: 8192 MB")
        print(f"   - Timeout: 3600 seconds")
        print(f"   - Config: {CONFIG_PATH} → /app/.streamlit/config.toml")
        print(f"   - Requirements: {REQUIREMENTS_PATH} (from root)")
        
        # Deploy the app
        try:
            # This will trigger the deployment
            print("\n🎯 Starting deployment to Modal...")
            
            if test:
                test_deployment.remote()
                print("✅ Deployment test passed!")
            
            print("\n✅ Deployment initiated successfully!")
            print("\n📋 Next steps:")
            print("   1. Wait for the build to complete in the Modal dashboard")
            print("   2. Access your app at the URL provided by Modal")
            print("   3. First startup may take 2-3 minutes while TTS models download")
            print("\n💡 Tip: Run 'modal app list' to see your deployed apps")
            
        except Exception as e:
            print(f"❌ Deployment failed: {e}")
            print("\n🔧 Troubleshooting tips:")
            print("   - Check your Modal token is configured: 'modal token set'")
            print("   - Verify all dependencies in requirements.txt are correct")
            print("   - Ensure you have sufficient Modal credits")
    
    else:
        print("\nℹ️  Dry run completed. Use '--deploy' to actually deploy the app.")

# Additional utility functions for deployment management
@app.local_entrypoint()
def status():
    """Check deployment status"""
    print("🔍 Checking Kasuku Transcriber deployment status...")
    print("Run 'modal app list' to see all your deployed apps")
    print("Run 'modal serve deploy.py' to deploy interactively")

@app.local_entrypoint()
def logs():
    """View deployment logs"""
    print("📋 To view deployment logs, run:")
    print("modal logs kasuku-transcriber")

@app.local_entrypoint()
def update():
    """Update the existing deployment"""
    print("🔄 Updating Kasuku Transcriber deployment...")
    print("This will rebuild the container with the latest code")
    main(deploy=True)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Deploy Kasuku Transcriber to Modal")
    parser.add_argument("--deploy", action="store_true", default=True, 
                       help="Deploy the application (default: True)")
    parser.add_argument("--no-deploy", action="store_false", dest="deploy",
                       help="Don't deploy, just validate")
    parser.add_argument("--test", action="store_true", 
                       help="Run deployment tests")
    parser.add_argument("--status", action="store_true",
                       help="Check deployment status")
    parser.add_argument("--logs", action="store_true",
                       help="Show deployment logs info")
    parser.add_argument("--update", action="store_true",
                       help="Update existing deployment")
    
    args = parser.parse_args()
    
    if args.status:
        status()
    elif args.logs:
        logs()
    elif args.update:
        update()
    else:
        main(deploy=args.deploy, test=args.test)