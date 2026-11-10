# Pulsar SDK API reference

Public reference for:

```python
from pulsar_sdk import ...
```

The behavior and workflow guide is in the [Pulsar SDK user contract](user_contract.md).

## Diagrams

- [Runtime architecture](assets/diagrams/runtime.png)
- [Public class model](assets/diagrams/class-model.png)
- [Lifecycle and recovery](assets/diagrams/lifecycle.png)
- [Setup, callback, and safety sequence](assets/diagrams/full-sequence.png)

# Type aliases and callbacks

```python
Telemetry = dict[TelemetryItems, int | float]
TelemetryBatch = dict[str, Telemetry]
ControlValues = dict[ControlParams, float]
ControlBatch = Mapping[str, Mapping[ControlParams, float]]

ControlCallback = Callable[
    [ControllerMetadata, TelemetryBatch],
    ControlBatch | None,
]

DiagnosticCallback = Callable[
    [ActuatorGroup, Actuator, ActuatorDiagnostic],
    None,
]
```

An actuator-level telemetry callback has this signature:

```python
Callable[[int | None, Telemetry], None]
```

An actuator-level diagnostic callback has this signature:

```python
Callable[[Actuator, ActuatorDiagnostic], None]
```

# Domains

## `ExecutionDomain`

```python
ExecutionDomain(*, logger: logging.Logger | None = None)
```

Base class for one transport or simulation clock. It also owns the callback worker, telemetry watchdog, and actuator leases.

### Properties

- `capabilities: Capability`
- `connection_state: ConnectionState`
- `is_connected: bool`

### Methods

- `supports(capability: Capability) -> bool` — Return whether the domain advertises the capability.
- `connect() -> None` — Explicitly keep the domain open. Repeated calls are safe.
- `disconnect() -> None` — Release the explicit connection. Raises `ResourceBusyError` while connected actuators still use the domain.
- `sync() -> FeatureResult` — Reset telemetry timestamps and counters for the domain when supported.
- `reset_telemetry_timestamp() -> FeatureResult` — Same operation as `sync()`.

The class supports `with`; entering connects and exiting disconnects.

## `PcpOverCan`

```python
PcpOverCan(
    port: str | None = None,
    *,
    logger: logging.Logger | None = None,
)
```

PCP domain for one USB-to-CAN adapter.

- `list_ports() -> tuple[str, ...]` — List detected Pulsar serial ports.
- `scan(start_address=16, end_address=255, *, timeout_s=0.12) -> tuple[int, ...]` — Probe the inclusive address range. The domain connects automatically if needed.
- `set_can_brs_enabled(enabled: bool) -> None` — Update connected actuators while output is inactive. Enabling BRS is verified and rolled back on failure.

CAN actuator addresses must be unique within the domain and lie in `16..16382`. Scan bounds use the same range, `start_address` must not exceed `end_address`, and `timeout_s` must be finite and positive.

## `PcpOverUsb`

```python
PcpOverUsb(
    port: str | None = None,
    *,
    logger: logging.Logger | None = None,
)
```

Direct-USB domain for exactly one actuator at address `0`.

- `list_ports() -> tuple[str, ...]` — List detected Pulsar serial ports.

## `VirtualWorld`

```python
VirtualWorld(
    *,
    time_step_hz: float = 20_000,
    assets_path: str | Path | None = None,
    logger: logging.Logger | None = None,
)
```

Deterministic digital-twin domain. The current model assets require exactly `20_000` Hz.

### Attributes

- `time_step_hz: float`
- `time_step_s: float`
- `assets_path: Path | None` — Explicit asset root, if supplied.
- `simulation_time_s: float`
- `simulation_step_count: int`

### Methods

- `scan() -> tuple[str, ...]` — Return available packaged models for the current host. Current supported names are `P90`, `P100`, `PULSE98-30G`, `PULSE98-55G`, `PULSE115-60G`, and `PULSE115-110G`.
- `sync() -> FeatureResult` — Reset virtual telemetry timestamps and counters without resetting plant physics.
- `step(*, loads_by_address: Mapping[int, float] | None = None) -> None` — Advance connected models to the earliest next telemetry event and wait for due callbacks. If no periodic telemetry is configured, advance one model tick.

Without `assets_path`, lookup checks `PULSAR_ASSETS_PATH`, then the active Conda prefix and Python environment prefix under `share/pulsar-assets` and `Library/share/pulsar-assets`.

Loads must be finite numbers keyed by connected virtual actuator address.

# Actuators

## `Actuator`

```python
Actuator(
    domain: ExecutionDomain,
    *,
    address: int | None,
    capabilities: Capability = Capability.NONE,
    diagnostic_actions: Mapping[DiagnosticFlag, ControllerErrorAction] | None = None,
    diagnostic_damping: float | None = None,
    logger: logging.Logger | None = None,
)
```

Backend-neutral actuator contract. Most users create `PulsarActuatorReal` or `PulsarActuatorVirtual` instead.

`diagnostic_actions` maps named `DiagnosticFlag` values to safety actions. Defaults are:

