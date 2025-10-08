import modal
<<<<<<< HEAD
import subprocess
import os

# Define the image with dependencies from your requirements.txt file
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install_from_requirements("requirements.txt")
)

app = modal.App("kasuku-transcriber-app", image=image)

# Define the path to your Streamlit app within the container
APP_DIR = "/app/src"
APP_PATH = os.path.join(APP_DIR, "app.py")

@app.function(
    gpu="T4",
    cpu=4.0, # Use float for CPU requests
    memory=2048,
    timeout=3600,
    # Mount the entire local directory to `/app` in the container
    mounts=[modal.Mount.from_local_dir(".", remote_path="/app")],
    container_idle_timeout=300,
)
@modal.web_server(port=8501, startup_timeout=180)
def run_streamlit():
    # Command to run the Streamlit app
    # We use the full path to the app script
    cmd = f"streamlit run {APP_PATH} --server.port=8501 --server.headless=true"
    subprocess.Popen(cmd, shell=True)
=======

# Use your optimized Docker image
image = modal.Image.from_registry(
    "yourusername/kasuku-transcriber:optimized",
    add_python="3.11"
)

app = modal.App("kasuku-transcriber", image=image)

@app.function(
    image=image,
    gpu="T4",  # Modal provides GPU drivers separately
    cpu=4,
    memory=2048,
    timeout=3600,
    max_containers=1
)
@modal.web_server(8501, startup_timeout=180)
def serve():
    import time
    while True:
        time.sleep(3600)
>>>>>>> ba0838bbbb968a3965fcf04cc3513c49ad0b0e3a
