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
    set_env(title="HUP Generator")
    
    # Main title and subtitle with attribution
    put_markdown("# HUP Generator").style('margin-bottom: 5px;')
    put_html('<div style="margin-bottom: 20px; color: #6c757d; font-size: 0.95rem;">Ontwikkeld door <a href="https://www.twankerkhof.nl" target="_blank" style="color: #3498db; font-weight: bold; text-decoration: none;">Twan Kerkhof</a></div>')
    
    # Application description and instructions
    put_markdown("""
    Met deze tool kunt u Handhavings Uitvoerings Programma (HUP) bestanden genereren op basis van KRO-gegevens.
    """)
    
    # Instructions in a clean box
    put_html("""
    <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #3498db; border-radius: 4px; margin: 20px 0;">
        <p style="font-weight: bold; margin-bottom: 10px;">Instructies:</p>
        <ol style="margin-left: 20px; padding-left: 0;">
            <li>Upload de benodigde CSV-bestanden (Gebruik & Aanzien)</li>
            <li>Kies welke filters u wilt toepassen</li>
            <li>Genereer de HUP als Excel bestand</li>
        </ol>
    </div>
    """)

def ui_file_upload() -> tuple:
    """Handle file upload UI and return the loaded dataframes."""
    put_markdown("## Stap 1: Upload Gegevensbestanden")
    
    try:
        # Section 1a: KRO-gebruik file upload
        put_html('<div style="margin-top: 20px; margin-bottom: 10px; padding: 10px; background-color: #e8f4f8; border-left: 4px solid #3498db; border-radius: 4px;">'
                '<strong>1a. KRO-gebruik bestand:</strong> Selecteer het CSV bestand met KRO-gebruik gegevens</div>')
        
        gebruik_file = file_upload(
            label="", 
            accept=".csv", 
            required=True,
            placeholder="Kies KRO-gebruik CSV bestand..."
        )
        
        # Process the gebruik file
        put_text("KRO-gebruik bestand verwerken...")
        try:
            # Modify load_data_from_content call to handle different delimiters
            df_gebruik = load_data_from_content(
                gebruik_file['content'], 
                gebruik_file['filename'],
                delimiters=[',', ';']  # Try both common CSV delimiters
            )
            put_success(f"KRO-gebruik bestand succesvol geladen: {gebruik_file['filename']}")
        except Exception as e:
            put_error(f"Fout bij het laden van KRO-gebruik bestand: {str(e)}")
            return None, None
        
        # Section 1b: KRO-aanzien file upload
        put_html('<div style="margin-top: 15px; margin-bottom: 10px; padding: 10px; background-color: #e8f4f8; border-left: 4px solid #3498db; border-radius: 4px;">'
                '<strong>1b. KRO-aanzien bestand:</strong> Selecteer het CSV bestand met KRO-aanzien gegevens</div>')
        
        aanzien_file = file_upload(
            label="", 
            accept=".csv", 
            required=True,
            placeholder="Kies KRO-aanzien CSV bestand..."
        )
        
        # Process the aanzien file
        put_text("KRO-aanzien bestand verwerken...")
        try:
            # Modify load_data_from_content call to handle different delimiters
            df_aanzien = load_data_from_content(
                aanzien_file['content'], 
                aanzien_file['filename'],
                delimiters=[',', ';']  # Try both common CSV delimiters
            )
            put_success(f"KRO-aanzien bestand succesvol geladen: {aanzien_file['filename']}")
        except Exception as e:
            put_error(f"Fout bij het laden van KRO-aanzien bestand: {str(e)}")
            return None, None
        
        # Both files loaded successfully
        return df_aanzien, df_gebruik
                
    except Exception as e:
        put_error(f"Fout tijdens bestandsupload: {str(e)}")
        return None, None

def ui_filter_selection() -> List[str]:
    """UI for filter selection."""
    put_markdown("## Stap 2: Selecteer Filters")
    
    # Create user-friendly options from filter definitions
    options = [
        {"label": f"{filter_def['name']} ({filter_def['description']})", "value": key}
        for key, filter_def in FILTER_DEFINITIONS.items()
    ]
    
    # Get all filter keys to pre-select them
    all_filter_keys = list(FILTER_DEFINITIONS.keys())
    
    # Render checkboxes with all options pre-selected
    selected_filters = checkbox(
        "Selecteer welke filters u wilt toepassen:", 
        options=options,
        required=True,
        value=all_filter_keys  # Pre-select all filters
    )
    
    if not selected_filters:
        put_warning("Geen filters geselecteerd. De HUP kan leeg zijn.")
    
    return selected_filters

def ui_export_options() -> Dict[str, Any]:
    """UI for export options."""
    put_markdown("## Stap 3: Configureer Uitvoeropties")
    
    template_selection = radio(
        "Kies Excel-sjabloon:",
        options=[
            {"label": "Gebruik ingebouwd HUP-sjabloon", "value": "builtin"},
            {"label": "Upload aangepast HUP-sjabloon", "value": "custom"}
        ],
        required=True
    )
    
    # Use get_resource_path for reading the template
    from data_management import get_resource_path
    template_path = get_resource_path(os.path.join("resources", "origineel (niet aanpassen).xlsx"))
    
    if template_selection == "custom":
        template_file = file_upload("Upload Excel-sjabloon:", accept=".xlsx", required=True)
        if template_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
                temp_file.write(template_file['content'])
                template_path = temp_file.name
    
    options = {}
    options["template_path"] = template_path
    
    options["remove_no_name"] = checkbox(
        "Uitvoeropties:", 
        options=[{"label": "Verwijder items zonder naam", "value": "remove_no_name"}]
    )
    
    options["add_A"] = checkbox(
        "Geavanceerde opties:", 
        options=[{"label": "Voeg klasse A objecten toe (waarschuwing: dit kan de verwerkingstijd aanzienlijk verlengen)", "value": "add_A"}]
    )
    
    return options

