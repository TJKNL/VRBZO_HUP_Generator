import os
import sys
import time
import threading
import webbrowser
import argparse
from datetime import datetime
import tempfile
from typing import List, Dict, Any

# PyWebIO imports
from pywebio.platform.flask import start_server
from pywebio import start_server as start_pywebio_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import set_env, info as session_info, run_js

# Local imports
from data_management import (
    load_data_from_content, 
    get_executable_relative_path, 
    FILTER_DEFINITIONS, 
    apply_filter_to_tree
)
from classes import KRO_Tree

def ui_header():
    """Display application header and information."""
    set_env(title="HUP Generator Tool")
    
    put_markdown("""
    # HUP Generator Tool
    
    This tool helps you generate Handhavings Uitvoerings Programma (HUP) files based on KRO data.
    
    **Instructions:**
    1. Upload the required CSV files
    2. Choose which filters to apply
    3. Generate the Excel output
    """)

def ui_footer():
    """Display footer with developer information."""
    put_markdown("""
    ---
    
    Developed by [Twan Kerkhof](https://www.twankerkhof.nl)
    """)

def ui_file_upload() -> tuple:
    """Handle file upload UI and return the loaded dataframes."""
    put_markdown("## Step 1: Upload Data Files")
    
    try:
        aanzien_file = file_upload("Upload KRO-aanzien CSV file:", accept=".csv", required=True)
        gebruik_file = file_upload("Upload KRO-gebruik CSV file:", accept=".csv", required=True)
        
        with put_loading("Loading and processing data files..."):
            try:
                df_aanzien = load_data_from_content(aanzien_file['content'], aanzien_file['filename'])
                df_gebruik = load_data_from_content(gebruik_file['content'], gebruik_file['filename'])
                
                put_success(f"Files loaded successfully: {aanzien_file['filename']} and {gebruik_file['filename']}")
                return df_aanzien, df_gebruik
                
            except Exception as e:
                put_error(f"Error loading files: {str(e)}")
                put_text("Please check that your files are valid CSV files with the expected columns.")
                return None, None
    except Exception as e:
        put_error(f"Error during file upload: {str(e)}")
        return None, None

def ui_filter_selection() -> List[str]:
    """UI for filter selection."""
    put_markdown("## Step 2: Select Filters to Apply")
    
    # Create user-friendly options from filter definitions
    options = [
        {"label": f"{filter_def['name']} ({filter_def['description']})", "value": key}
        for key, filter_def in FILTER_DEFINITIONS.items()
    ]
    
    selected_filters = checkbox(
        "Select which filters to apply:", 
        options=options,
        required=True
    )
    
    if not selected_filters:
        put_warning("No filters selected. The output may be empty.")
    
    return selected_filters

def ui_export_options() -> Dict[str, Any]:
    """UI for export options."""
    put_markdown("## Step 3: Configure Output Options")
    
    template_selection = radio(
        "Choose Excel template:",
        options=[
            {"label": "Use built-in template", "value": "builtin"},
            {"label": "Upload custom template", "value": "custom"}
        ],
        required=True
    )
    
    template_path = get_executable_relative_path("HUP", "origineel (niet aanpassen).xlsx")
    
    if template_selection == "custom":
        template_file = file_upload("Upload Excel template:", accept=".xlsx", required=True)
        if template_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
                temp_file.write(template_file['content'])
                template_path = temp_file.name
    
    options = {}
    options["template_path"] = template_path
    
    options["remove_no_name"] = checkbox(
        "Output options:", 
        options=[{"label": "Remove entries without name", "value": "remove_no_name"}]
    )
    
    options["add_A"] = checkbox(
        "Advanced options:", 
        options=[{"label": "Include class A objects (warning: this may significantly increase processing time)", "value": "add_A"}]
    )
    
    return options

