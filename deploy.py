import modal

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