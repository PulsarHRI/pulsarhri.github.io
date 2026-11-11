Pulsar Python SDK
{ .pulsar-home-eyebrow }

# Virtual actuators

`PulsarActuatorVirtual` runs a validated AUGUR Digital Twin actuator model inside a `VirtualWorld`.

## Install assets

Install [Pixi](https://pixi.prefix.dev/latest/installation/) first. The following commands are identical on Linux and Windows:

```bash
pixi workspace channel add --prepend https://prefix.dev/pulsarhri/pulsar-forge
pixi add pulsar-sdk pulsar-assets
```

List models available on the current host:

```bash
pixi run pulsar-cli virtual-scan
```

Supported models are:

- `P90`
- `P100`
- `PULSE98-30G`
- `PULSE98-55G`
- `PULSE115-60G`
- `PULSE115-110G`

## Create a world and actuator

```python
from pulsar_sdk import PulsarActuatorVirtual, VirtualWorld

world = VirtualWorld()
actuator = PulsarActuatorVirtual(
    world,
    model="PULSE115-60G",
    address=1,
)
```

Without an explicit `assets_path`, lookup checks `PULSAR_ASSETS_PATH` and then active Conda/Python environment asset locations.

## Configure and step

```python
from pulsar_sdk import ControlConfiguration, Mode, TelemetryItems

with actuator:
    actuator.configure(
        ControlConfiguration(
            Mode.POSITION,
            (TelemetryItems.POSITION, TelemetryItems.VELOCITY),
            500,
        )
    )
    actuator.enable()
    actuator.set_command(0.5)

    for _ in range(100):
        world.step()

    actuator.disable()
```

`VirtualWorld.step()`:

1. finds the earliest next periodic telemetry event among connected virtual actuators;
2. applies supplied loads for the required internal model ticks;
3. advances connected models in registration order;
4. delivers due telemetry;
5. waits for due actuator and group callbacks;
6. returns after callback commands are stored for the next public step.

If periodic telemetry is disabled, one call advances one 50 µs internal tick. Disconnected actuators do not participate in stepping and cannot stop other models in the world.

## External loads

```python
world.step(loads_by_address={1: 0.25})
```

Loads are finite output-shaft torques in N·m keyed by connected virtual actuator address. Positive load opposes positive output motion.

## Passive states

In `INIT_CONFIG` and `CONFIG_AND_TELEM`, the virtual plant remains mechanically movable under external load but produces passive zero torque. Telemetry is unavailable in `INIT_CONFIG`, matching physical lifecycle behavior. `DRIVE_ACTIVE` restores the configured control mode.

Telemetry staleness uses simulation time, so pausing the application or debugger does not fault a world that is not advancing. Raw or device-only telemetry is unsupported; virtual `BUS_VOLTAGE` reports the model's fixed 48 V supply.

Position reset occurs on one world-owned 50 µs tick. Every connected actuator advances on that tick, and members of one group reset together.

## Asset isolation

Each actuator instance loads an isolated copy of its generated model library because generated models contain process-global state.

For robot dynamics and MuJoCo ownership, read [Co-simulation coupling](../augur/co_sim_coupling.md).
