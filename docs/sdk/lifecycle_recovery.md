# Lifecycle and recovery

Operating state, connection state, and health are separate facts. Use `Actuator.status` and `GroupStatus` rather than inferring safety from one boolean.

![Pulsar SDK lifecycle](assets/diagrams/lifecycle.png)

## Operating states

| State | Meaning |
| --- | --- |
| `UNKNOWN` | disconnected or not observed; cannot be requested |
| `INIT_CONFIG` | output and runtime telemetry inactive; configuration allowed |
| `CONFIG_AND_TELEM` | telemetry active; drive output inactive |
| `DRIVE_ACTIVE` | commands can affect output |

A successful connection ends in `INIT_CONFIG`. `enable()` checks configuration and diagnostics, synchronizes the domain when required, and enters `DRIVE_ACTIVE`. `disable()` returns to `CONFIG_AND_TELEM`.

## Status

`Actuator.status` reports:

- current and last observed operating state;
- connection state;
- `HEALTHY`, `HOST_FAULT`, or `ACTUATOR_FAULT`;
- retained device diagnostics and host errors;
- the last safety attempt;
- peer inhibition;
- recommended recovery action.

![Status and recovery model](assets/diagrams/status.png)

## Default controller safety

The default `ControllerErrorPolicy` selects a mode-specific action:

| Mode | Default action |
| --- | --- |
| position | hold an available position; otherwise zero and command zero |
| impedance | hold position; otherwise damped release |
| velocity | command zero velocity |
| torque | enter output-inactive state, switch to velocity, re-enable through the safety path, and command zero velocity |

If the selected action fails, the default fallback requests `INIT_CONFIG`. Command-based hold, damping, and zero-command actions are best effort because they have no operation-specific device acknowledgement.

Safety applies only while output is active. Diagnostics received while output is inactive are retained and checked before a later enable, but they do not energize output or send active hold commands.

## Device diagnostics

Named `DiagnosticFlag` values are exposed instead of raw bit positions.

Default behavior includes:

- overtemperature → torque derating;
- internal or external encoder error → `INIT_CONFIG`;
- other unmapped errors → default safety;
- unmapped warnings → reported and logged without automatic safety.

Safety propagates to reachable group peers and, when present, other platform groups. Operations across actuators and domains are not atomic.

## Recovery sequences

| Situation | Action |
| --- | --- |
| Connection lost | reconnect; the previous physical state is unknown |
| Stale telemetry or controller fault | fix the cause, call `clear_faults()`, then `resume()` |
| Diagnostic handled while output remains active | wait for it to clear, call `clear_faults()`, then `resume()` if paused |
| Diagnostic safety entered `INIT_CONFIG` | clear the physical condition, call `recover()`, then `resume()` or `enable()` |

`clear_faults()` verifies current diagnostics and returns `False` while a mapped condition remains active. `recover()` is only for diagnostic safety that selected `INIT_CONFIG`; it is not a general host-fault clear operation.

## Advanced policies

`ControllerErrorPolicy`, diagnostic action mappings, damping, and explicit diagnostic overrides are documented in the [API reference](api_reference.md#controllererrorpolicy).

!!! danger
    `ControllerErrorAction.DO_NOTHING` and `override_diagnostic_safety()` can suppress automatic safety behavior. Use them only for a controlled, reviewed application with an independent safety plan.

## Connection loss

After transport loss, the SDK reports `UNKNOWN` and preserves the previous observation in `status.last_operating_state`. It does not claim that unreachable hardware is safe.
