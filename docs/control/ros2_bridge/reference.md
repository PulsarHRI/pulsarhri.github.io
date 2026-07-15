# ROS 2 Bridge Reference

This page is a compact map of the ROS 2 pieces in `pcp_ros2_bridge`: launch files, topics, services, configs, and the `ros2_control` hardware plugin.

## Launch Files

| Launch file | Use |
|---|---|
| `pcp_ros2_bridge.launch.py` | Direct bridge launch using `config/pcp/multi_actuator_virtual.yaml` by default. |
| `pcp_virtual.launch.py` | Direct bridge launch for one virtual actuator using `config/pcp/single_actuator_virtual.yaml`. |
| `pcp_real.launch.py` | Direct bridge launch for one real actuator using `config/pcp/single_actuator_real.yaml`. The actuator starts disabled by default. |
| `pcp_ros2_control.launch.py` | Recommended robot-integration launch with robot description, `controller_manager`, controller spawners, optional RViz, and `pcp_ros2_bridge/PcpSystemHardware`. |

## Direct Bridge Node

Node:

```text
pcp_ros2_bridge_node
```

Purpose:
Expose configured PCP actuators through ROS 2 topics and services.

Main parameters:

| Name | Type | Default | Meaning |
|---|---|---|---|
| `config_file` | string | `config/pcp/multi_actuator_virtual.yaml` | YAML file describing transport, actuator names, backend type, feedback, and startup behavior. |
| `enable_direct_joint_trajectory` | bool | `false` | Compatibility option for the old direct `/joint_trajectory` input. Prefer `ros2_control` for robot commands. |

Subscribed topics:

| Topic | Type | Purpose |
|---|---|---|
| `/actuators/<name>/command` | `pcp_ros2_bridge/msg/ActuatorCommand` | Direct PCP-rich command for one actuator. |

Published topics:

| Topic | Type | Purpose |
|---|---|---|
| `/joint_states` | `sensor_msgs/msg/JointState` | Standard joint state output for direct bridge workflows. |
| `/diagnostics` | `diagnostic_msgs/msg/DiagnosticArray` | Standard diagnostics for ROS tools. |
| `/actuators/<name>/state` | `pcp_ros2_bridge/msg/ActuatorState` | PCP-rich state, including mode, enable state, voltage, temperature, and feedback items. |
| `/actuators/<name>/diagnostics` | `pcp_ros2_bridge/msg/ActuatorDiagnostics` | Namespaced bridge-specific diagnostic details. |
| `/actuators/<name>/battery_state` | `sensor_msgs/msg/BatteryState` | Voltage-style telemetry for standard ROS consumers. |
| `/actuators/<name>/motor_temperature` | `sensor_msgs/msg/Temperature` | Motor temperature. |
| `/actuators/<name>/electronics_temperature` | `sensor_msgs/msg/Temperature` | Electronics temperature. |

Services:

| Service | Type | Purpose |
|---|---|---|
| `/actuators/<name>/enable` | `std_srvs/srv/SetBool` | Enable or disable an actuator. |
| `/actuators/<name>/stop` | `std_srvs/srv/Trigger` | Stop an actuator. |
| `/actuators/<name>/home` | `std_srvs/srv/Trigger` | Set the current actuator position as home. |
| `/actuators/<name>/blink` | `std_srvs/srv/Trigger` | Blink the actuator LED. |
| `/actuators/<name>/get_info` | `pcp_ros2_bridge/srv/GetActuatorInfo` | Read static info, parameters, feedback, and diagnostics. |
| `/actuators/<name>/set_parameters` | `pcp_ros2_bridge/srv/SetActuatorParameters` | Set actuator parameters. Keep `save_to_nvm` false for tuning. |
| `/actuators/<name>/set_mode` | `pcp_ros2_bridge/srv/SetActuatorMode` | Change actuator control mode. |
| `/actuators/<name>/set_feedback_config` | `pcp_ros2_bridge/srv/SetFeedbackConfig` | Select streamed PCP feedback items and rate. |
| `/actuators/<name>/set_virtual_load` | `pcp_ros2_bridge/srv/SetVirtualLoad` | Set virtual actuator load torque. |
| `/actuators/<name>/step_virtual` | `pcp_ros2_bridge/srv/StepVirtualActuator` | Step a virtual actuator simulation explicitly. |
| `/pcp/list_ports` | `pcp_ros2_bridge/srv/ListPcpPorts` | List available PCP serial ports. |
| `/pcp/discover_dtwin_models` | `pcp_ros2_bridge/srv/DiscoverDtwinModels` | Discover DTwin models in a bindings directory. |

