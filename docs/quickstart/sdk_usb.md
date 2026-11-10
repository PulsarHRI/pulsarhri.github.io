# Single actuator with Pulsar SDK

Control one physical actuator connected directly by USB.

## Prerequisites

- the actuator is securely mounted and powered;
- it is connected directly to the computer by USB;
- its firmware is **2.0.4 or newer**;
- Python 3.10–3.13 is available on Linux or Windows.

Read [Safety and prerequisites](../hardware/safety.md) before sending a command.

## Install with Pixi

```bash
pixi init pulsar-quickstart
cd pulsar-quickstart
pixi workspace channel add --prepend https://prefix.dev/pulsarhri/pulsar-forge
pixi add pulsar-sdk
```

## Run a short velocity command

Create `quickstart.py`:

```python
from time import sleep

from pulsar_sdk import ControlConfiguration, Mode, PcpOverUsb, PulsarActuatorReal

actuator = PulsarActuatorReal(PcpOverUsb(), address=0)

with actuator:
    actuator.configure(ControlConfiguration(Mode.VELOCITY))
    actuator.enable()
    actuator.set_command(1.0)  # rad/s
    sleep(2)
    actuator.disable()
```

Run it inside the project environment:

```bash
pixi run python quickstart.py
```

The context manager connects before the body and disconnects when the body exits. `disable()` turns drive output off while keeping runtime telemetry available until disconnect.

!!! danger
    Do not rely on Python object destruction to stop hardware. Use `disable()` and `disconnect()`, preferably through a context manager as shown above.

## Next steps

- [Core workflow](../sdk/core_workflow.md)
- [Direct USB](../sdk/physical/usb.md)
- [Commands and parameters](../sdk/commands_parameters.md)
- [Lifecycle and recovery](../sdk/lifecycle_recovery.md)
