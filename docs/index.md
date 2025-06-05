# Getting started
Welcome to the Pulsar API repository! This repository contains everything you need to begin working with the Pulsar Actuator or Pulsar Motor. Whether you're a researcher, developer, or engineer, this guide will walk you through setting up your environment, installing the API, and accessing the documentation and examples.

The Pulsar API is designed to provide a robust and flexible interface for controlling and monitoring Pulsar hardware. It includes:

* A well-documented Python package (pcp_api)
* Example scripts for common use cases
* Detailed descriptions of available classes, methods, and parameters
* Best practices for integration and deployment
## Installing the Pulsar API into your own Environment
To ensure a clean and manageable development setup, we strongly recommend using a virtual environment. This helps isolate your dependencies and avoid conflicts with other Python packages on your system. All examples and functionality have been tested on Windows 11 using Python 3.12.10.

### Step 1: Create a Virtual Environment
Open your terminal or command prompt and run:

```bash
python -m venv .venv
```
This will create a new virtual environment in a folder named .venv within your project directory.
### Step 2: Activate the Virtual Environment

Before installing the Pulsar API, activate the virtual environment. The activation command depends on your operating system:

=== "Linux/macOS"

    ```bash
    source .venv/bin/activate
    ```

=== "Windows (PowerShell)"

    ```bash
    .\.venv\Scripts\Activate.ps1
    ```

Once activated, your terminal prompt should change to indicate that you're working inside the virtual environment.

### Step 3: Install the Pulsar API
With the virtual environment active, install the Pulsar API package using `pip`:

```bash
pip install pcp_api
```
This command will download and install the latest version of the pcp_api package from PyPI or your configured package index. 

!!! Important
    Every time you want to use the Pulsar API or run the example scripts, make sure to activate your virtual environment first. If you close your terminal or restart your system, you’ll need to reactivate it.

## Verifying the Installation
To confirm that the installation was successful, you can run the following command:

```bash
python -c "import pcp_api; print(pcp_api.__version__)"
```
This should print the version number of the installed package, indicating that it's ready to use. For the present documentation the version is 0.9.1.

## Next Steps

Once the API is installed, you can:

* Explore the documentation for detailed usage instructions.
* Run example scripts provided in the examples/ directory.
* Integrate the API into your own applications or research workflows.

If you encounter any issues, please open an issue in this repository [project repository](https://github.com/PulsarHRI/pulsarhri.github.io).