import subprocess
import sys
import imageio_ffmpeg as ffmpeg

ffmpeg_path = ffmpeg.get_ffmpeg_exe()
st.write(f"FFmpeg executable path: {ffmpeg_path}")

def run_command(cmd):
    try:
        # If the command contains 'ffmpeg', replace it with the full path
        if "ffmpeg" in cmd:
            cmd = cmd.replace("ffmpeg", ffmpeg_path)
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        output = result.stdout + result.stderr
        st.session_state.console_output += f"> {cmd}\n{output}\n"
        # Save command if not already saved
        if cmd not in saved_commands:
            saved_commands.append(cmd)
            with open(COMMANDS_FILE, "w") as f:
                json.dump(saved_commands, f)
    except Exception as e:
        st.session_state.console_output += f"> {cmd}\nError: {e}\n"
