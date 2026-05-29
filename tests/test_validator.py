from wa_automate.validator import clean_phone_number, is_valid_phone_number

def test_clean_phone_number_valid_10_digits():
    # Prepend default country code '91' to 10 digit number
    assert clean_phone_number("9876543210") == "919876543210"
    assert clean_phone_number(9876543210) == "919876543210"

def test_clean_phone_number_with_country_code():
    assert clean_phone_number("919876543210") == "919876543210"
    assert clean_phone_number("+91 98765-43210") == "919876543210"

def test_clean_phone_number_float_format():
    # Excel sometimes reads as floats, e.g. 919876543210.0
    assert clean_phone_number("919876543210.0") == "919876543210"

def test_clean_phone_number_invalid():
    assert clean_phone_number("12345") is None  # Too short
    assert clean_phone_number("abcdef") is None  # No digits
    assert clean_phone_number("") is None
    assert clean_phone_number(None) is None

def test_is_valid_phone_number():
    assert is_valid_phone_number("9876543210") is True
    assert is_valid_phone_number("123") is False
    assert is_valid_phone_number(None) is False
