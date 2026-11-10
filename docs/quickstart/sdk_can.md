# Multiple actuators with Pulsar Python SDK

Use one USB-to-CAN adapter to control several physical actuators on one CAN FD bus.

## Prepare the bus

Before writing code:

1. securely mount and power every actuator;
2. wire the CAN bus with 120 Ω termination at both physical ends;
3. connect the Pulsar USB-to-CAN adapter;
4. confirm that every actuator has a unique address;
5. read [CAN FD connectivity](../hardware/connectivity/can.md).

## Find actuator addresses

After [installing Pulsar Python SDK](../sdk/install.md), scan the bus:

```bash
pixi run pulsar-cli scan --port /dev/ttyACM0
```

Replace the example addresses below with the values reported by the scan.

## Configure one group

```python
from time import sleep

from pulsar_sdk import (
    ActuatorGroup,
    ControlConfiguration,
    ControlParams,
    Mode,
    PcpOverCan,
    PulsarActuatorReal,
)

can = PcpOverCan("/dev/ttyACM0")
arm = ActuatorGroup(
    "arm",
    {
        "shoulder": PulsarActuatorReal(can, address=0x10),
        "elbow": PulsarActuatorReal(can, address=0x11),
    },
)

with arm:
    arm.configure(ControlConfiguration(Mode.VELOCITY))
    arm.enable()
    arm.set_commands({
        "shoulder": {ControlParams.COMMAND: 0.2},
        "elbow": {ControlParams.COMMAND: -0.2},
    })
    sleep(2)
    arm.disable()
```

The SDK validates the complete selected batch before the first write. Member writes are still sequential, so a later transport failure can occur after an earlier actuator was updated.

## Next steps

- [Groups and platforms](../sdk/groups_platforms.md)
- [CAN with Pulsar Python SDK](../sdk/physical/can.md)
- [CAN bus utilization](../hardware/connectivity/can_bus_utilization.md)
- [Telemetry and callbacks](../sdk/telemetry_callbacks.md)
