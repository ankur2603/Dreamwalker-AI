import os
import json

ROUTINES_FILE = "sanctum_routines.json"

def load_routines() -> dict:
    """Loads saved voice routines from disk."""
    if os.path.exists(ROUTINES_FILE):
        try:
            with open(ROUTINES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_routines(routines: dict):
    """Saves routines state to disk."""
    with open(ROUTINES_FILE, 'w', encoding='utf-8') as f:
        json.dump(routines, f, indent=2)

def save_custom_routine(name: str, steps: list) -> str:
    """Forges a new multi-step incantation and saves it persistently."""
    routines = load_routines()
    routines[name.lower()] = steps
    save_routines(routines)
    return f"Incantation '{name}' successfully forged into the Sanctum archives with {len(steps)} steps."

def get_custom_routine(name: str) -> list:
    """Retrieves steps for a forged incantation by name."""
    routines = load_routines()
    return routines.get(name.lower(), None)

def delete_custom_routine(name: str) -> str:
    """Erases a custom routine from the Sanctum archives."""
    routines = load_routines()
    if name.lower() in routines:
        del routines[name.lower()]
        save_routines(routines)
        return f"Incantation '{name}' erased from Sanctum archives."
    return f"Incantation '{name}' not found."
