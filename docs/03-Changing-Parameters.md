# 03. Advanced Features

This notebook demonstrates advanced configuration and control of a Pulsar actuator using the pcp_api library. It builds upon the basic example, which covers:

* Connecting to the actuator
* Setting feedback items and rates
* Running in speed mode with a fixed setpoint

## In this advanced tutorial, you will learn how to:

* 🔄 Reset the encoder to define a custom zero position
* 🆔 Change the actuator's PCP address dynamically
* ⚙️ Tune performance profiles (torque and speed)
* 🎛️ Set custom control parameters (e.g., stiffness and damping)
* 💾 Optionally save configuration to persistent memory

These features are useful for fine-tuning actuator behavior, multi-actuator setups, and persistent deployment scenarios.

## Import Required Modules

```py title="" 
# Import necessary modules
from pcp_api.PulsarActuator import PulsarActuator
from pcp_api.can_over_usb import CANoverUSB
from pprint import pprint
from time import sleep
```
## Detect and Connect to the CAN Adapter

```py title="" 
# Automatically detect the CAN port
port = CANoverUSB.get_port()
print(f"Connecting to {port}")

# Initialize the adapter
adapter = CANoverUSB(port)
```
## Initialize the Actuator

```py title="" 
# Create actuator instance with ID 0
actuator = PulsarActuator(adapter, 0)

# Attempt to connect
if not actuator.connect():
    print("Could not connect to the actuator")
    adapter.close()
    raise SystemExit("Exiting due to connection failure.")
print("Connected to the actuator")
```
Here we define the performance for Torque and Speed Loops:
* In this case we want a BALANCED behavior for the torque performance. 
* In thi case we want an AGRESSIVE mode for speed. 

Also it is possible to set some control parameters as the Damping Factor and The Stiffnes.

```py title=""
K_DAMPING = 7.7
K_STIFFNESS = 8.8 
```

```py title=""
try:
    # Reset encoder to define zero position
    actuator.reset_encoder_position()

    # Change the actuator's address (optional)
    actuator.changeAddress(0x15)

    # Set performance modes
    actuator.set_torque_performance(PulsarActuator.TorquePerformance.AGGRESSIVE)
    actuator.set_speed_performance(PulsarActuator.SpeedPerformance.AGGRESSIVE)

    # Set control parameters
    actuator.set_parameters({
        PulsarActuator.PCP_Parameters.K_DAMPING: K_DAMPING ,
        PulsarActuator.PCP_Parameters.K_STIFFNESS: K_STIFFNESS,
    })

    # Optional: Save configuration to persistent memory
    actuator.save_config()

except KeyboardInterrupt:
    print("Interrupted by user.")
    
finally:
    actuator.disconnect()
    sleep(0.1)
    adapter.close()
    print("Disconnected and cleaned up.")
```
# Run and Verify That the Motor Control Behaves as Required

```py title=""
def actuator_feedback(address: int, feedback: dict):
    print(feedback)
    speed_fb = feedback.get(PulsarActuator.PCP_Items.SPEED_FB, None)
    if speed_fb is not None:
        print(f"Actuator 0x{address:X} Speed feedback: {speed_fb:.2f} rad/s")
        
ACTUATOR_ADDRESS = 0
       
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