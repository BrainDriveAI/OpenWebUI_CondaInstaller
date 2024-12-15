import subprocess
import os
import threading
from base_installer import BaseInstaller


class OpenWebUIInstaller(BaseInstaller):
    def __init__(self, status_updater=None):
        super().__init__("Open WebUI", status_updater)
        self.env_path = os.path.join(self.config.base_path, "env")
        self.conda_exe = self.config.conda_exe


    def check_installed(self):
        """
        Check if Open WebUI is installed in the environment.
        Returns:
            bool: True if installed, False otherwise.
        """
        # Check if the environment is set up
        if not os.path.exists(self.env_path):
            print("Conda environment for Open WebUI is not set up.")
            return False

        # Check if open-webui is installed using pip show
        pip_show_cmd = [
            self.conda_exe,
            "run",
            "--prefix", self.env_path,
            "pip", "show", "open-webui"
        ]
        try:
            self.run_command(pip_show_cmd)
            print("Open WebUI is installed.")
            return True
        except subprocess.CalledProcessError:
            print("Open WebUI is not installed.")
        except FileNotFoundError:
            print("Conda executable not found. Ensure Miniconda is installed.")

        return False

    def install(self):
        """
        Install Open WebUI into the Conda environment.
        """
        self.status_updater.update_status(
            "Step: [1/2] Open WebUI Install, this could easily take 10-20 minutes depending on your computer.",
            "Installing Open WebUI using Pip",
            50,
        )

        # Ensure the environment is set up
        if not os.path.exists(self.env_path):
            self.setup_environment("env")

        print("Installing Open WebUI...")
    
        # Use run_command for consistent subprocess behavior
        self.run_command([
            self.conda_exe,
            "run",
            "--prefix", self.env_path,
            "pip",
            "install",
            "open-webui"
        ])
        
        print("Open WebUI installation complete.")


    def check_requirements(self):
        """
        Ensure Conda is installed.
        """
        if not os.path.exists(self.conda_exe):
            raise RuntimeError("Conda is not installed. Please install Miniconda first.")
        return True

    def setup_environment(self, env_name):
        """
        Set up the Conda environment for Open WebUI.
        """
        self.status_updater.update_status(
            "Step: [1/2] Setting Up Environment...",
            "Creating a Conda environment for Open WebUI.",
            50,
        )
        
        if not os.path.exists(self.env_path):
            print(f"Setting up environment {env_name}...")
            
            # Use run_command for consistency
            self.run_command([
                self.conda_exe,
                "create",
                "--prefix",
                self.env_path,
                "python=3.11",
                "-y"
            ])
            
            print(f"Environment {env_name} set up successfully.")
        
        self.status_updater.update_status(
            "Step: [2/2] Environment has been setup",
            "Created a Conda environment for Open WebUI.",
            100,
        )


    def update(self):
        """
        Update Open WebUI to the latest version.
        """
        try:
            # Update Open WebUI using pip via conda run
            pip_update_cmd = [
                self.conda_exe,
                "run",
                "--prefix", self.env_path,
                "pip", "install", "--upgrade", "open-webui"
            ]
            self.run_command(pip_update_cmd)
            print("Open WebUI updated successfully.")
        except Exception as e:
            print(f"Error updating Open WebUI: {e}")


    def run_command(self, cmd_list):
        """
        Runs a command and logs output in real-time.
        """
        try:
            command_str = ' '.join(cmd_list)
            print(f"Running command: {command_str}")

            # Prevent console window from popping up on Windows
            CREATE_NO_WINDOW = 0x08000000

            # Start the process
            process = subprocess.Popen(
                cmd_list,
                # stdout=subprocess.PIPE,
                # stderr=subprocess.STDOUT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,                
                text=True,
                creationflags=CREATE_NO_WINDOW,
                encoding="utf-8"
            )

            # Read and log output line by line
            # for line in process.stdout:
            #     print(line.strip())  # Real-time logging

            process.wait()

            # Raise an error if the process fails
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, cmd_list)

        except subprocess.CalledProcessError as e:
            print(f"Command failed with return code {e.returncode}")
            raise
    def check_update(self, callback=None):
        """
        Check if an update is available for Open WebUI.
        Runs the process in a separate thread if a callback is provided.
        :param callback: Optional callback function to receive the result (True/False).
        """
        def update_task():
            print("Checking for updates...")
            try:
                result = subprocess.run(
                    [self.conda_exe, "run", "--prefix", self.env_path, "pip", "list", "--outdated"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True,
                )

                # Parse the output to check for the package name
                update_available = "open-webui" in result.stdout
                print("An update is available for Open WebUI." if update_available else "Open WebUI is up to date.")
                
                # Pass the result to the callback if provided
                if callback:
                    callback(update_available)

            except subprocess.CalledProcessError as e:
                print(f"Error checking for updates: {e}")
                if callback:
                    callback(False)  # Assume no update in case of error

        # Run the update task in a separate thread
        threading.Thread(target=update_task, daemon=True).start()