- `DiagnosticFlag.OVERTEMPERATURE` → `LIMIT_TORQUE`
- `DiagnosticFlag.INTERNAL_ENCODER_ERROR` and `EXTERNAL_ENCODER_ERROR` → `INIT_CONFIG`
- other unmapped error diagnostics → `DEFAULT_SAFETY`

Map a diagnostic to `DO_NOTHING` to keep it report-only: callbacks and `status.diagnostic` still update, but it does not fault, inhibit, pause, propagate safety, or block direct commands/enabling. Mapping every `DiagnosticFlag` provides the explicit destructive-testing configuration.

`diagnostic_damping` must be `None` or a finite positive value.

### Properties

- `domain: ExecutionDomain` — Owning domain.
- `address: int | None` — Read-only transport or virtual identifier.
- `capabilities: Capability`
- `connection_state: ConnectionState`
- `is_connected: bool`
- `status: ActuatorStatus` — Includes the current and last observed operating state, connection, health, diagnostic, safety, and recovery information.
- `mode: Mode | None`
- `info: DeviceInfo`
- `dropped_telemetry_packets: int` — Pending actuator callback packets replaced by newer packets.

### Lifecycle and control

- `connect() -> None` — Connect the actuator and acquire its domain.
- `disconnect() -> None` — Request the backend safe disconnect state and release the domain lease.
- `configure(configuration: ControlConfiguration) -> None` — Apply mode and periodic telemetry configuration in `INIT_CONFIG` or `CONFIG_AND_TELEM`.
- `set_mode(mode: Mode) -> None` — Change mode while drive output is inactive. The cached mode changes only after the backend update succeeds.
- `switch_to(state: State) -> None` — Request `INIT_CONFIG`, `CONFIG_AND_TELEM`, or `DRIVE_ACTIVE`. `UNKNOWN` cannot be requested.
- `sync() -> FeatureResult` — Move to `CONFIG_AND_TELEM` when needed, then synchronize the whole domain.
- `enable() -> None` — Check configuration and diagnostics, synchronize when required, and enter `DRIVE_ACTIVE`.
- `disable() -> None` — Enter `CONFIG_AND_TELEM`.
- `set_command(command: float | Mapping[ControlParams, float]) -> None` — Send a primary command or a validated mode-specific control mapping in `DRIVE_ACTIVE`. A mapping must include `ControlParams.COMMAND`; omitted optional packet fields remain unchanged by firmware.

When the actuator belongs to a group, lifecycle and configuration operations are routed through that group.

### Telemetry and callbacks

- `read_telemetry(items: Iterable[TelemetryItems]) -> Telemetry` — Read a snapshot in `CONFIG_AND_TELEM` or `DRIVE_ACTIVE`.
- `set_telemetry_callback(callback: Callable[[int | None, Telemetry], None] | None) -> None` — Register or remove an actuator callback. One callback may run while one newest packet waits.
- `set_diagnostic_callback(callback: Callable[[Actuator, ActuatorDiagnostic], None] | None) -> None` — Register or remove an actuator diagnostic callback.

### Parameters and optional features

- `read_parameters(parameters: Iterable[Parameters]) -> dict[Parameters, int | float]`
- `set_parameters(parameters: Mapping[Parameters, int | float]) -> None` — Allowed only while drive output is inactive.
- `set_torque_gain_preset(preset: TorqueGainPreset) -> FeatureResult`
- `set_velocity_gain_preset(preset: VelocityGainPreset) -> FeatureResult`
- `zero_position() -> FeatureResult` — Allowed in `CONFIG_AND_TELEM` or `DRIVE_ACTIVE`. Position and impedance modes reset the COMMAND to zero to avoid sudden motion.
- `identify() -> FeatureResult`
- `set_address(address: int) -> FeatureResult`
- `save_parameters() -> FeatureResult`
- `enter_bootloader() -> FeatureResult`
- `supports(capability: Capability) -> bool`

Unsupported optional operations return `FeatureResult(UNSUPPORTED, ...)` unless the operation is invalid for the current lifecycle state.

### Fault and diagnostic methods

- `clear_faults() -> bool` — Verify current diagnostics, clear retained SDK faults when possible, and restore thermal torque limits after `OVERTEMPERATURE` clears. Returns `False` while a mapped diagnostic remains active.
- `recover() -> None` — Recover a diagnostic whose selected action entered `INIT_CONFIG`. This is not a general host-fault clear method.
- `resume() -> None` — Resume a healthy standalone actuator. If output is inactive, this runs the normal enable checks before entering `DRIVE_ACTIVE`. A grouped actuator routes the call through its group.
- `override_diagnostic_safety(flags: Iterable[DiagnosticFlag]) -> None` — Bypass SDK safety for currently active named diagnostics. Overrides expire when those diagnostics clear. This is a dangerous operation.

The class supports `with`; entering connects and exiting disconnects.

## `PulsarActuatorReal`

```python
PulsarActuatorReal(
    domain: ExecutionDomain,
    address: int,
    *,
    diagnostic_actions: Mapping[DiagnosticFlag, ControllerErrorAction] | None = None,
    diagnostic_damping: float | None = None,
    logger: logging.Logger | None = None,
)
```

