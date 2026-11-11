Quickstart
{ .pulsar-home-eyebrow }

# Multiple physical actuators over CAN FD with Pulsar Python SDK

Use one USB-to-CAN adapter to control several physical actuators on one CAN FD bus.

## Prepare the bus

Before writing code:

1. securely mount and power every actuator;
2. wire the CAN bus with 120 Ω termination at both physical ends;
3. connect the Pulsar USB-to-CAN adapter;
4. confirm that every actuator has a unique address using `pulsar-cli`;
5. read [CAN FD connectivity](../hardware/connectivity/can.md).

## Find actuator addresses

After [installing Pulsar Python SDK](../sdk/install.md), scan the bus:

```bash
pixi run pulsar-cli scan
# if you have multiple Pulsar devices connected
pixi run pulsar-cli scan --port /dev/ttyACM0 # on linux
pixi run pulsar-cli scan --port COM3 # Windows
```
Replace ports with the exact ports on your machine.

## Configure one group
Replace the example addresses below with the values reported by the scan.

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

can = PcpOverCan()
arm = ActuatorGroup(
    "arm",
    {
        "shoulder": PulsarActuatorReal(can, address=23),
        "elbow": PulsarActuatorReal(can, address=24),
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

Use can.list_ports() and provide the port to 'can.port = chosen_port' if multiple are available, otherwise the correct port is detected and chosen automatically.

The SDK validates the complete selected batch before the first write. Member writes are still sequential, so a later transport failure can occur after an earlier actuator was updated.

## Next steps

- [Groups and platforms](../sdk/groups_platforms.md)
- [CAN with Pulsar Python SDK](../sdk/physical/can.md)
- [CAN bus utilization](../hardware/connectivity/can_bus_utilization.md)
- [Telemetry and callbacks](../sdk/telemetry_callbacks.md)
