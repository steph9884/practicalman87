#!/usr/bin/env python3
"""
Build script for creating executables from the IP to Website converter applications.
Uses PyInstaller to create standalone executables.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{description}...")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print("✓ Success")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        if e.stdout:
            print(f"Stdout: {e.stdout}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return False


def check_pyinstaller():
    """Check if PyInstaller is installed."""
    try:
        subprocess.run(["pyinstaller", "--version"], 
                      capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    
    if not run_command("pip install -r requirements.txt", 
                      "Installing Python dependencies"):
        return False
    
    return True


def build_cli_executable():
    """Build the CLI executable."""
    print("\n" + "="*50)
    print("Building CLI Executable")
    print("="*50)
    
    # PyInstaller command for CLI
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--name=ip-to-website-cli",     # Output name
        "--console",                    # Console application
        "--clean",                      # Clean cache
        "ip_to_website_cli.py"
    ]
    
    return run_command(" ".join(cmd), "Building CLI executable")


def build_gui_executable():
    """Build the GUI executable."""
    print("\n" + "="*50)
    print("Building GUI Executable")
    print("="*50)
    
    # PyInstaller command for GUI
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--name=ip-to-website-gui",     # Output name
        "--windowed",                   # No console window
        "--clean",                      # Clean cache
        "ip_to_website_gui.py"
    ]
    
    return run_command(" ".join(cmd), "Building GUI executable")


def create_dist_structure():
    """Create a clean distribution structure."""
    print("\n" + "="*50)
    print("Creating Distribution Package")
    print("="*50)
    
    # Create dist directory if it doesn't exist
    dist_dir = Path("dist")
    if not dist_dir.exists():
        dist_dir.mkdir()
    
    # Create release directory
    release_dir = Path("release")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir()
    
    # Copy executables
    files_to_copy = []
    
    cli_exe = dist_dir / "ip-to-website-cli"
    gui_exe = dist_dir / "ip-to-website-gui"
    
    # Check for Windows executables
    if sys.platform == "win32":
        cli_exe = dist_dir / "ip-to-website-cli.exe"
        gui_exe = dist_dir / "ip-to-website-gui.exe"
    
    if cli_exe.exists():
        files_to_copy.append(("CLI executable", cli_exe))
    
    if gui_exe.exists():
        files_to_copy.append(("GUI executable", gui_exe))
    
    # Copy files
    for description, source in files_to_copy:
        dest = release_dir / source.name
        try:
            shutil.copy2(source, dest)
            print(f"✓ Copied {description}: {dest}")
        except Exception as e:
            print(f"✗ Failed to copy {description}: {e}")
    
    # Copy additional files
    additional_files = [
        ("README.md", "Documentation"),
        ("requirements.txt", "Dependencies list"),
        ("sample_ips.txt", "Sample IP addresses file")
    ]
    
    for filename, description in additional_files:
        source = Path(filename)
        if source.exists():
            dest = release_dir / filename
            try:
                shutil.copy2(source, dest)
                print(f"✓ Copied {description}: {dest}")
            except Exception as e:
                print(f"✗ Failed to copy {description}: {e}")
    
    print(f"\n✓ Distribution package created in: {release_dir.absolute()}")
    return True


def create_sample_file():
    """Create a sample IP addresses file."""
    sample_content = """# Sample IP addresses for testing
# One IP per line, comments start with #

8.8.8.8
1.1.1.1
208.67.222.222
9.9.9.9
8.8.4.4
1.0.0.1
"""
    
    try:
        with open("sample_ips.txt", "w") as f:
            f.write(sample_content)
        print("✓ Created sample_ips.txt")
        return True
    except Exception as e:
        print(f"✗ Failed to create sample file: {e}")
        return False


def main():
    """Main build function."""
    print("IP to Website Converter - Build Script")
    print("="*50)
    
    # Check if we're in the right directory
    if not Path("ip_to_website_cli.py").exists():
        print("✗ Error: ip_to_website_cli.py not found in current directory")
        print("Please run this script from the project root directory")
        sys.exit(1)
    
    # Check PyInstaller
    if not check_pyinstaller():
        print("PyInstaller not found. Installing dependencies...")
        if not install_dependencies():
            print("✗ Failed to install dependencies")
            sys.exit(1)
        
        # Check again
        if not check_pyinstaller():
            print("✗ PyInstaller still not available after installation")
            sys.exit(1)
    
    print("✓ PyInstaller is available")
    
    # Create sample file
    create_sample_file()
    
    # Build executables
    cli_success = build_cli_executable()
    gui_success = build_gui_executable()
    
    if not cli_success and not gui_success:
        print("\n✗ All builds failed")
        sys.exit(1)
    
    # Create distribution package
    create_dist_structure()
    
    # Summary
    print("\n" + "="*50)
    print("Build Summary")
    print("="*50)
    
    if cli_success:
        print("✓ CLI executable built successfully")
    else:
        print("✗ CLI executable build failed")
    
    if gui_success:
        print("✓ GUI executable built successfully")
    else:
        print("✗ GUI executable build failed")
    
    print(f"\n📁 Check the 'release' folder for your executables")
    print(f"🚀 Your IP to Website converter is ready to use!")
    
    # Usage instructions
    print("\n" + "="*50)
    print("Usage Instructions")
    print("="*50)
    print("CLI Tool:")
    print("  ./ip-to-website-cli 8.8.8.8")
    print("  ./ip-to-website-cli -v 1.1.1.1")
    print("  ./ip-to-website-cli -f sample_ips.txt")
    print("\nGUI Tool:")
    print("  Double-click ip-to-website-gui executable")
    print("  Or run: ./ip-to-website-gui")


if __name__ == "__main__":
    main()