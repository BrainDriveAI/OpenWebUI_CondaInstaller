import os
import shutil
import requests
import pythoncom
from win32com.shell import shell, shellcon
from win32com.client import Dispatch
from AppConfig import AppConfig


class AppDesktopIntegration:
    def __init__(self):
        """
        Initializes the DesktopIntegration class.
        Automatically fetches the base path from the existing AppConfig singleton.
        """
          # Importing here to avoid circular imports
        app_config = AppConfig()
        
        self.base_path = app_config.base_path
        self.exe_name = "InstallerAutoUpdater.exe"
        self.icon_name = "DigitalBrainBaseIcon.ico"
        self.desktop_path = shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, None, 0)
        self.shortcut_name = "Open WebUI Installer.lnk"
        self.shortcut_path = os.path.join(self.desktop_path, self.shortcut_name)
        self.exe_path = os.path.join(self.base_path, self.exe_name)
        self.icon_path = os.path.join(self.base_path, self.icon_name)
        self.repo_url = "https://github.com/BrainDriveAI/InstallerAutoUpdater/releases/latest/download/InstallerAutoUpdater.exe"

    def verify_exe_exists(self):
        """
        Verifies if the required executable exists in the base path.
        If not, downloads it from the repository.
        """
        try:
            if not os.path.exists(self.exe_path):
                print("Executable not found. Downloading...")
                response = requests.get(self.repo_url, stream=True)
                if response.status_code == 200:
                    with open(self.exe_path, "wb") as exe_file:
                        shutil.copyfileobj(response.raw, exe_file)
                    print("Executable downloaded successfully.")
                else:
                    raise Exception(f"Failed to download the executable. HTTP Code: {response.status_code}")
            else:
                print("Executable already exists.")
        except Exception as e:
            print(f"Error verifying executable: {e}")
            raise

    def create_desktop_icon(self):
        """
        Creates a desktop shortcut to the InstallerAutoUpdater.exe with the correct icon.
        """
        try:
            if not os.path.exists(self.exe_path):
                raise FileNotFoundError(f"{self.exe_name} not found at {self.base_path}")
            if not os.path.exists(self.icon_path):
                raise FileNotFoundError(f"{self.icon_name} not found at {self.base_path}")

            # Create the shortcut
            shell_instance = Dispatch('WScript.Shell')
            shortcut = shell_instance.CreateShortCut(self.shortcut_path)
            shortcut.TargetPath = self.exe_path
            shortcut.WorkingDirectory = self.base_path
            shortcut.IconLocation = self.icon_path
            shortcut.save()

            print("Desktop shortcut created successfully.")
        except Exception as e:
            print(f"Failed to create desktop shortcut: {e}")
            raise

    def verify_and_update_icon(self):
        """
        Checks if the existing desktop shortcut points to the correct executable.
        If not, updates it to point to the correct executable.
        """
        try:
            shortcut_exists = os.path.exists(self.shortcut_path)
            if not shortcut_exists:
                print("Shortcut does not exist. Creating a new one...")
                self.create_desktop_icon()
                return

            # Verify existing shortcut target
            shell_instance = Dispatch('WScript.Shell')
            shortcut = shell_instance.CreateShortCut(self.shortcut_path)
            current_target = shortcut.TargetPath

            if current_target != self.exe_path:
                print(f"Incorrect shortcut target found: {current_target}. Updating shortcut...")
                shortcut.TargetPath = self.exe_path
                shortcut.IconLocation = self.icon_path
                shortcut.save()
                print("Shortcut updated successfully.")
            else:
                print("Shortcut is already up-to-date.")
        except Exception as e:
            print(f"Error verifying or updating desktop shortcut: {e}")
            raise

