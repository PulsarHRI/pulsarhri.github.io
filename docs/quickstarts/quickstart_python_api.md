# Quickstart Tutorial: Python API for a Real Actuator via USB

This page walks you through running a real actuator connected via USB and controlling it with Python using [PULSAR HRI's Python API](../control/python_api/install_python_api.md).

## 👣 Step-by-Step Guide
1. Make sure your actuator is set up and connected via USB, as described in the [Quickstart Tutorial: Set Up a Real Actuator and Connect via USB](../quickstarts/quickstart_set_up_usb.md). 

!!! tip
    You can run this directly from the terminal and install libraries globally, but for a better experience we recommend the following:

    - Use an IDE such as [Visual Studio Code](https://code.visualstudio.com/download)

    - Set up a virtual environment using tools such as [venv](https://docs.python.org/3/library/venv.html) or [pipenv](https://pipenv.pypa.io/en/latest/quick_start.html) or [poetry](https://python-poetry.org/docs/) or [uv](https://docs.astral.sh/uv/getting-started/installation/#shell-autocompletion)

2. Install the [PULSAR HRI Python API](../control/python_api/install_python_api.md):
```bash
pip install --upgrade pcp_api
```

3. Check USB communication using the [CLI tool](../control/python_api/cli.md):
```bash
pulsar-cli scan
```
You should see your actuator's ID and connection information.

4. Run the following script. The actuator should rotate at a constant speed for 5 seconds:
```python
from pcp_api import PCP_over_USB, PulsarActuator
from time import sleep

# Auto-detect the USB port and create the adapter
port = PCP_over_USB.get_port()
adapter = PCP_over_USB(port)

# Connect to actuator at address 0 (USB)
actuator = PulsarActuator(adapter, 0)
actuator.connect()

# Set control mode and target speed
actuator.change_mode(PulsarActuator.Mode.SPEED)
actuator.change_setpoint(1.0)  # rad/s

# Start and run for 5 seconds
actuator.start()
sleep(5)
actuator.disconnect()
adapter.close()

```

!!! success
    You’ve just sent your first command using the PULSAR Python API!
    You can now do much more with it:

    - Checking out more example scripts, starting with [the simple actuator example](../control/python_api/example_single_actuator_nb.ipynb).
    
    - Trying communication methods beyond direct USB that enable control of multiple actuators, such as [PULSAR CAN Communication](../communicate/communicate_real.md#3-connect-via-can).

    - Becoming familiar with the Python API code reference, starting with the [actuator classes and methods](../control/python_api/class_PulsarActuator.md).

    - If you're interested in **simulating PULSAR actuators** without hardware, explore [how to create virtual actuators with the AUGUR Digital Twin](../set_up/set_up_virtual.md).

!!! question
    Need help or something doesn’t work? Head over to the [Support page](../support.md): we’ve got your back.
