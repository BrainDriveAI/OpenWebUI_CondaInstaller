import os
import sys
import threading
from tkinter import Tk, Label, Text, Button, Scrollbar, Frame, END, messagebox
from tkinter import ttk
from tkinter import StringVar
from MinicondaInstaller import MinicondaInstaller
from environment_setup import EnvironmentSetup
from logger import Logger
import subprocess
import shutil
import webbrowser
import socket

class TextRedirector:
    """Redirect console output to a Tkinter Text widget."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        """Write message to the Text widget in a thread-safe manner."""
        self.text_widget.after(0, self.text_widget.insert, END, message)
        self.text_widget.after(0, self.text_widget.see, END)  # Scroll to the end

    def flush(self):
        """Required for compatibility with sys.stdout and sys.stderr."""
        pass


class InstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Open WebUI Conda Installer (Beta v0.1.3)")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Determine the correct path for the icon
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, 'DigitalBrainBaseIcon.ico')        
        self.root.iconbitmap(icon_path)

        # Create the main frame
        frame = Frame(self.root)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        # Installation progress text variable
        self.progress_text = StringVar()
        self.progress_text.set("Installation Progress")

        # Instructions Section
        Label(frame, text="Instructions", font=("Arial", 14, "bold")).pack(anchor="w", pady=(10, 10))
        Label(
            frame,
            text="This installer will set up Miniconda and Open WebUI.Click 'Install' to begin.",
            font=("Arial", 12),
            wraplength=600,
        ).pack(anchor="w")

        # Installation Progress Section
        Label(frame, textvariable=self.progress_text, font=("Arial", 14, "bold")).pack(anchor="w", pady=(20, 10))
        output_frame = Frame(frame)
        output_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.output_box = Text(output_frame, height=10, wrap="word")
        self.output_box.pack(side="left", fill="both", expand=True)
        scroll = Scrollbar(output_frame, command=self.output_box.yview)
        scroll.pack(side="right", fill="y")
        self.output_box.configure(yscrollcommand=scroll.set)

        # Redirect stdout and stderr to the Text widget
        sys.stdout = TextRedirector(self.output_box)
        sys.stderr = TextRedirector(self.output_box)

        # Install and Start Buttons Frame
        button_frame = Frame(frame)
        button_frame.pack(pady=20)

        # Install Button
        self.install_button = Button(button_frame, text="Install", command=self.run_installation)
        self.install_button.pack(side="left", padx=5)
        self.install_button.config(state="disabled")

        # Start Open WebUI Button
        self.start_button = Button(button_frame, text="Start Open WebUI", command=self.start_open_webui)
        self.start_button.pack(side="left", padx=5)
        self.start_button.config(state="disabled")

        # Update Open WebUI Button
        self.update_button = Button(button_frame, text="Update Open WebUI", command=self.update_open_webui)
        self.update_button.pack(side="left", padx=5)
        self.update_button.config(state="disabled")        

       # Adding Ollama Section
        ollama_frame = Frame(frame)
        ollama_frame.pack(fill="x", pady=20)

        # Ollama Heading
        Label(ollama_frame, text="Ollama", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Ollama Description on the Left
        ollama_description = Label(
            ollama_frame,
            text="Open WebUI uses Ollama to handle serving local models to the interface. "
                 "If you need it, feel free to install it now.",
            font=("Arial", 12),
            wraplength=550,
            anchor="w",
            justify="left",
        )
        ollama_description.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # Install Ollama Button on the Right
        self.install_ollama_button = Button(
            ollama_frame,
            text="Install Ollama",
            command=self.install_ollama,
        )
        self.install_ollama_button.grid(row=1, column=1, sticky="e", padx=10, pady=5)
        self.install_ollama_button.config(state="disabled")  # Initially disabled

        # Perform initial checks
        self.perform_initial_checks()

    def update_progress(self, step, total_steps):
        """Update the progress label to show the current installation step or default message."""
        if step == 0 and total_steps == 0:
            self.progress_text.set("Installation Progress")
        else:
            self.progress_text.set(f"Installation Progress [{step}/{total_steps}]")



    def install_ollama(self):
        """Handle the installation of Ollama."""
        def ollama_install_task():
            try:
                self.install_ollama_button.config(state="disabled")
                # Define the URL and target path for the installer
                ollama_url = "https://ollama.com/download/OllamaSetup.exe"
                installer_name = "OllamaSetup.exe"
                installer_path = os.path.join(os.getcwd(), installer_name)  # Save in current directory
                
                Logger.log("Downloading Ollama installer...")
                
                # Download the installer
                import urllib.request
                with urllib.request.urlopen(ollama_url) as response, open(installer_path, 'wb') as out_file:
                    data = response.read()
                    out_file.write(data)

                Logger.log("Ollama installer downloaded successfully.")
                

                # Run the installer
                Logger.log("Running Ollama installer...")
                subprocess.Popen(installer_path, shell=True)

                Logger.log("Ollama installation initiated. Follow the on-screen instructions to complete the installation.")

            except Exception as e:
                Logger.log(f"Failed to install Ollama: {e}")
                messagebox.showerror("Error", f"Failed to install Ollama: {e}")

        # Run the installation task in a separate thread
        threading.Thread(target=ollama_install_task, daemon=True).start()

    def update_ollama_button_state(self):
        """Enable the Ollama button if the Start Open WebUI button is enabled."""
        if self.start_button["state"] == "normal":
            self.install_ollama_button.config(state="normal")
        else:
            self.install_ollama_button.config(state="disabled")

    def add_icon(self):
        """Create a desktop shortcut for the application."""
        def icon_task():
            try:
                # Ensure pywin32 modules are available
                import pythoncom
                from win32com.shell import shell, shellcon
                from win32com.client import Dispatch

                # Get the path to the desktop
                desktop_path = shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, None, 0)
                shortcut_name = "Open WebUI Installer.lnk"
                shortcut_path = os.path.join(desktop_path, shortcut_name)

                # Get the path to the application executable
                current_executable = os.path.abspath(sys.argv[0])
                install_directory = os.path.dirname(current_executable)
                base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
                icon_path = os.path.join(base_path, "DigitalBrainBaseIcon.ico")
                # Create the shortcut
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.Targetpath = current_executable
                shortcut.WorkingDirectory = install_directory
                shortcut.IconLocation = icon_path
                shortcut.save()

                Logger.log("Desktop shortcut created successfully.")
            except Exception as e:
                Logger.log(f"Failed to create desktop shortcut: {e}")
                print(f"Failed to create desktop shortcut: {e}")
                messagebox.showerror("Error", f"Failed to create desktop shortcut: {e}")

        # Run the icon creation task in a separate thread
        threading.Thread(target=icon_task, daemon=True).start()



    def perform_initial_checks(self):
        """Perform initial checks and display the results in the output box."""
        def checks_task():
            print("Performing initial checks...")
            try:
                # Initialize MinicondaInstaller
                installer = MinicondaInstaller()
                conda_installed = installer.verify_conda()
                if conda_installed:
                    print("Conda is installed.")
                else:
                    print("Conda is not installed.")

                # Initialize EnvironmentSetup
                env_setup = EnvironmentSetup(installer.base_path, installer.miniconda_path)
                env_exists = os.path.isdir(env_setup.env_path)
                if env_exists:
                    print("Conda environment is set up.")
                else:
                    print("Conda environment is not set up.")

                open_webui_installed = False  # Initialize as False
                update_available = False      # Initialize as False

                # Check if open-webui is installed only if the environment exists
                if conda_installed and env_exists:
                    pip_show_cmd = [
                        env_setup.conda_exe,
                        "run",
                        "--prefix", env_setup.env_path,
                        "pip", "show", "open-webui"
                    ]
                    CREATE_NO_WINDOW = 0x08000000
                    try:
                        result = subprocess.run(
                            pip_show_cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            creationflags=CREATE_NO_WINDOW,
                            check=True
                        )
                        if "Name: open-webui" in result.stdout:
                            print("open-webui is installed.")
                            open_webui_installed = True

                            # Now perform the update check
                            installed_version = None
                            for line in result.stdout.splitlines():
                                if line.startswith("Version:"):
                                    installed_version = line.split("Version:")[1].strip()
                                    break
                            if installed_version:
                                print(f"Installed open-webui version: {installed_version}")

                                # Get latest version from PyPI
                                import urllib.request
                                import json
                                try:
                                    with urllib.request.urlopen("https://pypi.org/pypi/open-webui/json") as response:
                                        data = json.loads(response.read().decode())
                                        latest_version = data["info"]["version"]
                                        print(f"Latest open-webui version: {latest_version}")
                                except Exception as e:
                                    print(f"Error fetching latest open-webui version: {e}")
                                    latest_version = None

                                # Compare versions
                                if installed_version and latest_version:
                                    if installed_version != latest_version:
                                        print("An update is available for open-webui.")
                                        update_available = True
                                    else:
                                        print("open-webui is up to date.")
                                        update_available = False
                                else:
                                    update_available = False
                            else:
                                update_available = False
                        else:
                            print("open-webui is not installed.")
                    except subprocess.CalledProcessError:
                        print("open-webui is not installed.")
                    except FileNotFoundError:
                        # Handle the case where conda or pip is not found
                        print("Error: Could not find conda executable or the environment is not properly set up.")
                        open_webui_installed = False
                else:
                    print("Please Click 'Install' to set up Open WebUI.")
                    open_webui_installed = False
                    update_available = False

                # Check if Open WebUI is already running
                open_webui_running = False
                pid_file = os.path.join(installer.base_path, "open_webui.pid")
                if os.path.exists(pid_file):
                    try:
                        with open(pid_file, "r") as f:
                            pid = int(f.read())
                        # Check if the process is running
                        if self.check_process_running(pid):
                            open_webui_running = True
                            print(f"Open WebUI is already running with PID {pid}.")
                        else:
                            # Remove stale PID file
                            os.remove(pid_file)
                    except Exception:
                        # If any error occurs, assume process is not running
                        os.remove(pid_file)

                # Update the buttons' state in the main thread
                self.root.after(0, self.update_install_button_state, conda_installed, env_exists, open_webui_installed, update_available)

                # Update the Start button state and command
                if open_webui_running:
                    self.root.after(0, self.start_button.config, {'state': 'normal', 'text': 'Stop Open WebUI', 'command': self.stop_open_webui})
                else:
                    if conda_installed and env_exists and open_webui_installed:
                        self.root.after(0, self.start_button.config, {'state': 'normal', 'text': 'Start Open WebUI', 'command': self.start_open_webui})
                    else:
                        self.root.after(0, self.start_button.config, {'state': 'disabled'})

                self.root.after(0, self.update_ollama_button_state)
            except Exception as e:
                print(f"Error during initial checks: {e}")
                # If there's an error, assume not all checks passed
                self.root.after(0, self.update_install_button_state, False, False, False, False)

        
        # Run the checks in a separate thread
        threading.Thread(target=checks_task, daemon=True).start()


    def update_install_button_state(self, conda_installed, env_exists, open_webui_installed, update_available):
        """Enable or disable the Install, Start, and Update buttons based on initial checks."""
        if conda_installed and env_exists and open_webui_installed:
            self.install_button.config(state="disabled")
            print("All components are installed.")
            print("Click 'Start Open WebUI' to Launch.")
        else:
            self.install_button.config(state="normal")
            self.start_button.config(state="disabled")

        # Update the Update button
        if open_webui_installed and update_available:
            self.update_button.config(state="normal")
        else:
            self.update_button.config(state="disabled")

        # Update Ollama button state
        self.update_ollama_button_state()


    def check_process_running(self, pid):
        """Check if a process with the given PID is running (Windows compatible)."""
        try:
            import psutil
        except ImportError:
            print("psutil is not installed. Unable to check if process is running.")
            return False

        return psutil.pid_exists(pid)

    def start_open_webui(self):
        """Start Open WebUI using conda run."""
        def start_task():
            try:
                self.start_button.config(state="disabled")
                Logger.log(f"Starting Open WebUI Server...")
                Logger.log(f"This may take a few minutes depending on your computer. Your browser will open automatically when the server is ready.")
                installer = MinicondaInstaller()
                env_setup = EnvironmentSetup(installer.base_path, installer.miniconda_path)
                conda_exe = env_setup.conda_exe
                env_path = env_setup.env_path

                # Command to run
                open_webui_cmd = [
                    conda_exe,
                    "run",
                    "--prefix", env_path,
                    "open-webui", "serve"
                ]

                CREATE_NO_WINDOW = 0x08000000  # Prevents console window from popping up

                # Start the process
                process = subprocess.Popen(
                    open_webui_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    creationflags=CREATE_NO_WINDOW
                )

                # Loop to check for the open-webui process
                import time
                import psutil
                open_webui_pid = None

                for attempt in range(60):
                    time.sleep(3)  # Wait for 3 seconds

                    # Use psutil to get the child processes
                    parent_proc = psutil.Process(process.pid)
                    children = parent_proc.children(recursive=True)

                    for child in children:
                        if 'open-webui' in child.name().lower():
                            open_webui_pid = child.pid
                            break  # Found the process, exit the inner loop

                    if open_webui_pid is not None:
                        break  # Found the process, exit the outer loop

                if open_webui_pid is None:
                    Logger.log("Failed to find open-webui process after multiple attempts.\n")
                    return

                # Store the PID in a file
                pid_file = os.path.join(installer.base_path, "open_webui.pid")
                with open(pid_file, "w") as f:
                    f.write(str(open_webui_pid))

                Logger.log(f"Open WebUI started with PID {open_webui_pid}.\n")


                # Check if the server is accessible on http://localhost:8080
                # Logger.log("Checking for server availability...")
                # Logger.log("Your browser will open automatically when the server is ready.")
                server_ready = False
                for attempt in range(120):  # Retry up to 20 times with a delay
                    try:
                        with socket.create_connection(("localhost", 8080), timeout=2):
                            server_ready = True
                            break
                    except (socket.timeout, ConnectionRefusedError):
                        time.sleep(2)

                if server_ready:
                    # Open the browser to http://localhost:8080
                    webbrowser.open("http://localhost:8080")
                    Logger.log("Opened browser to http://localhost:8080")
                else:
                    Logger.log("Server did not become ready after multiple attempts.\n")



                # Update Start button to "Stop Open WebUI"
                self.root.after(0, self.start_button.config, {'text': 'Stop Open WebUI', 'command': self.stop_open_webui})
                self.start_button.config(state="normal")
                # Read output and display in the output box
                for line in process.stdout:
                    self.output_box.after(0, self.output_box.insert, END, line)
                    self.output_box.after(0, self.output_box.see, END)

                process.wait()
                if process.returncode != 0:
                    Logger.log(f"Open WebUI exited with return code {process.returncode}.\n")
                else:
                    Logger.log("Open WebUI has stopped.\n")

                # After process ends, remove PID file
                if os.path.exists(pid_file):
                    os.remove(pid_file)

                # Update Start button to "Start Open WebUI"
                self.root.after(0, self.start_button.config, {'text': 'Start Open WebUI', 'command': self.start_open_webui})

            except Exception as e:
                Logger.log(f"Error starting Open WebUI: {e}\n")

        # Run the start task in a separate thread
        threading.Thread(target=start_task, daemon=True).start()

    def stop_open_webui(self):
        """Stop Open WebUI if it's running."""
        installer = MinicondaInstaller()
        pid_file = os.path.join(installer.base_path, "open_webui.pid")
        if os.path.exists(pid_file):
            try:
                with open(pid_file, "r") as f:
                    pid = int(f.read())
                # Terminate the process
                import psutil
                process = psutil.Process(pid)
                # Terminate the process and its children
                for child in process.children(recursive=True):
                    child.terminate()
                process.terminate()
                psutil.wait_procs([process], timeout=5)
                Logger.log(f"Open WebUI with PID {pid} has been terminated.\n")
                # Remove the PID file
                os.remove(pid_file)
                # Update the Start button
                self.start_button.config(state="normal", text="Start Open WebUI", command=self.start_open_webui)
            except Exception as e:
                Logger.log(f"Error stopping Open WebUI: {e}\n")
        else:
            Logger.log("Open WebUI is not running.\n")

    def run_installation(self):
        """Run the installation process in a background thread."""
        def installation_task():
            """Actual installation logic."""
            try:
                Logger.log("Starting installation process.")
                self.install_button.config(state="disabled")
                installer = MinicondaInstaller()
                installer.ensure_miniconda_installed()

                env_setup = EnvironmentSetup(installer.base_path, installer.miniconda_path)
                env_setup.setup_environment(self.output_box)

                Logger.log("Installation complete.")
                print("Installation complete.")

                # Additional Step: Check and copy the executable if necessary

                current_executable = sys.executable
                install_directory = installer.base_path
                executable_name = os.path.basename(current_executable)
                target_executable = os.path.join(install_directory, executable_name)

                if os.path.abspath(current_executable) != os.path.abspath(target_executable):
                    # Copy the executable to the install directory
                    Logger.log(f"Copying executable to {install_directory}")
                    shutil.copy2(current_executable, target_executable)
                    Logger.log("Executable copied successfully.")

                    # Create a desktop shortcut
                    try:
                        # Ensure pywin32 modules are available
                        import pythoncom
                        from win32com.shell import shell, shellcon
                        from win32com.client import Dispatch

                        # Get the desktop path
                        desktop_path = shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, None, 0)
                        shortcut_name = "Open WebUI Installer.lnk"
                        shortcut_path = os.path.join(desktop_path, shortcut_name)

                        # Determine the base path (handles PyInstaller runtime and normal execution)
                        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

                        # Path to the original icon in the temporary directory
                        temp_icon_path = os.path.join(base_path, "DigitalBrainBaseIcon.ico")

                        # Move the icon to the install directory if it doesn't already exist
                        persistent_icon_path = os.path.join(install_directory, "DigitalBrainBaseIcon.ico")
                        if not os.path.exists(persistent_icon_path):
                            shutil.copy(temp_icon_path, persistent_icon_path)

                        # Create the shortcut
                        shell = Dispatch('WScript.Shell')
                        shortcut = shell.CreateShortCut(shortcut_path)
                        shortcut.Targetpath = target_executable
                        shortcut.WorkingDirectory = install_directory
                        shortcut.IconLocation = persistent_icon_path  # Use the moved icon
                        shortcut.save()

                        Logger.log("Desktop shortcut created successfully.")
                        print("Desktop shortcut created successfully.")
                    except Exception as e:
                        Logger.log(f"Failed to create desktop shortcut: {e}")
                        print(f"Failed to create desktop shortcut: {e}")


                    # Restart the app from the install directory
                    Logger.log("Restarting application from install directory.")

                    # Define flags to detach the new process
                    DETACHED_PROCESS = 0x00000008
                    CREATE_NEW_PROCESS_GROUP = 0x00000200

                    subprocess.Popen(
                        [target_executable],
                        creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
                    )

                    # Close the current application
                    Logger.log("Closing current application.")
                    self.root.after(0, self.root.destroy)
                    return  # Exit the installation_task

                else:
                    Logger.log("Executable is already in the install directory.")
            except Exception as e:
                Logger.log(f"Installation error: {e}")
                print(f"Error: {e}")
                messagebox.showerror("Error", "Installation failed. Check logs for details.")
            finally:
                Logger.log("Installation process finished.")
                # After installation, perform checks again to update the buttons
                self.perform_initial_checks()

        # Run the installation task in a separate thread
        threading.Thread(target=installation_task, daemon=True).start()


    def update_open_webui(self):
        """Update Open WebUI to the latest version."""
        def update_task():
            try:
                installer = MinicondaInstaller()
                env_setup = EnvironmentSetup(installer.base_path, installer.miniconda_path)
                print("Updating Open WebUI...")
                env_setup.update_open_webui(self.output_box)
                print("Open WebUI has been updated.")
                # After updating, perform initial checks again to update the buttons
                self.perform_initial_checks()
            except Exception as e:
                print(f"Error updating Open WebUI: {e}")
        # Run the update task in a separate thread
        threading.Thread(target=update_task, daemon=True).start()


if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()  # Required for PyInstaller

    root = Tk()
    app = InstallerApp(root)
    root.mainloop()
