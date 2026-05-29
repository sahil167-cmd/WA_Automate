import os
import json
import pytest
import pandas as pd
from wa_automate.data_loader import load_contacts

@pytest.fixture
def temp_files():
    files = []
    def _create_file(name, content, file_type='json'):
        path = os.path.join(os.path.dirname(__file__), name)
        if file_type == 'json':
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(content, f)
        elif file_type == 'csv':
            df = pd.DataFrame(content)
            df.to_csv(path, index=False)
        elif file_type == 'xlsx':
            df = pd.DataFrame(content)
            df.to_excel(path, index=False, engine='openpyxl')
        files.append(path)
        return path

    yield _create_file

    for f in files:
        if os.path.exists(f):
            os.remove(f)

def test_load_contacts_non_existent():
    assert load_contacts("non_existent_file.csv") == []

def test_load_contacts_json(temp_files):
    data = [
        {"Name": "Alice", "Phone": "919999999999"},
        {"Name": "Bob", "Phone": "918888888888"}
    ]
    path = temp_files("contacts_test.json", data, 'json')
    contacts = load_contacts(path)
    assert len(contacts) == 2
    assert contacts[0]["Name"] == "Alice"
    assert contacts[1]["Phone"] == "918888888888"

def test_load_contacts_csv(temp_files):
    data = {
        "Name": ["Alice", "Bob"],
        "Phone": [919999999999, 918888888888]
    }
    path = temp_files("contacts_test.csv", data, 'csv')
    contacts = load_contacts(path)
    assert len(contacts) == 2
    # CSV reader might parse phone as int, which clean_phone_number will handle later
    assert contacts[0]["Name"] == "Alice"

def test_load_contacts_unsupported():
    assert load_contacts("invalid_file.txt") == []
