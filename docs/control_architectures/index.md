Control
{ .pulsar-home-eyebrow }

# Control

PULSE actuators provide four user-facing control modes.
The physical firmware and AUGUR Digital Twin models run the same low-level control algorithms at 20 kHz.

| Mode | Pulsar Python SDK enum | Primary command |
| --- | --- | --- |
| Torque control | `Mode.TORQUE` | torque in N·m |
| Speed/velocity control | `Mode.VELOCITY` | angular velocity in rad/s |
| Position control | `Mode.POSITION` | output position in rad |
| Impedance control | `Mode.IMPEDANCE` | position in rad plus optional impedance fields |

Pulsar App labels velocity mode as **Speed Control**. Pulsar Python SDK uses the more precise enum name `VELOCITY`.

## Torque

The command is converted to field-oriented current references and regulated by the motor current loop, subject to configured limits.

![Torque control signal flow](figs/control_mode_electromagnetic_torque.png)

## Velocity

An outer proportional-integral velocity loop produces the torque request for the inner torque/current control loop.

![Velocity control signal flow](figs/control_mode_speed.png)

## Position

An outer position controller generates a velocity request for the nested velocity and torque loops.

![Position control signal flow](figs/control_mode_position.png)

## Impedance

Virtual stiffness, damping, inertia, and feedforward terms produce a compliant torque request from position and velocity behavior.

![Impedance control signal flow](figs/control_mode_impedance.png)

For valid command fields and persistent parameters, continue with [Control parameters by mode](parameters.md).
