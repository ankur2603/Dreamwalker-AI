import subprocess
import os
import shutil

def _run_adb(args: list) -> tuple[bool, str]:
    """Runs ADB command safely with system PATH detection."""
    adb_path = shutil.which("adb")
    if not adb_path:
        return False, "ADB binary not found in system PATH. Install Android Platform Tools to enable phone control."

    try:
        cmd = [adb_path] + args
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if res.returncode == 0:
            return True, res.stdout.strip()
        return False, res.stderr.strip() or res.stdout.strip()
    except Exception as e:
        return False, str(e)

def phone_take_screenshot() -> str:
    """Captures a screenshot from the connected Android phone and pulls it to local PC."""
    success, msg = _run_adb(["shell", "screencap", "-p", "/sdcard/phone_cap.png"])
    if not success:
        return f"Failed to take phone screenshot: {msg}"
    
    os.makedirs("screenshots", exist_ok=True)
    local_path = os.path.join("screenshots", "phone_capture.png")
    success, msg = _run_adb(["pull", "/sdcard/phone_cap.png", local_path])
    if success:
        return f"Phone screenshot saved locally to {local_path}."
    return f"Failed to retrieve phone screenshot: {msg}"

def phone_launch_app(package_name: str) -> str:
    """Launches an app on the Android phone using its package name (e.g., com.android.chrome)."""
    success, msg = _run_adb(["shell", "monkey", "-p", package_name, "-c", "android.intent.category.LAUNCHER", "1"])
    if success:
        return f"Launched app '{package_name}' on Android phone."
    return f"Failed to launch app '{package_name}': {msg}"

def phone_tap(x: int, y: int) -> str:
    """Taps the screen at specific (x, y) pixel coordinates on the Android phone."""
    success, msg = _run_adb(["shell", "input", "tap", str(x), str(y)])
    if success:
        return f"Tapped coordinates ({x}, {y}) on phone."
    return f"Failed to tap coordinates: {msg}"

def phone_type_text(text: str) -> str:
    """Types text on the Android phone (replaces spaces with %s for adb input)."""
    formatted_text = text.replace(" ", "%s")
    success, msg = _run_adb(["shell", "input", "text", formatted_text])
    if success:
        return f"Typed text '{text}' on phone."
    return f"Failed to type text on phone: {msg}"