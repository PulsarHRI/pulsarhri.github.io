# CAN

Use `PcpOverCan` for a bus connected through one Pulsar USB-to-CAN adapter.

## Scan

```python
from pulsar_sdk import PcpOverCan

with PcpOverCan("/dev/ttyACM0") as can:
    print(can.scan())
```

The default scan range is 16–255. Actuator addresses must be unique within the domain and lie in 16–16382.

## Connect an actuator

```python
from pulsar_sdk import PcpOverCan, PulsarActuatorReal

can = PcpOverCan("/dev/ttyACM0")
actuator = PulsarActuatorReal(can, address=0x10)
```

Several actuators on the same bus must reuse the same `PcpOverCan` object.

## CAN bit-rate switching

`set_can_brs_enabled()` coordinates the setting across connected actuators while output is inactive:

```python
with can:
    can.set_can_brs_enabled(True)
```

Treat BRS as a bus-wide configuration. All devices must be compatible and configured consistently.

## Capacity

More than eight registered actuators is permitted, but the SDK emits a telemetry-utilization warning. Select only required telemetry and estimate the bus load with the [CAN bus utilization tool](../../hardware/connectivity/can_bus_utilization.md).

For multi-actuator composition, continue with [Groups and platforms](../groups_platforms.md).
