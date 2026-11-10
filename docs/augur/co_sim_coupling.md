# Co-simulation coupling

Pulsar SDK supports one validated MuJoCo coupling scheme: **the DTwin owns each coupled joint's position and velocity; MuJoCo is an inverse-dynamics load calculator for those coordinates**.

This contract is intentionally narrow. Do not let MuJoCo forward-integrate a DTwin-owned coordinate, and do not apply DTwin output torque to a MuJoCo actuator. Either action integrates the same mechanics twice.

## Units and coordinates

For every coupled joint:

- position: output-shaft radians;
- velocity: output-shaft radians per second;
- acceleration: output-shaft radians per second squared;
- DTwin `Load`: output-shaft N·m;
- positive joint direction: identical in DTwin and MuJoCo;
- positive `Load`: opposes positive DTwin motion (it is subtracted from positive motor torque).

The MuJoCo model must not duplicate motor rotor inertia, reflected gearbox inertia, or drivetrain friction already represented by the DTwin. Keep robot-link inertia, joint damping, springs, contacts, constraints, gravity, Coriolis terms, and centrifugal terms in MuJoCo. Do not set MuJoCo `armature` for DTwin-owned coordinates.

## Time stepping

The DTwin timestep is exactly 50 µs (20 kHz). Choose a coupling interval that is an integer multiple of 50 µs:

```text
coupling_dt = ticks_per_exchange * 0.00005
```

For example, 100 Hz uses 200 DTwin ticks per exchange. Smaller exchange intervals are more stable; validate convergence at 100, 200, 500, and 1,000 Hz for each robot.

## Exchange algorithm

At exchange `k`, retain the load calculated at exchange `k-1`:

1. Advance every actuator in the `VirtualWorld` by `ticks_per_exchange` ticks using that retained load. All actuators on the world must advance together.
2. Read DTwin output-shaft position `q_k` and velocity `v_k`.
3. Estimate acceleration from the exchange-rate velocity difference, then apply the validated first-order 10 Hz low-pass filter:

   ```text
   raw_a_k = (v_k - v_(k-1)) / coupling_dt
   alpha = 1 - exp(-2 * pi * 10 * coupling_dt)
   a_k = a_(k-1) + alpha * (raw_a_k - a_(k-1))
   ```

   Initialize `v_(k-1)` and `a_(k-1)` to zero. Filtering is required because even deterministic finite differences amplify output quantization and create unstable inverse-dynamics loads around constraints and contact. A different cutoff changes the coupling dynamics and must repeat the convergence and energy validation.
4. Assign `q_k` and `v_k` to the matching MuJoCo `qpos` and `qvel` entries. Call `mujoco.mj_forward(model, data)` to refresh kinematics, contacts, and constraints without advancing time; it may overwrite `qacc`.
5. Assign `a_k` to `qacc`, ensure MuJoCo actuator forces for those coordinates are zero, then call `mujoco.mj_inverse(model, data)`. Do not call `mj_step()` for DTwin-owned coordinates.
6. `qfrc_inverse` is the net generalized external force required for the requested acceleration. Subtract any separately applied generalized/body force that MuJoCo includes in that net value. The supported DTwin load is:

   ```text
   required_drive_torque = qfrc_inverse[dof]
                           - qfrc_applied[dof]
                           - generalized_body_applied_force[dof]
   dtwin_load_next = required_drive_torque
   ```

   Contact, equality-constraint, passive, gravity, Coriolis, centrifugal, and link-inertia effects are already handled by inverse dynamics and must not be added again.
7. Use `dtwin_load_next` for the next exchange. This is an explicit co-simulation coupling with one exchange-interval load delay.

If no generalized or body force is applied separately, `dtwin_load_next` is simply `data.qfrc_inverse[dof]`.

## Supported model scope

This scheme is supported for fixed-base MuJoCo models where every independently integrated actuated coordinate is DTwin-owned. The repository contact validation covers a deliberately compliant contact model; stiff/rigid impacts require model-specific stability validation. MuJoCo actuators on the same coordinates, compliant transmissions, and mixed forward/inverse ownership are not covered by this contract.

A floating-base humanoid is not fundamentally impossible, but it is not covered by this partition. MuJoCo would need to own the six free-base coordinates while DTwin owns the actuated joints. Base acceleration, contact reactions, and DTwin joint loads are mutually coupled and must be solved consistently rather than obtained by stepping MuJoCo and overwriting the joints. Until that hybrid solve is implemented and validated, only fixed-base humanoids are supported.

After injecting state, call inverse dynamics before reading the next load. Do not run `mj_step()` and then overwrite the resulting coupled `qpos`/`qvel`; that produces loads inconsistent with the imposed motion and can violate constraints.

## Validation

A coupled model is acceptable only when it passes:

1. no-load output matching standalone DTwin output;
2. positive-load sign (positive load drives acceleration in the negative joint direction from rest);
3. constant external torque direction and magnitude checks;
4. single-pendulum convergence at 100, 200, 500, and 1,000 Hz exchange rates;
5. uncommanded energy/passivity check;
6. two-joint cross-inertial coupling;
7. finite contact load, bounded penetration, and trajectory convergence as the exchange rate increases.

The SDK release validation performs these checks with actual MuJoCo models while setpoint and position/impedance sine references run through `PulsarActuatorVirtual` and `VirtualWorld`.

These fixtures establish the coupling implementation, signs, units, and fixed-base behavior; they do not certify arbitrary robot geometry or stiff impacts. Each production robot still needs its own convergence, energy, joint-limit, and contact validation.
