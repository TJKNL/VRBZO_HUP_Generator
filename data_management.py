import pandas as pd
import os
import sys
import tempfile
import io
import csv
from typing import Tuple, Dict, List, Any, Optional

def load_data_from_file(file_path: str) -> pd.DataFrame:
    """Load data from a CSV file with semicolon delimiter."""
    try:
        df_output = pd.read_csv(file_path, header=0, delimiter=';')
        print(f"Data loaded from {os.path.basename(file_path)}.")
        return df_output
    except Exception as e:
        print(f"Error loading data from {file_path}: {e}")
        raise

def detect_delimiter(file_content: bytes) -> str:
    """Auto-detect the delimiter in CSV content."""
    import csv
    
    # Write content to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
        temp_file.write(file_content)
        temp_file_path = temp_file.name
    
    try:
        # Try to detect delimiter using csv.Sniffer
        with open(temp_file_path, 'r', encoding='utf-8') as f:
            sample = f.read(4096)  # Read first 4KB
            try:
                dialect = csv.Sniffer().sniff(sample)
                return dialect.delimiter
            except:
                pass
        
        # Fallback method - try common delimiters
        common_delimiters = [',', ';', '\t', '|']
        for delimiter in common_delimiters:
            try:
                df = pd.read_csv(temp_file_path, nrows=5, sep=delimiter, encoding='utf-8')
                if len(df.columns) > 1:
                    return delimiter
            except:
                continue
                
        # If all else fails, return semicolon (most common for Dutch data)
        return ';'
    finally:
        try:
            os.unlink(temp_file_path)
        except:
            pass

def load_data_from_content(content: bytes, filename: str, delimiters: List[str] = None) -> pd.DataFrame:
    """
    Load data from file content with automatic delimiter detection.
    
    Args:
        content: Raw bytes content of the file
        filename: Original filename for reference
        delimiters: List of delimiters to try, defaults to [',', ';']
        
    Returns:
        pandas.DataFrame: Loaded data
    """
    if delimiters is None:
        delimiters = [',', ';']
    
    # Convert bytes to string
    text_content = content.decode('utf-8', errors='ignore')
    
    # Try to detect delimiter using csv.Sniffer
    try:
        sample = text_content[:4096]  # Use first 4096 characters as sample
        dialect = csv.Sniffer().sniff(sample)
        if dialect.delimiter in delimiters:
            return pd.read_csv(io.StringIO(text_content), sep=dialect.delimiter)
    except Exception:
        # Sniffer can fail if the format is unusual, continue to manual checks
        pass
    
    # If auto-detection fails, try each delimiter in order
    for delimiter in delimiters:
        try:
            df = pd.read_csv(io.StringIO(text_content), sep=delimiter)
            # Verify this looks like valid CSV data (has at least one row and multiple columns)
            if len(df) > 0 and len(df.columns) > 1:
                return df
        except Exception:
            continue
    
    # If all attempts fail, try a more aggressive approach with error handling
    try:
        # Try pandas with automatic delimiter detection and error handling
        return pd.read_csv(io.StringIO(text_content), sep=None, engine='python')
    except Exception as e:
        raise ValueError(f"Could not parse CSV file {filename}. Error: {str(e)}")

def get_resource_path(relative_path):
    """
    Get absolute path to a resource file, works both in development and when bundled with PyInstaller.
    
    Args:
        relative_path: Path relative to the application root
        
    Returns:
        Absolute path to the resource
    """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def get_executable_relative_path(*path_parts):
    """
    Generate a file path relative to the executable. For output files that need to be written.
    
    Args:
        path_parts: Path components to join with the base directory
        
    Returns:
        Absolute path relative to the executable
    """
    # When frozen, use the directory containing the executable
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        # In development mode, use the script's directory
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # Generate a file path relative to this directory
    path = os.path.join(base_dir, *path_parts)
    return path

