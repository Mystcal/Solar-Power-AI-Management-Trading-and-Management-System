import subprocess
import sys

def install(package):
    """
    Description: This function installs the required packages.
    Input: package (str) - The name of the package to be installed.
    Output: None
    """
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    required_packages = ['requests', 'pandas', 'xml.etree.ElementTree', 'streamlit', 'matplotlib']
    for package in required_packages:
        try:
            __import__(package)
            print(f"{package} is already installed.")
        except ImportError:
            print(f"Installing {package}...")
            install(package)
            print(f"{package} has been successfully installed.")