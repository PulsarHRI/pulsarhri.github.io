# ROS 2 Bridge

`pcp_ros2_bridge` connects PULSAR actuators to ROS 2 while keeping the same low-level PCP actuator behavior used by the [Python API](python_api/install_python_api.md) and [C++ API](cpp_api/install_cpp_api.md).

It supports two main workflows:

| Workflow | Use it for | Main entry point |
|---|---|---|
| Standard robot integration | Robot applications, planners, RViz, and trajectory control | `ros2_control` with `pcp_ros2_bridge/PcpSystemHardware` |
| PCP-specific actuator tools | Bring-up, parameters, diagnostics, raw feedback, virtual DTwin utilities, speed tests, and torque tests | Direct bridge topics, services, and `pcp_bridge_cli.py` |

<p align="center">
  <img src="/assets/images/pcp_ros2_bridge_golden_path.svg" alt="PCP ROS 2 bridge golden path" width="95%">
</p>

## Recommended Control Paths

For robot applications, use `ros2_control` as the motion owner:

```text
ROS 2 app or planner
  -> joint_trajectory_controller
  -> pcp_ros2_bridge/PcpSystemHardware
  -> PcpActuatorDriver
  -> pcp_api
  -> virtual DTwin or real PULSAR actuator
```

For actuator-specific inspection and tools, use the direct bridge:

```text
CLI, notebook, script, or dashboard
  -> /actuators/<name>/... topics and services
  -> pcp_ros2_bridge_node
  -> PcpActuatorDriver
  -> pcp_api
  -> virtual DTwin or real PULSAR actuator
```

!!! warning
    Do not use the direct bridge command path and the `ros2_control` hardware plugin as simultaneous command owners for the same real actuator. Pick one motion owner, then use read-only tools for inspection.

## What Should I Start With?

| Situation | Start here | Why |
|---|---|---|
| I have no hardware | `pixi run first-run-virtual`, then `pixi run launch-control-demo-rviz` | Validates the install with a virtual DTwin actuator, then shows the recommended `ros2_control` robot path in RViz. |
| I have one actuator | `pixi run launch-real`, then `pixi run real-info` and `pixi run real-state` | Starts from a conservative real-actuator config where motion is disabled until you explicitly command it. |
| I have a robot application | `pixi run launch-control-demo-rviz` or `ros2 launch pcp_ros2_bridge pcp_ros2_control.launch.py ...` | Uses the implemented `pcp_ros2_bridge/PcpSystemHardware` plugin with standard `joint_trajectory_controller` commands. |
| I need parameters or diagnostics | `ros2 run pcp_ros2_bridge pcp_bridge_cli.py ...` | Exposes PCP-specific information that standard ROS interfaces do not carry. |

## Current `ros2_control` Scope

| Interface | Supported today | Notes |
|---|---|---|
| `position` command | Yes | Used by `joint_trajectory_controller` and the demo robot assets. |
| `position`, `velocity`, `effort` state | Yes | Published through `ros2_control` state interfaces and `/joint_states`. |
| `velocity` or `effort` command | Not through `ros2_control` yet | Use the direct bridge CLI, topics, or services for speed and torque experiments. |

## Next Steps

- Install and build the package with [Install PCP ROS 2 Bridge](ros2_bridge/install_ros2_bridge.md).
- Use the terminal client from [Command-Line Interface](ros2_bridge/cli.md).
- Follow the [ROS 2 Bridge Tutorials](ros2_bridge/tutorials.md).
- Look up launch files, topics, services, and YAML files in the [ROS 2 Bridge Reference](ros2_bridge/reference.md).
