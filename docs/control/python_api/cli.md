# Command line interface (CLI)

The Command Line Interface (CLI) is included in the Python package. It provides a convenient way to interact with the actuator directly from a terminal. This is particularly useful for quick communication tests and for scanning devices on a CAN bus.


## Verifying the Installation

The CLI is installed alongside the Python package. To confirm that the CLI is working correctly, you can run the following command:

```bash
pulsar-cli -h
```
This should print the help message.

You can also check the installed package version:

```bash
pulsar-cli --version
```


## Using the CLI

The CLI provides several commands to interact with the Pulsar actuator. Here are some common commands:


### General notes

* If `--port` is omitted, the CLI tries to auto-detect the USB serial port.
* When using CAN,  `--address` is needed. It accepts both hexadecimal and decimal notation, for example `0x10` or `16`.


### Scan for Devices

```bash
pulsar-cli scan
```
This command scans the CAN bus for connected Pulsar devices and lists their addresses. You need a CAN adapter connected and a [correctly wired CAN bus](../../set_up/hardware_interfaces/electrical_interfaces.md#can-bus). Use the `-h` flag to see more options.


### Get Device parameters

```bash
pulsar-cli params
```
You can retrieve all the parameters of the connected device.  Use the `-h` flag to see more options.

Examples:

```bash
pulsar-cli params  # Connects directly over USB
```

```bash
pulsar-cli params --port COM3 --address 0x10
```


### Blink Device LED

```bash
pulsar-cli blink --address 0x10
```

This command blinks the actuator LED so you can identify a device on the CAN bus. An address is required for this command.


### Set Home Position

```bash
pulsar-cli home
```

This command stores the actuator's current position as the home position (zero reference). This position is stored in the device's non-volatile memory and is retained even after power cycling. Use the `-h` flag to see more options.
