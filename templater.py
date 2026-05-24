import re
from logger import logger

def format_message(template: str, context: dict) -> str:
    """
    Format message using template string and context dictionary.
    Placeholders are specified like {KeyName}.
    Missing keys are replaced with an empty string or logged as warning.
    """
    if not template:
        return ""

    # Find all placeholders in the template
    placeholders = re.findall(r"\{([^}]+)\}", template)

    formatted_msg = template
    for placeholder in placeholders:
        # Strip whitespace from placeholder name
        key = placeholder.strip()
        
        # Check matching context key (case-insensitive for robustness)
        match_found = False
        for k, v in context.items():
            if str(k).strip().lower() == key.lower():
                val = str(v) if v is not None and not (isinstance(v, float) and v != v) else ""
                formatted_msg = formatted_msg.replace(f"{{{placeholder}}}", val)
                match_found = True
                break
        
        if not match_found:
            logger.warning(f"Placeholder '{{{placeholder}}}' not found in contacts data.")
            formatted_msg = formatted_msg.replace(f"{{{placeholder}}}", "")

    return formatted_msg
