# Quickstart Tutorial: Python API for Real Actuator

This page walks you through running a Real Actuator connected via USB, and controlling it via Python scripting using [PULSAR HRI's Python API](../control/python_api/install_python_api.md) 

## 👣 Step-By-Step Guide
1. Make sure your actuator is set up and connected via USB, as per the [Quickstart Tutorial: Set up Real Actuator and connect via USB](../quickstarts/quickstart_set_up_usb.md) 

!!! tip
    You are of course free to run this straight from the terminal and installing libraries globally, but for a better experience we do recommend to: 

    - use an IDE such as [Visual Studio Code](https://code.visualstudio.com/download)

    - up a virtual environment using tools such as [venv](https://docs.python.org/3/library/venv.html) or [pipenv](https://pipenv.pypa.io/en/latest/quick_start.html) or [poetry](https://python-poetry.org/docs/) or [uv](https://docs.astral.sh/uv/getting-started/installation/#shell-autocompletion)

2. Install the PULSAR HRI Python API ([more details about it here](../control/python_api/install_python_api.md))
```bash
pip install --upgrade pcp_api
```

3. Check USB communication via the CLI tool ([more details about it here](../control/python_api/cli.md)):
```bash
pulsar-cli scan
```
You should see your actuator's ID and connection info.

4. Run the following script, the actuator should rotate at a constant speed for 5 seconds
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
    You’ve just sent your first command via the PULSAR Python API!
    Now you can explore doing much more by:

    - checkin out more [example scripts starting with this one](../control/python_api/example_single_actuator.md) and trying other communication methods beyond usb such as CAN

    - get intimate with the Python API code reference [starting from understanding the actuator classes and methods](../control/python_api/class_PulsarActuator.md) 

    - If you're interested in **simulating PULSAR actuators** without needing hardware, explore [how to create Virtual Actuators with the AUGUR Digital Twin](../set_up/set_up_virtual.md).

!!! question
    Need help or something doesn’t work? Head over to the [Support page](../support.md): we’ve got your back.
