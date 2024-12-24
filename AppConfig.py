import os
import sys

from status_updater import StatusUpdater

class AppConfig:
    _instance = None

    def __new__(cls, base_path=None):
        if not cls._instance:
            cls._instance = super(AppConfig, cls).__new__(cls)
            cls._instance._initialize(base_path)
        return cls._instance

    def _initialize(self, base_path):
        if not hasattr(self, "base_path"):  # Prevent reinitialization
            # Determine the base path based on the environment
            self.base_path = base_path or self.get_default_base_path()
            self.miniconda_path = os.path.join(self.base_path, "miniconda3")
            self.env_path = os.path.join(self.base_path, "env")  # Open WebUI environment
            self.env_pipelines_path = os.path.join(self.base_path, "env_pipelines")  # Pipelines environment
            self.pipelines_repo_path = os.path.join(self.base_path, "pipelines")
            self.conda_exe = os.path.join(self.miniconda_path, "Scripts", "conda.exe")

    @staticmethod
    def get_default_base_path():
        """
        Determines the default base path:
        - On Windows: Uses USERPROFILE to store in `OpenWebUI` under the user's home directory.
        - On other OS: Uses the current working directory or a fallback directory.
        """
        if os.name == 'nt':  # Windows
            return os.path.join(os.environ['USERPROFILE'], 'OpenWebUI')
        else:  # Unix-like systems
            if getattr(sys, 'frozen', False):  # Running as a PyInstaller executable
                return os.path.dirname(sys.executable)
            else:  # Running as a Python script
                return os.path.abspath(os.getcwd())

    @property
    def is_miniconda_installed(self):
        """
        Checks if Miniconda is installed by verifying the presence of conda.exe.
        """
        return os.path.exists(self.conda_exe)

    @property
    def has_openwebui_env(self):
        """
        Checks if the Open WebUI environment is set up.
        Ensures Miniconda is installed first.
        """
        if not self.is_miniconda_installed:
            print("Miniconda is not installed.")
            return False
        if not os.path.exists(self.env_path):
            print("Open WebUI environment is not set up.")
            return False
        return True

    @property
    def has_pipelines_env(self):
        """
        Checks if the Pipelines environment is set up.
        Ensures Miniconda is installed first.
        """
        if not self.is_miniconda_installed:
            print("Miniconda is not installed.")
            return False
        if not os.path.exists(self.env_pipelines_path):
            print("Pipelines environment is not set up.")
            return False
        return True

    @property
    def status_display(self):
        """Get or create the StatusDisplay."""
        if self._status_display is None:
            raise AttributeError("StatusDisplay has not been initialized.")
        return self._status_display

    @status_display.setter
    def status_display(self, display):
        """Set the StatusDisplay and initialize StatusUpdater."""
        self._status_display = display
        components = display.get_components()
        self._status_updater = StatusUpdater(*components)

    @property
    def status_updater(self):
        """Access the StatusUpdater."""
        if self._status_updater is None:
            raise AttributeError("StatusUpdater has not been initialized.")
        return self._status_updater

    def start_spinner(self):
        """Start the spinner."""
        if hasattr(self.status_display, "spinner"):
            self.status_display.spinner.start()

    def stop_spinner(self):
        """Stop the spinner."""
        if hasattr(self.status_display, "spinner"):
            self.status_display.spinner.stop()


    def __str__(self):
        """
        String representation for debugging.
        """
        return (
            f"Base Path: {self.base_path}\n"
            f"Miniconda Path: {self.miniconda_path}\n"
            f"Environment Path: {self.env_path}\n"
            f"Pipelines Environment Path: {self.env_pipelines_path}\n"
            f"Pipelines Repo Path: {self.pipelines_repo_path}\n"
            f"Conda Executable: {self.conda_exe}\n"
        )
