import streamlit as st
import subprocess
import json
import os

# File to save commands
COMMANDS_FILE = "commands.json"

# Load saved commands
if os.path.exists(COMMANDS_FILE):
    with open(COMMANDS_FILE, "r") as f:
        saved_commands = json.load(f)
else:
    saved_commands = []

st.set_page_config(page_title="Web CMD Terminal", layout="wide")

# Session state
if "console_output" not in st.session_state:
    st.session_state.console_output = []
if "command_history" not in st.session_state:
    st.session_state.command_history = []
if "history_index" not in st.session_state:
    st.session_state.history_index = -1

prompt_path = r"C:\Users\pc> "

# CSS for terminal
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
input#cmd_input {
    background-color: black;
    color: white;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 14px;
    border: none;
    outline: none;
    width: 100%;
}
.cursor {
    display: inline-block;
    width: 10px;
    animation: blink 1s step-start infinite;
}
@keyframes blink {
    50% { opacity: 0; }
}
.stdout { color: white; }
.stderr { color: red; }
</style>
""", unsafe_allow_html=True)

# Function to add output
def add_output(command, output, is_error=False):
    if is_error:
        st.session_state.console_output.append(f'<span class="stderr">{prompt_path}{command}\n{output}</span>')
    else:
        st.session_state.console_output.append(f'<span class="stdout">{prompt_path}{command}\n{output}</span>')

# Display terminal
terminal_html = "<br>".join(st.session_state.console_output) + '<span class="cursor">_</span>'
terminal_area = st.empty()
terminal_area.markdown(f'<div class="terminal" id="console_output_area">{terminal_html}</div>', unsafe_allow_html=True)

# Input field
command_input = st.text_input("", key="cmd_input", label_visibility="collapsed")

# Run command logic
if command_input.strip() != "":
    cmd_to_run = command_input.strip()
    try:
        result = subprocess.run(cmd_to_run, shell=True, capture_output=True, text=True)
        if result.stderr:
            add_output(cmd_to_run, result.stderr, is_error=True)
        else:
            add_output(cmd_to_run, result.stdout)
    except Exception as e:
        add_output(cmd_to_run, str(e), is_error=True)

    # Update command history
    st.session_state.command_history.append(cmd_to_run)
    st.session_state.history_index = len(st.session_state.command_history)

    # Save persistently
    if cmd_to_run not in saved_commands:
        saved_commands.append(cmd_to_run)
        with open(COMMANDS_FILE, "w") as f:
            json.dump(saved_commands, f)

    # Clear input
    st.session_state.cmd_input = ""

# Auto-scroll
st.markdown("""
<script>
var term = document.getElementById('console_output_area');
term.scrollTop = term.scrollHeight;
</script>
""", unsafe_allow_html=True)

# JS for Enter key and arrow keys for history
st.markdown("""
<script>
const input = window.parent.document.querySelector('input#cmd_input');
let history = [];
let history_index = -1;

input.addEventListener('keydown', function(e) {
    // Arrow Up
    if(e.key === 'ArrowUp') {
        window.parent.stSessionState = window.parent.stSessionState || {};
        let hist = Object.values(window.parent.stSessionState.command_history || []);
        if(hist.length > 0) {
            history_index = Math.max(0, history_index-1);
            input.value = hist[history_index] || '';
        }
        e.preventDefault();
    }
    // Arrow Down
    if(e.key === 'ArrowDown') {
        window.parent.stSessionState = window.parent.stSessionState || {};
        let hist = Object.values(window.parent.stSessionState.command_history || []);
        if(hist.length > 0) {
            history_index = Math.min(hist.length-1, history_index+1);
            input.value = hist[history_index] || '';
        }
        e.preventDefault();
    }
    // Enter key
    if(e.key === 'Enter') {
        let evt = new Event('change', { bubbles: true });
        input.dispatchEvent(evt);
    }
});
</script>
""", unsafe_allow_html=True)

# Show saved commands below
st.subheader("Saved Commands")
for cmd in saved_commands:
    st.write(cmd)