def ui_process_and_export(tree: KRO_Tree, selected_filters: List[str], export_options: Dict[str, Any]) -> None:
    """Process the data with selected filters and export to Excel."""
    put_markdown("## Processing and Generating Output")
    
    # Apply filters
    with put_loading("Applying filters..."):
        try:
            for filter_key in selected_filters:
                put_text(f"Applying filter: {FILTER_DEFINITIONS[filter_key]['name']}")
                apply_filter_to_tree(tree, filter_key)
        except Exception as e:
            put_error(f"Error applying filters: {str(e)}")
            return
    
    # Export to Excel
    with put_loading("Generating Excel file..."):
        try:
            # Create output directory if it doesn't exist
            output_dir = get_executable_relative_path("HUP")
            os.makedirs(output_dir, exist_ok=True)
            
            datetime_string = datetime.now().strftime("%d-%m-%Y_%H-%M")
            output_path = os.path.join(output_dir, f"HUP-{datetime_string}.xlsx")
            
            # Generate the Excel file
            tree.insert_dataframe_into_excel(
                export_options["template_path"],
                "Controle objecten", 
                2, 
                add_A="add_A" in export_options["add_A"],
                remove_no_name="remove_no_name" in export_options["remove_no_name"]
            )
            
            put_success(f"Excel file generated successfully at: {output_path}")
            
            # Add a download button
            put_text("You can find the output file in the following location:")
            put_code(os.path.abspath(output_path))
            
        except FileNotFoundError as e:
            put_error(f"Error: Template file not found. Please check that the template exists.")
            put_text(f"Details: {str(e)}")
        except PermissionError as e:
            put_error(f"Error: Permission denied when writing output file.")
            put_text(f"Details: {str(e)}")
            put_text("Make sure you have write permissions to the output directory and the file is not open in another program.")
        except Exception as e:
            put_error(f"Error generating Excel file: {str(e)}")

def main():
    """Main application flow."""
    try:
        ui_header()
        
        # Step 1: File Upload
        df_aanzien, df_gebruik = ui_file_upload()
        if df_aanzien is None or df_gebruik is None:
            put_text("Please try again with valid CSV files.")
            ui_footer()  # Still show footer even if there's an error
            return
        
        # Initialize KRO Tree
        try:
            tree = KRO_Tree(df_aanzien, df_gebruik)
        except Exception as e:
            put_error(f"Error initializing data processor: {str(e)}")
            put_text("There might be an issue with the structure of your CSV files.")
            ui_footer()
            return
        
        # Step 2: Filter Selection
        try:
            selected_filters = ui_filter_selection()
            if not selected_filters:
                put_warning("No filters were selected. The output may be empty.")
        except Exception as e:
            put_error(f"Error during filter selection: {str(e)}")
            ui_footer()
            return
        
        # Step 3: Export Options
        try:
            export_options = ui_export_options()
        except Exception as e:
            put_error(f"Error configuring export options: {str(e)}")
            ui_footer()
            return
        
        # Step 4: Processing and Export
        ui_process_and_export(tree, selected_filters, export_options)
        
        # Completion
        put_markdown("## Processing Complete")
        put_text("You can now close this window or process another set of files.")
        put_button("Process New Files", onclick=lambda: run_js('window.location.reload()'))
        
        # Add footer with developer information
        ui_footer()
        
    except Exception as e:
        put_error(f"An unexpected error occurred: {str(e)}")
        put_html("""
        <div style="margin-top: 20px; padding: 15px; border: 1px solid #f8d7da; background-color: #f8d7da; color: #721c24; border-radius: 5px;">
            <h3>Error Details</h3>
            <p>The application encountered an unexpected error. Here are some things you can try:</p>
            <ul>
                <li>Check that your input files are properly formatted CSV files</li>
                <li>Verify that you have read/write permissions for the application directory</li>
                <li>Restart the application and try again</li>
            </ul>
        </div>
        """)
        ui_footer()  # Still show footer even if there's an error

def setup_app_launcher():
    """Set up the application launcher with appropriate UI depending on environment."""
    parser = argparse.ArgumentParser(description="HUP Generator Tool")
    parser.add_argument("--port", type=int, default=8080, help="Port for the web server")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser automatically")
    parser.add_argument("--server", action="store_true", help="Run as a server instead of standalone app")
    args = parser.parse_args()
    
    is_frozen = getattr(sys, 'frozen', False)
    
    # Determine if we should run as a server or standalone app
    run_as_server = args.server and not is_frozen
    
    if not run_as_server:
        # We're running as a standalone app - open browser automatically
        if not args.no_browser:
            def open_browser():
                time.sleep(1.5)  # Wait a bit for the server to start
                url = f"http://localhost:{args.port}"
                print(f"Opening HUP Generator in your web browser: {url}")
                webbrowser.open(url)
            
            threading.Thread(target=open_browser).start()
        
        # Print instructions to console for clarity
        print("="*50)
        print("HUP Generator Tool")
        print("="*50)
        print(f"The application is running at: http://localhost:{args.port}")
        print("If the browser doesn't open automatically, please open the URL manually.")
        print("Press Ctrl+C to quit the application.")
        print("="*50)
        
        # Start the pywebio server
        start_pywebio_server(main, port=args.port, debug=False)
    else:
        # We're running as a server
        print(f"Starting HUP Generator server on port {args.port}")
        start_server(main, port=args.port, debug=False)

if __name__ == "__main__":
    setup_app_launcher()