Physical actuator using Pulsar Communication Protocols (PCP).

- `info` reports model and firmware version.
- Physical state requests complete only after the requested state is observed.
- Connection reads and caches maximum torque and the current torque limit for thermal safety.
- CAN-backed actuators advertise `ADDRESS_CHANGE`; USB-backed actuators do not.
- Physical maintenance methods may return `UNCONFIRMED` because transmission has no dedicated acknowledgement.

## `PulsarActuatorVirtual`

```python
PulsarActuatorVirtual(
    domain: VirtualWorld,
    *,
    model: str,
    address: int | None = None,
    diagnostic_actions: Mapping[DiagnosticFlag, ControllerErrorAction] | None = None,
    diagnostic_damping: float | None = None,
    logger: logging.Logger | None = None,
)
```

Generated digital-twin actuator.

- `model: str` — Requested model name.
- `info` reports the model name and generated model version.
- An omitted address is allocated monotonically within the world.
- Explicit addresses must be unique integers in `0..16382`.
- The plant remains enabled as a passive zero-torque model in `INIT_CONFIG` and `CONFIG_AND_TELEM`, so external loads can still move it.
- Telemetry is not available in `INIT_CONFIG`.
- `identify()` returns `UNSUPPORTED`.

# Groups

## `ActuatorGroup`

```python
ActuatorGroup(
    name: str,
    actuators: Mapping[str, Actuator],
    *,
    telemetry_timeout_s: float = 0.1,
    controller_timeout_s: float | None = 1.0,
    controller_error_policy: ControllerErrorPolicy | None = None,
    logger: logging.Logger | None = None,
)
```

A named set of actuators that share one domain and one control mode. The group name, member mapping, and every member name must be non-empty; members must be distinct actuator objects from one domain.

`telemetry_timeout_s` and a non-`None` `controller_timeout_s` must be finite and positive. Set `controller_timeout_s=None` to disable the callback deadline.

### Properties

- `name: str`
- `actuators: Mapping[str, Actuator]` — Read-only view.
- `domain: ExecutionDomain`
- `connection_state: ConnectionState`
- `is_connected: bool`
- `controller_state: ControllerState`
- `status: GroupStatus`

### Lifecycle

- `connect() -> None` — Connect every member; roll back earlier connections if a later member fails.
- `disconnect() -> None` — Stop callbacks, apply output-inactive safety where needed, and release group leases.
- `close(*, disconnect_actuators: bool = True) -> None` — Disconnect, detach members, and make the group unusable.
- `configure(configuration: ControlConfiguration) -> None` — Apply one configuration to every member. A partial failure invalidates the group configuration until the whole group is configured again.
- `set_mode(mode: Mode) -> None` — Change every member while all drives are inactive.
- `switch_to(state: State) -> None` — Request one state for every member and report aggregate failure.
- `sync() -> FeatureResult` — Enter `CONFIG_AND_TELEM` where needed and synchronize the shared domain.
- `reset_telemetry_timestamp() -> FeatureResult` — Same operation as `sync()`.
- `enable() -> None` — Check faults and diagnostics, synchronize when required, then enable every member. Failure attempts rollback to `CONFIG_AND_TELEM`.
- `disable() -> None` — Move every member to `CONFIG_AND_TELEM`.
- `zero_position() -> dict[str, FeatureResult]` — Zero every member in `CONFIG_AND_TELEM` or `DRIVE_ACTIVE`.

### Commands, parameters, and presets

- `set_commands(commands: ControlBatch) -> None` — Validate a selected member batch before the first write. Each member mapping accepts the same mode-specific `ControlParams` as standalone `set_command()`.
- `read_parameters(parameters: Mapping[str, Iterable[Parameters]]) -> dict[str, dict[Parameters, int | float]]`
- `set_parameters(parameters: Mapping[str, Mapping[Parameters, int | float]] | Mapping[Parameters, int | float], *, unify: bool = False) -> None`
- `set_torque_gain_presets(presets: Mapping[str, TorqueGainPreset] | TorqueGainPreset, *, unify: bool = False) -> dict[str, FeatureResult]`
- `set_velocity_gain_presets(presets: Mapping[str, VelocityGainPreset] | VelocityGainPreset, *, unify: bool = False) -> dict[str, FeatureResult]`
- `save_parameters() -> dict[str, FeatureResult]`

With `unify=False`, mappings are keyed by actuator name. With `unify=True`, one flat parameter map or one preset is applied to every member.

### Callbacks and recovery

- `set_control_callback(callback: ControlCallback | None) -> None`
- `set_diagnostic_callback(callback: DiagnosticCallback | None) -> None`
- `clear_faults() -> bool` — Attempt every member, then clear group fault state only when all checks pass.
- `resume() -> None` — Resume callback control after faults are clear and telemetry is fresh. If output is already active, it is not cycled.
- `recover() -> None` — Recover members whose diagnostic action selected `INIT_CONFIG`.
- `raise_for_host_error() -> None` — Raise `ControllerFaultError` when a host fault is latched.

