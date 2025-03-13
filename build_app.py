import PyInstaller.__main__
import os
import shutil

# Define the name of the application
app_name = "HUP_Generator"

# Create a spec file for PyInstaller
PyInstaller.__main__.run([
    'app.py',
    '--name=%s' % app_name,
    '--onefile',
    '--windowed',
    '--add-data=%s' % os.path.join('HUP', 'origineel (niet aanpassen).xlsx') + os.pathsep + os.path.join('HUP'),
    '--hidden-import=pandas',
    '--hidden-import=pandas._libs.tslibs.timedeltas',
    '--hidden-import=openpyxl',
    '--hidden-import=flask',
    '--hidden-import=pywebio',
    '--icon=%s' % 'icon.ico' if os.path.exists('icon.ico') else None,
    '--clean',
])

# Create necessary directories in the dist folder
data_dir = os.path.join('dist', 'data')
hup_dir = os.path.join('dist', 'HUP')

for directory in [data_dir, hup_dir]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Copy README and create a basic instruction document
readme_content = """
HUP Generator Tool
=================

Instructions:
1. Run the HUP_Generator executable
2. A browser window will open automatically with the application
3. Upload your KRO data files through the web interface
4. Select the desired filters and options
5. Generate your HUP Excel file

Output files will be saved in the 'HUP' folder next to the application.

For more detailed information, please see the full README.md file.
"""

with open(os.path.join('dist', 'Instructions.txt'), 'w') as f:
    f.write(readme_content)

# Copy the README if it exists
if os.path.exists('README.md'):
    shutil.copy('README.md', os.path.join('dist', 'README.md'))

print(f"Application built successfully as {app_name}")
print("You can find it in the 'dist' directory")
print("\nThe following files and directories have been created:")
print(f" - {app_name}.exe: The executable application")
print(" - data: Directory for CSV data files")
print(" - HUP: Directory for template and output files")
print(" - Instructions.txt: Basic usage instructions")
