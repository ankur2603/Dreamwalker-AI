import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# System & Mobile Tools
from pc_tools import (
    open_application, close_application, take_screenshot,
    read_clipboard, write_to_clipboard, list_directory,
    read_file, write_file, run_shell_command, adjust_volume
)
from phone_tools import (
    phone_take_screenshot, phone_launch_app, phone_tap, phone_type_text
)

# Sanctum Security & Integrity Modules
from ledger import log_action, is_risky, rewind_last_action
from verifier import verify_action
from privacy_masker import sanitize_text
from darkhold_shield import scan_for_darkhold
from routines import get_custom_routine, save_custom_routine
from guardian import WatchfulGuardian
from voice_stream import SanctumVoiceEngine

# Retrieve key safely from environment
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment or .env file.")

# Initialize Client & Aux Engines
client = genai.Client(api_key=API_KEY)
voice = SanctumVoiceEngine()
guardian = WatchfulGuardian(check_interval_seconds=30)

TOOL_MAP = {
    "open_application": open_application,
    "close_application": close_application,
    "take_screenshot": take_screenshot,
    "read_clipboard": read_clipboard,
    "write_to_clipboard": write_to_clipboard,
    "list_directory": list_directory,
    "read_file": read_file,
    "write_file": write_file,
    "run_shell_command": run_shell_command,
    "adjust_volume": adjust_volume,
    "phone_take_screenshot": phone_take_screenshot,
    "phone_launch_app": phone_launch_app,
    "phone_tap": phone_tap,
    "phone_type_text": phone_type_text
}

tools_list = list(TOOL_MAP.values())
MODEL_NAME = 'gemini-3.5-flash-lite'

print("\n✨ Dreamwalker AI Master Node Active!")
print("Type 'exit' to quit or 'rewind'/'undo' to reverse time.\n")

# Start background anomaly guardian
guardian.start()
voice.set_state("idle")

def execute_tool_call(fn_name: str, fn_args: dict):
    risky, reason = is_risky(fn_name)
    if risky:
        print(f"⚠️ RISKY ACTION: '{fn_name}' ({reason})")
        confirm = input(f"   Allow execution with parameters {fn_args}? [y/N]: ").strip().lower()
        if confirm != 'y':
            print("   └─ Action canceled by Master.\n")
            return "Canceled by user."

    undo_info = {}
    if fn_name == "write_to_clipboard":
        import pyperclip
        undo_info["previous_content"] = pyperclip.paste()
    elif fn_name == "write_file":
        undo_info["filepath"] = fn_args.get("filepath")

    print(f"⚙️ Executing tool: {fn_name}({fn_args})")
    
    if fn_name in TOOL_MAP:
        raw_output = TOOL_MAP[fn_name](**fn_args)
        is_verified, v_msg = verify_action(fn_name, fn_args, raw_output)
        print(f"   └─ Raw Result: {raw_output}")
        print(f"   └─ System State Check: {v_msg}\n")

        is_reversible = fn_name in ["write_file", "write_to_clipboard", "open_application"]
        log_action(fn_name, fn_args, raw_output, reversible=is_reversible, undo_data=undo_info)
        return raw_output
    else:
        print(f"   └─ Error: Tool '{fn_name}' not registered.\n")
        return "Tool unmapped."

try:
    while True:
        voice.set_state("listening")
        raw_prompt = input("You: ").strip()
        
        if raw_prompt.lower() in ['exit', 'quit']:
            print("Dreamwalker AI shutting down...")
            guardian.stop()
            break

        if not raw_prompt:
            voice.set_state("idle")
            continue

        if raw_prompt.lower() in ['stop', 'quiet', 'shut up', 'interrupt']:
            voice.sever_tether()
            continue

        if raw_prompt.lower() in ['undo', 'rewind', 'rewind time']:
            print("👁️ Eye of Agamotto: Rewinding time...")
            result = rewind_last_action()
            print(f"   └─ {result}\n")
            voice.speak(result)
            continue

        # Security pipelines
        clean_prompt = sanitize_text(raw_prompt)
        is_safe, neutralized_prompt, darkhold_msg = scan_for_darkhold(clean_prompt)
        if not is_safe:
            print(f"🛡️ {darkhold_msg}")
            clean_prompt = neutralized_prompt

        voice.set_state("thinking")

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=clean_prompt,
            config=types.GenerateContentConfig(
                tools=tools_list,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=True
                )
            )
        )

        if response.function_calls:
            for call in response.function_calls:
                fn_name = call.name
                fn_args = dict(call.args) if call.args else {}
                output = execute_tool_call(fn_name, fn_args)
                voice.speak(f"Executed {fn_name}")
        else:
            print(f"Dreamwalker: {response.text}\n")
            voice.speak(response.text)

except KeyboardInterrupt:
    guardian.stop()
    print("\nExiting...")