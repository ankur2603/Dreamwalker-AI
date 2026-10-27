import os
import subprocess
import pyperclip
import pyautogui
from PIL import Image

# Ensure screenshots folder exists
OS_SCREENSHOT_DIR = "screenshots"
os.makedirs(OS_SCREENSHOT_DIR, exist_ok=True)

# -------------------------------------------------------------
# Core Relics (PC System Tools)
# -------------------------------------------------------------

def open_application(app_name: str) -> str:
    """Opens a local application on Windows."""
    try:
        subprocess.Popen(app_name, shell=True)
        return f"Successfully launched {app_name}."
    except Exception as e:
        return f"Failed to open {app_name}: {e}"

def close_application(app_name: str) -> str:
    """Closes a running application by process name."""
    try:
        subprocess.run(f"taskkill /f /im {app_name}.exe", shell=True, check=True)
        return f"Closed {app_name} successfully."
    except Exception as e:
        return f"Failed to close {app_name}: {e}"

def take_screenshot() -> str:
    """Captures the current screen and saves it as an image."""
    try:
        filepath = os.path.join(OS_SCREENSHOT_DIR, "desktop_capture.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        return f"Screenshot captured and saved to {filepath}."
    except Exception as e:
        return f"Failed to take screenshot: {e}"

def read_clipboard() -> str:
    """Reads text content from the Windows system clipboard."""
    try:
        text = pyperclip.paste()
        return f"Clipboard content: '{text}'" if text else "Clipboard is empty."
    except Exception as e:
        return f"Failed to read clipboard: {e}"

def write_to_clipboard(text: str) -> str:
    """Writes text content to the Windows system clipboard."""
    try:
        pyperclip.copy(text)
        return f"Successfully copied '{text}' to clipboard."
    except Exception as e:
        return f"Failed to write to clipboard: {e}"

def list_directory(path: str = ".") -> str:
    """Lists files and folders inside a given directory path."""
    try:
        files = os.listdir(path)
        return f"Contents of '{path}': {', '.join(files[:20])}"
    except Exception as e:
        return f"Failed to list directory: {e}"

def read_file(filepath: str) -> str:
    """Reads the contents of a text file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(1000) # Read first 1000 chars safely
        return f"File content of '{filepath}':\n{content}"
    except Exception as e:
        return f"Failed to read file: {e}"

def write_file(filepath: str, content: str) -> str:
    """Writes content to a text file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote content to {filepath}."
    except Exception as e:
        return f"Failed to write file: {e}"

def run_shell_command(command: str) -> str:
    """Executes a PowerShell command with a strict 5-second timeout."""
    try:
        result = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout.strip() or result.stderr.strip()
        return f"Shell Output:\n{output[:500]}"
    except subprocess.TimeoutExpired:
        return "Error: Shell command timed out after 5 seconds."
    except Exception as e:
        return f"Error executing shell command: {e}"

def adjust_volume(action: str) -> str:
    """Adjusts Windows system master volume ('up', 'down', 'mute')."""
    try:
        if action.lower() == "up":
            pyautogui.press("volumeup", presses=5)
            return "Volume increased."
        elif action.lower() == "down":
            pyautogui.press("volumedown", presses=5)
            return "Volume decreased."
        elif action.lower() == "mute":
            pyautogui.press("volumemute")
            return "Volume muted/unmuted."
        return "Invalid action. Use 'up', 'down', or 'mute'."
    except Exception as e:
        return f"Failed to adjust volume: {e}"