# Filter definitions for the application
FILTER_DEFINITIONS = {
    "kdv": {
        "name": "Kinderdagverblijven",
        "description": "SBI: 88911, personen > 10",
        "filters": [
            {"type": "sbi", "codes": [88911]},
            {"type": "column", "column": "personen", "operator": ">", "value": 10}
        ],
        "risk": "C"
    },
    "cel": {
        "name": "Celfunctie",
        "description": "",
        "filters": [
            {"type": "column", "column": "celfunctie", "operator": "==", "value": 1}
        ],
        "risk": "C"
    },
    "gezond": {
        "name": "Gezondheidszorg met overnachting",
        "description": "SBI: 861, 87, personen > 10",
        "filters": [
            {"type": "sbi", "codes": [861, 87]},
            {"type": "column", "column": "personen", "operator": ">", "value": 10}
        ],
        "risk": "C"
    },
    "industrie": {
        "name": "Industrie",
        "description": "oppervlakte > 2500",
        "filters": [
            {"type": "column", "column": "industriefunctie", "operator": "==", "value": 1},
            {"type": "column", "column": "bag_oppvlk", "operator": ">", "value": 2500}
        ],
        "risk": "C"
    },
    "winkel": {
        "name": "Winkelfunctie",
        "description": "oppervlakte > 1000",
        "filters": [
            {"type": "column", "column": "winkelfunctie", "operator": "==", "value": 1},
            {"type": "column", "column": "woz_opp_nietwoon", "operator": ">", "value": 1000}
        ],
        "risk": "C"
    },
    "sport": {
        "name": "Sportfunctie",
        "description": "oppervlakte > 1000",
        "filters": [
            {"type": "column", "column": "sportfunctie", "operator": "==", "value": 1},
            {"type": "column", "column": "woz_opp_nietwoon", "operator": ">", "value": 1000}
        ],
        "risk": "C"
    },
    "onderwijs": {
        "name": "Onderwijsfunctie",
        "description": "oppervlakte > 1000, hoogte > 20",
        "filters": [
            {"type": "column", "column": "onderwijsfunctie", "operator": "==", "value": 1},
            {"type": "column", "column": "woz_opp_nietwoon", "operator": ">", "value": 1000},
            {"type": "column", "column": "pandhoogte", "operator": ">", "value": 20}
        ],
        "risk": "C"
    },
    "logies": {
        "name": "Logiesfunctie",
        "description": "SBI: 551, 552, personen > 10",
        "filters": [
            {"type": "sbi", "codes": [551, 552]},
            {"type": "column", "column": "personen", "operator": ">", "value": 10}
        ],
        "risk": "C"
    },
    "kantoor_b": {
        "name": "Kantoorfunctie (B)",
        "description": "oppervlakte > 1000, 20 < hoogte < 70",
        "filters": [
            {"type": "column", "column": "kantoorfunctie", "operator": "==", "value": 1},
            {"type": "column", "column": "woz_opp_nietwoon", "operator": ">", "value": 1000},
            {"type": "column", "column": "pandhoogte", "operator": ">", "value": 20}
        ],
        "risk": "B"
    },
    "kantoor_c": {
        "name": "Kantoorfunctie (C)",
        "description": "oppervlakte > 1000, hoogte > 70",
        "filters": [
            {"type": "column", "column": "kantoorfunctie", "operator": "==", "value": 1},
            {"type": "column", "column": "woz_opp_nietwoon", "operator": ">", "value": 1000},
            {"type": "column", "column": "pandhoogte", "operator": ">", "value": 70}
        ],
        "risk": "C"
    }
}

def apply_filter_to_tree(tree, filter_key):
    """Apply a predefined filter to a KRO_Tree instance."""
    if filter_key not in FILTER_DEFINITIONS:
        print(f"Unknown filter: {filter_key}")
        return False
        
    filter_def = FILTER_DEFINITIONS[filter_key]
    print(f"Applying filter: {filter_def['name']} ({filter_def['description']})")
    
    for filter_item in filter_def["filters"]:
        if filter_item["type"] == "sbi":
            tree.filter_SBI(filter_item["codes"])
        elif filter_item["type"] == "column":
            tree.filter(filter_item["column"], filter_item["operator"], filter_item["value"])
    
    tree.set_risk(filter_def["risk"])
    tree.store_results()
    tree.reset()
    return True
