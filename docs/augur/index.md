# AUGUR Digital Twin

AUGUR Digital Twin provides validated virtual models of PULSE actuators for software development, controller testing, and robot co-simulation.

## How it fits together

- `pulsar-assets` installs prebuilt model libraries.
- `VirtualWorld` owns one deterministic simulation clock.
- `PulsarActuatorVirtual` exposes the same lifecycle, modes, commands, grouping, status, and safety concepts as a physical actuator.
- An external simulator such as MuJoCo owns robot links, contacts, constraints, and other coupled dynamics.

## Supported actuator models

- P90
- P100
- PULSE98-30G
- PULSE98-55G
- PULSE115-60G
- PULSE115-110G

## Start here

- [Virtual actuator with Pulsar Python SDK](../quickstart/sdk_virtual.md)
- [Virtual actuators in Pulsar Python SDK](../sdk/virtual_actuators.md)
- [Co-simulation coupling](co_sim_coupling.md)
- [Robot modelling](robot_modelling.md)

## Model ownership

A virtual actuator model contains actuator plant and controller behavior. Coupled robot geometry and dynamics belong to the external simulator. Do not integrate the same joint mechanics in both systems.
