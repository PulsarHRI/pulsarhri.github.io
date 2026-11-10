# Core workflow

Pulsar Python SDK separates object construction, connection, configuration, output enable, commands, and shutdown.

## One physical actuator

```python
from pulsar_sdk import ControlConfiguration, Mode, PcpOverUsb, PulsarActuatorReal

actuator = PulsarActuatorReal(PcpOverUsb(), address=0)

with actuator:
    actuator.configure(ControlConfiguration(Mode.VELOCITY))
    actuator.enable()
    actuator.set_command(0.5)
    actuator.disable()
```

Constructors validate inputs but do not perform I/O. Entering the context manager connects; exiting disconnects.

## Recommended order

1. Construct domains, actuators, groups, and optionally a platform.
2. Connect.
3. Configure the control mode and periodic telemetry.
4. Optionally zero position.
5. Register callbacks.
6. Enable drive output.
7. Send commands or run the application controller.
8. Disable before changing mode, changing writable parameters, or shutting down.
9. Disconnect or exit the context manager.

## Execution domains

| Domain | Ownership |
| --- | --- |
| `PcpOverUsb` | one direct-USB actuator at address `0` |
| `PcpOverCan` | one USB-to-CAN adapter and its actuator addresses |
| `VirtualWorld` | one deterministic simulation clock and its virtual actuators |

Connected actuators hold leases on their domain. A domain cannot disconnect while an actuator still uses it.

## Configuration

```python
from pulsar_sdk import ControlConfiguration, Mode, TelemetryItems

configuration = ControlConfiguration(
    mode=Mode.POSITION,
    telemetry_items=(
        TelemetryItems.POSITION,
        TelemetryItems.VELOCITY,
        TelemetryItems.TIMESTAMP_MS,
    ),
    telemetry_rate_hz=500,
)
```

A configuration accepts at most 12 unique telemetry items. The periodic rate is `0` to disable it or `1..10_000` Hz.

## Commands and units

| Mode | Primary command |
| --- | --- |
| `Mode.TORQUE` | N·m |
| `Mode.VELOCITY` | rad/s |
| `Mode.POSITION` | rad |
| `Mode.IMPEDANCE` | position in rad, with optional impedance fields |

Commands are allowed only in `DRIVE_ACTIVE` and must be finite.

## Shutdown

`disable()` enters `CONFIG_AND_TELEM`: drive output is inactive while runtime telemetry remains available. Explicit physical disconnect then attempts to reach and observe `INIT_CONFIG` before releasing the transport.

!!! warning
    If communication is lost, the actuator's physical state is unknown. Software cannot confirm that unreachable hardware is safe.
