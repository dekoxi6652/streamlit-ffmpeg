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

prompt_path = r"C:\Users\pc> "

st.markdown(
    f'<div class="terminal" id="console_output_area">{st.session_state.console_output.replace(chr(10), "<br>")}</div>',
    unsafe_allow_html=True,
)

command = st.text_input(f"{prompt_path}", key="cmd_input", label_visibility="collapsed")

if st.button("Run") and command.strip() != "":
    # Run command and update output
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout + result.stderr
    st.session_state.console_output += f"{prompt_path}{command}\n{output}\n"

    if command not in saved_commands:
        saved_commands.append(command)
        with open(COMMANDS_FILE, "w") as f:
            json.dump(saved_commands, f)

    # Clear input by resetting the widget's key using a trick:
    # We can't set st.session_state["cmd_input"] = "" directly (Streamlit restrictions),
    # so we use a rerun but only after setting a flag in session state.

    st.session_state["clear_input"] = True

# Clear the input if flag is set
if st.session_state.get("clear_input", False):
    st.session_state["cmd_input"] = ""
    st.session_state["clear_input"] = False
    # Do not call rerun here to avoid infinite loop

st.subheader("Saved Commands")
for cmd in saved_commands:
    st.write(cmd)
