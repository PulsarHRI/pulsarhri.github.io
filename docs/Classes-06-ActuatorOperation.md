# Actuator Operation: Startup, Shutdown, and Control Modes

## Overview of Operation Modes

Before initiating any actuator movement, it is essential to configure the appropriate control mode. The selected mode determines how the actuator interprets and responds to setpoints. Once a control mode is active, the system will establish the corresponding setpoint based on the mode’s logic and parameters.

## Startup Calibration Mode

When the actuator is powered on with the control mode set to **Calibration**, the system performs an automatic offset calibration. This process aligns the electrical position of the motor with the mechanical position of the encoder, ensuring accurate motion control.

During this calibration:

- The relative position (also known as the "turn count") is reset to zero.
- **Note:** This does not affect the absolute position. To reset the absolute position, the `Set Zero Position` command must be used separately.

## Standard Control Modes

The actuator supports several core control strategies, each optimized for specific performance characteristics:

### 1. Electromagnetic Torque Control

This mode directly controls the torque output of the actuator by regulating the motor current. It includes three predefined profiles, each offering a different control bandwidth—from conservative to aggressive—tailored for various application needs.

### 2. Speed Control

Speed control is implemented using a dual-loop architecture:

- The inner loop manages torque via current control.
- The outer loop regulates speed using a Proportional-Integral (PI) controller.

Users can either manually tune the PI parameters or select from optimized preset profiles.

### 3. Position Control

Position control is achieved through a hierarchical control structure:

- A proportional controller governs the position loop.
- This loop operates over the speed and torque control layers, ensuring smooth and accurate positioning.

### 4. Impedance Control (Under development)

!!! important
    DO NOT USE THIS MODE AS IT IS UNDER DEVELOPMENT

This advanced mode simulates mechanical impedance (stiffness and damping) by manipulating motor currents at a low level. It is particularly useful for applications requiring compliant or human-interactive behavior. 

## Special-Purpose Modes

In addition to the standard modes, the actuator includes several specialized modes designed for debugging, testing, and system integration. These are not intended for regular operation but are invaluable during development and troubleshooting:

### Fixed Voltage Injection (FVI)

Injects a constant DC voltage into the motor phases. Useful for basic motor testing and diagnostics.

### Open-Loop Mode

Applies a rotating voltage vector to the motor using a V/f (voltage-to-frequency) control method. This mode typically runs at a constant speed or can be configured with user-defined parameters.

### Direct Voltage Injection (DVI)

Allows manual control of the voltage vector applied to the motor phases. The internal encoder is used to orient the voltage field, enabling precise testing of motor response.

## Changing Control Modes

To switch between control modes, use the following method:

**Parameters:**

- `mode (PulsarActuatorMode)`: The desired control mode to activate. Refer to **Table 6** for a complete list of available modes and their descriptions.

## Table 6 – Mode (Enum)

| Mode Name     | Enum Value | Description                              |
|---------------|------------|------------------------------------------|
| CALIBRATION   | `0x01`     | Calibration mode                         |
| FVI           | `0x02`     | Fixed Voltage Injection                  |
| OPEN_LOOP     | `0x03`     | Open-loop control                        |
| DVI           | `0x04`     | Direct Voltage Injection (field-oriented)|
| TORQUE        | `0x05`     | Electromagnetic Torque Control           |
| SPEED         | `0x06`     | Speed Control                            |
| POSITION      | `0x07`     | Position Control                         |
| IMPEDANCE     | `0x08`     | Impedance Control                        |