The class supports `with`; entering connects and exiting disconnects.

# Platforms

## `Platform`

```python
Platform(
    groups: Mapping[str, ActuatorGroup],
    *,
    logger: logging.Logger | None = None,
)
```

Top-level composition for lifecycle and safety across one or more domains. The group mapping and every platform group name must be non-empty. A group object cannot appear twice or already belong to another platform.

### Properties

- `groups: Mapping[str, ActuatorGroup]` — Read-only view.
- `domains: tuple[ExecutionDomain, ...]` — Unique domains in group order.
- `connection_state: ConnectionState` — Live aggregate. `FAULTED` takes priority, followed by `PARTIAL` and transition states.
- `is_connected: bool`
- `status: dict[str, GroupStatus]`

### Lifecycle

- `connect() -> None` — Connect every group and roll back earlier groups on failure.
- `disconnect() -> None` — Attempt every group and report incomplete shutdown.
- `close() -> None` — Disconnect and detach groups. Groups and actuators remain reusable.
- `configure(configurations: Mapping[str, ControlConfiguration]) -> None` — Requires exactly one configuration per group.
- `set_modes(modes: Mapping[str, Mode]) -> None` — Requires exactly one mode per group.
- `switch_to(state: State) -> None` — Attempt every group, then report aggregate failure.
- `sync() -> dict[ExecutionDomain, FeatureResult]` — Prepare groups and synchronize each domain independently.
- `reset_telemetry_timestamp() -> dict[ExecutionDomain, FeatureResult]` — Same operation as `sync()`.
- `enable() -> None` — Enable groups in order. On failure, attempt to disable every group already enabled.
- `disable() -> None` — Attempt every group before reporting failures.
- `zero_position() -> dict[str, dict[str, FeatureResult]]`

### Commands, parameters, and presets

- `set_commands(commands: Mapping[str, ControlBatch]) -> None` — Validate all selected groups before the first platform write. Nested actuator mappings accept the same mode-specific `ControlParams` as standalone `set_command()`.
- `read_parameters(parameters: Mapping[str, Mapping[str, Iterable[Parameters]]]) -> dict[str, dict[str, dict[Parameters, int | float]]]`
- `set_parameters(parameters: Mapping[str, Mapping[str, Mapping[Parameters, int | float]]] | Mapping[Parameters, int | float], *, unify: bool = False) -> None`
- `set_torque_gain_presets(presets: Mapping[str, Mapping[str, TorqueGainPreset]] | TorqueGainPreset, *, unify: bool = False) -> dict[str, dict[str, FeatureResult]]`
- `set_velocity_gain_presets(presets: Mapping[str, Mapping[str, VelocityGainPreset]] | VelocityGainPreset, *, unify: bool = False) -> dict[str, dict[str, FeatureResult]]`
- `save_parameters() -> dict[str, dict[str, FeatureResult]]`

Nested mappings preserve `group_name -> actuator_name -> value`. `unify=True` applies one parameter map or preset across all represented actuators and domains.

### Callbacks and recovery

- `set_control_callback(callback: ControlCallback | None) -> None` — Register the same callback on every group. Calls remain independent per group.
- `set_diagnostic_callback(callback: DiagnosticCallback | None) -> None`
- `clear_faults() -> bool` — Attempt every group.
- `resume() -> None` — Resume every group after validation.
- `recover() -> None` — Recover groups with `INIT_CONFIG` diagnostic safety, then verify that faults cleared.
- `raise_for_host_error() -> None` — Raise one aggregate `ControllerFaultError`.

The class supports `with`; entering connects and exiting disconnects.

# Records

## `FeatureResult`

```python
FeatureResult(
    status: FeatureStatus,
    message: str = "",
    acknowledged: bool = False,
)
```

Properties:

- `supported: bool` — `False` only for `UNSUPPORTED`.
- `ok: bool` — `True` only for `OK`.
- `unsupported: bool` — `True` only for `UNSUPPORTED`.

## `DeviceInfo`

```python
DeviceInfo(
    model: str,
    serial_number: str | None = None,
    firmware_version: str | None = None,
    model_version: str | None = None,
    control_model_crc: int | None = None,
)
```

## `ControlConfiguration`

```python
ControlConfiguration(
    mode: Mode,
    telemetry_items: tuple[TelemetryItems, ...] = (),
    telemetry_rate_hz: float = 0.0,
)
```

- `actual_telemetry_rate_hz: float` — Divider-derived rate based on a 20 kHz clock.
- The rate must be `0` or `1..10_000` Hz.
- At most 12 unique telemetry items are allowed.

## `ControllerErrorPolicy`

```python
ControllerErrorPolicy(
    action: ControllerErrorAction = ControllerErrorAction.DEFAULT_SAFETY,
    damping: float | None = None,
    fallback: ControllerErrorAction = ControllerErrorAction.INIT_CONFIG,
)
```

