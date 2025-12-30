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

st.title("Local CMD Web Interface")

# Input box for command
command = st.text_input("Enter command:")

if st.button("Run Command"):
    if command:
        try:
            # Run the command on the system
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = result.stdout + result.stderr
            st.text_area("Output:", output, height=300)
            
            # Save command if not already saved
            if command not in saved_commands:
                saved_commands.append(command)
                with open(COMMANDS_FILE, "w") as f:
                    json.dump(saved_commands, f)
        except Exception as e:
            st.error(f"Error: {e}")

st.subheader("Saved Commands")
for cmd in saved_commands:
    st.write(cmd)
