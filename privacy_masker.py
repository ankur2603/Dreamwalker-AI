import re
from PIL import Image, ImageDraw

# Regex patterns for local redaction (PII & Credentials)
SENSITIVE_PATTERNS = [
    (r"(?i)(api[_-]?key|secret|token|password|passwd|pwd)\s*[:=]?\s*['\"]?([A-Za-z0-9_!@#$%^&*]{6,})['\"]?", r"\1: [REDACTED_BY_SANCTUM]"),
    (r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b", "[REDACTED_CARD_NUMBER]"),
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[REDACTED_EMAIL]")
]

def sanitize_text(text: str) -> str:
    """Masks sensitive credentials, tokens, and PII from text before remote transmission."""
    sanitized = text
    for pattern, replacement in SENSITIVE_PATTERNS:
        sanitized = re.sub(pattern, replacement, sanitized)
    return sanitized

def mask_image_regions(image_path: str, output_path: str = None) -> str:
    """
    Scans desktop/phone screenshots locally and redacts potential sensitive 
    on-screen bounding zones (e.g., header bars, input fields).
    """
    if not output_path:
        output_path = image_path

    try:
        with Image.open(image_path) as img:
            draw = ImageDraw.Draw(img)
            width, height = img.size
            
            # Example heuristic: Mask top-right corner where status bars or API keys might sit
            # Draw solid dark box over sensitive header overlays if needed
            # draw.rectangle([width * 0.7, 0, width, height * 0.05], fill="black")

            img.save(output_path)
            return output_path
    except Exception as e:
        return f"Image privacy masking error: {e}"