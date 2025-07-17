# Controlling One Device

Learn how to control a Pulsar actuator through a step-by-step walkthrough covering connection setup, configuration, and basic motion control.
The full example is at the [bottom of the page](#full-example).

## Import necessary modules

```py
from pcp_api import PCP_over_USB, PulsarActuator
from time import sleep
```
## Instantiate the adapter

Pulsar devices understand the PCP protocol, which can be communicated over USB or CAN. The devices has a built-in USB interface, so you can connect directly to the actuator via USB. Alternatively, you can use a CAN adapter to connect to the actuator over a CAN bus. This can adapter is connected to the host computer via USB, so in both cases, you will use the `PCP_over_USB` class to create the adapter.

```py
port = "COM1"  # you need to specify the port of the device or the CAN adapter
# port = PCP_over_USB.get_port()  # there is also an auto-detect system that will find the first available port
print(f"Connecting to {port}")
adapter = PCP_over_USB(port)
```

## Instantiate the actuator

You can instantiate as many actuators as you want with the same CAN adapter. In this example we are going to control only one actuator, connected directly via USB. If you are using a CAN adapter, you need to specify the PCP address of the actuator. The PCP address is a unique identifier for each actuator. You can find this address with the  [CLI scan command](../../cli.md#scan-for-devices). If you are connecting directly via USB, use `0` as the address.

```py
ACTUATOR_ADDRESS = 0  # 0 for direct USB connection, or use the actuator address if using CAN adapter
actuator = PulsarActuator(adapter, ACTUATOR_ADDRESS)
actuator.connect()
print(f"Connected to the actuator {actuator.address} (model: {actuator.model}, firmware: {actuator.firmware_version})")
```

## Configure feedback

First, define a function to handle the feedback from the actuator. This function will be called whenever new feedback is received from the actuator.

```py
def actuator_feedback(address: int, feedback: dict):
    print(feedback)
```

Set up the feedback configuration:

* High-frequency feedback for data like speed, position, torque, ...
* Low-frequency feedback for data like bus voltage, temperatures....
You can set the feedback items you want to receive. The items are defined in `PulsarActuator.PCP_Items`. You can choose from items like `SPEED_FB`, `POSITION_FB`, `TORQUE_FB`, `VBUS`, `TEMP_MOTOR`, etc.

You can set the feedback rate for each type of feedback. The rates are defined in `PulsarActuator.Rates`, and you can choose from `RATE_1HZ`, `RATE_10HZ`, `RATE_100HZ`, `RATE_1KHZ`, or `DISABLED` to disable the feedback.

```py title="Configure feedback and control settings"
actuator.setHighFreqFeedbackItems([
    PulsarActuator.PCP_Items.SPEED_FB,
    PulsarActuator.PCP_Items.POSITION_FB,
    PulsarActuator.PCP_Items.TORQUE_FB,
    # You can add more items as needed
])
actuator.setHighFreqFeedbackRate(actuator.Rates.RATE_10HZ)

# Low-frequency feedback includes bus voltage and motor temperature.
actuator.setLowFreqFeedbackItems([
    PulsarActuator.PCP_Items.VBUS,
    PulsarActuator.PCP_Items.TEMP_MOTOR,
])
actuator.setLowFreqFeedbackRate(actuator.Rates.RATE_1HZ)

# Set the feedback callback function to handle the feedback data
actuator.set_feedback_callback(actuator_feedback)

# feedback_callback can be set to None to disable it
# and read the feedback manually with actuator.get_feedback()
```

As an alternative, do not set a callback function or call `actuator.set_feedback_callback(None)` and read the feedback manually using `feedback = actuator.get_feedback()`, but using a callback function is more efficient and allows you to process the feedback in real-time.


## Configure control settings

You can choose from different control modes, such as `SPEED`, `POSITION`, or `TORQUE`. These are defined in `PulsarActuator.Mode` In this example, we will use the speed mode. You can now set the setpoint for the actuator, which is the target speed in this case. The units are in SI (International System of Units), so the speed is in radians per second (rad/s), position in radians, and torque in Newton-meters (Nm).

```py title="Configure control settings"
    actuator.change_mode(PulsarActuator.Mode.SPEED)
    actuator.change_setpoint(1.0)  # rad/s
```


## Start the actuator

You can start the actuator with the current configuration with the `start()` method. This will begin the control loop and the actuator will start moving according to the setpoint you defined. The feedback will be received at the rates you configured earlier.
Its advisable to put these logic in a try-except block to ensure the actuator is properly disconnected and the adapter is closed when the program is interrupted (e.g., via Ctrl+C)

```py title="Shutdown"
try:
    # Put the configuration and control code here
    actuator.start()
    # The loop will keep running until interrupted (e.g., via Ctrl+C).
    while True:
        sleep(0.1)  # actuator_feedback() should be triggered
except KeyboardInterrupt:
    pass
finally:
    actuator.disconnect()  # will also stop the actuator
    sleep(0.1)
    adapter.close()
```

## Full Example

```py title="Full code" linenums="1"
from pcp_api import PCP_over_USB, PulsarActuator
from time import sleep


ACTUATOR_ADDRESS = 0  # 0 to indicate direct USB connection, or use the PCP address if using CAN adapter


def actuator_feedback(address: int, feedback: dict):
    print(feedback)
    speed_fb = feedback.get(PulsarActuator.PCP_Items.SPEED_FB, None)
    if speed_fb is not None:
        print(f"Actuator 0x{address:X} Speed feedback: {speed_fb:.2f} rad/s")


port = PCP_over_USB.get_port()  # auto-detect
# port = "COM1"
print(f"Connecting to {port}")
adapter = PCP_over_USB(port)
actuator = PulsarActuator(adapter, ACTUATOR_ADDRESS)

if not actuator.connect():
    print(f"Could not connect to the actuator {actuator.address}")
    adapter.close()
    exit(1)
print(f"Connected to the actuator {actuator.address} (model: {actuator.model}, firmware: {actuator.firmware_version})")
try:
    actuator.setHighFreqFeedbackItems([
        PulsarActuator.PCP_Items.SPEED_FB,
        PulsarActuator.PCP_Items.POSITION_FB,
        PulsarActuator.PCP_Items.TORQUE_FB,
    ])
    actuator.setHighFreqFeedbackRate(actuator.Rates.RATE_10HZ)
    actuator.set_feedback_callback(actuator_feedback)
    # feedback_callback can be set to None to disable it
    # and read the feedback manually with actuator.get_feedback()

    actuator.setLowFreqFeedbackItems([
        PulsarActuator.PCP_Items.VBUS,
        PulsarActuator.PCP_Items.TEMP_MOTOR,
    ])
    actuator.setLowFreqFeedbackRate(actuator.Rates.DISABLED)
    actuator.change_mode(PulsarActuator.Mode.SPEED)
    actuator.change_setpoint(1.0)  # rad/s because mode is SPEED

    actuator.start()
    print("Actuator started. Press Ctrl+C to stop.")
    while True:
        sleep(0.1)  # actuator_feedback() should be triggered
except KeyboardInterrupt:
    pass
finally:
    actuator.disconnect()  # also stops the actuator
    sleep(0.1)
    adapter.close()
```