A selected `DAMPED_RELEASE` needs finite positive damping; otherwise safety uses the fallback action. `DO_NOTHING` keeps controller errors report-only, retains the previous command, and allows later callback cycles and direct `set_commands()` calls to continue.

## `ControllerMetadata`

```python
ControllerMetadata(
    callback_count: int,
    elapsed_time_ms: int,
    mode: Mode,
    group_name: str,
)
```

`elapsed_time_ms` is measured from the group connection time.

## `ActuatorDiagnostic`

```python
ActuatorDiagnostic(
    address: int | None,
    flags: Mapping[DiagnosticFlag, str],
    severity: DiagnosticSeverity | None = None,
    device_timestamp_ms: int | None = None,
)
```

`flags` uses `DiagnosticFlag` keys. Raw integer keys are rejected.

## `SafetyAttempt`

```python
SafetyAttempt(
    action: ControllerErrorAction,
    transmitted: bool,
    acknowledged: bool,
    guaranteed: bool,
    message: str = "",
)
```

`guaranteed` is true only when the action was transmitted and acknowledged. Command-based hold, damping, and zero-command actions normally have no operation-specific acknowledgement.

## `HostError`

```python
HostError(
    code: HostErrorCode,
    message: str,
    actuator_addresses: tuple[int | None, ...],
    safety_attempt: SafetyAttempt | None = None,
)
```

## `ActuatorStatus`

```python
ActuatorStatus(
    operating_state: State,
    last_operating_state: State | None,
    connection_state: ConnectionState,
    health: HealthState,
    recovery: RecoveryAction,
    diagnostic: ActuatorDiagnostic | None = None,
    host_error: HostError | None = None,
    safety_attempt: SafetyAttempt | None = None,
    inhibited_by: str | None = None,
)
```

Properties:

- `can_configure: bool` — Connected and in `INIT_CONFIG` or `CONFIG_AND_TELEM`.
- `commands_effective: bool` — Output is enabled and the actuator is healthy and uninhibited.
- `output_enabled: bool` — Connected and physically in `DRIVE_ACTIVE`, including a faulted active hold/damping state.

`RecoveryAction.RECOVER` means a retained fault needs to be cleared or verified. It does not always mean that the `recover()` method is the next call; `recover()` is specifically for `INIT_CONFIG` diagnostic safety.

## `GroupStatus`

```python
GroupStatus(
    connection_state: ConnectionState,
    controller_state: ControllerState,
    operating_state: State,
    actuator_statuses: Mapping[str, ActuatorStatus] = ...,
    stale_names: tuple[str, ...] = (),
    stale_addresses: tuple[int | None, ...] = (),
    wait_reason: str | None = None,
    last_host_error: HostError | None = None,
    dropped_batches: int = 0,
    timestamp_skew_ms: int = 0,
)
```

`operating_state` is `UNKNOWN` when member states differ.

# Enumerations

## `ConnectionState`

| Constant | Value | Meaning |
| --- | ---: | --- |
| `DISCONNECTED` | `0` | No active backend connection. |
| `CONNECTING` | `1` | Connection is in progress. |
| `CONNECTED` | `2` | Connection is ready. |
| `PARTIAL` | `3` | Only part of an aggregate is connected. |
| `DISCONNECTING` | `4` | Shutdown is in progress. |
| `FAULTED` | `5` | Connection failed or was lost. |

## `ControllerState`

| Constant | Value | Meaning |
| --- | ---: | --- |
| `STOPPED` | `0` | Callback control is inactive. |
| `ACTIVE` | `1` | Complete telemetry batches invoke the controller. |
| `WAITING_FOR_TELEMETRY` | `2` | Control is paused pending explicit recovery or resume. |
| `FAULTED` | `3` | A host/controller fault is latched. |

## `State`

| Constant | Value | Meaning |
| --- | ---: | --- |
| `UNKNOWN` | `0` | Disconnected or unobserved; not requestable. |
| `INIT_CONFIG` | `1` | Drive output and runtime telemetry inactive; configuration allowed. |
| `CONFIG_AND_TELEM` | `2` | Telemetry active; drive output inactive. |
| `DRIVE_ACTIVE` | `3` | Commands can affect output. |

## `HealthState`

| Constant | Value | Meaning |
| --- | ---: | --- |
| `HEALTHY` | `0` | No retained actuator or host fault. |
| `HOST_FAULT` | `1` | SDK, controller, or transport fault retained. |
| `ACTUATOR_FAULT` | `2` | Device error diagnostic retained. |

## `RecoveryAction`

| Constant | Value | Meaning |
| --- | ---: | --- |
| `NONE` | `0` | No recovery action is required. |
| `RESUME` | `1` | A healthy actuator is paused or inhibited; resume after validation. |
| `RECOVER` | `2` | A retained fault must be cleared or verified. |
| `RECONNECT` | `3` | Connection is absent or faulted. |

## `Mode`

| Constant | Value | Command unit |
| --- | ---: | --- |
| `TORQUE` | `5` | N·m |
| `VELOCITY` | `6` | rad/s |
| `POSITION` | `7` | rad |
| `IMPEDANCE` | `8` | position command in rad |

