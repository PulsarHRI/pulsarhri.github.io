# Install PCP ROS 2 Bridge


## Install ROS 2 package

Go to your ROS 2 workspace and clone the github repository:

```bash
git clone https://github.com/PulsarHRI/pcp_ros2_bridge
```

### Requirements

This package is recommended to be used with Pixi.

Install Pixi:

```bash
curl -fsSL https://pixi.sh/install.sh | sh
```
!!! note
  Restart the terminal after installing Pixi.

### Build with Pixi

From the package directory:

```bash
pixi install
pixi shell
pixi run build
```

The build task runs `colcon build` from the workspace root.

After a successful build, go back to your ROS 2 workspace and run:

```bash
source install/setup.bash
```

## Launch the bridge

From the package directory, and using pixi:

```bash
pixi run launch
```

Equivalent manual command:

```bash
ros2 launch pcp_ros2_bridge pcp_ros2_bridge.launch.py
```

The default launch file loads:

```text
config/actuators.yaml
```

If you want to use a custom configuration file, it is possible with the argument config_file as:

```bash
ros2 launch pcp_ros2_bridge pcp_ros2_bridge.launch.py \
  config_file:=/absolute/path/to/actuators.yaml
```

## Next Steps

Once the PCP ROS 2 bridge package is installed, you can:

* Use the [command-line interface](cli.md) to quickly interact with PULSAR hardware.
* Run the [tutorials](tutorials.md).
* Integrate the API into your own applications or research workflows.

If you encounter any issues, please open an [issue](https://github.com/PulsarHRI/pcp_ros2_bridge/issues).