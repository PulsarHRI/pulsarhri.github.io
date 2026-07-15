# Command-Line Interface

The `pcp_ros2_bridge` package provides a user-facing command-line client:

```text
scripts/pcp_bridge_cli.py
```

It wraps the namespaced ROS 2 API so users can inspect, configure, enable, disable, stop, home, blink, and command actuators without writing full `ros2 service call` or `ros2 topic pub` commands.

!!! warning
    The ROS 2 bridge must be running before using the CLI. For example, start a virtual actuator with `pixi run launch-virtual` or a real actuator with `pixi run launch-real`.

## Actuator Names

The default package configs use these actuator names:

| Workflow | Default actuator |
|---|---|
| Single virtual actuator | `joint_1_virtual` |
| Single real actuator | `joint_1_real` |
| Multi-actuator virtual example | Names from `config/pcp/multi_actuator_virtual.yaml` |

The CLI talks to namespaced endpoints such as:

```text
/actuators/<name>/state
/actuators/<name>/command
/actuators/<name>/get_info
/actuators/<name>/enable
```

## Basic Information

Read static information, connection state, mode, diagnostics, and configured feedback:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py info joint_1_virtual
```

Include all public bridge-supported parameters:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py info joint_1_virtual --all-parameters
```

Include all cached feedback items:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py info joint_1_virtual --all-feedback
```

## Read Actuator State

Print one state sample:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py state joint_1_virtual
```

Wait for a fresh sample before printing:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py state joint_1_virtual --wait
```

## Read Parameters

Read all public bridge-supported parameters:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py param-get joint_1_virtual
```

Read selected parameters:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py param-get joint_1_virtual LIM_TORQUE KP_SPEED KI_SPEED
```

## Set Parameters

Set one parameter without saving it permanently:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py param-set joint_1_virtual LIM_TORQUE 2.0
```

Persist a parameter to non-volatile memory only when you intentionally want that value to survive power cycles:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py param-set joint_1_virtual LIM_TORQUE 2.0 --save-to-nvm
```

!!! tip
    Keep `save_to_nvm: false` in YAML files and avoid `--save-to-nvm` while learning or tuning.

## Change Actuator State

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py enable joint_1_virtual
ros2 run pcp_ros2_bridge pcp_bridge_cli.py disable joint_1_virtual
ros2 run pcp_ros2_bridge pcp_bridge_cli.py stop joint_1_virtual
ros2 run pcp_ros2_bridge pcp_bridge_cli.py home joint_1_virtual
ros2 run pcp_ros2_bridge pcp_bridge_cli.py blink joint_1_virtual
```

For real hardware, validate read-only state first:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py info joint_1_real
ros2 run pcp_ros2_bridge pcp_bridge_cli.py state joint_1_real
```

## Change Control Mode

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py mode joint_1_virtual SPEED
ros2 run pcp_ros2_bridge pcp_bridge_cli.py mode joint_1_virtual POSITION
ros2 run pcp_ros2_bridge pcp_bridge_cli.py mode joint_1_virtual TORQUE
```

The low-level mode behavior follows the actuator control modes described in [Control Modes Overview](../control_modes_explained/control_modes_overview.md).

## Send Motion Commands

Set speed mode, enable the actuator, and send a small speed command:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py speed joint_1_virtual 0.05 --set-mode --enable
```

Send a speed command without changing mode or enabling:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py speed joint_1_virtual 0.25
```

Send a position command:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py position joint_1_virtual 0.0 --set-mode --enable
```

Send a torque command:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py torque joint_1_virtual 0.01 --set-mode --enable
```

Publish a generic direct bridge command:

```bash
ros2 run pcp_ros2_bridge pcp_bridge_cli.py command joint_1_virtual POSITION 0.1
```

!!! warning
    Motion commands can move real hardware. Keep the mechanism mounted safely, keep the motion range clear, and keep a power-off or disable path ready.

## Pixi Shortcuts

When working from the package root, the Pixi tasks provide common CLI shortcuts:

| Task | Equivalent action |
|---|---|
| `pixi run virtual-info` | Read info for `joint_1_virtual`. |
| `pixi run virtual-state` | Read state for `joint_1_virtual`. |
| `pixi run virtual-move` | Move `joint_1_virtual` to a small position target. |
| `pixi run virtual-zero` | Command `joint_1_virtual` back to zero. |
| `pixi run virtual-disable` | Disable `joint_1_virtual`. |
| `pixi run real-info` | Read info for `joint_1_real`. |
| `pixi run real-state` | Read state for `joint_1_real`. |
| `pixi run real-stop` | Stop `joint_1_real`. |
| `pixi run real-disable` | Disable `joint_1_real`. |
