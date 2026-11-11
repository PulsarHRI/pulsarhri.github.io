Pulsar Python SDK
{ .pulsar-home-eyebrow }

# Groups and platforms

Use an `ActuatorGroup` for named actuators that share one execution domain and one control mode. Use a `Platform` to coordinate one or more groups, including groups on different domains.

## Actuator group

```python
from pulsar_sdk import ActuatorGroup, PcpOverCan, PulsarActuatorReal

can = PcpOverCan()
arm = ActuatorGroup(
    "arm",
    {
        "shoulder": PulsarActuatorReal(can, 0x10),
        "elbow": PulsarActuatorReal(can, 0x11),
    },
)
```

Group rules:

- every member belongs to the same domain;
- every member uses the same control mode;
- an actuator belongs to at most one active group;
- names and mappings remain stable and read-only;
- closing a group detaches its members for reuse.

## Configure and command a group

```python
from pulsar_sdk import ControlConfiguration, ControlParams, Mode

with arm:
    arm.configure(ControlConfiguration(Mode.VELOCITY))
    arm.enable()
    arm.set_commands({
        "shoulder": {ControlParams.COMMAND: 0.2},
        "elbow": {ControlParams.COMMAND: -0.2},
    })
    arm.disable()
```

A selected command batch may contain only some members; omitted members retain their previous device command. The whole selected batch is validated before writes begin, but member transmission is sequential rather than transactional.

## Platform

```python
from pulsar_sdk import Platform

robot = Platform({
    "right_arm": right_arm,
    "left_arm": left_arm,
})
```

A platform:

- keeps a stable, read-only mapping of group names;
- coordinates connect, configure, enable, disable, and recovery;
- can span several execution domains;
- propagates active safety across its groups;
- does not merge telemetry batches across domains;
- does not claim cross-domain clock synchronization.

## Configure a platform

```python
configuration = ControlConfiguration(Mode.IMPEDANCE)

with robot:
    robot.configure({
        "right_arm": configuration,
        "left_arm": configuration,
    })
    robot.enable()
    robot.disable()
```

Platform operations validate selected groups before writing and attempt safety-critical cleanup across all groups before reporting aggregate failures. They are not transactional across actuators or domains.

## Lifecycle routing

If an actuator belongs to a group, lifecycle operations invoked through that actuator route through the group. This prevents one member from silently changing the shared group lifecycle.
