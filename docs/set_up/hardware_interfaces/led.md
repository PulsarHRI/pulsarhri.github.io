# LED Status Indicators
PULSAR HRI devices features a simple RGB LED that provides visual feedback about their current operational state. This LED helps users quickly identify a device's status without needing to connect to a computer.

Below is a simple reference of what the led colours mean on each device 

## CAN Adapter Led Color Codes
<span style="color: white; background-color: #333; padding: 2px 6px; border-radius: 50%; font-size: 18px;">●</span> **White**: Device is powered up and working.

## Actuator Led Color Codes
<span style="color: white; background-color: #333; padding: 2px 6px; border-radius: 50%; font-size: 18px;">●</span> **White**: Device is powering up and initializing systems.

<span style="color: blue; font-size: 18px;">●</span> **Blue**: Device is idle and ready, waiting for PCP commands over CAN bus.

<span style="color: purple; font-size: 18px;">●</span> **Purple**: USB connection established, device is waiting for commands via USB interface.

<span style="color: green; font-size: 18px;">●</span> **Green**: Device is actively following the setpoint and operating normally.

<span style="color: red; font-size: 18px;">●</span> **Red**: Device has encountered an error and requires attention.

<span style="color: black; font-size: 18px;">●</span> **Off**: Device is in firmware update mode.

> **Note**: LED colors transition automatically based on device state changes. If the LED remains red, consult the troubleshooting guide.
