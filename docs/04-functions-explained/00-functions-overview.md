# Actuator class overview

The PulsarActuator class is the core of the Pulsar Control Protocol (PCP) communication interface. It provides a high-level API for interacting with and managing Pulsar motors or actuators via the CAN bus. Key capabilities include:

* **Real-Time Command and Control**: Send precise control commands to the actuator in real time.
* **Mode Switching**: Seamlessly transition between various control modes such as torque, velocity, position, and impedance.
* **Live Feedback Monitoring**: Continuously receive and process real-time feedback from the actuator via CAN messages.
* **Parameter Configuration and Management**: Set, retrieve, and persist actuator parameters for fine-tuned performance.
* **Diagnostics and Health Monitoring**: Access diagnostic data to evaluate actuator status and detect potential issues.

## Initialization and Constructor

To create an instance of the PulsarActuator class, you need to provide a CAN bus handler and the actuator’s CAN address. Optionally, you can supply a custom logger for debugging and monitoring purposes.
```py title="Create an instance of the PulsarActuator class"
PulsarActuator(canbus_handler, address: int, logger=None)
```

## Connection and Address Management

* **Connecting to the Actuator**: Use the [connect()](02-pcp-api-functions.md/#connecttimeout10-bool) method to initiate communication.
* **Disconnecting from the Actuator**: Use the [disconnect()](02-pcp-api-functions.md/#disconnect) method to safely terminate communication.
* **Pinging the Actuator**: Use the [send_ping()](02-pcp-api-functions.md/#send_pingtimeout10-bool) method to check if a specific CAN address is active and responsive.
* **Changing the Actuator's CAN Address**: Use the [changeAddress(new_address)](02-pcp-api-functions.md/#changeaddressnew_address) method to assign a specific address.


## Predefined Performance Profiles
The actuator provides predefined performance profiles for both [torque](02-pcp-api-functions.md/#set_torque_performanceperformance-torqueperformance) and [speed](02-pcp-api-functions.md/#set_speed_performanceperformance-speedperformance) control loops:

* **Torque Control Loop Performance**: Profiles include AGGRESSIVE, BALANCED, SOFT.
* **Speed Loop Performance**: Profiles include AGGRESSIVE, BALANCED, SOFT, and CUSTOM. In this case all the profiles have a similar response time without load, making it more agressive implies a faster rejection time of a perturbation. The parameters are obtained for the no-load motor operation.

### Torque Control Loop Performance

This setting determines how quickly and aggressively the actuator responds to torque commands. The available profiles are:

#### AGGRESSIVE

- **Bandwidth**: ~1000 Hz  
- **Behavior**: Maximizes responsiveness and torque application speed.  
- **Use Case**: Ideal for dynamic tasks such as impedance control or joint torque control.  
- **Trade-off**: May reduce steady-state precision.

#### BALANCED

- **Bandwidth**: ~500 Hz  
- **Behavior**: Offers a compromise between responsiveness and stability.  
- **Use Case**: Suitable for general-purpose applications.

#### SOFT

- **Bandwidth**: ~100 Hz  
- **Behavior**: Prioritizes smoothness and precision over speed.  
- **Use Case**: Best for tasks requiring high torque fidelity and low noise.  
- **Trade-off**: Lower responsiveness.

**Table – TorquePerformance**

| Name       | Value | Bandwidth (Hz) | Description                                 |
|------------|-------|----------------|---------------------------------------------|
| AGGRESSIVE | 1     | ~1000 Hz       | Fast response, less precision in steady state |
| BALANCED   | 2     | ~500 Hz        | Balanced between response and stability     |
| SOFT       | 3     | ~100 Hz        | Stable and quiet, low responsiveness        |

## Changing Control Modes
Use the [change_mode(mode)](02-pcp-api-functions.md/#change_modemode-mode) method to switch between control modes such as CALIBRATION, FVI, OPEN_LOOP, DVI, TORQUE, SPEED, POSITION, and IMPEDANCE.

## Actuator Control: Start and Stop
* **Start**: Use the [start()](02-pcp-api-functions.md/#start) method to initiate the actuator's operation.
* **Stop**: Use the [stop()](02-pcp-api-functions.md/#stop) method to halt the actuator's current motion.

## Save Configuration
Use the [save_config()](02-pcp-api-functions.md/#save_config) method to store the current settings in non-volatile memory.

## Feedback Configuration

The PulsarActuator API supports two feedback channels with configurable update rates:
* **High-Frequency Feedback**: For fast-changing signals (e.g., torque, speed).
* **Low-Frequency Feedback**: For slower or less critical signals (e.g., temperature, voltage).

## Actuator Calibration
Use the [calibrate()](02-pcp-api-functions.md/#calibrate) method to perform internal calibration routines.

!!! warning
    DO NOT USE THIS UNLESS SPECIFIED BY PULSAR TEAM

