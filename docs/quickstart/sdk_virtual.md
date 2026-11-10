# Virtual actuator with Pulsar Python SDK

Run a PULSE115-60G virtual actuator using AUGUR Digital Twin assets. No physical actuator, power supply, USB cable, or CAN adapter is required.

## Install the SDK and assets

```bash
pixi init pulsar-virtual-quickstart
cd pulsar-virtual-quickstart
pixi workspace channel add --prepend https://prefix.dev/pulsarhri/pulsar-forge
pixi add pulsar-sdk pulsar-assets
```

Check the installed models:

```bash
pixi run pulsar-cli virtual-scan
```

## Run the virtual actuator

Create `virtual_quickstart.py`:

```python
from pulsar_sdk import (
    ControlConfiguration,
    Mode,
    PulsarActuatorVirtual,
    TelemetryItems,
    VirtualWorld,
)

world = VirtualWorld()
actuator = PulsarActuatorVirtual(
    world,
    model="PULSE115-60G",
    address=1,
)

with actuator:
    actuator.configure(
        ControlConfiguration(
            mode=Mode.VELOCITY,
            telemetry_items=(
                TelemetryItems.POSITION,
                TelemetryItems.VELOCITY,
            ),
            telemetry_rate_hz=100,
        )
    )
    actuator.enable()
    actuator.set_command(1.0)

    for _ in range(10):
        world.step()

    print(actuator.read_telemetry((
        TelemetryItems.POSITION,
        TelemetryItems.VELOCITY,
    )))
    actuator.disable()
```

Run it:

```bash
pixi run python virtual_quickstart.py
```

`VirtualWorld.step()` advances to the next periodic telemetry event and waits for due callbacks. If periodic telemetry is disabled, each call advances one 50 µs model tick.

## Next steps

- [Virtual actuators](../sdk/virtual_actuators.md)
- [AUGUR Digital Twin concepts](../augur/index.md)
- [Co-simulation coupling](../augur/co_sim_coupling.md)
