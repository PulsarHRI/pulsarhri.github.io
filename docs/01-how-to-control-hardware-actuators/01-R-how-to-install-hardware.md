# Installing the Pulsar actuator API (pcp_api)
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

!!! tip
    Every time you want to use the Pulsar API or run the example scripts, make sure to activate your virtual environment first. If you close your terminal or restart your system, you’ll need to reactivate it.

## Verifying the Installation
To confirm that the installation was successful, you can run the following command:

```bash
python -c "import pcp_api; print(pcp_api.__version__)"
```
This should print the version number of the installed package, indicating that it's ready to use. **For the present documentation the version is 0.9.1.**

## Next Steps

Once the API is installed, you can:

* Explore the documentation for detailed usage instructions.
* Run example scripts provided in the [examples directory](02-R-actuator-control-examples/00-R-examples-overview.md).
* Integrate the API into your own applications or research workflows.

If you encounter any issues, please open an issue in this repository [project repository](https://github.com/PulsarHRI/pulsarhri.github.io).