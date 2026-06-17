# Quickstart Tutorial: Python API for a Real Actuator via USB

This page walks you through the fastest way to run a real actuator connected via USB and control it with Python. It installs the Python API globally so you can test quickly from a terminal.

For best-practice project setup, dependency management, and reusable examples, start with [Install Python API](../control/python_api/install_python_api.md), then follow the [Python API Examples](../control/python_api/examples.md) repository README, beginning with the quickstart examples.

## 👣 Step-by-Step Guide
1. Make sure your actuator is set up and connected via USB, as described in the [Quickstart Tutorial: Set Up a Real Actuator and Connect via USB](../quickstarts/quickstart_set_up_usb.md). 

!!! tip
    This quickstart is optimized for speed, not long-term project hygiene. For normal development, use the installation workflow in [Install Python API](../control/python_api/install_python_api.md) and run the maintained quickstarts and tutorials from [Python API Examples](../control/python_api/examples.md).

2. Install the [PULSAR HRI Python API](../control/python_api/install_python_api.md):
```bash
python -m pip install --upgrade pcp-api
```

3. Check USB communication using the [CLI tool](../control/python_api/cli.md):
```bash
pulsar-cli scan
```
You should see your actuator's ID and connection information.

4. Copy and paste the following command into your terminal. The actuator should rotate at a constant speed for 5 seconds:
```bash
python - <<'PY'
from time import sleep

from pcp_api import PcpOverUsb, PulsarActuatorReal

# Auto-detect the USB port and create the adapter
port = PcpOverUsb.get_port()
adapter = PcpOverUsb(port)

# Connect to actuator at address 0 (USB)
actuator = PulsarActuatorReal(adapter, 0)
actuator.connect()

# Set control mode and target speed
actuator.change_mode(PulsarActuatorReal.Mode.SPEED)
actuator.change_setpoint(1.0)  # rad/s

# Start and run for 5 seconds
actuator.start()
sleep(5)
actuator.disconnect()
adapter.close()
PY
```

!!! success
    You’ve just sent your first command using the PULSAR Python API!
    You can now do much more with it:

    - Following the [public Python examples repository](../control/python_api/examples.md), starting with the quickstart examples and then moving to the in-depth tutorials.
    
    - Trying communication methods beyond direct USB that enable control of multiple actuators, such as [PULSAR CAN Communication](../communicate/communicate_real.md#3-connect-via-can).

    - Becoming familiar with the Python API code reference, starting with [`PulsarActuatorReal`](../control/python_api/class_PulsarActuatorReal.md).

    - If you're interested in **simulating PULSAR actuators** without hardware, explore [how to create virtual actuators with the AUGUR Digital Twin](../set_up/set_up_virtual.md). The first public DTwin beta asset release is available for Linux x86_64 and Windows x86_64.

!!! question
    Need help or something doesn’t work? Head over to the [Support page](../support.md): we’ve got your back.
