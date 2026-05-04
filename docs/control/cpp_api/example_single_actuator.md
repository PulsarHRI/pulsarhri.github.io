# Controlling One Real Actuator

This tutorial shows how to connect to one PULSAR actuator, configure feedback, select a control mode, start the actuator, and stop it safely from a terminal application.

The example uses a direct USB connection. If you are using a CAN to USB adapter, replace the actuator address with the correct PCP address of your actuator.

!!! warning
    Make sure the actuator can move freely and safely before starting the example.

## Requirements
Before running the example, make sure:
- the C++ API is built,
- the actuator is connected,
- the user has permission to access the communication device,
- the correct port is available.

## Include files
The following headers are required for this example:

```cpp
#include <pcp_api/pcp_api.hpp>
#include <atomic>
#include <chrono>
#include <csignal>
#include <iostream>
#include <stdexcept>
#include <string>
#include <thread>
#include <unordered_map>

using namespace pcp_api;
```

---

## Connect to the adapter

PULSAR devices communicate through the PCP protocol over USB or CAN. In both cases, the host computer communicates through a USB connection, so the adapter is created with `PCP_over_USB`.

```cpp
std::string port = PCP_over_USB::get_port();
// std::string port = "COM1";  // You can specify a port if there are multiple devices

std::cout << "Connecting to " << port << std::endl;
PCP_over_USB adapter(port);
```

---

## Connect the actuator

When connecting directly through USB, use address `0`. When using CAN, replace it with the actuator PCP address.

```cpp
constexpr int ACTUATOR_ADDRESS = 0;

PulsarActuator actuator(adapter, ACTUATOR_ADDRESS);
if (!actuator.connect()) {
    std::cerr << "Failed to connect to actuator" << std::endl;
    adapter.close();
    throw std::runtime_error("Actuator connection failed");
}

std::cout << "Connected to the actuator "
          << actuator.address()
          << " (model: "
          << actuator.model()
          << ", firmware: "
          << actuator.firmware_version()
          << ")"
          << std::endl;
```

---

## Configure feedback

The feedback callback is invoked whenever new feedback data is received.

```cpp
void actuator_feedback(
    int address,
    const std::unordered_map<PulsarActuator::PCP_Items, float>& feedback)
{
    std::cout << "Feedback from actuator " << address << std::endl;
    for (const auto& [item, value] : feedback) {
        std::cout << "  item " << static_cast<int>(item)
                  << " -> " << value << std::endl;
    }
}
```

Configure the feedback items and feedback rate:

```cpp
actuator.setFeedbackItems({
    PulsarActuator::PCP_Items::SPEED_FB,
    PulsarActuator::PCP_Items::POSITION_FB,
    PulsarActuator::PCP_Items::TORQUE_FB,
});

actuator.setFeedbackRate(PulsarActuator::Rates::RATE_10HZ);
actuator.set_feedback_callback(actuator_feedback);
```

Additional feedback values can be requested when needed:

```cpp
auto other_feedback = actuator.getItemsBlocking({
    PulsarActuator::PCP_Items::VBUS,
    PulsarActuator::PCP_Items::TEMP_PCB,
    PulsarActuator::PCP_Items::TEMP_MOTOR,
});

for (const auto& [item, value] : other_feedback) {
    std::cout << "item " << static_cast<int>(item)
              << " -> " << value << std::endl;
}
```

---

## Select the control mode

Choose one control mode depending on the behavior you want to test.

### Speed mode

```cpp
actuator.change_mode(PulsarActuator::Mode::SPEED);
actuator.change_setpoint(1.0f);  // rad/s
```

### Torque mode

```cpp
actuator.change_mode(PulsarActuator::Mode::TORQUE);
actuator.change_setpoint(2.0f);  // Nm
```

### Position mode

```cpp
actuator.change_mode(PulsarActuator::Mode::POSITION);
actuator.set_home_position();
actuator.change_setpoint(3.1416f); // rad
```

---

## Run the actuator

