# Commands and parameters

Pulsar SDK distinguishes runtime commands from stored or readable parameters.

## Primary command

A standalone actuator accepts a scalar command:

```python
actuator.set_command(0.5)
```

The unit depends on the configured mode:

| Mode | Unit |
| --- | --- |
| `TORQUE` | N·m |
| `VELOCITY` | rad/s |
| `POSITION` | rad |
| `IMPEDANCE` | position in rad |

Commands must be finite and are accepted only in `DRIVE_ACTIVE`.

## Mode-specific command fields

```python
from pulsar_sdk import ControlParams

actuator.set_command({
    ControlParams.COMMAND: 0.5,
    ControlParams.VELOCITY_KP: 1.2,
})
```

Every mapping requires `ControlParams.COMMAND`. Optional fields may use `NaN` to keep their current value.

| Field | Allowed modes |
| --- | --- |
| `D_AXIS_CURRENT_KP`, `D_AXIS_CURRENT_KI` | torque |
| `Q_AXIS_CURRENT_KP`, `Q_AXIS_CURRENT_KI` | torque |
| `FEEDFORWARD_GAIN` | velocity, position, impedance |
| `VELOCITY_KP`, `VELOCITY_KI` | velocity, position |
| `TORQUE_FEEDFORWARD` | velocity, position, impedance |
| `POSITION_KP` | position |
| `IMPEDANCE_STIFFNESS`, `IMPEDANCE_DAMPING`, `IMPEDANCE_INERTIA` | impedance |
| `IMPEDANCE_VELOCITY_COMMANDED`, `IMPEDANCE_ACCELERATION_COMMANDED` | impedance |

## Group commands

```python
arm.set_commands({
    "shoulder": {ControlParams.COMMAND: 0.2},
    "elbow": {ControlParams.COMMAND: -0.2},
})
```

Direct batch failures raise `CommandTransmissionError`. Its `successful_members` field identifies writes completed before the failure.

## Parameters

Read parameters with enum identity preserved:

```python
from pulsar_sdk import Parameters

values = actuator.read_parameters((
    Parameters.TORQUE_LIMIT,
    Parameters.POSITION_KP,
))
```

Write parameters only while drive output is inactive:

```python
actuator.set_parameters({
    Parameters.TORQUE_LIMIT: 2.0,
    Parameters.POSITION_KP: 0.8,
})
```

Use dedicated methods for mode, commands, gain presets, address, telemetry rate, and persistence.

## Unified group or platform updates

Parameter and preset methods accept `unify=True` to apply one value across represented actuators. Commands intentionally do not support `unify=True`.

## Atomicity

Validation occurs before transmission, but parameter, preset, and member command writes are not transactional. A transport failure can leave earlier writes applied and later writes unapplied.

See the [API reference](api_reference.md#parameters) for every parameter and exact validation rule.
