# Direct USB

Use `PcpOverUsb` for one actuator connected directly to the computer. The actuator address must be `0`.

```python
from pulsar_sdk import PcpOverUsb, PulsarActuatorReal

usb = PcpOverUsb()  # Auto-detect when one Pulsar serial device is available.
actuator = PulsarActuatorReal(usb, address=0)
```

Pass a port when auto-detection is ambiguous:

```python
usb = PcpOverUsb("/dev/ttyACM0")
```

On Windows, use a port such as `COM3`.

## Complete short run

```python
from time import sleep

from pulsar_sdk import ControlConfiguration, Mode, PcpOverUsb, PulsarActuatorReal

actuator = PulsarActuatorReal(PcpOverUsb(), address=0)
with actuator:
    actuator.configure(ControlConfiguration(Mode.VELOCITY))
    actuator.enable()
    actuator.set_command(1.0)
    sleep(2)
    actuator.disable()
```

See [Direct USB hardware connectivity](../../hardware/connectivity/usb.md) for wiring and [Safety and prerequisites](../../hardware/safety.md) before running motion code.
