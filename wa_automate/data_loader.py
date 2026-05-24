import os
import pandas as pd
from .logger import logger

def load_contacts(file_path: str) -> list:
    """
    Load contacts from an Excel (.xlsx, .xls) or CSV file.
    Returns a list of dictionaries representing each contact row.
    """
    if not os.path.exists(file_path):
        logger.error(f"Contacts file not found: {file_path}")
        return []

    ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path, engine="openpyxl")
        elif ext == '.csv':
            df = pd.read_csv(file_path)
        else:
            logger.error(f"Unsupported file format: {ext}. Only Excel and CSV files are supported.")
            return []

        # Convert empty fields or NaN to None
        df = df.where(pd.notnull(df), None)
        
        # Convert df to a list of dicts
        contacts = df.to_dict(orient="records")
        logger.info(f"Successfully loaded {len(contacts)} contacts from {file_path}")
        return contacts

    except Exception as e:
        logger.error(f"Failed to load contacts from {file_path}: {e}")
        return []
