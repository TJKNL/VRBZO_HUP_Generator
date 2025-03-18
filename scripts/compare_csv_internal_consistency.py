import os
print('imported os')

import glob
print('imported glob')
from collections import defaultdict
print('imported defaultdict from collections')
import csv
print('imported csv')
import io
print('imported io')
import pandas as pd
print('imported pandas as pd')
print('test')
#%% Find the CSV files
def find_csv_files(directory, pattern):
    """Find CSV files in directory (and subdirectories) matching the pattern."""
    return glob.glob(os.path.join(directory, f"**/*{pattern}*.csv"), recursive=True)

# Define the data directory
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
print(f"Looking for CSV files in: {data_dir}")

# Find files with 'aanzien' and 'gebruik' in their names
aanzien_files = find_csv_files(data_dir, 'aanzien')
gebruik_files = find_csv_files(data_dir, 'gebruik')

print(f"Found {len(aanzien_files)} aanzien files and {len(gebruik_files)} gebruik files.")

#%% Function to detect delimiter
def detect_delimiter(file_path):
    """Detect the delimiter of a CSV file using csv.Sniffer and fallback methods."""
    try:
        # Read a sample of the file to detect the delimiter
        sample_size = 4096  # Read first 4KB to detect delimiter
        with open(file_path, 'r', encoding='utf-8') as f:
            sample = f.read(sample_size)
        
        # Try using csv.Sniffer
        try:
            dialect = csv.Sniffer().sniff(sample)
            return dialect.delimiter
        except:
            # If sniffer fails, check for common delimiters
            delimiters = [',', ';', '\t', '|']
            lines = sample.split('\n')
            if not lines:
                return ','  # Default to comma if file is empty
                
            # Count occurrences of each delimiter in the first non-empty line
            for line in lines:
                if line.strip():
                    counts = {delim: line.count(delim) for delim in delimiters}
                    max_count = max(counts.values())
                    if max_count > 0:
                        # Return the delimiter that appears most frequently
                        return max(counts.items(), key=lambda x: x[1])[0]
            
            # If no delimiter found, default to comma
            return ','
    except Exception as e:
        print(f"Error detecting delimiter in {file_path}: {e}")
        return ','  # Default to comma on error

#%% Function to get column names from a file
def get_column_names(file_path):
    """Read a CSV file and return its column names, automatically detecting the delimiter."""
    try:
        # First detect the delimiter
        delimiter = detect_delimiter(file_path)
        print(f"Detected delimiter '{delimiter}' for file: {os.path.basename(file_path)}")
        
        # Try reading the file with the detected delimiter
        df = pd.read_csv(file_path, encoding='utf-8', nrows=0, sep=delimiter)
        
        # Check if we got a proper header
        if len(df.columns) == 1 and any(common_delim in df.columns[0] for common_delim in [';', ',', '\t']):
            # If we got just one column but it contains delimiters, try other common delimiters
            for other_delim in [';', ',', '\t', '|']:
                if other_delim != delimiter:
                    try:
                        test_df = pd.read_csv(file_path, encoding='utf-8', nrows=0, sep=other_delim)
                        if len(test_df.columns) > 1:
                            print(f"Switched to delimiter '{other_delim}' for better column detection")
                            return list(test_df.columns)
                    except:
                        continue
        
        return list(df.columns)
    except pd.errors.EmptyDataError:
        print(f"Empty file: {file_path}")
        return []
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

#%% Compare columns within aanzien files
print("\n--- Internal Consistency for 'aanzien' Files ---")

if len(aanzien_files) <= 1:
    print("Not enough 'aanzien' files to compare (need at least 2)")
else:
    # Get columns for each file
    aanzien_columns_by_file = {}
    for file in aanzien_files:
        file_name = os.path.basename(file)
        aanzien_columns_by_file[file_name] = get_column_names(file)
    
    # Check if all files have the same columns
    all_same = True
    first_file = list(aanzien_columns_by_file.keys())[0]
    base_columns = set(aanzien_columns_by_file[first_file])
    
    # Compare each file with the first one
    differences = {}
    for file_name, columns in aanzien_columns_by_file.items():
        file_columns = set(columns)
        if file_columns != base_columns:
            all_same = False
            missing = base_columns - file_columns
            extra = file_columns - base_columns
            differences[file_name] = {'missing': missing, 'extra': extra}
    
    if all_same:
        print(f"✓ All {len(aanzien_files)} 'aanzien' files have identical columns ({len(base_columns)} columns)")
        print(f"Columns: {', '.join(sorted(base_columns))}")
    else:
        print(f"✗ Column differences found between 'aanzien' files:")
        print(f"Base file: {first_file} with {len(base_columns)} columns")
        
        for file_name, diff in differences.items():
            if diff['missing'] or diff['extra']:
                print(f"\n  File: {file_name}")
                if diff['missing']:
                    print(f"    Missing columns: {', '.join(sorted(diff['missing']))}")
                if diff['extra']:
                    print(f"    Extra columns: {', '.join(sorted(diff['extra']))}")

#%% Compare columns within gebruik files
print("\n--- Internal Consistency for 'gebruik' Files ---")

if len(gebruik_files) <= 1:
    print("Not enough 'gebruik' files to compare (need at least 2)")
else:
    # Get columns for each file
    gebruik_columns_by_file = {}
    for file in gebruik_files:
        file_name = os.path.basename(file)
        gebruik_columns_by_file[file_name] = get_column_names(file)
    
    # Check if all files have the same columns
    all_same = True
    first_file = list(gebruik_columns_by_file.keys())[0]
    base_columns = set(gebruik_columns_by_file[first_file])
    
    # Compare each file with the first one
    differences = {}
    for file_name, columns in gebruik_columns_by_file.items():
        file_columns = set(columns)
        if file_columns != base_columns:
            all_same = False
            missing = base_columns - file_columns
            extra = file_columns - base_columns
            differences[file_name] = {'missing': missing, 'extra': extra}
    
    if all_same:
        print(f"✓ All {len(gebruik_files)} 'gebruik' files have identical columns ({len(base_columns)} columns)")
        print(f"Columns: {', '.join(sorted(base_columns))}")
    else:
        print(f"✗ Column differences found between 'gebruik' files:")
        print(f"Base file: {first_file} with {len(base_columns)} columns")
        
        for file_name, diff in differences.items():
            if diff['missing'] or diff['extra']:
                print(f"\n  File: {file_name}")
                if diff['missing']:
                    print(f"    Missing columns: {', '.join(sorted(diff['missing']))}")
                if diff['extra']:
                    print(f"    Extra columns: {', '.join(sorted(diff['extra']))}")

#%% Create summary table of file columns
print("\n--- Summary Table of Columns per File ---")

print("\nAANZIEN FILES:")
for file in aanzien_files:
    file_name = os.path.basename(file)
    columns = get_column_names(file)
    print(f"{file_name}: {len(columns)} columns")

print("\nGEBRUIK FILES:")
for file in gebruik_files:
    file_name = os.path.basename(file)
    columns = get_column_names(file)
    print(f"{file_name}: {len(columns)} columns")
