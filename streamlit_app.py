import streamlit as st
import subprocess
import json
import os
import sys

# ----- Auto-install FFmpeg -----
try:
    import imageio_ffmpeg as ffmpeg
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "imageio-ffmpeg"])
    import imageio_ffmpeg as ffmpeg

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

# ----- Function to Run Command -----
def run_command(cmd):
    try:
        # Replace 'ffmpeg' with the full path
        if "ffmpeg" in cmd:
            cmd = cmd.replace("ffmpeg", ffmpeg_path)
        
        # Run the command
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        output = result.stdout + result.stderr
        
        # Append to console
        st.session_state.console_output += f"> {cmd}\n{output}\n"
        
        # Save command if not already saved
        if cmd not in saved_commands:
            saved_commands.append(cmd)
            with open(COMMANDS_FILE, "w") as f:
                json.dump(saved_commands, f)
                
    except Exception as e:
        st.session_state.console_output += f"> {cmd}\nError: {e}\n"

# ----- Run Command on Button Click -----
if st.button("Run"):
    if command.strip() != "":
        run_command(command)
        st.session_state.last_command = command

# ----- Show Console Output -----
st.text_area("Console Output", value=st.session_state.console_output, height=400, max_chars=None)

# ----- Show Saved Commands -----
st.subheader("Saved Commands")
for cmd in saved_commands:
    st.write(cmd)
