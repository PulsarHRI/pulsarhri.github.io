# Set Up Real Actuators

This page walks you through the mechanical and electrical setup of a real PULSAR actuator, excluding communication. For guidance on connecting via USB or CAN, see the next section: [Communicate with Real Actuators](../communicate/communicate_real.md).

## 🧰 What You’ll Need

Usually provided by PULSAR HRI:

* 1x PULSAR HRI **actuator**
* 1x **Power Bus Cable** ([more details here](../set_up/hardware_interfaces/electrical_interfaces.md#power-bus-cable))

Usually NOT provided by PULSAR HRI:

* A **mechanical support** and **screws** to secure the actuator ([see mounting hole patterns and printable designs](../set_up/hardware_interfaces/mechanical_interfaces.md))
* A **48V Power Supply Unit** ([more details here](../set_up/hardware_interfaces/electrical_interfaces.md#power-bus))
* A **Computer** (only needed later for communication setup)

!!! Operating-System-Compatibility
Currently the ecosystem is mainly compatible with, and tested on Windows and Linux Ubuntu operating systems

## 👣 Step-By-Step Guide

1. **Mechanically mount** the actuator using the recommended fixture or a custom support. Refer to [Mechanical Interfaces](../set_up/hardware_interfaces/mechanical_interfaces.md) for guidance.

2. **Connect the Power Bus Cable**:

   * Plug the Power Bus Cable into the actuator’s power port.
   * Connect the other end to the 48V Power Supply Unit.

3. **Power on the actuator**:

   * Switch on the PSU.
   * The [actuator status LED](../set_up/hardware_interfaces/led.md) should light up, confirming it is receiving power.

!!! success
    Your actuator is now powered and mounted correctly. You’re ready to move on to the next step: [Communicate with Real Actuators](../communicate/communicate_real.md) to establish a connection for sending commands and reading telemetry!

!!! question
    Need help or something doesn’t work? Head over to the [Support page](../support.md): we’ve got your back.
