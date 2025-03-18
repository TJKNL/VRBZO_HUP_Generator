# HUP Generator Tool

Een tool voor het genereren van Handhavings Uitvoerings Programma (HUP) bestanden op basis van KRO-gegevens.

## Features

- Web-based user interface for easy data upload and configuration
- Automatic CSV delimiter detection
- Predefined filters for different building types
- Excel export with customizable options
- Standalone executable that doesn't require Python installation

## Vereisten voor ontwikkeling

- Python 3.8+
- Externe bibliotheken (zie `requirements.txt`)

## Installatie (ontwikkeling)

1. Clone de repository
2. Installeer de vereiste packages:

```bash
pip install -r requirements.txt
```

3. Zorg dat het Excel-sjabloon aanwezig is in de `HUP` map:
   - Bestandsnaam: `origineel (niet aanpassen).xlsx`

## Gebruik (ontwikkeling)

Start de applicatie vanuit de hoofdmap:

```bash
python app.py
```

## Maken van een standalone executable

Je kunt een standalone executable maken met behulp van PyInstaller:

```bash
# Standaard build (64-bit op moderne systemen)
python build_app.py

# Specifieke architectuur bouwen (alleen Windows)
python build_app.py --arch x64  # 64-bit executable
python build_app.py --arch x86  # 32-bit executable

# Beide architecturen bouwen (alleen Windows)
python build_app.py --arch both
```

Voor het bouwen van een 32-bit (x86) versie is een 32-bit Python-installatie nodig.

Dit creëert een executable in de `dist` map die zonder Python-installatie kan worden uitgevoerd.

## Cross-Platform Builds

### Building on M1 Mac

```bash
# Build for macOS (default)
python build_app.py

# Attempt best-effort Windows build (limited support)
python build_app.py --platform windows
```

⚠️ **Note about Windows builds**: Building Windows executables from macOS has limitations:

1. For the most reliable Windows build, use a Windows system or VM.
2. Building from Mac M1 for Windows will attempt a best-effort build, but:
   - The executable may not include all required dependencies
   - It may not work properly on all Windows systems

For production Windows builds, consider:
- Using a Windows virtual machine
- Setting up a CI/CD pipeline on GitHub Actions with Windows runners
- Using a Windows machine for the final build

## Usage

1. **Upload Data Files**:
   - Upload de KRO-gebruik CSV file
   - Upload de KRO-aanzien CSV file

2. **Select Filters**:
   - Kies welke filters je wilt toepassen

3. **Configure Output**:
   - Selecteer of je het ingebouwde Excel-sjabloon wilt gebruiken of een aangepast sjabloon wilt uploaden
   - Kies extra opties zoals het verwijderen van items zonder namen

4. **Generate Output**:
   - De applicatie verwerkt de gegevens en genereert een Excel-bestand
   - De locatie van het uitvoerbestand wordt weergegeven

## Project Structure

- `app.py`: Hoofd-applicatiecode met UI
- `data_management.py`: Functies voor gegevensbeheer en filtering
- `classes.py`: Klasse-definities voor het gegevensmodel
- `build_app.py`: Script om de standalone executable te maken
- `HUP/`: Directory met Excel-sjablonen

## License

[Insert License Information]
