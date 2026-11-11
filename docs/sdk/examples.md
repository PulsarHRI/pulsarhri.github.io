Pulsar Python SDK
{ .pulsar-home-eyebrow }

# Examples

The maintained examples repository will be published as:

[github.com/PulsarHRI/pulsar-sdk-examples](https://github.com/PulsarHRI/pulsar-sdk-examples)

It is organized by user goal and will contain Python examples plus future Rust examples.

## First-release example set

### Physical actuator over USB

Use the complete [Physical actuator over direct USB with Pulsar Python SDK](../quickstart/sdk_usb.md).

### Scan and use CAN

Use [Multiple physical actuators over CAN FD with Pulsar Python SDK](../quickstart/sdk_can.md) and [CAN](physical/can.md).

### Virtual actuator

Use [Virtual actuator with Pulsar Python SDK](../quickstart/sdk_virtual.md).

### Telemetry logging

```python
import csv
from time import sleep

from pulsar_sdk import (
    ControlConfiguration,
    Mode,
    PcpOverUsb,
    PulsarActuatorReal,
    TelemetryItems,
)

items = (TelemetryItems.POSITION, TelemetryItems.VELOCITY)
actuator = PulsarActuatorReal(PcpOverUsb(), address=0)

with actuator, open("telemetry.csv", "w", newline="") as output:
    writer = csv.writer(output)
    writer.writerow(("position_rad", "velocity_rad_s"))

    def log_sample(address, telemetry):
        writer.writerow((telemetry[items[0]], telemetry[items[1]]))

    actuator.configure(ControlConfiguration(Mode.VELOCITY, items, 100))
    actuator.set_telemetry_callback(log_sample)
    actuator.enable()
    actuator.set_command(0.0)
    sleep(2)
    actuator.disable()
    actuator.set_telemetry_callback(None)
```

### Multiple actuators in one group

```python
arm.set_commands({
    "shoulder": {ControlParams.COMMAND: 0.2},
    "elbow": {ControlParams.COMMAND: -0.2},
})
```

### Platform callback

```python
def controller(metadata, telemetry):
    return {
        name: {ControlParams.COMMAND: 0.0}
        for name in telemetry
    }

robot.set_control_callback(controller)
```

The callback runs independently for each group. Use `metadata.group_name` when behavior differs by group.

### Diagnostics and recovery

```python
status = arm.status
if status.last_host_error is not None:
    # Fix the reported cause first.
    if arm.clear_faults():
        arm.resume()
```

If diagnostic safety entered `INIT_CONFIG`, use `recover()` after the physical condition is clear.

### Two CAN domains in one platform

Use a separate `PcpOverCan` domain for each USB-to-CAN adapter. The platform coordinates lifecycle and safety, while each group keeps its own telemetry stream and callback timing.

```python
from pulsar_sdk import (
    ActuatorGroup,
    ControlConfiguration,
    ControlParams,
    Mode,
    PcpOverCan,
    Platform,
    PulsarActuatorReal,
    TelemetryItems,
)

right_can = PcpOverCan("<right-adapter-port>")
left_can = PcpOverCan("<left-adapter-port>")

right_arm = ActuatorGroup(
    "right_arm",
    {
        "shoulder": PulsarActuatorReal(right_can, address=23),
        "elbow": PulsarActuatorReal(right_can, address=24),
    },
)
left_arm = ActuatorGroup(
    "left_arm",
    {
        "shoulder": PulsarActuatorReal(left_can, address=23),
        "elbow": PulsarActuatorReal(left_can, address=24),
    },
)
robot = Platform({"right_arm": right_arm, "left_arm": left_arm})
configuration = ControlConfiguration(
    mode=Mode.IMPEDANCE,
    telemetry_items=(
        TelemetryItems.POSITION,
        TelemetryItems.VELOCITY,
    ),
    telemetry_rate_hz=500,
)


def controller(metadata, telemetry):
    return {
        name: {ControlParams.COMMAND: values[TelemetryItems.POSITION]}
        for name, values in telemetry.items()
    }


with robot:
    robot.configure({
        "right_arm": configuration,
        "left_arm": configuration,
    })
    robot.zero_position()
    robot.set_control_callback(controller)
    robot.enable()

    # Run the application control loop here.

    robot.disable()
```

The same actuator addresses may be reused because the adapters are separate domains. Replace the port placeholders with values returned by `PcpOverCan.list_ports()`.

### Mixed physical and virtual platform

```python
from pulsar_sdk import (
    ActuatorGroup,
    ControlConfiguration,
    ControlParams,
    Mode,
    PcpOverUsb,
    Platform,
    PulsarActuatorReal,
    PulsarActuatorVirtual,
    TelemetryItems,
    VirtualWorld,
)

physical = ActuatorGroup(
    "physical",
    {"joint": PulsarActuatorReal(PcpOverUsb(), address=0)},
)
world = VirtualWorld()
virtual = ActuatorGroup(
    "virtual",
    {"joint": PulsarActuatorVirtual(world, model="PULSE115-60G", address=1)},
)
robot = Platform({"physical": physical, "virtual": virtual})
configuration = ControlConfiguration(
    Mode.VELOCITY,
    (TelemetryItems.VELOCITY,),
    100,
)


def controller(metadata, telemetry):
    return {
        "joint": {ControlParams.COMMAND: 0.0}
    }


with robot:
    robot.configure({"physical": configuration, "virtual": configuration})
    robot.set_control_callback(controller)
    robot.enable()

    # Physical telemetry arrives from its serial domain. The application must
    # explicitly advance the independent virtual simulation domain.
    for _ in range(100):
        world.step()

    robot.disable()
```

A platform coordinates lifecycle and safety across these groups, but it does not merge their telemetry or synchronize their independent clocks.

!!! warning
    Motion examples must be validated on the intended hardware and mechanism before publication or reuse. Start with conservative commands and limits.
