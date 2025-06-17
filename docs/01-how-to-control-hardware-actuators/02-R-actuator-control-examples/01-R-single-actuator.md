# Controlling One Target

This notebook demonstrates how to connect to a PULSAR HRI actuator using the pcp_api library and CANoverUSB, configure feedback settings, and control one actuator in speed mode.

## Import necessary modules

```py title="Import" 
# Import necessary modules
from pcp_api.PulsarActuator import PulsarActuator
from pcp_api.can_over_usb import CANoverUSB
from pprint import pprint
from time import sleep
```
## Define the actuator address

Specify the address of the actuator. Use `0` if you're connecting directly via USB. If you're using a CAN adapter, replace it with the appropriate PCP address assigned to your actuator.

```py title="Define the actuator address" 
ACTUATOR_ADDRESS = 0
```
## Define a feedback callback function

This function is automatically triggered whenever feedback is received from the actuator. It prints the full feedback dictionary and extracts the speed feedback (if available), displaying it in a readable format.

```py title="Define a feedback callback function" 
def actuator_feedback(address: int, feedback: dict):
    print(feedback)
    speed_fb = feedback.get(PulsarActuator.PCP_Items.SPEED_FB, None)
    if speed_fb is not None:
        print(f"Actuator 0x{address:X} Speed feedback: {speed_fb:.2f} rad/s")
```
## Connect to the actuator

Automatically detect the USB port, create the CAN adapter, and attempt to connect to the actuator. If the connection fails, the program exits gracefully.

```py title="Connect to the actuator"
port = CANoverUSB.get_port()  # auto-detect
print(f"Connecting to {port}")
adapter = CANoverUSB(port)
actuator = PulsarActuator(adapter, ACTUATOR_ADDRESS)

if not actuator.connect():
    print(f"Could not connect to the actuator {actuator.address}")
    adapter.close()
    exit(1)
else:
    print(f"Connected to the actuator {actuator.address}")
```
## Configure feedback and control settings

Set up the feedback configuration and control mode:

* High-frequency feedback includes speed, position, and torque.
* Low-frequency feedback includes bus voltage and motor temperature.
* The actuator is switched to SPEED mode and given a setpoint of 1 rad/s.
* Parameters are retrieved and printed for inspection.
* The actuator is started and feedback is monitored in a loop.

```py title="Configure feedback and control settings"
try:
    # High-frequency feedback includes speed, position, and torque.
    actuator.setHighFreqFeedbackItems([
        PulsarActuator.PCP_Items.SPEED_FB,
        PulsarActuator.PCP_Items.POSITION_FB,
        PulsarActuator.PCP_Items.TORQUE_FB,
    ])
    actuator.setHighFreqFeedbackRate(actuator.Rates.RATE_10HZ)
    actuator.set_feedback_callback(actuator_feedback)

    # Low-frequency feedback includes bus voltage and motor temperature.
    actuator.setLowFreqFeedbackItems([
        PulsarActuator.PCP_Items.VBUS,
        PulsarActuator.PCP_Items.TEMP_MOTOR,
    ])
    actuator.setLowFreqFeedbackRate(actuator.Rates.RATE_1HZ)

    # The actuator is switched to SPEED mode and given a setpoint of 1 rad/s.
    actuator.change_mode(PulsarActuator.Mode.SPEED)
    actuator.change_setpoint(1)  # rad/s

    # Parameters are retrieved and printed for inspection.
    params = actuator.get_parameters_all()
    pprint(params)
    
    # The actuator is started and feedback is monitored in a loop.
    # The loop will keep running until interrupted (e.g., by pressing `Stop` in the notebook).
    actuator.start()
    while True:
        sleep(0.1)  # actuator_feedback() should be triggered

```
## Shutdown
Ensure the actuator is properly disconnected and the adapter is closed when the program is interrupted (e.g., via Ctrl+C or notebook stop if running from a Jupyter notebook).

```py title="Shutdown"
#Disconnect the actuator and close the adapter when the program is interrupted.
except KeyboardInterrupt:
    pass
finally:
    actuator.disconnect()
    sleep(0.1)
    adapter.close()
```

## Full code

The Jupyter notebook can be downloaded [here](01-R-single-actuator.ipynb).

```py title="Full code" linenums="1"
# Import necessary modules
from pcp_api.PulsarActuator import PulsarActuator
from pcp_api.can_over_usb import CANoverUSB
from pprint import pprint
from time import sleep

ACTUATOR_ADDRESS = 0

def actuator_feedback(address: int, feedback: dict):
    print(feedback)
    speed_fb = feedback.get(PulsarActuator.PCP_Items.SPEED_FB, None)
    if speed_fb is not None:
        print(f"Actuator 0x{address:X} Speed feedback: {speed_fb:.2f} rad/s")

port = CANoverUSB.get_port()  # auto-detect
print(f"Connecting to {port}")
adapter = CANoverUSB(port)
actuator = PulsarActuator(adapter, ACTUATOR_ADDRESS)

if not actuator.connect():
    print(f"Could not connect to the actuator {actuator.address}")
    adapter.close()
    exit(1)
else:
    print(f"Connected to the actuator {actuator.address}")

try:
    # High-frequency feedback includes speed, position, and torque.
    actuator.setHighFreqFeedbackItems([
        PulsarActuator.PCP_Items.SPEED_FB,
        PulsarActuator.PCP_Items.POSITION_FB,
        PulsarActuator.PCP_Items.TORQUE_FB,
    ])
    actuator.setHighFreqFeedbackRate(actuator.Rates.RATE_10HZ)
    actuator.set_feedback_callback(actuator_feedback)

    # Low-frequency feedback includes bus voltage and motor temperature.
    actuator.setLowFreqFeedbackItems([
        PulsarActuator.PCP_Items.VBUS,
        PulsarActuator.PCP_Items.TEMP_MOTOR,
    ])
    actuator.setLowFreqFeedbackRate(actuator.Rates.RATE_1HZ)

    # The actuator is switched to SPEED mode and given a setpoint of 1 rad/s.
    actuator.change_mode(PulsarActuator.Mode.SPEED)
    actuator.change_setpoint(1)  # rad/s

    # Parameters are retrieved and printed for inspection.
    params = actuator.get_parameters_all()
    pprint(params)
    
    # The actuator is started and feedback is monitored in a loop.
    # The loop will keep running until interrupted (e.g., by pressing `Stop` in the notebook).
    actuator.start()
    while True:
        sleep(0.1)  # actuator_feedback() should be triggered


## Shutdown

#Disconnect the actuator and close the adapter when the program is interrupted.

except KeyboardInterrupt:
    pass
finally:
    actuator.disconnect()
    sleep(0.1)
    adapter.close()
```