## `ros2_control` Hardware Plugin

Plugin:

```text
pcp_ros2_bridge/PcpSystemHardware
```

Purpose:
Expose PCP actuators as a `hardware_interface::SystemInterface` so standard ROS 2 controllers can command them.

Used by:

- `controller_manager`
- `joint_state_broadcaster`
- `joint_trajectory_controller`

Hardware parameters:

| Name | Type | Default | Meaning |
|---|---|---|---|
| `config_file` | string | required | PCP actuator YAML file used by `PcpActuatorDriver`. |
| `enable_on_activate` | bool | `false` | Enable actuators when `ros2_control` activates the hardware. Keep false for first real-hardware tests. |
| `command_epsilon` | double | `0.000001` | Minimum command change before sending a new PCP command. |

Interfaces:

| Interface | Direction | Meaning |
|---|---|---|
| `position` | command | Desired joint position in radians. |
| `position` | state | Measured joint position in radians. |
| `velocity` | state | Measured joint velocity in radians per second. |
| `effort` | state | Measured torque or effort in Nm. |

Unsupported `ros2_control` command interfaces:

| Interface | Use instead |
|---|---|
| `velocity` command | Direct bridge CLI, topic, or service speed commands. |
| `effort` command | Direct bridge CLI, topic, or service torque commands. |

## Configuration Files

PCP actuator configs live in `config/pcp/`. These files are read by `pcp_ros2_bridge_node` or `PcpSystemHardware`.

| File | Purpose |
|---|---|
| `config/pcp/multi_actuator_virtual.yaml` | Multi-actuator virtual bridge default used by `pcp_ros2_bridge.launch.py`. |
| `config/pcp/single_actuator_virtual.yaml` | Single virtual actuator quickstart. |
| `config/pcp/single_actuator_real.yaml` | Single real actuator with safe startup defaults, used by `pcp_real.launch.py`. |
| `config/pcp/paired_real_virtual.yaml` | Paired real and virtual actuator workflow. |
| `config/pcp/single_link_1dof_virtual.yaml` | PCP virtual config for the single-link `ros2_control` demo. |
| `config/pcp/pulse_arm_4dof_virtual.yaml` | PCP virtual config for the Pulse Arm 4DOF `ros2_control` demo. |

`ros2_control` controller configs live in `config/ros2_control/`. These files are read by `controller_manager`.

| File | Purpose |
|---|---|
| `config/ros2_control/single_link_1dof_controllers.yaml` | Controller plugins, joints, interfaces, and constraints for the single-link demo. |
| `config/ros2_control/pulse_arm_4dof_controllers.yaml` | Controller plugins, joints, interfaces, and constraints for the Pulse Arm 4DOF demo. |

## Package Tools

| Path | Purpose |
|---|---|
| `scripts/pcp_bridge_cli.py` | Terminal client for actuator inspection and simple direct bridge commands. |
| `scripts/pcp_bridge_benchmark.py` | Benchmark helper for bridge timing and throughput experiments. |
| `scripts/pcp_support_report.py` | Static support report. It does not connect to hardware or command motion. |
| `scripts/pcp_virtual_quickstart.py` | Virtual smoke-test helper used by `pixi run first-run-virtual`. |
| `scripts/ros2_control_trajectory_example.py` | Beginner trajectory client for `joint_trajectory_controller`. |

## Rule of Thumb

1. Use `ros2_control` when building a robot application.
2. Use `/joint_states`, `/diagnostics`, battery, and temperature topics for standard ROS consumers.
3. Use PCP-rich topics and services when you need actuator-specific information.
4. Keep `start_enabled: false` for first real-hardware bring-up.
5. Keep `save_to_nvm: false` while learning or tuning parameters.
6. Use `pixi run support-report` before asking for support.
