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
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=CREATE_NO_WINDOW,
                encoding="utf-8"
            )

            # Capture the output
            stdout, stderr = process.communicate()

            # Raise an error if the process fails
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, cmd_list, output=stdout, stderr=stderr)

            return stdout, stderr  # Ensure (stdout, stderr) is always returned

        except subprocess.CalledProcessError as e:
            print(f"Command failed with return code {e.returncode}")
            print(f"Error output: {e.stderr}")
            raise
        except Exception as e:
            print(f"Unexpected error while running command: {e}")
            raise


    def check_update(self, callback=None):
        """
        Check if an update is available for Open WebUI.
        Runs the process in a separate thread if a callback is provided.
        :param callback: Optional callback function to receive the result (True/False).
        """
        def update_task():
            print("Checking for updates...")
            update_available = False
            try:
                # Check if open-webui is installed using pip show
                stdout, _ = self.run_command(
                    [self.conda_exe, "run", "--prefix", self.env_path, "pip", "show", "open-webui"]
                )

                # Parse the installed version of open-webui
                installed_version = None
                for line in stdout.splitlines():
                    if line.startswith("Version:"):
                        installed_version = line.split("Version:")[1].strip()
                        break

                if installed_version:
                    print(f"Installed open-webui version: {installed_version}")

                    # Fetch the latest version from PyPI
                    import urllib.request
                    import json
                    try:
                        with urllib.request.urlopen("https://pypi.org/pypi/open-webui/json") as response:
                            data = json.loads(response.read().decode())
                            latest_version = data["info"]["version"]
                            print(f"Latest open-webui version: {latest_version}")

                        # Compare installed and latest versions
                        if installed_version != latest_version:
                            print("An update is available for open-webui.")
                            update_available = True
                        else:
                            print("open-webui is up to date.")
                            update_available = False
                    except Exception as e:
                        print(f"Error fetching latest open-webui version: {e}")
                else:
                    print("open-webui is not installed.")
                    update_available = False

            except subprocess.CalledProcessError:
                print("open-webui is not installed.")
            except FileNotFoundError:
                print("Error: Could not find conda executable or the environment is not properly set up.")

            # Pass the result to the callback if provided
            if callback:
                callback(update_available)

        # Run the update task in a separate thread
        threading.Thread(target=update_task, daemon=True).start()


