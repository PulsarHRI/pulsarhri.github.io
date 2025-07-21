# Install Python API

In this document we will guide you through the installation of the PULSAR HRI Python API, which allows you to programmatically control and interact with PULSAR actuators.


## Installation

You can use a virtual environment to install this and other packages for your project. There are several ways to create a virtual environments. In this guide, we will skip the virtual environment and install the PULSAR HRI Python API globally.

```bash
pip install pcp_api
```


## Verifying the Installation

To confirm that the installation was successful, you can run the following command:

```bash
pip show pcp_api
```
This should provide information about the installed package, including its version and location. If you see this information, the installation was successful.


## Next Steps

Once the API is installed, you can:

* Use the [Command line interface](cli.md) to quickly interact with the PULSAR hardware.
* Run the [example scripts](example_single_actuator.md)
* Explore the [code documentation](class_PulsarActuator.md) for detailed usage instructions.
* Integrate the API into your own applications or research workflows.

If you encounter any issues, please open an issue [issue](https://github.com/PulsarHRI/pulsarhri.github.io/issues).
