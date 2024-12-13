import os
import threading
import urllib.request
import subprocess
from base_installer import BaseInstaller

class MinicondaInstaller(BaseInstaller):
    def __init__(self, status_updater=None):
        super().__init__("Miniconda", status_updater)
        self.miniconda_path = self.config.miniconda_path
        self.installer_path = os.path.join(self.config.base_path, "MinicondaInstaller.exe")
        self.miniconda_url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe"
        self.conda_exe = self.config.conda_exe

    def check_installed(self):
        """
        Check if Miniconda is installed by verifying the presence of conda.exe.
        """
        return os.path.exists(self.conda_exe)

    def install(self):
        """
        Install Miniconda by downloading and running the installer sequentially.
        """
        if self.check_installed():
            if self.status_updater:
                self.status_updater.update_status(
                    "Step: [3/3] Miniconda Already Installed.",
                    "Miniconda is already installed. Skipping installation.",
                    100,
                )
            return

        try:
            self.download_installer()

            # Run the installer silently
            if self.status_updater:
                self.status_updater.update_status(
                    "Step: [2/3] Installing Miniconda...",
                    "Running the Miniconda installer. Please wait.",
                    60,
                )
            subprocess.run(
                [
                    self.installer_path,
                    "/S",
                    "/InstallationType=JustMe",
                    "/AddToPath=0",
                    "/RegisterPython=0",
                    f"/D={self.miniconda_path}",
                ],
                check=True,
            )
            if self.status_updater:
                self.status_updater.update_status(
                    "Step: [3/3] Installation Complete.",
                    "Miniconda installation completed successfully.",
                    100,
                )
        except Exception as e:
            if self.status_updater:
                self.status_updater.update_status(
                    "Error: Installation Failed.",
                    f"An error occurred: {e}",
                    0,
                )


    def download_installer(self):
        """
        Download the Miniconda installer.
        """
        if not os.path.exists(self.installer_path):
            if self.status_updater:
                self.status_updater.update_status(
                    "Step: [1/3] Downloading Miniconda...",
                    "Downloading the Miniconda installer. This may take a few minutes.",
                    10,
                )
            urllib.request.urlretrieve(self.miniconda_url, self.installer_path)
            if self.status_updater:
                self.status_updater.update_status(
                    "Step: [1/3] Download Complete.",
                    "Miniconda installer downloaded successfully.",
                    30,
                )
        else:
            if self.status_updater:
                self.status_updater.update_status(
                    "Step: [1/3] Installer Found.",
                    "Miniconda installer already exists. Skipping download.",
                    30,
                )

    def check_requirements(self):
        """
        Ensure the installation directory exists.
        """
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path, exist_ok=True)
            print(f"Created base path: {self.base_path}")
        return True

    def setup_environment(self, env_name, packages=None):
        """
        Set up a Conda environment with optional additional packages.
        
        :param env_name: The name of the environment to create.
        :param packages: A list of additional packages to install. Defaults to None.
        """
        if not self.check_installed():
            raise RuntimeError(f"{self.name} is not installed. Please install it first.")

        env_path = os.path.join(self.config.base_path, env_name)

        # Base command to create the environment
        create_cmd = [
            self.conda_exe,
            "create",
            "--prefix", env_path,
            "python=3.11"
        ]

        # Add additional packages to the command if provided
        if packages:
            create_cmd.extend(packages)

        # Add the '-y' flag to confirm environment creation
        create_cmd.append("-y")

        # Log the command for debugging
        print(f"Running command: {' '.join(create_cmd)}")

        # Execute the command
        try:
            subprocess.run(create_cmd, check=True)
            print(f"Environment {env_name} set up successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to create environment {env_name}: {e}")
            print(f"Command output: {e.output if hasattr(e, 'output') else 'No output available'}")
            raise



    def update(self):
        """
        Update Conda to the latest version.
        """
        if not self.check_installed():
            raise RuntimeError(f"{self.name} is not installed. Please install it first.")

        subprocess.run([self.conda_exe, "update", "-n", "base", "-c", "defaults", "conda", "-y"], check=True)
        print(f"{self.name} updated successfully.")
