# Command line interface (CLI)

The Command Line Interface (CLI) is included in the python package. It provides a convenient way to interact with the actuator directly from a terminal. This is particularly useful for quick communication test and for scanning devices on a CAN bus.


## Verifying the Installation

The CLI is installed along the python package. To confirm that the CLI is working correctly, you can run the following command:

```bash
pulsar-cli -h
```
This should print the help message.


## Using the CLI

The CLI provides several commands to interact with the Pulsar actuator. Here are some common commands:


### Scan for Devices

```bash
pulsar-cli scan
```
This command scans the CAN bus for connected Pulsar devices and lists their addresses. You need a CAN adapter connected and a [correctly wired CAN bus](../electrical_interfaces.md#can-bus). Use the `-h` flag to see more options.


### Get Device parameters

```bash
pulsar-cli params
```
You can retrieve all the parameters of the connected device.  Use the `-h` flag to see more options.
