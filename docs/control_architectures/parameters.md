Control
{ .pulsar-home-eyebrow }

# Control parameters by mode

Pulsar Python SDK separates command-scoped `ControlParams` from readable/writable `Parameters`.

## Command-scoped fields

Every command mapping requires `ControlParams.COMMAND`.

| `ControlParams` field | Torque | Velocity | Position | Impedance |
| --- | :---: | :---: | :---: | :---: |
| `COMMAND` | ✓ | ✓ | ✓ | ✓ |
| `D_AXIS_CURRENT_KP`, `D_AXIS_CURRENT_KI` | ✓ |  |  |  |
| `Q_AXIS_CURRENT_KP`, `Q_AXIS_CURRENT_KI` | ✓ |  |  |  |
| `VELOCITY_KP`, `VELOCITY_KI` |  | ✓ | ✓ |  |
| `TORQUE_FEEDFORWARD` |  | ✓ | ✓ | ✓ |
| `POSITION_KP` |  |  | ✓ |  |
| `IMPEDANCE_STIFFNESS`, `IMPEDANCE_DAMPING` |  |  |  | ✓ |
| `IMPEDANCE_INERTIA` |  |  |  | ✓ |
| `IMPEDANCE_VELOCITY_COMMANDED` |  |  |  | ✓ |
| `IMPEDANCE_ACCELERATION_COMMANDED` |  |  |  | ✓ |

Optional command fields may be `NaN` to retain the current value. Virtual models expose shared d/q current gains and reject different finite d-axis and q-axis values in one command.

## Stored parameters

Common writable control `Parameters` include:

- torque, position, velocity;
- velocity-profile and acceleration-profile limits;
- impedance stiffness and damping;
- velocity and position loop gains;
- direction inversion;

## Presets

`TorqueGainPreset` and `VelocityGainPreset` provide `AGGRESSIVE`, `BALANCED`, and `SOFT` choices that are pre-tuned by Pulsar for different application requirements.

## Limits

Positive upper limits may use `+inf` and negative lower limits may use `-inf` where documented. Other command and parameter values must be finite.

See [Commands and parameters](../sdk/commands_parameters.md) and the [API reference](../sdk/api_reference.md) for exact names and validation.
