# Safety and prerequisites

PULSE actuators can move quickly and produce substantial torque. Treat every connected actuator as capable of immediate motion.

## Before applying power

- Secure the actuator to a fixture or robot structure suitable for the expected load.
- Keep the output and attached mechanism clear of people, cables, tools, and loose objects.
- Confirm the power supply voltage, current capacity, polarity, and connector wiring.
- Provide a reliable way to remove power.
- Check mechanical travel, collisions, and cable strain before enabling drive output.

## Before running software

- Use firmware **2.0.4 or newer** with Pulsar SDK.
- Start with conservative commands, gains, limits, and telemetry rates.
- Set the current position as zero only when the resulting reference is understood.
- Do not change control parameters in large jumps while the actuator is active.
- For CAN FD, verify unique addresses and termination at both physical ends of the bus.

## Safe software lifecycle

With Pulsar Python SDK:

1. connect;
2. configure while output is inactive;
3. enable only when the mechanism is clear;
4. send bounded commands;
5. disable before reconfiguration or shutdown;
6. disconnect or exit the context manager.

Do not rely on garbage collection or process exit as a hardware stop mechanism.

!!! warning
    Software safety actions are best effort when communication is lost. If an actuator is unreachable, the SDK reports its state as unknown rather than claiming that it is safe.
