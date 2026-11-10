# Electrical interfaces

## Power bus

- Voltage: **48 V DC**
- Current: up to **30 A**
- Actuator connector: **XT30 male**

Actuators usually draw much less than the maximum current without load, but the supply and wiring must be suitable for the configured limits and application. If the supply cannot provide the possible demand, configure an appropriate current or torque limit.

### Power cable

The actuator requires an XT30 female connector on the power cable.

<p align="center">
  <img src="../assets/images/XT30_01_inv.png" alt="XT30 power connector pinout" width="60%">
</p>

![XT30 power connection](../assets/images/power_connection.jpeg){ width="50%" }

!!! danger
    Verify polarity before applying power. Incorrect wiring can damage equipment and create a fire or injury hazard.

## USB

The actuator USB connector supports direct connection to one computer for configuration, single-actuator testing, control, and maintenance. Use a standard USB-A to USB-C cable.

Direct USB uses actuator address `0` in Pulsar Python SDK.

## CAN FD

PULSE actuators support CAN FD with a 1 Mbit/s arbitration rate and selectable 1 or 5 Mbit/s data phase. Dual CAN connectors allow daisy chaining.

![CAN bus example](../assets/images/can_02_inv.png)

### USB-to-CAN adapter

A CAN adapter connects the host computer to the actuator bus. PulsarHRI provides a USB-to-CAN adapter.

![Pulsar CAN adapter](../assets/images/CAN_adapter.png)

### CAN cables

Compatible cables use 3-pin Molex PicoBlade connectors.

![CAN bus cable](../assets/images/Can_bus_cable.jpeg){ width="50%" }

![CAN bus connector pinout](../assets/images/can_01.png)

Preserve the pinout at both cable ends:

![CAN cable pin mapping](../assets/images/Can_cable_pins_ends.png)

### Termination

Place one 120 Ω termination resistor at each physical end of the CAN bus.

![CAN termination resistor](../assets/images/termination_resistor.jpeg){ width="30%" }

Continue with [CAN FD connectivity](connectivity/can.md).
