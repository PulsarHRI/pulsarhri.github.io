AUGUR Digital Twin
{ .pulsar-home-eyebrow }

# Robot modelling

This page describes how to build external robot models for co-simulation use between rigid-body simulators and AUGUR virtual actuators. Read the [co-simulation coupling](co_sim_coupling.md) first for more information; the models described here supplies the robot dynamics used to calculate each actuator's load.

## Model one actuator-driven joint

Represent each PULSE actuator as one revolute robot joint between a parent link and a child link:

```text
parent link ── revolute joint ── child link
                    │
                    └── one PulsarActuatorVirtual
```

The joint coordinate must describe the actuator output shaft directly:

- angle in radians;
- angular velocity in radians per second;
- joint effort in N·m;
- double check the joint axis and positive direction matching the AUGUR actuator;
- gear ratio of 1 at the coupling boundary, because AUGUR already reports output-shaft state and accounts internally for transmission and its effects.

Give every coupled joint a stable name and map it to one virtual actuator address in the integration code.

## Divide the physical properties correctly

The external model should -depending on the format- include:

- the mass, center of mass, and inertia of every robot link;
- actuator housing and structural mass assigned to the link that carries it;
- downstream brackets, output flanges, tools, and payloads assigned to the appropriate link;
- any mechanism-level damping, springs, or friction not represented by AUGUR, like external bearings, belt drive, linkages, etc;
- visual and collision geometry;
- environmental contacts and constraints.

Do not add duplicate motor or transmission model to an AUGUR-owned joint. In particular, do not duplicate:

- motor rotor inertia;
- reflected gearbox inertia;
- drivetrain friction;
- a torque, position, velocity, or impedance drive;
- simulator armature added for the virtual actuator.

## Build a multi-joint robot

For a serial robot, repeat the same pattern for each degree of freedom:

```text
base ─ joint_1 ─ link_1 ─ joint_2 ─ link_2 ─ ... ─ joint_n ─ link_n
          │                    │                              │
       AUGUR 1              AUGUR 2                        AUGUR n
```

Each independently actuated revolute joint needs:

1. one joint coordinate in the robot model;
2. one `PulsarActuatorVirtual` in the shared `VirtualWorld`;
3. one joint-name-to-actuator-address mapping;
4. the same zero position and positive direction in both systems.

Dependent joints, mimic joints, tendons, closed loops, and compliant transmissions need an explicit constraint or transmission model. Do not assign an independent AUGUR virtual actuator to a dependent coordinate unless the physical robot actually has one there, which is very unlikely, but for example an AUGUR actuator connected to a rod that is also actuated by a linear motor, both will see the dependant motion as load and will result in undefined behavior.

## Common model checklist

Before choosing a file format, define:

| Property | What to provide |
| --- | --- |
| Link frames | A consistent parent-to-child frame convention |
| Joint origin | Position and orientation of the output shaft relative to the parent link |
| Joint axis | Unit axis with the same positive direction as AUGUR |
| Joint limits | Physical lower, upper, velocity, and effort limits where supported |
| Link inertia | Mass, center of mass, and a valid positive-definite inertia tensor |
| Collision geometry | Simple, stable shapes where possible |
| Visual geometry | Optional detailed meshes, separate from collision meshes |
| Passive mechanics | Only effects outside the AUGUR drivetrain model |
| Simulator drive | None on an AUGUR-owned joint |

Start with a single joint and no contact. Add the remaining links, then gravity, and contacts only after the basic joint mapping is correct.

| Simulator | Typical input |
| --- | --- |
| MuJoCo | MJCF; URDF can be imported and inspected |
| Gazebo | SDF or URDF |
| Newton | URDF, MJCF, or OpenUSD |
| Other simulators | Their native format or a verified URDF/MJCF/OpenUSD importer |

