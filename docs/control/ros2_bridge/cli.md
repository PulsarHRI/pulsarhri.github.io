# Command-Line Interface (CLI)

The [PCP ROS 2 bridge package](https://github.com/cconejob-arc/pcp_ros2_bridge) provides a user-facing command-line client:

```text
scripts/pcp_bridge_cli.py
```

It is a compact wrapper around the namespaced ROS2 API. It lets users inspect, configure, enable, disable, and command actuators without manually writing full `ros2 service call` or `ros2 topic pub` commands.

!!! warning
    The ROS 2 bridge must be running before using the CLI with the command `ros2 launch pcp_ros2_bridge pcp_ros2_bridge.launch.py` or `pixi run launch`

## Using the CLI

### Basic information

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py info joint_1
```

Include all public bridge-supported parameters:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py info joint_1 --all-parameters
```

Include all public feedback items:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py info joint_1 --all-feedback
```

### Read actuator state

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py state joint_1
```

### Read parameters

Read all public bridge-supported parameters:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py param-get joint_1
```

Read selected parameters:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py param-get joint_1 LIM_TORQUE KP_SPEED KI_SPEED
```

### Set parameters

Set `LIM_TORQUE`:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py param-set joint_1 LIM_TORQUE 2.0
```

### Change actuator state

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py enable joint_1
ros2 run pcp_ros2_bridge pcp_bridge_cli.py disable joint_1
ros2 run pcp_ros2_bridge pcp_bridge_cli.py stop joint_1
ros2 run pcp_ros2_bridge pcp_bridge_cli.py home joint_1
ros2 run pcp_ros2_bridge pcp_bridge_cli.py blink joint_1
```

### Change control mode

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py mode joint_1 SPEED
ros2 run pcp_ros2_bridge pcp_bridge_cli.py mode joint_1 POSITION
ros2 run pcp_ros2_bridge pcp_bridge_cli.py mode joint_1 TORQUE
```

### Send motion commands

Set speed mode, enable the actuator, and send a small speed command:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py speed joint_1 0.05 --set-mode --enable
```

Send a speed command without changing mode or enabling:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py speed joint_1 0.25
```

Send a position command:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py position joint_1 0.0 --set-mode --enable
```

Send a torque command:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py torque joint_1 0.01 --set-mode --enable
```
