from wa_automate.templater import format_message

def test_format_message_basic():
    template = "Hello {Name}, welcome to {City}!"
    context = {"Name": "Sahil", "City": "Mumbai"}
    assert format_message(template, context) == "Hello Sahil, welcome to Mumbai!"

def test_format_message_case_insensitive():
    template = "Hello {name}, welcome to {city}!"
    context = {"Name": "Sahil", "CITY": "Mumbai"}
    assert format_message(template, context) == "Hello Sahil, welcome to Mumbai!"

def test_format_message_with_fallback():
    template = "Hello {Name|Customer}, your order {OrderID|is pending}."
    context = {"Name": "", "OrderID": "12345"}
    # Name is empty, so should use fallback. OrderID has value, so should use value.
    assert format_message(template, context) == "Hello Customer, your order 12345."

def test_format_message_missing_key_no_fallback():
    template = "Hello {Name}, code is {Code}."
    context = {"Name": "Sahil"}
    assert format_message(template, context) == "Hello Sahil, code is ."

def test_format_message_empty_template():
    assert format_message("", {"Name": "Sahil"}) == ""
    assert format_message(None, {"Name": "Sahil"}) == ""
