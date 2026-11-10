# Command-line interface

Installing Pulsar SDK provides `pulsar-cli` in the active environment.

With Pixi, prefix commands with `pixi run`:

```bash
pixi run pulsar-cli --help
```

## Scan a CAN bus

```bash
pulsar-cli scan --port /dev/ttyACM0
```

Optional bounds accept decimal or hexadecimal integers:

```bash
pulsar-cli scan --begin 0x10 --end 0x40 --timeout 0.12
```

## Scan virtual assets

```bash
pulsar-cli virtual-scan
```

Aliases: `vsan`, `vs`.

## Read parameters

Direct USB:

```bash
pulsar-cli params
```

CAN:

```bash
pulsar-cli params --port /dev/ttyACM0 --address 0x10
```

## Identify an actuator

```bash
pulsar-cli blink --port /dev/ttyACM0 --address 0x10
```

## Zero the current position

Direct USB:

```bash
pulsar-cli home
```

CAN:

```bash
pulsar-cli home --port /dev/ttyACM0 --address 0x10
```

The CLI enters `CONFIG_AND_TELEM` before requesting the zero operation.

## Change a CAN address

```bash
pulsar-cli change-address --port /dev/ttyACM0 NEW_ADDRESS CURRENT_ADDRESS
```

Direct-USB address changes are unsupported.

Run `pulsar-cli <command> --help` for exact options.
