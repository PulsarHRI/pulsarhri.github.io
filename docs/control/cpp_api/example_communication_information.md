# Checking Communication and Reading Device Information

This tutorial shows how to verify communication with a PULSAR HRI actuator before running motion-control examples. It covers how to connect through a known serial port, check whether the adapter is available, connect to the actuator, identify it with the LED blink function, and read the full parameter set.

## Requirements

Before running the example, make sure:

- the C++ API is built,
- the actuator is connected and reachable,
- the user has permission to access the communication device,
- the serial port is known and available.

## Include files

The following headers are required for this example:

```cpp
#include <pcp_api/pcp_api.hpp>
#include <iostream>
#include <string>

using namespace pcp_api;
```

## Connect to a known serial port

This example uses a fixed serial port instead of automatic port detection. Replace the port string with the device path used on your system.

```cpp
const std::string port = "/dev/ttyACM0";  // Replace with your device port
PCP_over_USB adapter(port);
```

The example below uses a Linux-style device path. On other systems, the port name may look different.

## Check that the adapter is connected

Use `is_connected()` to verify that the adapter is available before trying to communicate with the actuator.

```cpp
if (!adapter.is_connected()) {
    std::cerr << "Adapter not connected on port " << port << std::endl;
    adapter.close();
    throw std::runtime_error("Adapter connection failed");
}
```

## Connect to the actuator

Create the actuator instance and connect to it. When connecting directly through USB, use address `0`. If you are using CAN, replace it with the correct actuator PCP address.

```cpp
constexpr int ACTUATOR_ADDRESS = 0;

PulsarActuator actuator(adapter, ACTUATOR_ADDRESS);

if (!actuator.connect()) {
    std::cerr << "Actuator not responding at address "
              << ACTUATOR_ADDRESS << std::endl;
    adapter.close();
    throw std::runtime_error("Actuator connection failed");
}

std::cout << "Connected to actuator " << actuator.address()
          << " (model: " << actuator.model()
          << ", firmware: " << actuator.firmware_version()
          << ")"
          << std::endl;
```

## Identify the actuator with the LED blink function

Use `blink()` to flash the actuator LED and confirm that you are communicating with the expected device.

```cpp
actuator.blink();
```

## Read the full parameter set

Use `get_parameters_all()` to retrieve the full set of parameters from the actuator.

```cpp
auto params = actuator.get_parameters_all();
std::cout << "Read " << params.size() << " parameters" << std::endl;
```

This is useful for diagnostics, configuration inspection, and confirming that the actuator is responding correctly.

## Disconnect and clean up

Disconnect the actuator and close the adapter when the check is finished.

```cpp
actuator.disconnect();
adapter.close();
```

## Complete example

The following program is a complete example that can be copied into a `.cpp` file and compiled directly.

```cpp
#include <pcp_api/pcp_api.hpp>
#include <iostream>
#include <stdexcept>
#include <string>

using namespace pcp_api;

int main()
{
    PCP_over_USB* adapter_ptr = nullptr;

    try {
        constexpr int ACTUATOR_ADDRESS = 0;
        const std::string port = "/dev/ttyACM0";  // Replace with your device port

        PCP_over_USB adapter(port);
        adapter_ptr = &adapter;

        if (!adapter.is_connected()) {
            std::cerr << "Adapter not connected on port " << port << std::endl;
            adapter.close();
            return 1;
        }

        PulsarActuator actuator(adapter, ACTUATOR_ADDRESS);

        if (!actuator.connect()) {
            std::cerr << "Actuator not responding at address "
                      << ACTUATOR_ADDRESS << std::endl;
            adapter.close();
            return 1;
        }

        std::cout << "Connected to actuator " << actuator.address()
                  << " (model: " << actuator.model()
                  << ", firmware: " << actuator.firmware_version()
                  << ")"
                  << std::endl;

        actuator.blink();

        auto params = actuator.get_parameters_all();
        std::cout << "Read " << params.size() << " parameters" << std::endl;

        actuator.disconnect();
        adapter.close();
    }
    catch (const std::exception& e) {
        if (adapter_ptr != nullptr) {
            try {
                adapter_ptr->close();
            } catch (...) {
            }
        }

        std::cerr << "Fatal error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
```

## Example build command

Adjust the include path, library path, and library names to match your build output.

```bash
g++ -std=c++17 test_device_info.cpp -I../include -L. -lpcp_api -lpthread -lserialport -o test_device_info
```