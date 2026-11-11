Hardware
{ .pulsar-home-eyebrow }

# Actuator setup

This page covers physical setup before USB or CAN communication.

## What you need

Usually supplied by PULSAR HRI:

- one PULSE actuator;
- one power bus cable.

Usually supplied by the user:

- a secure mechanical support and suitable screws;
- a 48 V DC power supply;
- a computer for configuration or control.

## Setup

1. Review [Safety and prerequisites](safety.md).
2. Review the [electrical interfaces](electrical_interfaces.md) before connecting or applying power, and review the [mechanical interfaces](mechanical_interfaces.md) before mounting.
3. For a shared DC bus or an application that may return energy, review [Regenerative energy management](regenerative_energy_management.md) before selecting or energizing the power system.
4. Mount the actuator using the documented [mechanical interfaces](mechanical_interfaces.md).
5. Connect the power cable to the actuator and power supply.
6. Verify polarity and wiring before switching on the supply.
7. Apply power and check the [status LED](led.md).
8. Choose a method through the [Connectivity overview](connectivity/index.md), then continue with [USB](connectivity/usb.md) or [CAN FD](connectivity/can.md).

For the shortest first-use workflow, continue to [Physical actuator over direct USB with Pulsar App (browser)](../quickstart/pulsar_app.md).
