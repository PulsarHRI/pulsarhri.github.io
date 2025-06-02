# 01. Controlling One Target

This notebook demonstrates how to connect to a Pulsar actuator using the `pcp_api` library and `CANoverUSB`, configure feedback settings, and control one actuator in speed mode.

```py title="" 
# Import necessary modules
from pcp_api.PulsarActuator import PulsarActuator
from pcp_api.can_over_usb import CANoverUSB
from pprint import pprint
from time import sleep
```
## Define the actuator address

Use `0` for direct USB connection. If using a CAN adapter, specify the appropriate PCP address.

```py title="" 
ACTUATOR_ADDRESS = 0
```
## Define a feedback callback function

This function will be called automatically when feedback is received from the actuator.

```py title="" 
def actuator_feedback(address: int, feedback: dict):
    print(feedback)
    speed_fb = feedback.get(PulsarActuator.PCP_Items.SPEED_FB, None)
    if speed_fb is not None:
        print(f"Actuator 0x{address:X} Speed feedback: {speed_fb:.2f} rad/s")
```
## Connect to the actuator

Automatically detect the USB port and establish a connection to the actuator.

```py title=""
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

Set high-frequency and low-frequency feedback items, change the actuator mode to SPEED, and set a speed setpoint.

```py title=""
try:
    actuator.setHighFreqFeedbackItems([
        PulsarActuator.PCP_Items.SPEED_FB,
        PulsarActuator.PCP_Items.POSITION_FB,
        PulsarActuator.PCP_Items.TORQUE_FB,
    ])
    actuator.setHighFreqFeedbackRate(actuator.Rates.RATE_10HZ)
    actuator.set_feedback_callback(actuator_feedback)

    actuator.setLowFreqFeedbackItems([
        PulsarActuator.PCP_Items.VBUS,
        PulsarActuator.PCP_Items.TEMP_MOTOR,
    ])
    actuator.setLowFreqFeedbackRate(actuator.Rates.RATE_1HZ)

    actuator.change_mode(PulsarActuator.Mode.SPEED)
    actuator.change_setpoint(1)  # rad/s
    # Retrieve and Display Actuator Parameters
    params = actuator.get_parameters_all()
    pprint(params)
    
    # Start the actuator and monitor feedback

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
