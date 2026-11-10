# FAQ and issues

## Frequently asked questions

### Which interface should I use first?

Use [Pulsar App](pulsar_app/index.md) for one physical actuator without code, direct USB with [Pulsar SDK](quickstart/sdk_usb.md) for Python development, CAN FD for several physical actuators, and `VirtualWorld` when no hardware is available.

### Which firmware is required by Pulsar SDK?

Physical actuators require firmware 2.0.4 or newer. [Contact support](support.md) if an update is needed.

### Is macOS supported?

No. Current supported hosts are Linux x86_64, Linux ARM64, and Windows x86_64.

### Does Pulsar App control virtual actuators?

No. Pulsar App currently controls one physical actuator at a time. Use Pulsar SDK for virtual actuators.

### Where are the Rust SDK docs?

The Pulsar Rust SDK is coming soon. Its section will be expanded when the crate, examples, and reference are released.

## Open SDK issues

The following work is currently tracked for Pulsar SDK:

- **#5 — Reconnect isolation:** queued transport-loss handling must not affect a newly reconnected actuator session.
- **#6 — Physical-domain validation:** `PulsarActuatorReal` must reject `VirtualWorld` instead of accepting a non-physical domain.
- **#7 — Stale telemetry recovery:** implementation and documentation need one consistent, explicitly tested recovery sequence.
- **#8 — CAN bit-rate switching:** BRS must be applied consistently to every PCP operation on a configured CAN domain.
- **#9 — Parameter input validation:** invalid `read_parameters()` entries should raise a clear public-boundary type error.
- **#10 — Co-simulation ergonomics:** a future bulk exchange helper should return elapsed ticks and telemetry while retaining the low-level `step()` API.

These notes describe tracked work, not alternative usage instructions. For help with a current application, use [Support](support.md) or open an issue in the [Developer Hub repository](https://github.com/PulsarHRI/pulsarhri.github.io/issues).
