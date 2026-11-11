Hardware
{ .pulsar-home-eyebrow }

# LED status indicators

The RGB LED gives a quick indication of device state.

## CAN adapter

- **Blue:** powered and operating.
- **Red:** Error in communication, restart required.

## Actuator

- **Orange:** powered up and initialized.
- **Purple:** direct USB connection established and waiting for commands.
- **Green:** drive is active.
- **Red:** an error requires attention.
- **Off:** firmware update mode or no power.

LED state is a useful first check, but it does not replace SDK status and diagnostic information. If an actuator remains red, doesn't provide diagnostics over SDK, doesn't return to normal after a reboot, stop the actuator and [contact support](../support.md) to avoid any further damage.
