import os
import subprocess

def verify_action(tool_name: str, args: dict, result_str: str) -> tuple[bool, str]:
    """
    Pierces the Illusion: Validates the actual system state 
    after a tool executes to ensure true outcome.
    """
    try:
        if tool_name == "open_application":
            app = args.get("app_name", "").lower()
            # Check if process exists in Windows tasklist
            tasks = subprocess.check_output("tasklist", text=True).lower()
            if app in tasks or f"{app}.exe" in tasks:
                return True, f"Verified: Process '{app}' is actively running in system memory."
            return False, f"Illusion Detected: Command reported success, but process '{app}' was not found in tasklist."

        elif tool_name == "write_file":
            filepath = args.get("filepath", "")
            if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                return True, f"Verified: File '{filepath}' exists on disk with content."
            return False, f"Illusion Detected: File '{filepath}' was not created or is empty."

        elif tool_name == "close_application":
            app = args.get("app_name", "").lower()
            tasks = subprocess.check_output("tasklist", text=True).lower()
            if app not in tasks and f"{app}.exe" not in tasks:
                return True, f"Verified: Process '{app}' successfully terminated."
            return False, f"Illusion Detected: Process '{app}' is still active in memory."

        elif tool_name == "write_to_clipboard":
            import pyperclip
            expected = args.get("text", "")
            actual = pyperclip.paste()
            if actual == expected:
                return True, "Verified: System clipboard content matches target string."
            return False, "Illusion Detected: Clipboard text does not match written value."

        # Default fallback verification for non-state tools (e.g., screenshots, reads)
        if "Failed" in result_str or "Error" in result_str:
            return False, f"Action reported error: {result_str}"
        return True, "Action completed without reported exceptions."

    except Exception as e:
        return False, f"Verification failed due to system check error: {e}"