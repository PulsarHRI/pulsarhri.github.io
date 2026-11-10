# Control parameters by mode

Pulsar Python SDK separates command-scoped `ControlParams` from readable/writable `Parameters`.

## Command-scoped fields

Every command mapping requires `ControlParams.COMMAND`.

| `ControlParams` field | Torque | Velocity | Position | Impedance |
| --- | :---: | :---: | :---: | :---: |
| `COMMAND` | ✓ | ✓ | ✓ | ✓ |
| `D_AXIS_CURRENT_KP`, `D_AXIS_CURRENT_KI` | ✓ |  |  |  |
| `Q_AXIS_CURRENT_KP`, `Q_AXIS_CURRENT_KI` | ✓ |  |  |  |
| `FEEDFORWARD_GAIN` |  | ✓ | ✓ | ✓ |
| `VELOCITY_KP`, `VELOCITY_KI` |  | ✓ | ✓ |  |
| `TORQUE_FEEDFORWARD` |  | ✓ | ✓ | ✓ |
| `POSITION_KP` |  |  | ✓ |  |
| `IMPEDANCE_STIFFNESS`, `IMPEDANCE_DAMPING` |  |  |  | ✓ |
| `IMPEDANCE_INERTIA` |  |  |  | ✓ |
| `IMPEDANCE_VELOCITY_COMMANDED` |  |  |  | ✓ |
| `IMPEDANCE_ACCELERATION_COMMANDED` |  |  |  | ✓ |

Optional command fields may be `NaN` to retain the current value. Virtual models expose shared d/q current gains and reject different finite d-axis and q-axis values in one command.

## Stored parameters

Common writable `Parameters` include:

- torque, position, velocity, profile-velocity, and profile-acceleration limits;
- impedance stiffness and damping;
- velocity and position loop gains;
- direction inversion;
- feedforward gain;
- velocity and current filter cutoffs;
- CAN bit-rate switching.

Writes are allowed only while drive output is inactive.

Use dedicated methods instead of parameter writes for:

- mode;
- runtime commands;
- torque and velocity gain presets;
- actuator address;
- periodic telemetry rate;
- persistence.

## Presets

`TorqueGainPreset` and `VelocityGainPreset` provide `AGGRESSIVE`, `BALANCED`, and `SOFT` choices.

## Limits

Positive upper limits may use `+inf` and negative lower limits may use `-inf` where documented. Other command and parameter values must be finite.

See [Commands and parameters](../sdk/commands_parameters.md) and the [API reference](../sdk/api_reference.md) for exact names and validation.
