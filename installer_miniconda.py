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
        self.base_path = self.config.base_path

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
            self.config.status_updater.update_status(
                    "Step: [3/3] Miniconda Already Installed.",
                    "Miniconda is already installed. Skipping installation.",
                    100,
                )
            return

        try:

                # Ensure the base path exists
            base_path = os.path.dirname(self.installer_path)
            if not os.path.exists(base_path):
                os.makedirs(base_path)
            self.download_installer()

            # Run the installer silently
            self.config.status_updater.update_status(
                    "Step: [2/3] Installing Miniconda...",
                    "Running the Miniconda installer. Please wait.",
                    60,
                )
            self.run_command(
                [
                    self.installer_path,
                    "/S",
                    "/InstallationType=JustMe",
                    "/AddToPath=0",
                    "/RegisterPython=0",
                    f"/D={self.miniconda_path}",
                ],
                capture_output=False  # Optionally set to False if real-time logging is preferred

            )
            self.config.status_updater.update_status(
                    "Step: [3/3] Installation Complete.",
                    "Miniconda installation completed successfully.",
                    100,
                )
        except Exception as e:
            self.config.status_updater.update_status(
                    "Error: Installation Failed.",
                    f"An error occurred: {e}",
                    0,
                )


    def download_installer(self):
        """
        Download the Miniconda installer.
        """
        if not os.path.exists(self.installer_path):
            self.config.status_updater.update_status(
                    "Step: [1/3] Downloading Miniconda...",
                    "Downloading the Miniconda installer. This may take a few minutes.",
                    10,
                )
            urllib.request.urlretrieve(self.miniconda_url, self.installer_path)
            self.config.status_updater.update_status(
                    "Step: [1/3] Download Complete.",
                    "Miniconda installer downloaded successfully.",
                    30,
                )
        else:
            self.config.status_updater.update_status(
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

        try:
            self.run_command(create_cmd)
            print(f"Environment {env_name} set up successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to create environment {env_name}: {e}")
            raise



    def update(self):
        """
        Update Conda to the latest version.
        """
        if not self.check_installed():
            raise RuntimeError(f"{self.name} is not installed. Please install it first.")

        try:
            self.run_command([self.conda_exe, "update", "-n", "base", "-c", "defaults", "conda", "-y"])
            print(f"{self.name} updated successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to update Conda: {e}")
            raise



    def run_command(self, cmd_list, cwd=None, capture_output=True):
        """
        Runs a command and logs output in real-time. Prevents console windows from appearing.
        
        :param cmd_list: List of command and arguments to run.
        :param cwd: Directory to execute the command in.
        :param capture_output: Whether to capture and return stdout and stderr.
        :return: The process's stdout and stderr as a tuple (stdout, stderr).
        :raises: subprocess.CalledProcessError if the command fails.
        """
        try:
            command_str = ' '.join(cmd_list)
            print(f"Running command: {command_str}")

            # Windows-specific flag to suppress console window
            CREATE_NO_WINDOW = 0x08000000

            # Configure STARTUPINFO to hide the console window
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            process = subprocess.Popen(
                cmd_list,
                stdout=subprocess.PIPE if capture_output else None,
                stderr=subprocess.PIPE if capture_output else None,
                text=True,
                creationflags=CREATE_NO_WINDOW,
                startupinfo=startupinfo,
                cwd=cwd,
                env=os.environ.copy()  # Ensure environment variables are inherited
            )

            stdout, stderr = process.communicate()

            # Log output if capture_output is True
            if stdout:
                print(stdout)
            if stderr:
                print(stderr)

            # Check for errors and raise if process failed
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, cmd_list, output=stdout, stderr=stderr)

            return stdout, stderr
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {' '.join(e.cmd)}, Return Code: {e.returncode}")
            print(f"Error Output: {e.stderr}")
            raise
        except Exception as e:
            print(f"Unexpected error while running command: {e}")
            raise
