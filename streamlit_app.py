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

st.markdown(
    """
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
    """,
    unsafe_allow_html=True,
)

if "console_output" not in st.session_state:
    st.session_state.console_output = ""

if "input_reset_counter" not in st.session_state:
    st.session_state.input_reset_counter = 0

prompt_path = r"C:\Users\pc> "

# Show console output area
st.markdown(
    f'<div class="terminal" id="console_output_area">{st.session_state.console_output.replace(chr(10), "<br>")}</div>',
    unsafe_allow_html=True,
)

# Use input_reset_counter to force input reset
input_key = f"cmd_input_{st.session_state.input_reset_counter}"

command = st.text_input(f"{prompt_path}", key=input_key, label_visibility="collapsed")

if st.button("Run") and command.strip() != "":
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout + result.stderr
    st.session_state.console_output += f"{prompt_path}{command}\n{output}\n"

    if command not in saved_commands:
        saved_commands.append(command)
        with open(COMMANDS_FILE, "w") as f:
            json.dump(saved_commands, f)

    # Increment counter to reset input on next rerun
    st.session_state.input_reset_counter += 1

st.subheader("Saved Commands")
for cmd in saved_commands:
    st.write(cmd)
