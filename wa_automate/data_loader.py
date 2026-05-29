import os
import json
from typing import List, Dict, Any
import pandas as pd
from .logger import logger
from .exceptions import DataLoaderError

def load_contacts(file_path: str) -> List[Dict[str, Any]]:
    """
    Load contacts from an Excel (.xlsx, .xls), CSV (.csv), or JSON (.json) file.
    Returns a list of dictionaries representing each contact row.
    """
    if not file_path:
        logger.error("Contacts file path is empty.")
        return []

    if not os.path.exists(file_path):
        logger.error(f"Contacts file not found: {file_path}")
        return []

    ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path, engine="openpyxl")
            # Convert empty fields or NaN to None
            df = df.where(pd.notnull(df), None)
            contacts = df.to_dict(orient="records")
        elif ext == '.csv':
            df = pd.read_csv(file_path)
            # Convert empty fields or NaN to None
            df = df.where(pd.notnull(df), None)
            contacts = df.to_dict(orient="records")
        elif ext == '.json':
            with open(file_path, "r", encoding="utf-8") as f:
                contacts = json.load(f)
                if not isinstance(contacts, list):
                    raise DataLoaderError("JSON file content must be a list of contact objects.")
        else:
            logger.error(f"Unsupported file format: {ext}. Only Excel, CSV, and JSON files are supported.")
            return []

        logger.info(f"Successfully loaded {len(contacts)} contacts from {file_path}")
        return contacts

    except Exception as e:
        logger.error(f"Failed to load contacts from {file_path}: {e}")
        return []
