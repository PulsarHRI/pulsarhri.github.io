# Class Definitions
## Overview of the PulsarActuator Communication Interface
At the core of PCP (Pulsar Control Protocol) communication lies the PulsarActuator class. This class serves as the primary high-level interface for interacting with and managing a Pulsar motor or actuator controller via the CAN (Controller Area Network) bus. It abstracts the complexities of low-level communication, providing developers with a streamlined and intuitive API for real-time control and monitoring.

## Key Capabilities of the PulsarActuator API
The PulsarActuator class offers a comprehensive suite of features designed to facilitate robust and flexible actuator control. These include:

* Real-Time Command and Control: Send precise control commands to the actuator in real time.
* Mode Switching: Seamlessly transition between various control modes such as torque, velocity, position, and impedance.
* Live Feedback Monitoring: Continuously receive and process real-time feedback from the actuator via CAN messages.
* Parameter Configuration and Management: Set, retrieve, and persist actuator parameters for fine-tuned performance.
* Diagnostics and Health Monitoring: Access diagnostic data to evaluate actuator status and detect potential issues.

## What This Class Definition Covers
This manual provides detailed guidance on how to effectively use the PulsarActuator class to:

### Operate the actuator in multiple control modes, including:

* Torque Control: Apply a specific torque to the actuator.
* Speed Control: Regulate the actuator’s rotational velocity.
* Position Control: Move the actuator to a defined position.
* Impedance Control: Combine position and force control for compliant motion.
### Configure and query actuator parameters, such as:
* PID gains
* Safety limits
* Communication settings

### Receive and interpret real-time feedback, including:

* Position, velocity, and torque readings
* Temperature and voltage levels
* Error and status flags

### Modify actuator settings and perform diagnostics, enabling:
* Firmware updates
* Fault detection and recovery
* System calibration and tuning