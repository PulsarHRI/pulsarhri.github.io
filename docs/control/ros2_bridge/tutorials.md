# PCP ROS 2 Bridge Tutorials

This page gives a recommended learning order for `pcp_ros2_bridge`. Start with the virtual workflow, then prove the standard `ros2_control` path, then connect real hardware in read-only mode before commanding motion.

!!! note
    Client software should communicate with the bridge through ROS 2 topics, services, or `ros2_control`. It should not call `pcp_api` directly.

## First-Day Acceptance Path

| Step | Command | Success looks like |
|---|---|---|
| Install and build | `pixi run setup` then `pixi run build` | The package builds without missing `pcp_api`, ROS 2, or asset errors. |
| Virtual smoke test | `pixi run first-run-virtual` | `joint_1_virtual` moves, state is printed, and the bridge shuts down cleanly. |
| Robot demo with RViz | `pixi run launch-control-demo-rviz` | RViz opens and the `single_link_1dof` model appears. |
| Standard trajectory command | `pixi run control-demo-command` | The robot moves through `joint_trajectory_controller`. |
| PCP-specific inspection | `pixi run launch-virtual`, then `pixi run virtual-info` | Info includes model, firmware, connection state, diagnostics, and feedback names. |
| Real actuator read-only check | `pixi run launch-real`, then `pixi run real-info` and `pixi run real-state` | The real actuator reports the expected model, address, voltage, temperature, and position while disabled. |

Stop before motion if any read-only real-hardware check looks wrong.

## Tutorial 1: Prove the Virtual Actuator Path

Run:

```bash
pixi run first-run-virtual
```

This tutorial validates the no-hardware path. Success means:

- the virtual bridge starts,
- `/actuators/joint_1_virtual/get_info` appears,
- the actuator moves to a small target,
- state is printed before and after motion,
- the actuator returns to zero unless the default options were changed.

This proves that the local ROS 2 environment, generated interfaces, bridge executable, PCP API binding, and AUGUR DTwin backend are usable.

## Tutorial 2: Discover Topics and Services

Terminal 1:

```bash
pixi run launch-virtual
```

Terminal 2:

```bash
pixi run topics
pixi run services
pixi run virtual-info
pixi run virtual-state
```

The most important direct bridge endpoints are namespaced by actuator:

| Endpoint | Type | Purpose |
|---|---|---|
| `/actuators/<name>/state` | Topic | PCP-rich state, including position, velocity, torque, voltage, temperature, mode, and enable state. |
| `/actuators/<name>/command` | Topic | Direct PCP-rich command for one actuator. |
| `/actuators/<name>/get_info` | Service | Static info, parameters, feedback, and diagnostics. |
| `/actuators/<name>/enable` | Service | Enable or disable an actuator. |
| `/actuators/<name>/stop` | Service | Stop an actuator. |

!!! success
    After this tutorial, users should understand that the direct bridge API is namespaced per actuator and that read-only inspection does not require motion.

## Tutorial 3: Use the Standard Robot Path

Use this when building robot applications, planners, RViz demos, or trajectory-control workflows.

Terminal 1:

```bash
pixi run launch-control-demo-rviz
```

Terminal 2:

```bash
pixi run control-demo-command
```

Success means:

- `controller_manager` starts,
- `joint_state_broadcaster` and `joint_trajectory_controller` load,
- RViz shows the `single_link_1dof` model,
- the trajectory command is sent through `joint_trajectory_controller`,
- motion is visible through `/joint_states`.

The same launch file also supports the Pulse Arm 4DOF demo:

```bash
pixi run launch-pulse-arm-control-demo-rviz
pixi run control-demo-pulse-arm-command
```

## Tutorial 4: Inspect PCP-Specific Data

Some actuator information does not fit in standard ROS interfaces. Use the direct bridge for parameters, diagnostics, DTwin load/step tools, speed experiments, torque experiments, and support checks.

