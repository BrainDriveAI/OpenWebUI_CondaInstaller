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
        Starts the pipelines process and returns the process object.
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

            # Create the process with no window creation (Windows specific)
            CREATE_NO_WINDOW = 0x08000000
            process = subprocess.Popen(
                pipeline_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=CREATE_NO_WINDOW,
                cwd=cwd
            )

            # Write the PID to a file
            pid_file = os.path.join(self.config.base_path, "pipelines.pid")
            with open(pid_file, "w") as f:
                f.write(str(process.pid))

            print(f"Pipelines process started with PID {process.pid}.")

            return process

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

    def install(self):
        """
        Install pipelines by setting up the environment and cloning the repository.
        """
        print(f"Installing {self.name}...")

        try:
            # Step 1: Clone the repository
            if not os.path.exists(self.pipelines_repo_path):
                print(f"[1/3] Cloning pipelines repository from {self.pipelines_repo_url}...")
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
                print(f"[2/3] Installing dependencies from {requirements_file}...")
                try:
                    self._install_dependencies(requirements_file)
                except Exception as e:
                    raise RuntimeError(f"Failed to install dependencies: {e}")
            else:
                print("[2/3] No requirements.txt found. Skipping dependency installation.")

            # Step 3: Finalize installation
            print(f"[3/3] {self.name} installation complete.")

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
            print(f"Environment {env_name} already exists. Skipping setup.")
            return

        print(f"Setting up environment {env_name}...")
        subprocess.run(
            [
                self.conda_exe,
                "create",
                "--prefix", self.env_pipelines_path,
                "python=3.11",
                "git",
                "-y",
            ],
            check=True,
        )
        print(f"Environment {env_name} set up successfully.")

    def _install_dependencies(self, requirements_file):
        """
        Install dependencies for pipelines using the requirements.txt file.

        :param requirements_file: Path to the requirements.txt file.
        """
        if not os.path.exists(requirements_file):
            raise FileNotFoundError(f"Requirements file not found: {requirements_file}")

        print("Installing dependencies from requirements.txt...")
        python_executable = self._find_python_executable()

        # Command to install dependencies
        pip_install_cmd = [
            python_executable,
            "-m", "pip",
            "install",
            "-r", requirements_file
        ]

        # Ensure no console windows pop up (Windows-specific)
        CREATE_NO_WINDOW = 0x08000000

        try:
            process = subprocess.Popen(
                pip_install_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=CREATE_NO_WINDOW,
                env=os.environ.copy()  # Inherit environment variables
            )

            stdout, stderr = process.communicate()

            # Log stdout
            if stdout:
                print(stdout)

            # Log stderr
            if stderr:
                print(stderr)

            # Check for process completion
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, pip_install_cmd)

            print("Dependencies installed successfully.")

        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies. Command: {' '.join(e.cmd)}, Return Code: {e.returncode}")
            raise
        except Exception as e:
            print(f"Unexpected error during dependencies installation: {e}")
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
