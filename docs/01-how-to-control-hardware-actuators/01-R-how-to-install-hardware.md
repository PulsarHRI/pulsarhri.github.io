# Installing the PULSAR HRI actuator API (pcp_api)
To ensure a clean and manageable development setup, we strongly recommend using a virtual environment. This helps isolate your dependencies and avoid conflicts with other Python packages on your system. **All examples and functionality have been tested on Windows 11 using Python 3.12.10.**

## Installation

### Step 1: Create a Virtual Environment
Open your terminal or command prompt and run:

```bash
python -m venv .venv
```
This will create a new virtual environment in a folder named .venv within your project directory.

!!! warning
    The installation can be done in the root environment but we do not recommend it.

### Step 2: Activate the Virtual Environment

Before installing the PULSAR HRI API, activate the virtual environment. The activation command depends on your operating system:

=== "Linux/macOS"

    ```bash
    source .venv/bin/activate
    ```

=== "Windows (PowerShell)"

    ```bat
    .\.venv\Scripts\Activate.ps1
    ```

Once activated, your terminal prompt should change to indicate that you're working inside the virtual environment.

### Step 3: Install the PULSAR HRI API
With the virtual environment active, install the PULSAR HRI API package using `pip`:

```bash
pip install pcp_api
```
This command will download and install the latest version of the pcp_api package from PyPI or your configured package index. 

!!! tip
    Every time you want to use the PULSAR HRI API or run the example scripts, make sure to activate your virtual environment first. If you close your terminal or restart your system, you’ll need to reactivate it.

## Verifying the Installation
To confirm that the installation was successful, you can run the following command:

```bash
pip show pcp_api
```
This should provide information about the installed package, including its version and location. If you see this information, the installation was successful.

## Next Steps

Once the API is installed, you can:

* Use the CLI (command line interface) to quickly interact with the PULSAR hardware.
* Run example scripts provided in the [examples directory](02-R-actuator-control-examples/00-R-examples-overview.md).
* Explore the documentation for detailed usage instructions.
* Integrate the API into your own applications or research workflows.

If you encounter any issues, please open an issue in this repository [project repository](https://github.com/PulsarHRI/pulsarhri.github.io).