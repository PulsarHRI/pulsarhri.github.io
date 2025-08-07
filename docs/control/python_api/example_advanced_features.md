# Advanced Features

These code snippets demonstrate more advanced configuration and control of a PULSAR HRI actuator. It builds upon the basic example so you can upgrade it by adding these features.

In this document you will learn how to:

* 🆔 Change the actuator's PCP address
* ⚙️ Tune performance profiles (torque and speed)
* 🎛️ Set custom control parameters (e.g., stiffness and damping)
* 💾 Optionally save configuration to persistent memory


## Changes the actuator's address

Sets a new address. This gets stored in the actuator's persistent memory, so it will be retained across power cycles. For actuators we recommend to use addresses from 0x10 (16) Lower addresses are reserved for adapters and special purposes.

```py
actuator.changeAddress(0x15)
```


## Change performance profiles for torque and speed

The available performance profiles are defined in the [`PulsarActuator.TorquePerformance`](class_PulsarActuator.md#pcp_api.pulsar_actuator.PulsarActuator.TorquePerformance) and [`PulsarActuator.SpeedPerformance`](class_PulsarActuator.md#pcp_api.pulsar_actuator.PulsarActuator.SpeedPerformance)

```py
actuator.set_torque_performance(PulsarActuator.TorquePerformance.AGGRESSIVE)
actuator.set_speed_performance(PulsarActuator.SpeedPerformance.BALANCED)
```


## Sets custom control parameters

The available parameters are defined in the [`PulsarActuator.PCP_Parameters`](class_PulsarActuator.md#pcp_api.pulsar_actuator.PulsarActuator.PCP_Parameters). Note that the `set_parameters` method takes a dictionary, where the keys are the parameter names and the values are the desired settings.

```py
actuator.set_parameters({
    PulsarActuator.PCP_Parameters.K_DAMPING: 7.7,
    PulsarActuator.PCP_Parameters.K_STIFFNESS: 8.8,
})
```


## Read back parameters

This will read back the current configuration from the actuator. In this case, the `get_parameters` method takes a list of parameters instead of a dictionary. You can also use `get_parameters_all()` to read all parameters at once.

```py
params = actuator.get_parameters([
    PulsarActuator.PCP_Parameters.MODE,
    PulsarActuator.PCP_Parameters.SETPOINT,
    PulsarActuator.PCP_Parameters.K_STIFFNESS,
])
# params = actuator.get_parameters_all()
print(params)
print(params[PulsarActuator.PCP_Parameters.K_STIFFNESS])
```


## Saves the configuration to persistent memory

This will save the current parameters to the actuator's persistent memory, so it will be retained across power cycles.

```py
actuator.save_config()
```
