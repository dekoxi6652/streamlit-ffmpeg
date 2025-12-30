import streamlit as st
import subprocess
import json
import os
import requests
import imageio_ffmpeg as ffmpeg  # Import normally

# Get FFmpeg executable path
ffmpeg_path = ffmpeg.get_ffmpeg_exe()

# ----- File to store commands -----
COMMANDS_FILE = "commands.json"

# Load saved commands
if os.path.exists(COMMANDS_FILE):
    with open(COMMANDS_FILE, "r") as f:
        saved_commands = json.load(f)
else:
    saved_commands = []

# ----- Streamlit Page Setup -----
st.set_page_config(page_title="Web CMD", layout="wide")
st.title("Web Command Line Interface")
st.write(f"FFmpeg executable path: `{ffmpeg_path}`")

# ----- Initialize Session State -----
if "console_output" not in st.session_state:
    st.session_state.console_output = ""

if "last_command" not in st.session_state:
    st.session_state.last_command = ""

# ----- Input for Command -----
command = st.text_input("Enter command:", value=st.session_state.last_command, key="cmd_input")

# ----- Input for download URL -----
download_url = st.text_input("Enter file download URL (optional):", "")

# ----- Function to log output -----
def log_output(msg):
    st.session_state.console_output += msg + "\n"
    st.experimental_rerun()

# ----- Function to download file -----
def download_file(url, filename="input.mkv"):
    log_output(f"Starting download from: {url}")
    try:
        r = requests.get(url, stream=True)
        total = int(r.headers.get('content-length', 0))
        downloaded = 0
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    progress = downloaded / total * 100 if total else 0
                    st.session_state.console_output = f"Downloading... {progress:.2f}%"
        log_output(f"Download complete: {filename}")
        return filename
    except Exception as e:
        log_output(f"Download failed: {e}")
        return None

# ----- Function to Run Command -----
def run_command(cmd):
    try:
        # Replace 'ffmpeg' with the full path
        if cmd.strip().startswith("ffmpeg"):
            cmd = cmd.replace("ffmpeg", ffmpeg_path, 1)
        
        log_output(f"> Running: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        output = result.stdout + result.stderr
        log_output(output)

        # Save command if not already saved
        if cmd not in saved_commands:
            saved_commands.append(cmd)
            with open(COMMANDS_FILE, "w") as f:
                json.dump(saved_commands, f)

    except Exception as e:
        log_output(f"Error: {e}")

# ----- Run Button -----
if st.button("Run"):
    st.session_state.last_command = command

    # Step 1: Download file if URL is provided
    input_file = None
    if download_url.strip() != "":
        input_file = download_file(download_url)
    
    # Step 2: Run command if provided
    if command.strip() != "":
        # Replace placeholder with downloaded file if present
        if input_file:
            command_to_run = command.replace("{input}", input_file)
        else:
            command_to_run = command
        run_command(command_to_run)

# ----- Show Console Output -----
st.subheader("Console Output")
st.code(st.session_state.console_output)

# ----- Show Saved Commands -----
st.subheader("Saved Commands")
for i, cmd in enumerate(saved_commands):
    if st.button(f"Run: {cmd}", key=f"run_{i}"):
        run_command(cmd)
