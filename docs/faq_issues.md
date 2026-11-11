Developer Hub
{ .pulsar-home-eyebrow }

# FAQ and Support

## Support { #support }

For product and integration support, contact PULSAR HRI:

- Email: [support.dt@pulsarhri.com](mailto:support.dt@pulsarhri.com)
- Monday–Thursday: 08:00–17:00 GMT
- Friday: 08:00–13:00 GMT

Include the actuator model, firmware version, host operating system, connection type, and a concise description of what happened.

For Developer Hub bugs or documentation requests, open an issue:

[github.com/PulsarHRI/pulsarhri.github.io/issues](https://github.com/PulsarHRI/pulsarhri.github.io/issues)

Do not post credentials, private packages, serial numbers, or other sensitive information in a public issue.

## Frequently asked questions

### Which interface should I use first?

Use [Pulsar App](pulsar_app/index.md) for one physical actuator without code, direct USB with [Pulsar Python SDK](quickstart/sdk_usb.md) for Python development, CAN FD for several physical actuators, and `VirtualWorld` when no hardware is available and you want to explore the actuator's performance to your specific project.

### Which firmware is required by Pulsar SDK?

Physical actuators require firmware 2.0.4 or newer. [Update Firmware](firmware/index.md) if an update is needed.

### Is macOS supported?

No. Current supported hosts are Linux x86_64, Linux ARM64, and Windows x86_64.

### Does Pulsar App control virtual actuators?

No. Pulsar App currently controls one physical actuator at a time through USB. Use Pulsar SDK for other phsycal/virtual actuators needs.

## Do you support EtherCAT?

EtherCAT support is planned for Q1 2027 through native board integration, or through an EtherCAT-to-CAN adapter if you own CAN-based Pulsar Actuator.

### Where are the Rust SDK docs?

The Pulsar Rust SDK is coming soon. Its section will be expanded when the crate, examples, and reference are released.

## Open Pulsar Python SDK issues

The following issues are currently tracked for Pulsar Python SDK and will be fixed in a future release:

- **#1 — Reconnect isolation:** queued transport-loss handling affects a newly reconnected actuator session.
- **#2 — Physical-domain validation:** `PulsarActuatorReal` must doesn't reject `VirtualWorld` as a domain.
- **#3 — Stale telemetry recovery:** enable() is allowed to recover the actuators to operational state without clearing the faults first.
- **#4 — CAN bit-rate switching:** BRS is applied to high frequency items such as commands and feedback, other parameters run at the standard 1Mbps speed.
- **#5 — Co-simulation ergonomics:** a future bulk exchange helper should return elapsed ticks and telemetry while retaining the low-level `step()` API.

For help with a current application, use [Support](#support) or open an issue in the [Developer Hub repository](https://github.com/PulsarHRI/pulsarhri.github.io/issues).
