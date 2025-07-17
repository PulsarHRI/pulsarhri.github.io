# Advanced Features

This notebook demonstrates advanced configuration and control of a PULSAR HRI actuator. It builds upon the basic example.

In this document you will learn how to:

* 🔄 Reset the encoder to define a custom zero position
* 🆔 Change the actuator's PCP address dynamically
* ⚙️ Tune performance profiles (torque and speed)
* 🎛️ Set custom control parameters (e.g., stiffness and damping)
* 💾 Optionally save configuration to persistent memory

These features are useful for fine-tuning actuator behavior, multi-actuator setups, and persistent deployment scenarios.


## Apply Advanced Configuration

The code shows several features of the PULSAR HRI actuator:


### Resets the encoder to define a new zero position

```py
actuator.reset_encoder_position()
```


### Changes the actuator's address

```py
actuator.changeAddress(0x15)
```


### Applies performance profiles for torque and speed

The available performance profiles are defined in the `PulsarActuator.TorquePerformance` and `PulsarActuator.SpeedPerformance`

```py
actuator.set_torque_performance(PulsarActuator.TorquePerformance.AGGRESSIVE)
actuator.set_speed_performance(PulsarActuator.SpeedPerformance.AGGRESSIVE)
```


### Sets custom control parameters

The available parameters are defined in the `PulsarActuator.PCP_Parameters`

```py
actuator.set_parameters({
    PulsarActuator.PCP_Parameters.K_DAMPING: 7.7,
    PulsarActuator.PCP_Parameters.K_STIFFNESS: 8.8,
})
```


### Saves the configuration to persistent memory

This will save the current configuration to the actuator's persistent memory, so it will be retained across power cycles.

```py
actuator.save_config()
```


### Reads back parameters

This will read back the current configuration from the actuator.

```py
params = actuator.get_parameters([
    PulsarActuator.PCP_Parameters.MODE,
    PulsarActuator.PCP_Parameters.SETPOINT,
    PulsarActuator.PCP_Parameters.K_STIFFNESS,
])
# params = actuator.get_parameters_all()
pprint(params)
```


## Full code

The Jupyter notebook can be downloaded [here](../assets/jnotebooks/changing-parameters.ipynb).

```py title="Full code" linenums="1"
from pcp_api import  PCP_over_USB, PulsarActuator
from pprint import pprint


ACTUATOR_ADDRESS = 0  # 0 to indicate direct USB connection

port = PCP_over_USB.get_port()
# port = "COM1"
print(f"Connecting to {port}")

adapter = PCP_over_USB(port)
actuator = PulsarActuator(adapter, ACTUATOR_ADDRESS)

if not actuator.connect():
    print(f"Could not connect to the actuator 0x{actuator.address:X} ({actuator.address})")
    adapter.close()
    exit(1)
print(f"Connected to {actuator.model} at address 0x{actuator.address:X} ({actuator.address})  firmware: v{actuator.firmware_version}")

# Define actual position as zero position
actuator.reset_encoder_position()

# Change the actuator's address
actuator.changeAddress(0x15)

# Set performance modes
actuator.set_torque_performance(PulsarActuator.TorquePerformance.AGGRESSIVE)
actuator.set_speed_performance(PulsarActuator.SpeedPerformance.AGGRESSIVE)

# Set control parameters
actuator.set_parameters({
    PulsarActuator.PCP_Parameters.K_DAMPING: 7.7,
    PulsarActuator.PCP_Parameters.K_STIFFNESS: 8.8,
})

# Optional: Save configuration to persistent memory
# actuator.save_config()

# Read back parameters 
params = actuator.get_parameters([
    PulsarActuator.PCP_Parameters.MODE,
    PulsarActuator.PCP_Parameters.SETPOINT,
    PulsarActuator.PCP_Parameters.K_STIFFNESS,
])
# params = actuator.get_parameters_all()
pprint(params)

adapter.close()
```
