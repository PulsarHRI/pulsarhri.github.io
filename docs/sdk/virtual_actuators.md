# Virtual actuators

`PulsarActuatorVirtual` runs a validated AUGUR Digital Twin actuator model inside a `VirtualWorld`.

## Install assets

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

`VirtualWorld.step()` advances every connected model in registration order to the next periodic telemetry event, applies supplied loads, dispatches telemetry, waits for due callbacks, and returns after callback commands are stored for the next public step.

If periodic telemetry is disabled, one call advances one 50 µs internal tick.

## External loads

```python
world.step(loads_by_address={1: 0.25})
```

Loads are finite output-shaft torques in N·m keyed by connected virtual actuator address. Positive load opposes positive output motion.

## Passive states

In `INIT_CONFIG` and `CONFIG_AND_TELEM`, the virtual plant remains mechanically movable under external load but produces passive zero torque. Telemetry is unavailable in `INIT_CONFIG`, matching physical lifecycle behavior.

## Asset isolation

Each actuator instance loads an isolated copy of its generated model library because generated models contain process-global state.

For robot dynamics and MuJoCo ownership, read [Co-simulation coupling](../augur/co_sim_coupling.md).