## Gain presets

| Type | Constant | Value |
| --- | --- | ---: |
| `TorqueGainPreset` | `AGGRESSIVE` | `1` |
| `TorqueGainPreset` | `BALANCED` | `2` |
| `TorqueGainPreset` | `SOFT` | `3` |
| `VelocityGainPreset` | `AGGRESSIVE` | `1` |
| `VelocityGainPreset` | `BALANCED` | `2` |
| `VelocityGainPreset` | `SOFT` | `3` |

## `FeatureStatus`

| Constant | Value | Meaning |
| --- | ---: | --- |
| `OK` | `0` | Operation completed and was confirmed where applicable. |
| `UNSUPPORTED` | `1` | Backend does not provide the feature. |
| `FAILED` | `2` | Operation failed. |
| `UNCONFIRMED` | `3` | Transmission occurred without dedicated confirmation. |

## `ControllerErrorAction`

| Constant | Value | Behavior |
| --- | ---: | --- |
| `DRIVE_INACTIVE` | `0` | Request `CONFIG_AND_TELEM`. |
| `HOLD_POSITION` | `1` | Send the latest known position in position or impedance mode. |
| `DAMPED_RELEASE` | `2` | Use zero stiffness and positive damping in impedance mode; velocity mode sends zero velocity. |
| `DEFAULT_SAFETY` | `3` | Select hold, damped release, or zero velocity from mode and damping. Torque mode quick-switches to velocity mode and commands zero velocity. |
| `INIT_CONFIG` | `4` | Request `INIT_CONFIG`. |
| `LIMIT_TORQUE` | `5` | Apply diagnostic torque derating. |
| `DO_NOTHING` | `6` | Report the diagnostic/controller error without changing control, state, inhibition, or command availability. |

## `DiagnosticFlag`

Named firmware diagnostics. Values are firmware bit positions, but applications use the enum names rather than raw integers.

| Constant | Value | Severity class |
| --- | ---: | --- |
| `OVERTEMPERATURE` | `0` | warning |
| `POSITION_REFERENCE_MAXIMUM` | `2` | warning |
| `POSITION_REFERENCE_MINIMUM` | `3` | warning |
| `VELOCITY_TELEMETRY_MAXIMUM` | `4` | warning |
| `BUS_VOLTAGE_OUT_OF_RANGE` | `5` | warning |
| `TORQUE_REFERENCE_MAXIMUM` | `6` | warning |
| `TORQUE_TELEMETRY_MAXIMUM` | `7` | warning |
| `POSITION_TELEMETRY_MAXIMUM` | `8` | warning |
| `POSITION_TELEMETRY_MINIMUM` | `9` | warning |
| `CONTROL_OVERRUN` | `12` | warning |
| `COMMUNICATION_OVERRUN` | `13` | warning |
| `CURRENT_MAXIMUM` | `16` | error |
| `INVALID_LIMITS` | `17` | error |
| `BUS_VOLTAGE_CRITICAL_RANGE` | `29` | error |
| `INTERNAL_ENCODER_ERROR` | `30` | error |
| `EXTERNAL_ENCODER_ERROR` | `31` | error |

## `DiagnosticSeverity`

| Constant | Value |
| --- | ---: |
| `INFO` | `0` |
| `WARNING` | `1` |
| `ERROR` | `2` |

## `HostErrorCode`

| Constant | Value | Meaning |
| --- | ---: | --- |
| `CONTROLLER_EXCEPTION` | `1` | Controller callback raised. |
| `INVALID_CONTROLLER_OUTPUT` | `2` | Controller returned an invalid command batch. |
| `CONNECTION_LOST` | `3` | Transport connection was lost. |
| `SAFETY_ACTION_FAILED` | `4` | Selected host safety action failed or could not be confirmed. |
| `STALE_TELEMETRY` | `5` | Required callback telemetry became stale. |
| `COMMAND_TRANSMISSION_FAILED` | `6` | A callback command write failed. |
| `CONTROLLER_TIMEOUT` | `7` | Controller callback exceeded its deadline. |

# `Parameters`

Parameter reads are backend-specific. Writes are allowed only while drive output is inactive.

These values are directly writable with `set_parameters()`:

- impedance gains: `IMPEDANCE_DAMPING`, `IMPEDANCE_STIFFNESS`;
- torque, position, velocity, profile-velocity, and profile-acceleration limits;
- loop gains: `VELOCITY_KP`, `VELOCITY_KI`, `POSITION_KP`, `FEEDFORWARD_GAIN`;
- `DIRECTION_INVERTED`, `VELOCITY_FILTER_CUTOFF`, `CURRENT_FILTER_CUTOFF`, and `CAN_BRS_ENABLED`.

The following values require dedicated methods instead:

- `MODE` → `set_mode()`;
- `COMMAND` → command methods;
- `TORQUE_GAIN_PRESET` and `VELOCITY_GAIN_PRESET` → preset methods;
- `PCP_ADDRESS` → `set_address()`;
- `TELEMETRY_RATE_HZ` → `configure()`.

