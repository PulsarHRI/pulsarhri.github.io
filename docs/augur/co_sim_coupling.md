AUGUR Digital Twin
{ .pulsar-home-eyebrow }

# Co-simulation coupling

AUGUR can be coupled to any multibody simulator that can evaluate the joint load produced by a robot model at an imposed joint state.

The coupling has one essential ownership rule:

- **AUGUR owns and integrates each coupled actuator's position and velocity.**
- **The external simulator owns the robot links, inertia, gravity, contacts, constraints, and other mechanism dynamics.**

Do not let both systems integrate the same joint. The simulator must calculate the load for an AUGUR-owned joint without forward-integrating that joint or applying a second actuator model to it.

## AUGUR's Interface

For co-simulation, each virtual actuator can be treated as a stateful function:

$$
\left(x_{a,k+1}, q_{k+1}, \dot q_{k+1}\right)
= F_{\mathrm{AUGUR}}\left(u_k, \tau_{L,k}, \Delta t_c\right),
$$

where:

- $x_a$ is AUGUR's internal actuator state which includes all values reported by the real/physical actuator;
- $u$ is the command sent through Pulsar SDK;
- $\tau_L$ is the load at the actuator output shaft, in N·m;
- $q$ and $\dot q$ are output-shaft position and velocity, in rad and rad/s;
- $\Delta t_c$ is the coupling interval.

AUGUR contains its own dynamics and integrator. The external simulator therefore receives $q$ and $\dot q$ from AUGUR and returns the load $\tau_L$ required by the robot mechanism.

Use the same positive direction for the AUGUR output shaft and the corresponding robot joint. Pass the simulator's required joint load to AUGUR in that natural joint sign; no additional sign inversion is needed.

## Robot dynamics

For $n$ coupled joints, a robot model can be written as

$$
M(q)\ddot q + h(q, \dot q) = \tau_L + \tau_{\mathrm{ext}},
$$

where:

- $M(q)$ is the joint-space mass matrix;
- $h(q, \dot q)$ contains gravity, Coriolis, centrifugal, passive, constraint, and contact effects represented by the simulator;
- $\tau_{\mathrm{ext}}$ contains any separately applied generalized forces that might be in the simulation, like contacts, interaction forces, etc.;
- $\tau_L$ is the generalized effort that the coupled actuators must provide.

The external simulator evaluates the corresponding inverse-dynamics problem:

$$
\tau_L = M(q)\ddot q + h(q, \dot q) - \tau_{\mathrm{ext}}.
$$

In practice, use the simulator's inverse-dynamics or generalized-effort result rather than assembling these terms manually. Contacts and constraints may require the simulator's own solver.

Do not duplicate/define motor rotor inertia, reflected gearbox inertia, drivetrain friction, motor/actuator damping, or joint limits, these are either already represented by AUGUR or can be set as parameters, like limits for example. On the other hand, keep link inertia, gravity, mechanism damping or springs, contacts, constraints, and externally applied forces in the robot model. Basically anything that is inside the actuator's envlope is modeled by AUGUR, anything attached to it, should be defined in the simulator.

## Coupling timestep

AUGUR's internal timestep is

$$
\Delta t_a = 50\ \mu\mathrm{s} = \frac{1}{20{,}000}\ \mathrm{s}.
$$

Choose a coupling interval that is an integer multiple of this timestep:

$$
\Delta t_c = N\Delta t_a, \qquad N \in \mathbb{N}^{+}.
$$

For example, a 1000 Hz exchange rate has $\Delta t_c=0.001$ s and $N=20$ AUGUR ticks. Smaller coupling intervals reduce the one-exchange load delay and usually improve stability. All actuators in one `VirtualWorld` must advance together.

## Exchange algorithm

This is an explicit co-simulation scheme. During exchange $k$, AUGUR uses the load calculated at the previous exchange.

