import streamlit as st
import subprocess
import json
import os

COMMANDS_FILE = "commands.json"

# Load saved commands
if os.path.exists(COMMANDS_FILE):
    with open(COMMANDS_FILE, "r") as f:
        saved_commands = json.load(f)
else:
    saved_commands = []

st.set_page_config(page_title="Web CMD Terminal", layout="wide")

st.markdown("""
<style>
.terminal {
    background-color: black;
    color: white;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 14px;
    padding: 10px;
    border-radius: 5px;
    white-space: pre-wrap;
    overflow-y: auto;
    height: 400px;
}
input[type="text"] {
    background-color: black;
    color: white;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 14px;
    border: none;
    outline: none;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

if "console_output" not in st.session_state:
    st.session_state.console_output = ""

prompt_path = r"C:\Users\pc> "

# Display console output
st.markdown(
    f'<div class="terminal">{st.session_state.console_output.replace(chr(10), "<br>")}</div>',
    unsafe_allow_html=True,
)

# Capture input safely
command_input = st.text_input(f"{prompt_path}", key="cmd_input", label_visibility="collapsed")

# Run button
if st.button("Run") and command_input.strip() != "":
    # Capture the value immediately
    command_to_run = command_input.strip()

    # Run command
    result = subprocess.run(command_to_run, shell=True, capture_output=True, text=True)
    output = result.stdout + result.stderr

    # Append output to console
    st.session_state.console_output += f"{prompt_path}{command_to_run}\n{output}\n"

    # Save command
    if command_to_run not in saved_commands:
        saved_commands.append(command_to_run)
        with open(COMMANDS_FILE, "w") as f:
            json.dump(saved_commands, f)

    # Clear input by resetting the widget
    st.session_state.cmd_input = ""  # now safe because we already captured command_to_run

# Show saved commands
st.subheader("Saved Commands")
for cmd in saved_commands:
    st.write(cmd)