Start the actuator with the `start()` method. The actuator will begin following the setpoint you defined and feedback will be received at the configured rates.

```cpp
std::atomic<bool> keep_running{true};

extern "C" void stop_actuator_handler(int)
{
    keep_running = false;
}

std::signal(SIGINT, stop_actuator_handler);

try {
    actuator.start();
    std::cout << "Actuator started. Press Ctrl+C to stop." << std::endl;

    while (keep_running) {
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}
catch (const std::exception& e) {
    std::cerr << "Error: " << e.what() << std::endl;
    throw;
}

actuator.disconnect();
std::this_thread::sleep_for(std::chrono::milliseconds(100));
adapter.close();
```

## Complete example
The following program is a complete example that can be copied into a `.cpp` file and compiled directly.

```cpp
#include <pcp_api/pcp_api.hpp>
#include <atomic>
#include <chrono>
#include <csignal>
#include <iostream>
#include <stdexcept>
#include <string>
#include <thread>
#include <unordered_map>

using namespace pcp_api;

std::atomic<bool> keep_running{true};

void actuator_feedback(
    int address,
    const std::unordered_map<PulsarActuator::PCP_Items, float>& feedback)
{
    std::cout << "Feedback from actuator " << address << std::endl;
    for (const auto& [item, value] : feedback) {
        std::cout << "  item " << static_cast<int>(item)
                  << " -> " << value << std::endl;
    }
    std::cout << "\nPress Ctrl+C to stop the test\n" << std::endl;
}

extern "C" void stop_actuator_handler(int)
{
    keep_running = false;
}

int main()
{
    PCP_over_USB* adapter_ptr = nullptr;
    PulsarActuator* actuator_ptr = nullptr;

    try {
        std::string port = PCP_over_USB::get_port();
        // std::string port = "COM1";

        std::cout << "Connecting to " << port << std::endl;
        PCP_over_USB adapter(port);
        adapter_ptr = &adapter;

        constexpr int ACTUATOR_ADDRESS = 0;

        PulsarActuator actuator(adapter, ACTUATOR_ADDRESS);
        actuator_ptr = &actuator;

        if (!actuator.connect()) {
            std::cerr << "Failed to connect to actuator" << std::endl;
            adapter.close();
            return 1;
        }

        std::cout << "Connected to the actuator "
                  << actuator.address()
                  << " (model: "
                  << actuator.model()
                  << ", firmware: "
                  << actuator.firmware_version()
                  << ")"
                  << std::endl;

        actuator.setFeedbackItems({
            PulsarActuator::PCP_Items::SPEED_FB,
            PulsarActuator::PCP_Items::POSITION_FB,
            PulsarActuator::PCP_Items::TORQUE_FB,
        });

        actuator.setFeedbackRate(PulsarActuator::Rates::RATE_10HZ);
        actuator.set_feedback_callback(actuator_feedback);

        auto other_feedback = actuator.getItemsBlocking({
            PulsarActuator::PCP_Items::VBUS,
            PulsarActuator::PCP_Items::TEMP_PCB,
            PulsarActuator::PCP_Items::TEMP_MOTOR,
        });

        for (const auto& [item, value] : other_feedback) {
            std::cout << "item " << static_cast<int>(item)
                      << " -> " << value << std::endl;
        }

        actuator.change_mode(PulsarActuator::Mode::SPEED);
        actuator.change_setpoint(1.0f);  // rad/s

        std::signal(SIGINT, stop_actuator_handler);

        actuator.start();
        std::cout << "Actuator started. Press Ctrl+C to stop." << std::endl;

        while (keep_running) {
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }

        actuator.disconnect();
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        adapter.close();
    }
    catch (const std::exception& e) {
        if (actuator_ptr != nullptr) {
            try {
                actuator_ptr->disconnect();
            } catch (...) {
            }
        }

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
g++ -std=c++17 <filename>.cpp -I../include -L. -lpcp_api -lpthread -lserialport -o <filename>
```