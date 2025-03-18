#!/usr/bin/env python3
"""
Build script for the HUP Generator application.
Creates a standalone executable using PyInstaller.
"""

import os
import sys
import shutil
import subprocess
import platform
import argparse
from pathlib import Path

def build_executable(target_platform=None, clean=True):
    """
    Build the HUP Generator executable.
    
    Args:
        target_platform: Target platform ('macos' or 'windows')
        clean: Whether to clean previous build files
    """
    if not target_platform:
        target_platform = 'macos' if sys.platform == 'darwin' else 'windows'
    
    print(f"Building HUP Generator for platform: {target_platform}")
    print(f"Current system: {platform.system()} {platform.machine()}")
    
    # Create resources directory if it doesn't exist
    resources_dir = Path("resources")
    resources_dir.mkdir(exist_ok=True)
    
    # Copy template file to resources if it exists in HUP directory
    template_src = Path("HUP") / "origineel (niet aanpassen).xlsx"
    template_dst = resources_dir / "origineel (niet aanpassen).xlsx"
    
    if template_src.exists():
        print(f"Copying template from {template_src} to {template_dst}")
        shutil.copy2(template_src, template_dst)
    else:
        print(f"Warning: Template file not found at {template_src}")
        print("Please make sure the template exists before building.")
        return 1
    
    # Clean previous build if requested
    if clean:
        for dir_to_clean in ['build', 'dist']:
            if os.path.exists(dir_to_clean):
                print(f"Cleaning {dir_to_clean} directory...")
                shutil.rmtree(dir_to_clean)
    
    # Setup platform-specific configuration
    if target_platform == 'macos':
        # For macOS (including M1/ARM)
        data_arg = "--add-data=resources/*:resources"
        output_name = "HUP_Generator_macOS"
        icon_file = "app_icon.icns" if Path("app_icon.icns").exists() else None
    else:  # windows
        # For Windows builds
        data_arg = "--add-data=resources/*;resources"
        output_name = "HUP_Generator_Win64"
        icon_file = "app_icon.ico" if Path("app_icon.ico").exists() else None
        
        # Check if we're on macOS trying to build for Windows
        if sys.platform == 'darwin':
            print("Warning: Building Windows executables from macOS has limited support.")
            print("For best results, build the Windows version on a Windows system.")
            print("Continuing with best-effort build...")

    # Base PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        data_arg,
        f"--name={output_name}"
    ]
    
    # Add icon if available
    if icon_file:
        cmd.append(f"--icon={icon_file}")
    
    # Add hidden imports that might be needed
    cmd.extend(["--hidden-import=pandas", "--hidden-import=openpyxl"])
    
    # Add the main script
    cmd.append("app.py")
    
    print("Running PyInstaller with command:", " ".join(cmd))
    
    try:
        result = subprocess.run(cmd, check=True)
        print(f"Build completed for {target_platform}. Executable can be found in the dist directory.")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        return e.returncode

def main():
    """Main function to parse arguments and build executables."""
    parser = argparse.ArgumentParser(description="Build HUP Generator executable")
    parser.add_argument('--platform', choices=['macos', 'windows'], 
                        help="Target platform (default: current platform)")
    parser.add_argument('--no-clean', action='store_true', help="Don't clean previous build files")
    
    args = parser.parse_args()
    
    return build_executable(args.platform, not args.no_clean)

if __name__ == "__main__":
    sys.exit(main())