=== "MuJoCo"
    
    MuJoCo's default format is MJCF, but also accepts import and translation of URDF and OpenUSD (experimental).
    MJCF represents a robot through nested bodies. A minimal hinge joint has this structure:
    
    ```xml
    <mujoco model="augur_robot">
      <compiler angle="radian"/>
      <worldbody>
        <body name="base">
          <body name="link_1" pos="0 0 0">
            <joint name="joint_1" type="hinge" axis="0 0 1"
                   range="-1.57 1.57" armature="0"/>
            <inertial pos="0 0 0.1" mass="2.0"
                      diaginertia="0.02 0.02 0.01"/>
            <geom type="mesh" mesh="link_1_visual" contype="0" conaffinity="0"/>
            <geom type="capsule" size="0.04 0.2"/>
          </body>
        </body>
      </worldbody>
    </mujoco>
    ```
    
    For an AUGUR-owned joint:
    
    - use a hinge joint whose axis and reference position match AUGUR, or invert the direction inside `PulsarActuatorVirtual`;
    - keep `armature="0"` unless it represents mechanism inertia not already in AUGUR;
    - omit an entry for that joint from the MJCF `<actuator>` section;
    - use joint damping, friction loss, and springs only for passive mechanism effects outside the actuator model;
    - keep detailed visual meshes separate from simpler collision geometry where practical.
    
    URDF import can provide an initial MuJoCo model, but inspect the converted inertias, joint ranges, mesh scales, and any generated actuator or armature settings before using it for co-simulation. MuJoCo had previously had issues with importing inertias correctly from URDF especially if they use diagnoal not the full inertia values, its worth a double check if you're seeing unexpected behavior.

=== "Gazebo"
    
    Gazebo work primarily with URDF and SDF formats.
    URDF represents a robot as links connected by joints. A minimal actuator-driven revolute joint has this structure:
    
    ```xml
    <link name="base"/>
    
    <link name="link_1">
      <inertial>
        <origin xyz="0 0 0.1" rpy="0 0 0"/>
        <mass value="2.0"/>
        <inertia ixx="0.02" ixy="0" ixz="0"
                 iyy="0.02" iyz="0" izz="0.01"/>
      </inertial>
      <visual>...</visual>
      <collision>...</collision>
    </link>
    
    <joint name="joint_1" type="revolute">
      <parent link="base"/>
      <child link="link_1"/>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <axis xyz="0 0 1"/>
    </joint>
    ```
    
    For an AUGUR-owned joint:
    
    - use `revolute` for a limited joint or `continuous` for an unlimited rotary joint;
    - make the URDF axis match the actuator's positive output direction or you can simply invert the direction in the `PulsarActuatorVirtual` class;
    - omit transmissions and controller plugins that apply effort to that joint;
    - avoid joint damping or friction values that duplicate actuator drivetrain losses. you can add them if you physcially have extra mechanisms that physically add this behavior in addition to the actuator internals, such as bearings, springs, belt drives, etc.
    
    Gazebo can consume URDF or SDF. In SDF, create the equivalent `model`, `link`, and `joint` elements and leave the coupled joint without a competing drive plugin. Use Gazebo-specific sensors, contact parameters, and environment definitions only for effects that belong to the robot or world model.

=== "Newton" 
    
    Newton can work with several formats since it has many internal solvers (including MuJoCo for rigid body), so it can support MJCF, but it is recommended to use OpenUSD to work seamlessly with the other solvers.

    In OpenUSD, represent the robot as a rigid-body articulation:
    
    1. create one rigid body for each link;
    2. assign mass properties and collision geometry to each body;
    3. connect parent and child bodies with a revolute physics joint;
    4. set the joint frames, axis, and limits to match the actuator output shaft;
    5. apply the articulation schema expected by the target simulator;
    6. do not apply a joint drive schema to an AUGUR-owned joint.
    
    Newton can build a model from URDF, MJCF, or OpenUSD. Whichever source is used, verify the resulting articulation, joint axes, inertias, collision shapes, units, and drive settings after import. Prefer a native OpenUSD representation when an importer cannot preserve those properties reliably.

=== "Other Simulators"
    
    The same model structure applies to another simulator or native format:
    
    - rigid links carry mass and inertia;
    - revolute joints define the AUGUR output coordinates;
    - the environment supplies gravity, contacts, and constraints;
    - no second actuator drives an AUGUR-owned joint.
    
    A file format being accepted by a simulator does not guarantee that the simulator exposes the state-imposition and inverse-dynamics operations required by the coupling. Confirm those capabilities before investing in a detailed model.

## Verify the model before coupling

Check the robot model independently:

1. link masses and centers of mass match the intended mechanism;
2. inertia tensors are valid and expressed in the correct frames;
3. joint axes, zeros, limits, and mesh scales are correct;
4. collision shapes do not begin in penetration;
5. gravity produces the expected joint-load direction and approximate magnitude;
6. no hidden drive, transmission, armature, or duplicated drivetrain loss remains, including the default values of each simulator since some inject base damping values to stabelize their solvers;
7. a single-joint inverse-dynamics test agrees with expected result or a hand calculation.

Then apply the convergence, energy, multi-joint, limit, and contact tips from [Co-simulation coupling](co_sim_coupling.md#validation).
