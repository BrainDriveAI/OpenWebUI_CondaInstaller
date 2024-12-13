from abc import ABC, abstractmethod
from AppConfig import AppConfig 

class BaseInstaller(ABC):
    """
    Abstract base class for handling system installations and configurations.
    """

    def __init__(self, name, status_updater=None):
        self.name = name
        self.status_updater = status_updater
        self._is_installed = False
        self._has_env = False
        self.config = AppConfig()

    @property
    def is_installed(self):
        """
        Property to check if the system is installed.
        This should be overridden by subclasses with specific checks.
        """
        return self._is_installed

    @property
    def has_env(self):
        """
        Property to check if the required environment is set up.
        This should be overridden by subclasses with specific checks.
        """
        return self._has_env


    @abstractmethod
    def check_installed(self):
        """
        Check if the system is already installed.
        :return: Boolean indicating installation status.
        """
        pass

    @abstractmethod
    def install(self):
        """
        Install the system.
        """
        pass

    @abstractmethod
    def check_requirements(self):
        """
        Check if all pre-installation requirements are met.
        :return: Boolean indicating readiness to install.
        """
        pass

    @abstractmethod
    def setup_environment(self, env_name):
        """
        Set up the required environment for the system.
        :param env_name: The name of the environment to set up.
        """
        pass

    @abstractmethod
    def update(self):
        """
        Update the system to the latest version.
        """
        pass