Terminal 1:

```bash
pixi run launch-virtual
```

Terminal 2:

```bash
pixi run virtual-info
pixi run virtual-state
ros2 run pcp_ros2_bridge pcp_bridge_cli.py param-get joint_1_virtual
```

This path should print actuator name, PCP address, model, firmware, connection state, mode, enable state, diagnostics, voltage, temperature, position, velocity, torque, and configured feedback.

## Tutorial 5: Connect One Real Actuator Safely

Edit:

```text
config/pcp/single_actuator_real.yaml
```

Check:

- `port` matches the adapter, or is intentionally `auto`,
- `address` matches the actuator CAN address,
- `real.address` matches `address`,
- `start_enabled` remains `false`,
- `startup_parameters` remains `{}` while learning.

Terminal 1:

```bash
pixi run launch-real
```

Terminal 2:

```bash
pixi run real-info
pixi run real-state
```

Success means:

- `connected: true`,
- the model is the expected PULSAR actuator,
- voltage and temperatures are plausible,
- position feedback is stable,
- diagnostics do not report unexpected connection or backend errors.

Do not move the real actuator until these read-only checks pass.

## Tutorial 6: First Real Motion

Use a staged command sequence so every side effect is visible:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py info joint_1_real
ros2 run pcp_ros2_bridge pcp_bridge_cli.py state joint_1_real
ros2 run pcp_ros2_bridge pcp_bridge_cli.py mode joint_1_real SPEED
ros2 run pcp_ros2_bridge pcp_bridge_cli.py enable joint_1_real
ros2 run pcp_ros2_bridge pcp_bridge_cli.py speed joint_1_real 0.02
ros2 run pcp_ros2_bridge pcp_bridge_cli.py stop joint_1_real
ros2 run pcp_ros2_bridge pcp_bridge_cli.py disable joint_1_real
```

!!! warning
    This tutorial can move real actuator hardware. Make sure the actuator is mechanically safe to move, the output shaft is clear or properly constrained, and a power-off or disable path is ready.

## Notebook Tutorials

The package also includes Jupyter notebooks.

Run:

```bash
pixi run setup
pixi run build
pixi run notebooks
```

Use the Jupyter kernel named:

```text
Python (pcp_ros2_bridge)
```

Recommended quickstart order:

| Notebook | Backend | Purpose |
|---|---|---|
| `quickstarts/V_01_virtual_dtwin_quickstart.ipynb` | virtual | First no-hardware bridge launch and virtual actuator motion. |
| `quickstarts/V_02_virtual_topics_and_services.ipynb` | virtual | Explore ROS topics, services, and CLI. |
| `quickstarts/V_03_ros_single_actuator_basic_control.ipynb` | virtual | Move one virtual actuator through ROS 2. |
| `quickstarts/R_01_real_hardware_safety.ipynb` | real | Read-only real-hardware connection and safety checks. |
| `quickstarts/R_02_ros_real_single_actuator_basic_control.ipynb` | real | Carefully move one real actuator after safety checks. |
| `quickstarts/RV_01_paired_sim2real_quickstart.ipynb` | paired | Mirror a small command to paired real and virtual backends. |

Advanced notebooks:

| Notebook | Backend | Purpose |
|---|---|---|
| `advanced/A_01_parameters_feedback_and_virtual_services.ipynb` | virtual | Read/set parameters, configure feedback, discover DTwin models, set virtual load, and step the virtual actuator. |
| `advanced/A_02_mujoco_visual_position_control.ipynb` | virtual/MuJoCo | Command position through ROS 2 and visualize the resulting state trajectory with MuJoCo. |

## Support Report

Before asking for support, run:

```bash
pixi run support-report
```

Include the generated report with the command you ran, terminal output around the failure, the YAML config you selected, whether the actuator was virtual, real, or paired, and whether motion was commanded through `ros2_control` or the direct bridge.
