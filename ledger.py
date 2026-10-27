import os
import json
import time

LEDGER_FILE = "sanctum_ledger.json"

# Categorize tools by risk level (Eye of Agamotto)
RISKY_TOOLS = {
    "close_application": "Requires closing a running process on your PC.",
    "write_file": "Overwrites/creates local files on disk.",
    "run_shell_command": "Executes shell-level commands on your PC.",
    "phone_launch_app": "Launches an application directly on your connected mobile device."
}

def load_ledger() -> list:
    """Loads the persistent action ledger from disk."""
    if os.path.exists(LEDGER_FILE):
        try:
            with open(LEDGER_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_ledger(ledger: list):
    """Saves the ledger state to disk."""
    with open(LEDGER_FILE, 'w', encoding='utf-8') as f:
        json.dump(ledger, f, indent=2)

def log_action(tool_name: str, args: dict, result: str, reversible: bool = True, undo_data: dict = None):
    """Appends a completed action entry to the Sanctum ledger."""
    ledger = load_ledger()
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "tool_name": tool_name,
        "args": args,
        "result": result,
        "reversible": reversible,
        "undo_data": undo_data or {}
    }
    ledger.append(entry)
    save_ledger(ledger)

def is_risky(tool_name: str) -> tuple[bool, str]:
    """Checks if a tool action requires master confirmation."""
    if tool_name in RISKY_TOOLS:
        return True, RISKY_TOOLS[tool_name]
    return False, ""

def get_last_action() -> dict:
    """Retrieves the most recent action logged in the ledger."""
    ledger = load_ledger()
    return ledger[-1] if ledger else None

def rewind_last_action() -> str:
    """Undoes the most recent reversible action recorded in the ledger."""
    ledger = load_ledger()
    if not ledger:
        return "The Sanctum ledger is empty. Nothing to rewind."
    
    # Retrieve and remove last entry
    last_entry = ledger.pop()
    save_ledger(ledger)
    
    if not last_entry.get("reversible", False):
        return f"Action '{last_entry['tool_name']}' cannot be undone by the Eye of Agamotto."

    tool_name = last_entry["tool_name"]
    undo_data = last_entry.get("undo_data", {})

    # Rewind execution mapping
    try:
        if tool_name == "write_file":
            filepath = undo_data.get("filepath")
            if filepath and os.path.exists(filepath):
                os.remove(filepath)
                return f"Rewound: Deleted file '{filepath}' created by previous action."
        elif tool_name == "write_to_clipboard":
            import pyperclip
            pyperclip.copy(undo_data.get("previous_content", ""))
            return "Rewound: Restored previous clipboard content."
        elif tool_name == "open_application":
            import subprocess
            app = last_entry["args"].get("app_name")
            if app:
                subprocess.run(f"taskkill /f /im {app}.exe", shell=True, capture_output=True)
                return f"Rewound: Closed application '{app}'."
        
        return f"Action '{tool_name}' was rewound from the ledger."
    except Exception as e:
        return f"Failed to rewind action '{tool_name}': {e}"