# Install PCP ROS 2 Bridge

This guide installs and builds `pcp_ros2_bridge`, the ROS 2 package for controlling PULSAR actuators through either the direct PCP bridge or the standard `ros2_control` path.

The package is designed to be used from a ROS 2 workspace, for example:

```text
ros_ws/
└── src/
    └── pcp_ros2_bridge/
```

## Requirements

- Linux x86_64.
- [Pixi](https://pixi.prefix.dev/dev/) for the packaged ROS 2 Jazzy development environment.
- USB/CAN adapter access when using real hardware.

Install Pixi:

```bash
curl -fsSL https://pixi.sh/install.sh | sh
```

!!! note
    Restart the terminal after installing Pixi so the `pixi` command is available.

For real actuator access on Ubuntu/Debian, your user may need serial-device permissions:

```bash
sudo usermod -aG dialout $USER
```

Log out and log back in after changing groups.

## Get the Package

Create a ROS 2 workspace and place the package in `src/`:

```bash
mkdir -p ~/ros_ws/src
cd ~/ros_ws/src
git clone https://github.com/PulsarHRI/pcp_ros2_bridge.git
```

If you received the package as an archive, extract it so the package folder is:

```text
~/ros_ws/src/pcp_ros2_bridge
```

## Install Assets and Build

From the package root:

```bash
cd ~/ros_ws/src/pcp_ros2_bridge
pixi install
pixi run setup
pixi run build
```

The `setup` task prepares:

- the local PCP C++ SDK used by the bridge,
- AUGUR DTwin actuator assets,
- robot assets for the demos,
- the Jupyter kernel used by the notebooks.

The `build` task runs `colcon build` from the ROS 2 workspace root and builds only `pcp_ros2_bridge`.

If the build fails because `pcp_api` is missing, run:

```bash
pixi run setup_pcp_api
pixi run build
```

## First Virtual Run

Run the complete no-hardware smoke test:

```bash
pixi run first-run-virtual
```

This launches one virtual actuator, moves `joint_1_virtual`, prints state, and shuts down cleanly. It validates the generated ROS 2 interfaces, the bridge executable, the PCP API binding, and the virtual DTwin backend.

## Launch Direct Bridge Workflows

Use the direct bridge for PCP-specific topics, services, diagnostics, parameters, speed commands, torque commands, and first real-actuator inspection.

Single virtual actuator:

```bash
pixi run launch-virtual
```

Equivalent manual command:

```bash
cd ~/ros_ws
source install/setup.bash
ros2 launch pcp_ros2_bridge pcp_virtual.launch.py
```

Single real actuator:

```bash
pixi run launch-real
```

Equivalent manual command:

```bash
cd ~/ros_ws
source install/setup.bash
ros2 launch pcp_ros2_bridge pcp_real.launch.py
```

The real-actuator default configuration keeps the actuator disabled on startup.

## Launch `ros2_control` Workflows

Use `ros2_control` for robot applications, planners, RViz, and trajectory control.

Terminal 1:

```bash
pixi run launch-control-demo-rviz
```

Terminal 2:

```bash
pixi run control-demo-command
```

The demo starts `robot_state_publisher`, `controller_manager`, `joint_state_broadcaster`, `joint_trajectory_controller`, and RViz for the `single_link_1dof` virtual robot.

Manual launch:

```bash
cd ~/ros_ws
source install/setup.bash
ros2 launch pcp_ros2_bridge pcp_ros2_control.launch.py robot:=single_link_1dof rviz:=true
```

The available demo robot names are:

| Robot | Purpose |
|---|---|
| `single_link_1dof` | One-joint virtual actuator demo. |
| `pulse_arm_4dof` | Four-joint Pulse Arm virtual demo. |

## Configuration Files

PCP actuator configs live in `config/pcp/`. They describe actuator names, backends, CAN addresses, feedback, startup behavior, and DTwin settings.

`ros2_control` controller configs live in `config/ros2_control/`. They describe controller plugins, joints, interfaces, update rates, and trajectory constraints.

Use a custom direct-bridge config:

```bash
ros2 launch pcp_ros2_bridge pcp_virtual.launch.py \
  config_file:=/absolute/path/to/my_pcp_config.yaml
```

Use custom `ros2_control` configs:

```bash
ros2 launch pcp_ros2_bridge pcp_ros2_control.launch.py \
  pcp_config_file:=/absolute/path/to/my_pcp_config.yaml \
  controllers_file:=/absolute/path/to/my_controllers.yaml
```

## Next Steps

- Use the [command-line interface](cli.md) to inspect and command configured actuators.
- Follow the [ROS 2 Bridge Tutorials](tutorials.md).
- Check launch files, topics, services, and configs in the [ROS 2 Bridge Reference](reference.md).
- For support, run `pixi run support-report` and include the generated output.
