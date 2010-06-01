# general utils

def safe_string(text):
    try:
        return str(text)
    except (ValueError, AttributeError):
        return ""