def ui_process_and_export(tree: KRO_Tree, selected_filters: List[str], export_options: Dict[str, Any]) -> None:
    """Process the data with selected filters and export to Excel."""
    put_markdown("## Verwerken en Genereren van de HUP")
    
    # Initialize process bar
    put_processbar('process_bar')
    set_processbar('process_bar', 0)
    
    total_steps = len(selected_filters) + 1  # Filters + Excel export
    current_step = 0
    
    # Apply filters
    put_info("Filters toepassen...")
    try:
        for filter_key in selected_filters:
            current_step += 1
            put_text(f"Filter toepassen: {FILTER_DEFINITIONS[filter_key]['name']}")
            apply_filter_to_tree(tree, filter_key)
            set_processbar('process_bar', current_step / total_steps)
    except Exception as e:
        put_error(f"Fout bij het toepassen van filters: {str(e)}")
        return
    
    # Export to Excel
    put_info("Excel-bestand genereren...")
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
        
        current_step += 1
        set_processbar('process_bar', current_step / total_steps)
        
        put_success(f"Excel-bestand succesvol gegenereerd op: {output_path}")
        
        # Add a download button
        put_text("U kunt het uitvoerbestand vinden op de volgende locatie:")
        put_code(os.path.abspath(output_path))
        
    except FileNotFoundError as e:
        put_error(f"Fout: Sjabloonbestand niet gevonden. Controleer of het sjabloon bestaat.")
        put_text(f"Details: {str(e)}")
    except PermissionError as e:
        put_error(f"Fout: Toegang geweigerd bij het schrijven van uitvoerbestand.")
        put_text(f"Details: {str(e)}")
        put_text("Zorg ervoor dat u schrijfrechten heeft voor de uitvoermap en dat het bestand niet open is in een ander programma.")
    except Exception as e:
        put_error(f"Fout bij het genereren van Excel-bestand: {str(e)}")
    
    # Process completed
    set_processbar('process_bar', 1)

def main():
    """Main application flow."""
    try:
        ui_header()
        
        # Step 1: File Upload
        df_aanzien, df_gebruik = ui_file_upload()
        if df_aanzien is None or df_gebruik is None:
            put_text("Probeer het opnieuw met geldige CSV-bestanden.")
            return
        
        # Initialize KRO Tree
        try:
            tree = KRO_Tree(df_aanzien, df_gebruik)
        except Exception as e:
            put_error(f"Fout bij het initialiseren van de gegevensverwerker: {str(e)}")
            put_text("Er kan een probleem zijn met de structuur van uw CSV-bestanden.")
            return
        
        # Step 2: Filter Selection
        try:
            selected_filters = ui_filter_selection()
            if not selected_filters:
                put_warning("Er zijn geen filters geselecteerd. De uitvoer kan leeg zijn.")
        except Exception as e:
            put_error(f"Fout tijdens filterselectie: {str(e)}")
            return
        
        # Step 3: Export Options
        try:
            export_options = ui_export_options()
        except Exception as e:
            put_error(f"Fout bij het configureren van uitvoeropties: {str(e)}")
            return
        
        # Step 4: Processing and Export
        ui_process_and_export(tree, selected_filters, export_options)
        
        # Completion
        put_markdown("## Verwerking Voltooid")
        put_text("U kunt dit venster nu sluiten of een andere set bestanden verwerken.")
        put_button("Nieuwe Bestanden Verwerken", onclick=lambda: run_js('window.location.reload()'))
        
    except Exception as e:
        put_error(f"Er is een onverwachte fout opgetreden: {str(e)}")
        put_html("""
        <div style="margin-top: 20px; padding: 15px; border: 1px solid #f8d7da; background-color: #f8d7da; color: #721c24; border-radius: 5px;">
            <h3>Foutdetails</h3>
            <p>De applicatie is op een onverwachte fout gestuit. Hier zijn enkele dingen die u kunt proberen:</p>
            <ul>
                <li>Controleer of uw invoerbestanden correct geformatteerde CSV-bestanden zijn</li>
                <li>Verifieer dat u lees-/schrijfrechten hebt voor de applicatiemap</li>
                <li>Herstart de applicatie en probeer het opnieuw</li>
            </ul>
        </div>
        """)

def setup_app_launcher():
    """Set up the application launcher with appropriate UI depending on environment."""
    parser = argparse.ArgumentParser(description="HUP Generator Tool")
    parser.add_argument("--port", type=int, default=8080, help="Port voor de webserver")
    parser.add_argument("--no-browser", action="store_true", help="Browser niet automatisch openen")
    parser.add_argument("--server", action="store_true", help="Als server draaien in plaats van standalone app")
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
                print(f"HUP Generator openen in uw webbrowser: {url}")
                webbrowser.open(url)
            
            threading.Thread(target=open_browser).start()
        
        # Print instructions to console for clarity
        print("="*50)
        print("HUP Generator Tool")
        print("="*50)
        print(f"De applicatie draait op: http://localhost:{args.port}")
        print("Als de browser niet automatisch opent, open dan handmatig de URL.")
        print("Druk op Ctrl+C om de applicatie af te sluiten.")
        print("="*50)
        
        # Start the pywebio server
        start_pywebio_server(main, port=args.port, debug=False)
    else:
        # We're running as a server
        print(f"HUP Generator server starten op poort {args.port}")
        start_server(main, port=args.port, debug=False)

if __name__ == "__main__":
    setup_app_launcher()