These fields are read-only: `RATED_VELOCITY_RAD_S`, `MAXIMUM_TORQUE_NM`, `FIRMWARE_VERSION`, `SERIAL_NUMBER`, `DEVICE_MODEL`, and `CONTROL_MODEL_CRC`. A backend may reject an otherwise writable field that its device or model does not provide.

For CAN BRS, prefer `PcpOverCan.set_can_brs_enabled()`. It coordinates all connected actuators, verifies the new setting, and rolls back a failed enable.

| Constant | Value | Meaning |
| --- | ---: | --- |
| `IMPEDANCE_DAMPING` | `1` | Impedance damping gain. |
| `IMPEDANCE_STIFFNESS` | `2` | Impedance stiffness gain. |
| `TORQUE_LIMIT` | `4` | Torque limit in N·m; `+inf` restores the unbounded software default. |
| `POSITION_LIMIT_MAX` | `5` | Maximum position in rad; `+inf` is unbounded. |
| `POSITION_LIMIT_MIN` | `6` | Minimum position in rad; `-inf` is unbounded. |
| `VELOCITY_LIMIT_MAX` | `7` | Maximum velocity in rad/s; `+inf` is unbounded. |
| `VELOCITY_LIMIT_MIN` | `8` | Minimum velocity in rad/s; `-inf` is unbounded. |
| `POSITION_PROFILE_VELOCITY_MAX` | `9` | Positive position-profile velocity limit; `+inf` is unbounded. |
| `POSITION_PROFILE_VELOCITY_MIN` | `10` | Negative position-profile velocity limit; `-inf` is unbounded. |
| `VELOCITY_PROFILE_ACCELERATION_MAX` | `11` | Positive velocity-profile acceleration limit; `+inf` is unbounded. |
| `VELOCITY_PROFILE_ACCELERATION_MIN` | `12` | Negative velocity-profile acceleration limit; `-inf` is unbounded. |
| `VELOCITY_KP` | `13` | Velocity-loop proportional gain. |
| `VELOCITY_KI` | `14` | Velocity-loop integral gain. |
| `POSITION_KP` | `15` | Position-loop proportional gain. |
| `MODE` | `48` | Current mode. |
| `COMMAND` | `49` | Current primary command. |
| `TORQUE_GAIN_PRESET` | `64` | Current torque gain preset. |
| `VELOCITY_GAIN_PRESET` | `65` | Current velocity gain preset. |
| `RATED_VELOCITY_RAD_S` | `66` | Rated velocity. |
| `MAXIMUM_TORQUE_NM` | `67` | Maximum actuator torque. |
| `DIRECTION_INVERTED` | `68` | Direction inversion flag. |
| `FEEDFORWARD_GAIN` | `69` | Controller feedforward gain. |
| `VELOCITY_FILTER_CUTOFF` | `70` | Velocity filter cutoff. |
| `CURRENT_FILTER_CUTOFF` | `71` | Current filter cutoff. |
| `FIRMWARE_VERSION` | `128` | Encoded physical firmware version. |
| `PCP_ADDRESS` | `129` | PCP address. |
| `SERIAL_NUMBER` | `130` | Device serial number. |
| `DEVICE_MODEL` | `131` | Encoded device model. |
| `CONTROL_MODEL_CRC` | `132` | Control-model compatibility identifier. |
| `CAN_BRS_ENABLED` | `133` | CAN bit-rate switching flag. |
| `TELEMETRY_RATE_HZ` | `134` | Effective periodic telemetry rate. |

# `TelemetryItems`

