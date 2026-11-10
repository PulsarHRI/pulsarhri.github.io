PULSAR HRI Developer Hub
{ .pulsar-home-eyebrow }

# Build with PULSAR HRI { .pulsar-home-title }

The PULSAR HRI Developer Hub brings together the hardware, software, control, and simulation information needed to build robotics systems with PULSE actuators.
{ .pulsar-home-intro }

## Choose your path { .pulsar-home-paths }

| I want to… | Start here |
| --- | --- |
| Move one physical actuator without code | [Pulsar App · direct USB](quickstart/pulsar_app.md) |
| Control one physical actuator with Python | [Pulsar Python SDK · direct USB](quickstart/sdk_usb.md) |
| Control several physical actuators with Python | [Pulsar Python SDK · CAN FD](quickstart/sdk_can.md) |
| Develop with a virtual actuator | [Pulsar Python SDK · virtual actuators](quickstart/sdk_virtual.md) |
| Design a robotic platform | [Hardware](hardware/index.md) and [AUGUR Digital Twin](augur/index.md) |

## Main areas { .pulsar-home-areas }

-   ### Hardware

    Mount and power an actuator, understand its interfaces, and connect by USB or CAN FD.

    [Explore hardware](hardware/index.md)

-   ### Firmware

    Learn how the Pulsar App checks for firmware releases and access the current update portal.

    [Explore firmware](firmware/index.md)

-   ### Control

    The physical firmware and AUGUR Digital Twin models run the same low-level control algorithms at 20 kHz.

    [Explore Control](control_architectures/index.md)

-   ### Pulsar App

    Use the browser or desktop GUI to configure, command, and inspect one physical actuator.

    [Open the Pulsar App documentation](pulsar_app/index.md)

-   ### Pulsar Python SDK

    Build Python applications for physical and virtual actuators, from one device to multi-domain robot platforms.

    [Explore Pulsar Python SDK](sdk/index.md)

-   ### Pulsar Rust SDK

    Build actuator applications with the Pulsar Rust SDK.

    [Explore Pulsar Rust SDK](pulsar_rust_sdk/index.md)

-   ### AUGUR Digital Twin

    Run validated virtual actuator models and couple them to external robot simulators.

    [Explore AUGUR Digital Twin](augur/index.md)

## Compatibility at a glance

- Physical SDK firmware requirement: **2.0.4 or newer**.
- Supported hosts: **Linux x86_64**, **Linux ARM64**, and **Windows x86_64**.
- Supported Python versions: **3.10–3.13**.
- macOS is not currently supported.
- The Pulsar App controls one physical actuator at a time.

Need help? Visit [Support](support.md) or [FAQ and Issues](faq_issues.md).

![Blue digital-twin overlays appear on two of five actuators.](assets/images/actuators_digital_twin_transition_5loops.gif){ .pulsar-home-animation loading="lazy" }
