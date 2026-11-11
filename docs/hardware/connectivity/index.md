Hardware
{ .pulsar-home-eyebrow }

# Connectivity

Choose a physical communication method based on the system size and use case.

| Method | Use it for | Status |
| --- | --- | --- |
| [Direct USB](usb.md) | One actuator, setup, testing, and development | Available |
| [CAN FD](can.md) | One or more actuators on a shared bus | Available |
| [EtherCAT](ethercat.md) | Future industrial network integration | In development |

Virtual actuators do not use a physical bus. They run through Pulsar Python SDK and `VirtualWorld`; see [Virtual actuators](../../sdk/virtual_actuators.md).