1. Hold $\tau_{L,k-1}$ constant and advance every virtual actuator by $\Delta t_c$.
2. Read the new output-shaft state $q_k$ and $\dot q_k$ from AUGUR.
3. If needed, you can also estimate acceleration from the exchange-rate velocity difference which could improve the simulator's stability. The currently validated estimator applies a first-order 10 Hz low-pass filter:

   $$
   \ddot q_k^{\mathrm{raw}} = \frac{\dot q_k-\dot q_{k-1}}{\Delta t_c},
   $$

   $$
   \alpha = 1-e^{-2\pi(10)\Delta t_c},
   $$

   $$
   \ddot q_k = \ddot q_{k-1}
   + \alpha\left(\ddot q_k^{\mathrm{raw}}-\ddot q_{k-1}\right).
   $$

4. Initialize $\dot q_{-1}$ and $\ddot q_{-1}$ to zero. The filter limits load noise caused by differentiating quantized velocity, especially near contacts and constraints. Changing the filter changes the coupled dynamics and requires new convergence and energy validation.
5. Impose $q_k$, $\dot q_k$, and $\ddot q_k$ on the corresponding robot joints without advancing those joint coordinates in the external simulator.
6. Refresh the simulator's kinematics, contacts, and constraints, then evaluate inverse dynamics or the equivalent generalized-effort calculation.
7. Read the required joint load $\tau_{L,k}$, accounting once for any separately applied generalized forces already included in the simulator result.
8. Pass $\tau_{L,k}$ directly to AUGUR for the next exchange.

In compact form:

$$
\tau_{L,k-1}
\xrightarrow{\ F_{\mathrm{AUGUR}}\ }
(q_k,\dot q_k)
\xrightarrow{\ \mathrm{differentiate/filter\ if\ needed}\ }
\ddot q_k
\xrightarrow{\ \mathrm{robot\ inverse\ dynamics}\ }
\tau_{L,k}.
$$

## External simulator requirements

The simulator or its integration layer written by you must be able to:

- represent the robot's multibody dynamics, contacts, and constraints;
- accept imposed $q$, $\dot q$, and optional $\ddot q$ for AUGUR-owned joints;
- update kinematics and constraints without forward-integrating those joints;
- calculate the generalized joint effort required by the imposed motion;
- expose that effort in N·m for each coupled revolute joint.

Loading URDF, MJCF, SDF, or OpenUSD does not by itself guarantee these capabilities. A simulator that can only forward-integrate the coupled joints cannot implement this ownership partition directly.

## Supported model scope

The validated partition covers fixed-base robots where every independently actuated coordinate is owned by AUGUR. The external simulator owns the links and environmental dynamics, but it does not contain another motor, drive, transmission, or forward-integrated state for those coordinates.

Floating-base robots and mixed coordinate ownership require a coupled solve. For example, if the simulator owns a free base while AUGUR owns the joints, base acceleration, contact reactions, and actuator loads depend on each other. Stepping the simulator and then overwriting the actuator joints does not solve that system consistently.

Compliant transmissions, stiff impacts, closed-loop mechanisms, and other strongly constrained systems may also require model-specific coupling and stability work.

## Validation

Validate each robot model and coupling implementation with:

1. no-load motion matching the standalone AUGUR actuator;
2. joint-load direction and magnitude checks;
3. constant external torque tests;
4. trajectory convergence as the exchange rate increases, we recommends starting from >= 500hz, but depends on the platform and trajectories;
5. bounded uncommanded energy and passive behavior;
6. multi-joint cross-inertial coupling;
7. finite contact loads, bounded penetration, and converging contact trajectories;
8. joint-limit and collision behavior.

A useful starting sweep is 100, 200, 500, and 1,000 Hz. Passing these checks confirms the implementation for the tested mechanism and operating range.

See [Robot modelling](robot_modelling.md) for constructing the external robot model in URDF, MJCF, SDF, OpenUSD, or another simulator format.
