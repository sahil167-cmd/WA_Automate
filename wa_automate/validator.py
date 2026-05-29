import re
from typing import Optional
from .logger import logger
from .exceptions import ValidationError

def clean_phone_number(phone: Optional[str], default_country_code: str = "91") -> Optional[str]:
    """
    Clean and format phone number for WhatsApp Web.
    - Strips all non-digit characters.
    - Prepends default country code if number doesn't have it.
    - Checks for E.164 validity constraints (between 7 and 15 digits).
    
    Returns:
        Cleaned phone number string, or None if invalid.
    """
    if not phone:
        return None

    # Convert to string and strip spaces
    phone_str = str(phone).strip()
    
    # Strip any decimal point if read as float (e.g. 919876543210.0 -> 919876543210)
    if phone_str.endswith('.0'):
        phone_str = phone_str[:-2]

    # Remove non-digit characters
    digits = re.sub(r"\D", "", phone_str)

    if not digits:
        return None

    # Handle local numbers without country code (typically 10 digits for India)
    if len(digits) == 10 and default_country_code:
        digits = f"{default_country_code}{digits}"
        logger.debug(f"Prepended country code: {default_country_code} -> {digits}")

    # Validate E.164 length (typically 7 to 15 digits)
    if not (7 <= len(digits) <= 15):
        logger.warning(f"Phone number '{phone}' (cleaned: '{digits}') failed length validation (7-15 digits).")
        return None

    return digits


def is_valid_phone_number(phone: Optional[str], default_country_code: str = "91") -> bool:
    """
    Boolean helper to check if a phone number is valid after cleaning.
    """
    try:
        cleaned = clean_phone_number(phone, default_country_code)
        return cleaned is not None
    except Exception:
        return False
