import streamlit as st
import subprocess
import json
import os

# File to store commands
COMMANDS_FILE = "commands.json"

# Load saved commands
if os.path.exists(COMMANDS_FILE):
    with open(COMMANDS_FILE, "r") as f:
        saved_commands = json.load(f)
else:
    saved_commands = []

# Streamlit page setup
st.set_page_config(page_title="Web CMD", layout="wide")
st.title("🌐 Web Command Line Interface")

# Initialize session state for console output
if "console_output" not in st.session_state:
    st.session_state.console_output = ""

# Input for command
command = st.text_input("Enter command:", key="cmd_input")

if st.button("Run") or st.session_state.get("auto_run", False):
    if command:
        try:
            # Run the command
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = result.stdout + result.stderr

            # Append to console output
            st.session_state.console_output += f"> {command}\n{output}\n"

            # Save command if not already saved
            if command not in saved_commands:
                saved_commands.append(command)
                with open(COMMANDS_FILE, "w") as f:
                    json.dump(saved_commands, f)

        except Exception as e:
            st.session_state.console_output += f"> {command}\nError: {e}\n"

# Display console output
st.text_area("Console", value=st.session_state.console_output, height=400, max_chars=None)

# Show saved commands
st.subheader("Saved Commands")
for cmd in saved_commands:
    st.write(cmd)
