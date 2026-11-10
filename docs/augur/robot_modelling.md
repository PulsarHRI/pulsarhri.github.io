# Robot modelling

Use AUGUR Digital Twin actuator models with an external robot simulator when the application needs link inertia, gravity, contacts, constraints, or multi-body dynamics.

## Ownership boundary

- `VirtualWorld` owns the PULSE actuator model and its output-shaft state.
- The external simulator owns robot links, geometry, gravity, contacts, constraints, and applied forces.
- The supported MuJoCo scheme uses inverse dynamics to calculate the load for DTwin-owned joint coordinates.

Do not forward-integrate a DTwin-owned coordinate in MuJoCo and do not apply DTwin output torque to a MuJoCo actuator on the same coordinate. Either approach integrates the same mechanics twice.

## Supported scope

The validated coupling currently covers fixed-base models whose independently integrated actuated coordinates are DTwin-owned. Floating-base robots, mixed coordinate ownership, stiff impacts, and arbitrary compliant transmissions require additional model-specific validation.

## Validation expectations

A production robot model should be checked for:

- no-load agreement with standalone actuator models;
- load sign and magnitude;
- convergence as exchange rate increases;
- bounded energy and contact behavior;
- joint limits and collision behavior;
- cross-joint inertial effects.

Read the exact [Co-simulation coupling](co_sim_coupling.md) contract before implementing an exchange loop.
