import os
import subprocess
from dulwich import porcelain
from base_installer import BaseInstaller

class PipelinesInstaller(BaseInstaller):
    def __init__(self, status_updater=None):
        super().__init__("Pipelines", status_updater)
        self.env_pipelines_path = os.path.join(self.config.base_path, "env_pipelines")
        self.pipelines_repo_path = os.path.join(self.config.base_path, "pipelines")
        self.pipelines_repo_url = "https://github.com/open-webui/pipelines.git"
        self.conda_exe = self.config.conda_exe        

    def check_installed(self):
        """
        Check if the pipelines are installed by verifying both the environment and the repository.
        """
        return os.path.exists(self.env_pipelines_path) and os.path.exists(self.pipelines_repo_path)

    def start_pipelines(self):
        """
        Starts the pipelines process and writes the PID to a file.
        """
        try:
            # Path to python in the pipelines environment
            python_executable = os.path.join(self.env_pipelines_path, "python.exe")
            pipeline_cmd = [
                python_executable,
                "-m", "uvicorn",
                "main:app",
                "--host", "0.0.0.0",
                "--port", "9099",
                "--forwarded-allow-ips", "0.0.0.0"
            ]

            # Working directory for the pipelines repository
            cwd = self.config.pipelines_repo_path

            # Windows-specific flag to suppress console window
            CREATE_NO_WINDOW = 0x08000000

            # Start the process
            process = subprocess.Popen(
                pipeline_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=CREATE_NO_WINDOW,
                cwd=cwd,
                env=os.environ.copy()  # Inherit environment variables
            )

            # Write the PID to a file
            pid_file = os.path.join(self.config.base_path, "pipelines.pid")
            with open(pid_file, "w") as f:
                f.write(str(process.pid))

            print(f"Pipelines process started with PID {process.pid}.")

            return process.pid  # Return the PID for further use if needed

        except Exception as e:
            print(f"Failed to start pipelines process: {e}")
            raise



    def find_python_executable(self):
        """Attempt to find the python executable in the conda environment."""
        possible_locations = [
            os.path.join(self.env_pipelines_path, "python.exe"),
            os.path.join(self.env_pipelines_path, "python3.exe"),
            os.path.join(self.env_pipelines_path, "Scripts", "python.exe"),
            os.path.join(self.env_pipelines_path, "bin", "python"),
            os.path.join(self.env_pipelines_path, "bin", "python3")
        ]
    def check_for_updates(self):
        """
        Checks if there are updates available for the pipelines repository.
        :return: True if updates are available, False otherwise.
        """
        try:
            # Ensure the repository exists
            if not os.path.exists(self.pipelines_repo_path):
                raise RuntimeError("Pipelines repository is not cloned. Please install pipelines first.")

            print("Checking for updates in the pipelines repository...")

            # Fetch changes from the remote repository
            with porcelain.open_repo_closing(self.pipelines_repo_path) as repo:
                remote_refs = porcelain.fetch(repo, self.pipelines_repo_url)
            
            # Compare local HEAD with the fetched remote HEAD
            local_head = repo.head().decode("utf-8")
            remote_head = remote_refs[b"HEAD"].decode("utf-8")

            if local_head != remote_head:
                print("Updates are available for the pipelines repository.")
                return True
            else:
                print("Pipelines repository is up-to-date.")
                return False
        except Exception as e:
            print(f"Error checking for updates: {e}")
            raise
    def install(self):
        """
        Install pipelines by setting up the environment and cloning the repository.
        """
        print(f"Installing {self.name}...")

        try:
            # Step 1: Clone the repository
            if not os.path.exists(self.pipelines_repo_path):
                if self.status_updater:
                    self.status_updater.update_status(
                        "Step: [4/6] Pipelines Cloning...",
                        "Cloning the Pipelines repository, this could take 5-7 minutes depending on your system",
                        50,
                    )

                print(f"[4/6] Cloning pipelines repository from {self.pipelines_repo_url}...")

                try:
                    porcelain.clone(self.pipelines_repo_url, self.pipelines_repo_path)
                    print("Pipelines repository cloned successfully.")
                except Exception as e:
                    raise RuntimeError(f"Failed to clone pipelines repository: {e}")
            else:
                print("Pipelines repository already exists. Skipping cloning.")

            # Step 2: Install dependencies using the previously set up Conda environment
            requirements_file = os.path.join(self.pipelines_repo_path, "requirements.txt")
            if os.path.exists(requirements_file):
                print(f"[5/6] Installing dependencies from {requirements_file}...")
                if self.status_updater:
                    self.status_updater.update_status(
                        "Step: [5/6] Pipelines Installing Dependencies...",
                        "Installing requirements, this could take 5-7 minutes depending on your system",
                        75,
                    )
                try:
                    self._install_dependencies(requirements_file)
                except Exception as e:
                    raise RuntimeError(f"Failed to install dependencies: {e}")
            else:
                print("[6/6] No requirements.txt found. Skipping dependency installation.")

            # Step 3: Finalize installation
            print(f"[6/6] {self.name} installation complete.")
            if self.status_updater:
                self.status_updater.update_status(
                    "Step: [6/6] Pipelines Install Complete.",
                    "Pipelines installed successfully.",
                    100,
                )

        except Exception as e:
            print(f"Error during installation: {e}")
            raise RuntimeError(f"{self.name} installation failed.") from e


    def check_requirements(self):
        """
        Ensure that Miniconda is installed and accessible.
        """
        if not os.path.exists(self.conda_exe):
            raise RuntimeError("Conda executable not found. Please install Miniconda first.")
        return True

    def setup_environment(self, env_name):
        """
        Set up the Conda environment for pipelines.
        """
        if os.path.exists(self.env_pipelines_path):
            self.status_updater.update_status(
                "Pipelines Environment Setup",
                f"Environment '{env_name}' already exists. Skipping setup.",
                100,
            )
            print(f"Environment {env_name} already exists. Skipping setup.")
            return

        self.status_updater.update_status(
            "PipelinesEnvironment Setup",
            f"Setting up environment '{env_name}'. This may take a few minutes.",
            0,
        )
        print(f"Setting up environment {env_name}...")

        try:
            self.run_command([
                self.conda_exe,
                "create",
                "--prefix", self.env_pipelines_path,
                "python=3.11",
                "git",
                "-y",
            ])
            self.status_updater.update_status(
                "Pipelines Environment Setup Complete",
                f"Environment '{env_name}' set up successfully.",
                100,
            )
            print(f"Environment {env_name} set up successfully.")
        except Exception as e:
            self.status_updater.update_status(
                "Environment Setup Failed",
                f"Failed to set up environment '{env_name}': {e}",
                0,
            )
            print(f"Failed to set up environment {env_name}: {e}")
            raise



    def _install_dependencies(self, requirements_file):
        """
        Install dependencies for pipelines using the requirements.txt file.
        """
        if not os.path.exists(requirements_file):
            raise FileNotFoundError(f"Requirements file not found: {requirements_file}")

        print("Installing dependencies from requirements.txt...")
        python_executable = self._find_python_executable()

        # self.status_updater.update_status(
        #     "Step: [1/2] Pipelines Installing Dependencies...",
        #     "Installing requirements, this could take 5-7 minutes depending on your system",
        #     50,
        # )

        # Command to install dependencies
        pip_install_cmd = [
            python_executable,
            "-m", "pip",
            "install",
            "-r", requirements_file
        ]

        try:
            stdout, stderr = self.run_command(pip_install_cmd)
            # self.status_updater.update_status(
            #     "Step: [2/2] Pipelines Dependencies Installed.",
            #     "Dependencies installed successfully.",
            #     100,
            # )
            print("Dependencies installed successfully.")

        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies: {' '.join(e.cmd)}, Return Code: {e.returncode}")
            raise


    def update(self):
        """
        Update the pipelines repository and dependencies.
        """
        print(f"Updating {self.name}...")

        try:
            # Step 1: Ensure the repository is cloned
            if not os.path.exists(self.pipelines_repo_path):
                raise RuntimeError("Pipelines repository is not cloned. Please install pipelines first.")

            # Step 2: Pull the latest changes
            print(f"[1/2] Pulling the latest changes from {self.pipelines_repo_url}...")
            try:
                with porcelain.open_repo_closing(self.pipelines_repo_path) as repo:
                    porcelain.pull(repo, self.pipelines_repo_url)
                print("Pipelines repository updated successfully.")
            except Exception as e:
                raise RuntimeError(f"Failed to update pipelines repository: {e}")

            # Step 3: Install or update dependencies
            requirements_file = os.path.join(self.pipelines_repo_path, "requirements.txt")
            if os.path.exists(requirements_file):
                print(f"[2/2] Installing or updating dependencies from {requirements_file}...")
                try:
                    self._install_dependencies(requirements_file)
                except Exception as e:
                    raise RuntimeError(f"Failed to update dependencies: {e}")
            else:
                print("[2/2] No requirements.txt found. Skipping dependency update.")

            # Step 4: Finalize the update process
            print(f"{self.name} update complete.")

        except Exception as e:
            print(f"Error during update: {e}")
            raise RuntimeError(f"{self.name} update failed.") from e


    def _find_python_executable(self):
        """
        Find the Python executable within the pipelines environment.
        """
        possible_locations = [
            os.path.join(self.env_pipelines_path, "python.exe"),
            os.path.join(self.env_pipelines_path, "bin", "python"),
            os.path.join(self.env_pipelines_path, "Scripts", "python.exe"),
        ]

        for path in possible_locations:
            if os.path.exists(path):
                return path

        raise FileNotFoundError(
            "Could not locate the Python executable in the environment. "
            f"Tried locations: {possible_locations}"
        )

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

            process = subprocess.Popen(
                cmd_list,
                stdout=subprocess.PIPE if capture_output else None,
                stderr=subprocess.PIPE if capture_output else None,
                text=True,
                creationflags=CREATE_NO_WINDOW,
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