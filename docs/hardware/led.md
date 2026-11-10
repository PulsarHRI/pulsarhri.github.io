# LED status indicators

The RGB LED gives a quick indication of device state.

## CAN adapter

- **White:** powered and operating.

## Actuator

- **White:** powering up and initializing.
- **Blue:** idle and waiting for PCP commands over CAN.
- **Purple:** direct USB connection established and waiting for commands.
- **Green:** actively following a command.
- **Red:** an error requires attention.
- **Off:** firmware update mode or no power.

LED state is a useful first check, but it does not replace SDK status and diagnostic information. If an actuator remains red, stop commanding it and [contact support](../support.md).
