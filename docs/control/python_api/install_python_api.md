# Install Python API

This guide walks you through the installation of the PULSAR HRI Python API, which allows you to programmatically control and interact with PULSAR actuators.


## Installation

You can use a virtual environment to install this package and other dependencies for your project. There are several ways to create virtual environments. In this guide, we skip the virtual environment setup and install the PULSAR HRI Python API globally.

```bash
pip install --upgrade pcp_api
```


## Verifying the Installation

To confirm that the installation was successful, run the following command:

```bash
pip show pcp_api
```

This command should display information about the installed package, including its version and location. If you see this information, the installation was successful.

## Next Steps

Once the API is installed, you can:

* Use the [command-line interface](cli.md) to quickly interact with PULSAR hardware.
* Run the [example scripts](example_single_actuator_nb.ipynb).
* Explore the [code documentation](class_PulsarActuator.md) for detailed usage instructions.
* Integrate the API into your own applications or research workflows.

If you encounter any issues, please open an [issue](https://github.com/PulsarHRI/pulsarhri.github.io/issues).
