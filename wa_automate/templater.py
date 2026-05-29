import re
from typing import Dict, Any
from .logger import logger

def format_message(template: str, context: Dict[str, Any]) -> str:
    """
    Format message using template string and context dictionary.
    Placeholders are specified like {KeyName} or with default fallback {KeyName|fallback_value}.
    Missing keys without a fallback are replaced with an empty string.
    """
    if not template:
        return ""

    # Find all placeholders in the template (e.g. {Name} or {Name|there})
    placeholders = re.findall(r"\{([^}]+)\}", template)

    formatted_msg = template
    for placeholder in placeholders:
        # Check if placeholder has a fallback value, e.g. Name|Customer
        parts = placeholder.split('|', 1)
        key = parts[0].strip()
        fallback = parts[1].strip() if len(parts) > 1 else ""
        
        # Check matching context key (case-insensitive for robustness)
        match_found = False
        for k, v in context.items():
            if str(k).strip().lower() == key.lower():
                # Treat empty string or NaN float as missing value to trigger fallback
                is_empty = v is None or (isinstance(v, float) and v != v) or str(v).strip() == ""
                val = str(v) if not is_empty else fallback
                formatted_msg = formatted_msg.replace(f"{{{placeholder}}}", val)
                match_found = True
                break
        
        if not match_found:
            logger.debug(f"Placeholder '{key}' not found in contacts data. Using fallback: '{fallback}'")
            formatted_msg = formatted_msg.replace(f"{{{placeholder}}}", fallback)

    return formatted_msg
