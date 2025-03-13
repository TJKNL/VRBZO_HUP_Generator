# HUP Generator Tool

A tool for generating Handhavings Uitvoerings Programma (HUP) files based on KRO data.

## Features

- Web-based user interface for easy data upload and configuration
- Automatic CSV delimiter detection
- Predefined filters for different building types
- Excel export with customizable options
- Standalone executable that doesn't require Python installation

## Installation

### For End Users (No Python Required)

1. Download the latest release from the Releases section
2. Extract the ZIP file to your preferred location
3. Run the `HUP_Generator.exe` file

When you run the application:
- A command window will appear with the application status
- Your default web browser will automatically open with the application interface
- If the browser doesn't open automatically, you can manually navigate to the URL shown in the command window

### For Developers (With Python)

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application in development mode:
   ```
   python app.py
   ```

## Building the Standalone Application

To build the standalone executable:

```
python build_app.py
```

The executable will be created in the `dist` directory.

## Usage

1. **Upload Data Files**:
   - Upload the KRO-aanzien CSV file
   - Upload the KRO-gebruik CSV file

2. **Select Filters**:
   - Choose which building types to include in the HUP

3. **Configure Output**:
   - Select whether to use the built-in Excel template or upload a custom one
   - Choose additional options like removing entries without names

4. **Generate Output**:
   - The application will process the data and generate an Excel file
   - The location of the output file will be displayed

## Project Structure

- `app.py`: Main application with UI
- `data_management.py`: Data handling functions
- `classes.py`: Core logic and data processing classes
- `build_app.py`: Script to build the standalone executable
- `HUP/`: Directory containing Excel templates

## License

[Insert License Information]
