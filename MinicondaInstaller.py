import os
import urllib.request
import subprocess
from logger import Logger

class MinicondaInstaller:
    def __init__(self):
        """Initialize MinicondaInstaller with user directory paths."""
        # Use the user's home directory for installation
        self.base_path = os.path.join(os.environ['USERPROFILE'], 'OpenWebUI')
        self.miniconda_path = os.path.normpath(os.path.join(self.base_path, "miniconda3"))
        self.installer_path = os.path.join(self.base_path, "MinicondaInstaller.exe")
        self.miniconda_url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"
        self.conda_bat_path = os.path.join(self.miniconda_path, "Scripts", "conda.exe")

    def ensure_directories(self):
        """Ensure base directory and Miniconda directory structure exist."""
        if not os.path.exists(self.base_path):
            Logger.log(f"Creating base directory: {self.base_path}")
            os.makedirs(self.base_path, exist_ok=True)

    def verify_conda(self):
        """Verify if Conda is installed by checking for conda.exe."""
        return os.path.exists(self.conda_bat_path)

    def install_miniconda(self):
        """Download and install Miniconda."""
        try:
            # Ensure required directories exist
            self.ensure_directories()

            # Download Miniconda installer if not already downloaded
            if not os.path.exists(self.installer_path):
                Logger.log(f"Downloading Miniconda installer to {self.installer_path}.")
                self.download_installer()
            else:
                Logger.log(f"Miniconda installer already exists at {self.installer_path}.")

            # Run the Miniconda installer silently and wait for it to complete
            Logger.log("Running Miniconda installer.")
            result = subprocess.run(
                [
                    self.installer_path,
                    "/S",
                    "/InstallationType=JustMe",
                    "/AddToPath=0",
                    "/RegisterPython=0",
                    f"/D={self.miniconda_path}",  # No quotes, placed last
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            Logger.log(f"Installer command: {' '.join(result.args)}")
            Logger.log(f"Miniconda installation complete. Output:\n{result.stdout}")
        except subprocess.CalledProcessError as e:
            Logger.log(f"Miniconda installation failed. Return code: {e.returncode}")
            Logger.log(f"Standard output:\n{e.stdout}")
            Logger.log(f"Standard error:\n{e.stderr}")
            # Also, print to the GUI output
            print(f"Installation failed with return code {e.returncode}")
            print(f"Standard output:\n{e.stdout}")
            print(f"Standard error:\n{e.stderr}")
            raise

    def download_installer(self):
        """Download the Miniconda installer."""
        try:
            urllib.request.urlretrieve(self.miniconda_url, self.installer_path)
            Logger.log("Miniconda installer downloaded successfully.")
        except Exception as e:
            Logger.log(f"Failed to download Miniconda installer: {e}")
            raise

    def ensure_miniconda_installed(self):
        """Ensure Miniconda is installed and ready to use."""
        if self.verify_conda():
            Logger.log("Conda is already installed and verified.")
        else:
            Logger.log("Conda not found. Proceeding with installation.")
            self.install_miniconda()

        if not self.verify_conda():
            raise RuntimeError("Miniconda installation failed. Conda is not available.")
