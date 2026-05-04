# Command-Line Interface (CLI)

The C++ API includes a command-line interface executable named `pulsar-cli`. It provides a convenient way to interact with the actuator directly from the terminal. This is useful for quick communication tests, checking connectivity, and scanning devices on the CAN bus.

## Building the CLI

Build the C++ API first so that the `pulsar-cli` executable is generated in the build directory.

## Verifying the Installation

From the build folder of the C++ API, run:

```bash
./pulsar-cli -h
```

This should display the help message.

You can also check the version with:

```bash
./pulsar-cli --version
```

If the executable does not have sufficient execution permissions, you may need to run it with `sudo`.

This can happen when your user does not have permission to execute files in that folder or to access the required device interfaces.

## Using the CLI

The CLI provides several commands to interact with PULSAR devices.

### General notes

- Run the commands from the **build folder** where `pulsar-cli` was generated.
- If `--port` is omitted, the CLI tries to auto-detect the USB serial port.
- When using CAN, `--address` is required. It accepts both hexadecimal and decimal notation, for example `0x10` or `16`.
- In some systems, you may need to prepend `sudo` if your user does not have sufficient permissions to execute the binary or access the communication interface.

### Scan for Devices

```bash
./pulsar-cli scan
```

This command scans the CAN bus for connected PULSAR devices and lists their addresses. You need a CAN adapter connected and a [correctly wired CAN bus](../../set_up/hardware_interfaces/electrical_interfaces.md#can-bus). Use the `-h` flag to see more options.

### Get Device Parameters

```bash
./pulsar-cli params
```

This command retrieves the parameters of the connected device. Use the `-h` flag to see more options.

Examples:

```bash
./pulsar-cli params
```

This connects directly over USB.

```bash
./pulsar-cli params --port COM3 --address 0x10
```

This connects through the specified port to the actuator with address `0x10`.

### Blink Device LED

```bash
./pulsar-cli blink --address 0x10
```

This command blinks the actuator LED so that you can identify a device on the CAN bus. An address is required for this command.

### Set Home Position

```bash
./pulsar-cli home
```

This command stores the actuator's current position as the home position. The value is stored in the device's non-volatile memory and is retained after power cycling. Use the `-h` flag to see more options.

## Permission considerations

In some environments, you may need to run the CLI with `sudo`, for example:

```bash
sudo ./pulsar-cli scan
```

This is typically only necessary when your user account does not have sufficient permissions to execute the binary or access the device interface used for communication.