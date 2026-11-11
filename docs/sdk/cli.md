Pulsar Python SDK
{ .pulsar-home-eyebrow }

# Command-line interface

Installing Pulsar Python SDK provides `pulsar-cli` in the active environment.

With [Pixi](https://pixi.prefix.dev/latest/installation/), prefix commands with `pixi run`:

```bash
pixi run pulsar-cli --help
```

Commands without a serial port are identical on Linux and Windows. Where a port is required, use the platform-specific form shown below.

## Scan a CAN bus

The CLI automatically uses the adapter when exactly one Pulsar serial device is connected:

```bash
pulsar-cli scan
```

Select a port when several devices are connected:

=== "Linux"

    ```bash
    pulsar-cli scan --port /dev/ttyACM0
    ```

=== "Windows PowerShell"

    ```powershell
    pulsar-cli scan --port COM3
    ```

Optional bounds accept decimal or hexadecimal integers:

```bash
pulsar-cli scan --begin 0x10 --end 0x40 --timeout 0.12
```

## Scan virtual assets

```bash
pulsar-cli virtual-scan
```

Aliases: `vscan`, `vs`.

## Read parameters

Direct USB:

```bash
pulsar-cli params
```

CAN:

=== "Linux"

    ```bash
    pulsar-cli params --port /dev/ttyACM0 --address 16
    ```

=== "Windows PowerShell"

    ```powershell
    pulsar-cli params --port COM3 --address 16
    ```

## Identify an actuator

=== "Linux"

    ```bash
    pulsar-cli blink --port /dev/ttyACM0 --address 16
    ```

=== "Windows PowerShell"

    ```powershell
    pulsar-cli blink --port COM3 --address 16
    ```

## Zero the current position

Direct USB:

```bash
pulsar-cli home
```

CAN:

=== "Linux"

    ```bash
    pulsar-cli home --port /dev/ttyACM0 --address 0x10
    ```

=== "Windows PowerShell"

    ```powershell
    pulsar-cli home --port COM3 --address 0x10
    ```

The CLI enters `CONFIG_AND_TELEM` before requesting the zero operation.

## Change a CAN address

=== "Linux"

    ```bash
    pulsar-cli change-address --port /dev/ttyACM0 NEW_ADDRESS CURRENT_ADDRESS
    ```

=== "Windows PowerShell"

    ```powershell
    pulsar-cli change-address --port COM3 NEW_ADDRESS CURRENT_ADDRESS
    ```

Direct-USB address changes are unsupported.

Run `pulsar-cli <command> --help` for exact options.
