# Physical actuators

`PulsarActuatorReal` controls a physical PULSE actuator through a PCP execution domain.

Choose:

- [Direct USB](usb.md) for one actuator at address `0`.
- [CAN](can.md) for one or more actuators with unique addresses.

## Common workflow

```python
from pulsar_sdk import ControlConfiguration, Mode, PulsarActuatorReal

actuator = PulsarActuatorReal(domain, address)
with actuator:
    actuator.configure(ControlConfiguration(Mode.POSITION))
    actuator.enable()
    actuator.set_command(0.0)
    actuator.disable()
```

Physical state transitions complete only after the requested state is observed. Optional maintenance operations return a structured `FeatureResult`; operations without dedicated firmware acknowledgement may report `UNCONFIRMED`.

Physical actuator firmware must be **2.0.4 or newer**.
