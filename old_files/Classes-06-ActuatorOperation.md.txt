# Actuator Operation: Startup, Shutdown, and Control Modes

## Overview of Operation Modes

Before initiating any actuator movement, it is essential to configure the appropriate control mode. The selected mode determines how the actuator interprets and responds to setpoints. Once a control mode is active, the system will establish the corresponding setpoint based on the mode’s logic and parameters.

## Startup Calibration Mode

!!! important
    DO NOT USE THIS MODE UNLESS SPECIFIED BY PULSAR DEVELOPMENT TEAM

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

!!! warning
    DO NOT USE THIS MODE AS IT IS UNDER DEVELOPMENT

This advanced mode simulates mechanical impedance (stiffness and damping) by manipulating motor currents at a low level. It is particularly useful for applications requiring compliant or human-interactive behavior. 

## Special-Purpose Modes

!!! warning
    DO NOT USE THESE MODES UNLESS SPECIFIED BY PULSAR DEVELOPMENT TEAM

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

## Set Zero Position

The Set Zero Position command is used to redefine the actuator's current physical location as the new reference point, or "zero" position, for all subsequent position-based operations. For Position or Impedance Mode, defining a consistent starting point is critical. Therefore, before commanding absolute positions, you must perform a zero-positioning action to establish the actuator's current location as the reference zero. Failure to do so will result in unpredictable or incorrect absolute positioning.

`reset_encoder_position(self)`: Resets the encoder absolute position to 0.

## Actuator Control: Start and Stop 

Once the actuator has been configured with the desired control mode and setpoint, these methods are used to initiate and cease its motion. 

To initiate the actuator's operation, causing it to reach and maintain its configured setpoint according to the active control mode, use the following command: 

`start()`:  Starts the actuator. 

To halt the actuator's current motion and operation, use the following command: 

`stop()`: Stops the actuator. 

## Save configuration

After configuring the actuator parameters (e.g., control mode, gains, limits), it is important to store the current settings to ensure they persist after a power cycle. The command that saves the current actuator configuration to non-volatile memory—making it the default startup configuration—is: 

`save_config(self)`: Saves the current configuration of the actuator in the non-volatile memory.

## Actuator calibration

The actuator includes an internal calibration routine that can be triggered directly. During calibration, the system performs offset calibration for both current sensing and position measurement—aligning the motor’s electrical position with the mechanical position of the encoder. As part of this process, the relative position (turn count) is reset to zero. This command should not be used.

The command to perform the actuator calibration is: 

`calibrate()`: Calibrates the actuator.

!!! important
    Note that not all parameters apply to every control mode; refer to **Table 7** for specific usage information. 

## Table 7 – Use of the parameters depending on the control type

| Parameter                                | Calibration (CtrlType = 1) | FVI (CtrlType = 2) | Open loop (CtrlType = 3) | DVI (CtrlType = 4) | Torque control (CtrlType = 5) | Speed control (CtrlType = 6) | Position control (CtrlType = 7) | Impedance control (CtrlType = 8) |
|------------------------------------------|----------------------------|--------------------|---------------------------|--------------------|-------------------------------|------------------------------|----------------------------------|------------------------------------|
| Torque loop performance                  | No                         | No                 | No                        | No                 | Yes                           | Yes                          | Yes                              | Yes                                |
| Speed loop performance                   | No                         | No                 | No                        | No                 | No                            | Yes                          | Yes                              | No                                 |
| Kp position                              | No                         | No                 | No                        | No                 | No                            | No                           | Yes                              | No                                 |
| Kp speed                                 | No                         | No                 | No                        | No                 | No                            | Yes (if custom selected)     | Yes (if custom selected)         | No                                 |
| Ki speed                                 | No                         | No                 | No                        | No                 | No                            | Yes (if custom selected)     | Yes (if custom selected)         | No                                 |
| Stiffness gain                           | No                         | No                 | No                        | No                 | No                            | No                           | No                               | Yes                                |
| Damping gain                             | No                         | No                 | No                        | No                 | No                            | No                           | No                               | Yes                                |
| FF torque                                | No                         | No                 | No                        | No                 | No                            | No                           | No                               | Yes                                |
| Max positive speed (rad/s) (Profile)     | No                         | No                 | No                        | No                 | No                            | No                           | Yes                              | No                                 |
| Min negative speed (rad/s) (Profile)     | No                         | No                 | No                        | No                 | No                            | No                           | Yes                              | No                                 |
| Max acceleration (rad/s²) (Profile)      | No                         | No                 | No                        | No                 | No                            | Yes                          | Yes                              | No                                 |
| Max deceleration (rad/s²) (Profile)      | No                         | No                 | No                        | No                 | No                            | Yes                          | Yes                              | No                                 |
| Max speed (rad/s)                        | No                         | No                 | No                        | No                 | No                            | Yes                          | Yes                              | No                                 |
| Min speed (rad/s)                        | No                         | No                 | No                        | No                 | No                            | Yes                          | Yes                              | No                                 |
| Max position (rad)                       | No                         | No                 | No                        | No                 | No                            | No                           | Yes                              | Yes                                |
| Min position (rad)                       | No                         | No                 | No                        | No                 | No                            | No                           | Yes                              | Yes                                |
| Max absolute torque (Nm)                 | Yes (for the debug bus)    | Yes (for the debug bus) | Yes (for the debug bus)   | Yes (for the debug bus) | Yes                       | Yes                          | Yes                              | Yes                                |


