# Communicate with Virtual Actuators

Virtual actuators communicate through the Python API directly, not through USB, CAN, serial ports, or a CAN adapter.

The main virtual actuator class is [`PulsarActuatorVirtual`](../control/python_api/class_PulsarActuatorVirtual.md). It mirrors the real actuator control-mode API where practical, while adding virtual-only methods for DTwin model selection and simulation stepping. The first public DTwin beta asset release is available for Linux x86_64 and Windows x86_64.

Typical virtual-actuator communication flow:

1. Configure a virtual actuator from installed DTwin assets.
2. Connect to the configured virtual actuator object.
3. Change control mode and setpoints through the Python API.
4. Advance the simulation with virtual stepping methods.
5. Read feedback from the simulated actuator state.

For a first runnable workflow, start with the [Python API for Virtual Actuator with DTwin](../quickstarts/quickstart_virtual_python_api.md) quickstart and the [Python API Examples](../control/python_api/examples.md) repository.
