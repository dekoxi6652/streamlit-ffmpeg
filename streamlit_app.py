import streamlit as st
import subprocess
import json
import os

# Path to save commands
COMMANDS_FILE = "commands.json"

# Load saved commands
if os.path.exists(COMMANDS_FILE):
    with open(COMMANDS_FILE, "r") as f:
        saved_commands = json.load(f)
else:
    saved_commands = []

# Set up page layout and style
st.set_page_config(page_title="Web CMD Terminal", layout="wide")

# Custom CSS for terminal style
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

# Initialize session state for console output if needed
if "console_output" not in st.session_state:
    st.session_state.console_output = ""

# Current prompt path (simulate Windows prompt)
prompt_path = r"C:\Users\pc> "

# Display the console output area with black background
st.markdown('<div class="terminal" id="console_output_area">{}</div>'.format(st.session_state.console_output.replace('\n', '<br>')), unsafe_allow_html=True)

# Command input (simulate prompt)
command = st.text_input(f"{prompt_path}", key="cmd_input", label_visibility="collapsed")

# Run command if input given
if command:
    try:
        # Run the command in shell and capture output
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout + result.stderr

        # Format output with prompt and command
        full_output = f"{prompt_path}{command}\n{output}"
        st.session_state.console_output += full_output

        # Save command persistently if not saved
        if command not in saved_commands:
            saved_commands.append(command)
            with open(COMMANDS_FILE, "w") as f:
                json.dump(saved_commands, f)

    except Exception as e:
        st.session_state.console_output += f"{prompt_path}{command}\nError: {e}\n"

    # Clear command input box after running
    st.session_state.cmd_input = ""

    # Rerun the app to update console display and clear input
    st.experimental_rerun()
