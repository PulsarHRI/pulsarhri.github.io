Pulsar Python SDK
{ .pulsar-home-eyebrow }

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

Physical state transitions complete only after the requested state is observed. After communication loss, the SDK reports `UNKNOWN` rather than assuming the previous state is still safe.

CAN addresses must be unique within one `PcpOverCan` domain and lie in `16..16382`. Direct USB supports one actuator at address `0`.

Address change, identify, parameter persistence, bootloader entry, and CAN bit-rate switching are physical-only capabilities. Check `supports()` or the returned `FeatureResult` instead of assuming every transport provides them. Operations without dedicated firmware acknowledgement may report `UNCONFIRMED`.

Physical actuator firmware must be **2.0.4 or newer**.