| Constant | Value | Meaning |
| --- | ---: | --- |
| `INTERNAL_ENCODER_POSITION` | `65` | Internal encoder position. |
| `INTERNAL_ENCODER_RAW` | `66` | Raw internal encoder count. |
| `EXTERNAL_ENCODER_POSITION` | `67` | External encoder position. |
| `EXTERNAL_ENCODER_RAW` | `68` | Raw external encoder count. |
| `VELOCITY` | `69` | Measured angular velocity. |
| `PHASE_A_CURRENT` | `70` | Phase-A current. |
| `PHASE_B_CURRENT` | `71` | Phase-B current. |
| `PHASE_C_CURRENT` | `72` | Phase-C current. |
| `TORQUE_SENSOR_MEASUREMENT` | `73` | Calibrated torque-sensor measurement. |
| `TORQUE_SENSOR_RAW` | `74` | Raw torque-sensor value. |
| `POSITION_COMMANDED` | `75` | Position reference reported by control. |
| `POSITION` | `76` | Measured output position. |
| `VELOCITY_COMMANDED` | `77` | Velocity reference reported by control. |
| `D_AXIS_CURRENT_COMMANDED` | `79` | Commanded d-axis current. |
| `D_AXIS_CURRENT_ACTUAL` | `80` | Measured d-axis current. |
| `Q_AXIS_CURRENT_COMMANDED` | `81` | Commanded q-axis current. |
| `Q_AXIS_CURRENT_ACTUAL` | `82` | Measured q-axis current. |
| `D_AXIS_VOLTAGE_COMMANDED` | `83` | Commanded d-axis voltage. |
| `Q_AXIS_VOLTAGE_COMMANDED` | `84` | Commanded q-axis voltage. |
| `TORQUE_COMMANDED` | `85` | Torque reference reported by control. |
| `TORQUE_ESTIMATE` | `86` | Estimated actuator torque. |
| `PHASE_A_VOLTAGE_COMMANDED` | `87` | Commanded phase-A voltage. |
| `PHASE_B_VOLTAGE_COMMANDED` | `88` | Commanded phase-B voltage. |
| `PHASE_C_VOLTAGE_COMMANDED` | `89` | Commanded phase-C voltage. |
| `BUS_POWER` | `90` | DC bus power. |
| `BUS_CURRENT` | `91` | DC bus current. |
| `THREE_PHASE_ELECTRICAL_POWER` | `92` | Three-phase electrical power. |
| `MECHANICAL_POWER` | `93` | Mechanical output power. |
| `INVERTER_EFFICIENCY` | `94` | Inverter efficiency. |
| `MOTOR_EFFICIENCY` | `95` | Motor efficiency. |
| `INTERNAL_ENCODER_ERROR_COUNT` | `96` | Internal encoder error counter. |
| `EXTERNAL_ENCODER_ERROR_COUNT` | `97` | External encoder error counter. |
| `CONTROL_OVERRUN_COUNT` | `98` | Control-loop overrun counter. |
| `DIAGNOSTIC_FLAGS` | `99` | Firmware diagnostic bitfield. |
| `TIMESTAMP_MS` | `103` | Device telemetry timestamp in ms. |
| `PERIODIC_MESSAGE_COUNT` | `104` | Periodic telemetry message counter. |
| `BUS_VOLTAGE` | `112` | DC bus voltage. |
| `PCB_TEMPERATURE` | `113` | PCB temperature. |
| `MOTOR_TEMPERATURE` | `114` | Motor temperature. |
| `INTERNAL_POSITION_ACTUAL` | `115` | Internal control position. |

# `ControlParams`

Every selected command mapping requires `COMMAND`. Other fields are valid only in the modes listed below.

| Constant | Value | Allowed modes |
| --- | ---: | --- |
| `COMMAND` | `4` | all modes |
| `D_AXIS_CURRENT_KP` | `193` | `TORQUE` |
| `D_AXIS_CURRENT_KI` | `195` | `TORQUE` |
| `Q_AXIS_CURRENT_KP` | `194` | `TORQUE` |
| `Q_AXIS_CURRENT_KI` | `196` | `TORQUE` |
| `FEEDFORWARD_GAIN` | `197` | `VELOCITY`, `POSITION`, `IMPEDANCE` |
| `VELOCITY_KI` | `198` | `VELOCITY`, `POSITION` |
| `VELOCITY_KP` | `199` | `VELOCITY`, `POSITION` |
| `TORQUE_FEEDFORWARD` | `200` | `VELOCITY`, `POSITION`, `IMPEDANCE` |
| `POSITION_KP` | `201` | `POSITION` |
| `IMPEDANCE_STIFFNESS` | `202` | `IMPEDANCE` |
| `IMPEDANCE_DAMPING` | `203` | `IMPEDANCE` |
| `IMPEDANCE_INERTIA` | `204` | `IMPEDANCE` |
| `IMPEDANCE_VELOCITY_COMMANDED` | `205` | `IMPEDANCE` |
| `IMPEDANCE_ACCELERATION_COMMANDED` | `206` | `IMPEDANCE` |

Virtual models expose shared d/q current gains. Supplying different finite d-axis and q-axis values in one command raises `ValueError`.

# `Capability`

| Constant | Value | Meaning |
| --- | ---: | --- |
| `NONE` | `0` | No optional capabilities. |
| `IDENTIFY` | `1 << 0` | Physical identify action. |
| `PERSIST_PARAMETERS` | `1 << 1` | Parameter persistence. |
| `BOOTLOADER` | `1 << 2` | Bootloader entry. |
| `EXPLICIT_STEP` | `1 << 3` | Explicit simulation stepping. |
| `EXTERNAL_LOAD` | `1 << 4` | External load input. |
| `DISCOVERY` | `1 << 5` | Backend discovery. |
| `ADDRESS_CHANGE` | `1 << 9` | CAN address change. |
| `CAN_BRS` | `1 << 10` | CAN bit-rate switching. |

# Exceptions

- `SdkError` — Base class for SDK runtime errors.
- `ConnectionFailedError` — A connect, disconnect, aggregate transition, rollback, or safe shutdown did not complete fully.
- `InvalidLifecycleError` — Operation is invalid in the current lifecycle state.
- `ResourceBusyError` — Shared resource or callback is currently in use.
- `ControllerFaultError` — A retained controller or host fault blocks the requested operation.
- `CommandTransmissionError(message: str, successful_members: tuple[str, ...] = ())` — A sequential direct command batch failed. `successful_members` lists completed writes.
- `UnsupportedOperationError` — Backend or model does not support the operation.
