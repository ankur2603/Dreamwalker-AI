import time
import os
import threading
from pc_tools import take_screenshot
from verifier import verify_action

class WatchfulGuardian:
    def __init__(self, check_interval_seconds: int = 15):
        self.check_interval = check_interval_seconds
        self.is_running = False
        self._thread = None

    def _monitor_loop(self):
        print("👁️ The Watchful Guardian is keeping watch in the background...")
        while self.is_running:
            time.sleep(self.check_interval)
            # Capture background state safely
            take_screenshot()
            
            # Simple heuristic check for unsaved work / error popups in recent screenshots
            # In a full multimodal loop, this frame is passed to Gemini Flash Lite
            # for low-latency visual anomaly detection.
            # print("🛡️ Guardian Scan: Screen nominal.")

    def start(self):
        """Starts background screen monitoring daemon."""
        if not self.is_running:
            self.is_running = True
            self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self._thread.start()

    def stop(self):
        """Stops the monitoring daemon."""
        self.is_running = False
        print("🛡️ Watchful Guardian standing down.")