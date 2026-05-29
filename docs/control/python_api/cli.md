# Command-Line Interface (CLI)

The Command-Line Interface (CLI) is included in the Python package. It provides a convenient way to interact with the actuator directly from the terminal. This is particularly useful for quick communication tests and for scanning devices on the CAN bus.

This section targets Python API 2.0.0.

## Verifying the Installation

The CLI is installed alongside the Python package. To confirm that it is working correctly, run the following command:

```bash
pulsar-cli -h
```
This should display the help message.

You can also check the installed package version:

```bash
pulsar-cli --version
```


## Using the CLI

### General notes

* If `--port` is omitted, the CLI tries to auto-detect the USB serial port.
* When using CAN, `--address` is required. It accepts both hexadecimal and decimal notation, for example `0x10` or `16`.
* Run `pulsar-cli <command> -h` to see the options for a specific command.

### Commands

| Command | Purpose |
| --- | --- |
| `scan` | Scan the CAN bus for connected PULSAR devices. |
| `params` | Read parameters from a connected actuator. |
| `blink` | Blink an actuator LED to identify a device. |
| `home` | Store the current actuator position as the home position. |


### Scan for Devices

```bash
pulsar-cli scan
```
This command scans the CAN bus for connected PULSAR devices and lists their addresses. You need a CAN adapter connected and a [correctly wired CAN bus](../../set_up/hardware_interfaces/electrical_interfaces.md#can-bus).


### Get Device Parameters

```bash
pulsar-cli params
```
You can retrieve all parameters of the connected device.

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

This command blinks the actuator LED so that you can identify a device on the CAN bus. An address is required when identifying an actuator on a CAN bus.


### Set Home Position

```bash
pulsar-cli home
```

This command stores the actuator's current position as the home position (zero reference). The position is stored in the device's non-volatile memory and is retained even after power cycling.
