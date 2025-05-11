> ⚠️ **Archived Project**  
> This project is no longer actively maintained by the original authors.  
> The repository remains available for reference and community use.

# OpenWebUI_CondaInstaller

---

## Overview

**OpenWebUI_CondaInstaller** is a Python-based GUI installer for setting up Miniconda and managing an environment to run the Open WebUI application. This installer simplifies the process of installing dependencies, configuring environments, and starting the Open WebUI server for users.

## Features

- **Miniconda Installation:** Automatically downloads and installs Miniconda if not already installed.
- **Environment Management:** Creates and configures a Conda environment with Python 3.11 for Open WebUI.
- **Open WebUI Setup and Updates:** Installs and updates the Open WebUI application.
- **Graphical User Interface:** Provides an intuitive interface for installation and configuration.
- **Shortcut Creation:** Optionally creates a desktop shortcut for easy access.
- **Start/Stop Open WebUI:** Manage the Open WebUI server with a simple button click.

---

## Getting Started

### Prerequisites

1. **Windows OS:** The installer is designed for Windows systems.
2. **Python 3.11 or Miniconda:** Ensure Python 3.11 or Miniconda3 is installed.

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/BrainDriveAI/OpenWebUI_CondaInstaller.git
   cd OpenWebUI_CondaInstaller
   ```

3. **Handle requirements:**
   Launch the application:
   ```bash
   pip install -r requirements.txt
   ```


2. **Run the Installer:**
   Launch the application:
   ```bash
   python main_interface.py
   ```
   Alternatively, use the executable if provided in the releases.

---

## Usage

1. **Start the Application:**
   Run the `main_interface.py` script to launch the installer GUI.

2. **Perform Installation:**
   - Click the **Install** button to set up Miniconda, create a Conda environment, and install Open WebUI.

3. **Start Open WebUI:**
   - Once installation is complete, click the **Start Open WebUI** button to launch the server.
   - The server will open in your default browser at `http://localhost:8080`.

4. **Update Open WebUI:**
   - Use the **Update Open WebUI** button to fetch and install the latest version.

5. **Stop Open WebUI:**
   - Click the **Stop Open WebUI** button to terminate the server.

---


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature description"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request on the main repository.

---

## License

This project is licensed under the [MIT License](https://github.com/BrainDriveAI/OpenWebUI_CondaInstaller/blob/main/LICENSE).

---

## Acknowledgments

- [Open WebUI](https://github.com/open-webui/open-webui) for the web interface.
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) for simplified Python package management.

