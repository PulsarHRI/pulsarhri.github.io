# Command line interface (CLI)

The Command Line Interface (CLI) for the Pulsar API provides a convenient way to interact with the actuator directly from a terminal. This is particularly useful for quick communication test and for scanning devices on a CAN bus.

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
pulsar-cli scan -p <port>
```
This command scans the CAN bus for connected Pulsar devices and lists their IDs and statuses. Replace `<port>` with the appropriate serial port of the CAN adapter (e.g., `/dev/ttyUSB0` on Linux or `COM3` on Windows).
Use the `-h` flag to see more options


### Get Device parameters
```bash
pulsar-cli params -p <port>
```
Then connected to a device via USB, you can retrieve all the parameters of the device. This command will display the current configuration and status of the actuator. Replace `<port>` with the appropriate serial port of the actuator (e.g., `/dev/ttyUSB0` on Linux or `COM3` on Windows).