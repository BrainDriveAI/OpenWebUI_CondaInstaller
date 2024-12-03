import os
import subprocess
import threading
from logger import Logger

class EnvironmentSetup:
    def __init__(self, base_path, miniconda_path):
        self.base_path = base_path
        self.miniconda_path = miniconda_path
        self.env_path = os.path.join(self.base_path, "env")
        self.conda_exe = os.path.join(miniconda_path, "Scripts", "conda.exe")

    def setup_environment(self, output_box):
        """Sets up Conda environment and installs Open WebUI."""
        try:
            # Create the environment using conda.exe
            create_env_cmd = [
                self.conda_exe,
                "create",
                "--prefix", self.env_path,
                "python=3.11",
                "-y"
            ]
            Logger.log(f"********************************************************************************")
            Logger.log(f"[3/4] This step can take up to 5 minutes depending on your computer")
            self.run_command(create_env_cmd, output_box)
            Logger.log("Environment setup complete.")
            Logger.log("This can take a while, please be patient")
            
            # Install open-webui using pip via conda run
            pip_install_cmd = [
                self.conda_exe,
                "run",
                "--prefix", self.env_path,
                "pip", "install", "open-webui"
            ]
            Logger.log(f"********************************************************************************")
            Logger.log(f"[4/4] This step can take up to 10 minutes depending on your computer")
            self.run_command(pip_install_cmd, output_box)
            Logger.log("Open WebUI setup complete.")
           
            # self.safe_output_insert(output_box, "Environment setup complete.\n")

        except Exception as e:
            Logger.log(f"Environment setup failed: {e}")
            self.safe_output_insert(output_box, f"Environment setup failed: {e}\n")
            raise

    def update_open_webui(self, output_box):
            """Updates Open WebUI to the latest version."""
            try:
                # Update open-webui using pip via conda run
                pip_update_cmd = [
                    self.conda_exe,
                    "run",
                    "--prefix", self.env_path,
                    "pip", "install", "--upgrade", "open-webui"
                ]
                self.run_command(pip_update_cmd, output_box)
                Logger.log("Open WebUI update complete.")
                self.safe_output_insert(output_box, "Open WebUI update complete.\n")
            except Exception as e:
                Logger.log(f"Open WebUI update failed: {e}")
                self.safe_output_insert(output_box, f"Open WebUI update failed: {e}\n")
                raise

    def run_command(self, cmd_list, output_box):
        """Runs a command and logs output."""
        try:
            command_str = ' '.join(cmd_list)
            Logger.log(f"Running command: {command_str}")
            # self.safe_output_insert(output_box, f"Running command: {command_str}\n")

            CREATE_NO_WINDOW = 0x08000000  # Prevents console window from popping up

            process = subprocess.Popen(
                cmd_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=CREATE_NO_WINDOW  # Prevent console window
            )

            # Read output line by line
            for line in process.stdout:
                # self.safe_output_insert(output_box, line)
                Logger.log(line.strip())

            process.wait()
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, cmd_list)
        except subprocess.CalledProcessError as e:
            Logger.log(f"Command failed with return code {e.returncode}")
            self.safe_output_insert(output_box, f"Command failed with return code {e.returncode}\n")
            raise

    def safe_output_insert(self, output_box, text):
        """Safely insert text into the output_box from a background thread."""
        output_box.after(0, self._insert_text, output_box, text)

    def _insert_text(self, output_box, text):
        """Helper method to insert text into the output_box."""
        output_box.insert("end", text)
        output_box.see("end")
