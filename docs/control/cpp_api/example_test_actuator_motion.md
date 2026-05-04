# Validating Actuator Motion with Small Position Tests

This tutorial shows how to run a small-motion validation test on connected PULSAR HRI actuators. It is intended as a commissioning and diagnostic example rather than a normal control application.

The example connects to two actuators through the same adapter, reads their initial feedback, applies small relative position moves, checks the feedback after each step, and returns each actuator to its initial position.

This tutorial is especially useful when you want to verify that communication, position control, and basic motion behavior are all working as expected.

!!! warning
    Make sure the actuators can move freely and safely before starting the example.

## Requirements

Before running the example, make sure:

- the C++ API is built,
- the adapter is connected and reachable,
- the actuators are powered and reachable,
- the user has permission to access the communication device,
- the selected motion range is safe for your setup.

## Include files

The following headers are required for this example:

```cpp
#include <pcp_api/pcp_api.hpp>
#include <chrono>
#include <iostream>
#include <string>
#include <thread>
#include <unordered_map>
#include <vector>

using namespace pcp_api;
```

## Overview

This example performs the following steps:

1. Connects to one adapter.
2. Attempts to connect to two actuators.
3. Reads the initial feedback from each connected actuator.
4. Configures temporary motion profile and position limits.
5. Moves the actuator by a small positive offset.
6. Moves the actuator by a small negative offset.
7. Returns the actuator to its starting position.
8. Repeats the same validation sequence for the other connected actuator.
9. Disconnects all connected actuators and closes the adapter.

## Helper function for short delays

This helper keeps the code easier to read when waiting between commands.

```cpp
static void wait_ms(int ms)
{
    std::this_thread::sleep_for(std::chrono::milliseconds(ms));
}
```

## Helper function to print feedback

This helper prints the values returned by `getItemsBlocking()`.

```cpp
static void print_basic_feedback(
    const std::string& name,
    const std::unordered_map<PulsarActuator::PCP_Items, float>& feedback)
{
    std::cout << name << " feedback:\n";
    for (const auto& [item, value] : feedback) {
        std::cout << "  item " << static_cast<int>(item)
                  << " = " << value << "\n";
    }
}
```

## Define the small-motion validation test

This function performs a complete validation sequence on one actuator:

- read initial feedback,
- compute relative targets from the current position,
- configure temporary motion parameters,
- move to a positive target,
- move to a negative target,
- return to the starting position,
- stop the actuator cleanly.

```cpp
static bool move_small_position_test(PulsarActuator& actuator, const std::string& name)
{
    try {
        std::cout << "\n=== " << name << " small motion test ===\n";

        std::vector<PulsarActuator::PCP_Items> items = {
            PulsarActuator::PCP_Items::POSITION_FB,
            PulsarActuator::PCP_Items::SPEED_FB,
            PulsarActuator::PCP_Items::TORQUE_FB
        };

        auto feedback_initial = actuator.getItemsBlocking(items, 1.0f);
        print_basic_feedback(name + " initial", feedback_initial);

        float initial_position = 0.0f;
        auto it = feedback_initial.find(PulsarActuator::PCP_Items::POSITION_FB);
        if (it != feedback_initial.end()) {
            initial_position = it->second;
        } else {
            std::cerr << "Could not read initial position for " << name << "\n";
            return false;
        }

        const float delta = 1.0f;
        const float target_positive = initial_position + delta;
        const float target_negative = initial_position - delta;

        actuator.set_parameters({
            {PulsarActuator::PCP_Parameters::PROFILE_POSITION_MAX, 2.0f},
            {PulsarActuator::PCP_Parameters::PROFILE_POSITION_MIN, -2.0f},
            {PulsarActuator::PCP_Parameters::LIM_POSITION_MAX, target_positive + 1.0f},
            {PulsarActuator::PCP_Parameters::LIM_POSITION_MIN, target_negative - 1.0f}
        });

        wait_ms(100);

        std::cout << "Changing mode to POSITION...\n";
        actuator.change_mode(PulsarActuator::Mode::POSITION);
        wait_ms(100);

        std::cout << "Starting actuator...\n";
        actuator.start();
        wait_ms(200);

        std::cout << "Move to target_positive = " << target_positive << " rad\n";
        actuator.change_setpoint(target_positive);
        wait_ms(1500);

        auto feedback_after_positive = actuator.getItemsBlocking(items, 1.0f);
        print_basic_feedback(name + " after positive target", feedback_after_positive);

        std::cout << "Move to target_negative = " << target_negative << " rad\n";
        actuator.change_setpoint(target_negative);
        wait_ms(1500);

        auto feedback_after_negative = actuator.getItemsBlocking(items, 1.0f);
        print_basic_feedback(name + " after negative target", feedback_after_negative);

        std::cout << "Return to initial position = " << initial_position << " rad\n";
        actuator.change_setpoint(initial_position);
        wait_ms(1500);

        auto feedback_after_return = actuator.getItemsBlocking(items, 1.0f);
        print_basic_feedback(name + " after return", feedback_after_return);

        std::cout << "Stopping actuator...\n";
        actuator.stop();
        wait_ms(100);

        return true;
    }
    catch (const std::exception& e) {
        std::cerr << "Exception during movement test on " << name
                  << ": " << e.what() << "\n";
        try {
            actuator.stop();
        } catch (...) {
        }
        return false;
    }
    catch (...) {
        std::cerr << "Unknown exception during movement test on " << name << "\n";
        try {
            actuator.stop();
        } catch (...) {
        }
        return false;
    }
}
```

## Configure the adapter and actuator addresses

This example uses one direct USB actuator and one CAN actuator on the same adapter.

```cpp
const std::string port = "";   // "" = auto-detect
const int addr1 = 0;           // direct USB actuator
const int addr2 = 0x36;        // CAN actuator
```

Adjust these values to match your setup.

## Connect to the adapter

Create the adapter and verify that it is connected before proceeding.

```cpp
PCP_over_USB adapter(port, true);
if (!adapter.is_connected()) {
    std::cerr << "ERROR: could not connect to USB adapter\n";
    return 1;
}
```

## Connect to the actuators

Attempt to connect to both actuators. The example continues as long as at least one actuator is available.

```cpp
PulsarActuator actuator1(adapter, addr1);
PulsarActuator actuator2(adapter, addr2);

bool actuator1_connected = actuator1.connect();
bool actuator2_connected = actuator2.connect();
```

You can print basic information for each actuator as soon as the connection succeeds.

```cpp
if (actuator1_connected) {
    std::cout << "Actuator 1 -> address: 0x" << std::hex << addr1 << std::dec
              << " | model: " << actuator1.model()
              << " | fw: " << actuator1.firmware_version() << "\n";
} else {
    std::cerr << "WARNING: actuator 1 not responding (address 0x"
              << std::hex << addr1 << std::dec << ")\n";
}

if (actuator2_connected) {
    std::cout << "Actuator 2 -> address: 0x" << std::hex << addr2 << std::dec
              << " | model: " << actuator2.model()
              << " | fw: " << actuator2.firmware_version() << "\n";
} else {
    std::cerr << "WARNING: actuator 2 not responding (address 0x"
              << std::hex << addr2 << std::dec << ")\n";
}
```

## Run the validation test on each connected actuator

This example tests each connected actuator sequentially, not simultaneously.

```cpp
bool ok1 = false;
bool ok2 = false;

if (actuator1_connected) {
    ok1 = move_small_position_test(actuator1, "Actuator 1");
    wait_ms(500);
}

if (actuator2_connected) {
    ok2 = move_small_position_test(actuator2, "Actuator 2");
    wait_ms(500);
}
```

## Disconnect and clean up

Disconnect any connected actuators and close the adapter.

```cpp
if (actuator1_connected) {
    try {
        actuator1.disconnect();
    } catch (...) {
    }
}

if (actuator2_connected) {
    try {
        actuator2.disconnect();
    } catch (...) {
    }
}

adapter.close();
```

## Complete example

The following program is a complete example that can be copied into a `.cpp` file and compiled directly.

```cpp
#include <pcp_api/pcp_api.hpp>
#include <chrono>
#include <iostream>
#include <string>
#include <thread>
#include <unordered_map>
#include <vector>

using namespace pcp_api;

static void wait_ms(int ms)
{
    std::this_thread::sleep_for(std::chrono::milliseconds(ms));
}

static void print_basic_feedback(
    const std::string& name,
    const std::unordered_map<PulsarActuator::PCP_Items, float>& feedback)
{
    std::cout << name << " feedback:\n";
    for (const auto& [item, value] : feedback) {
        std::cout << "  item " << static_cast<int>(item)
                  << " = " << value << "\n";
    }
}

static bool move_small_position_test(PulsarActuator& actuator, const std::string& name)
{
    try {
        std::cout << "\n=== " << name << " small motion test ===\n";

        std::vector<PulsarActuator::PCP_Items> items = {
            PulsarActuator::PCP_Items::POSITION_FB,
            PulsarActuator::PCP_Items::SPEED_FB,
            PulsarActuator::PCP_Items::TORQUE_FB
        };

        auto feedback_initial = actuator.getItemsBlocking(items, 1.0f);
        print_basic_feedback(name + " initial", feedback_initial);

        float initial_position = 0.0f;
        auto it = feedback_initial.find(PulsarActuator::PCP_Items::POSITION_FB);
        if (it != feedback_initial.end()) {
            initial_position = it->second;
        } else {
            std::cerr << "Could not read initial position for " << name << "\n";
            return false;
        }

        const float delta = 1.0f;
        const float target_positive = initial_position + delta;
        const float target_negative = initial_position - delta;

        actuator.set_parameters({
            {PulsarActuator::PCP_Parameters::PROFILE_POSITION_MAX, 2.0f},
            {PulsarActuator::PCP_Parameters::PROFILE_POSITION_MIN, -2.0f},
            {PulsarActuator::PCP_Parameters::LIM_POSITION_MAX, target_positive + 1.0f},
            {PulsarActuator::PCP_Parameters::LIM_POSITION_MIN, target_negative - 1.0f}
        });

        wait_ms(100);

        std::cout << "Changing mode to POSITION...\n";
        actuator.change_mode(PulsarActuator::Mode::POSITION);
        wait_ms(100);

        std::cout << "Starting actuator...\n";
        actuator.start();
        wait_ms(200);

        std::cout << "Move to target_positive = " << target_positive << " rad\n";
        actuator.change_setpoint(target_positive);
        wait_ms(1500);

        auto feedback_after_positive = actuator.getItemsBlocking(items, 1.0f);
        print_basic_feedback(name + " after positive target", feedback_after_positive);

        std::cout << "Move to target_negative = " << target_negative << " rad\n";
        actuator.change_setpoint(target_negative);
        wait_ms(1500);

        auto feedback_after_negative = actuator.getItemsBlocking(items, 1.0f);
        print_basic_feedback(name + " after negative target", feedback_after_negative);

        std::cout << "Return to initial position = " << initial_position << " rad\n";
        actuator.change_setpoint(initial_position);
        wait_ms(1500);

        auto feedback_after_return = actuator.getItemsBlocking(items, 1.0f);
        print_basic_feedback(name + " after return", feedback_after_return);

        std::cout << "Stopping actuator...\n";
        actuator.stop();
        wait_ms(100);

        return true;
    }
    catch (const std::exception& e) {
        std::cerr << "Exception during movement test on " << name
                  << ": " << e.what() << "\n";
        try {
            actuator.stop();
        } catch (...) {
        }
        return false;
    }
    catch (...) {
        std::cerr << "Unknown exception during movement test on " << name << "\n";
        try {
            actuator.stop();
        } catch (...) {
        }
        return false;
    }
}

int main()
{
    const std::string port = "";   // "" = auto-detect
    const int addr1 = 0;           // direct USB actuator
    const int addr2 = 0x36;        // CAN actuator

    bool actuator1_connected = false;
    bool actuator2_connected = false;
    bool ok1 = false;
    bool ok2 = false;

    try {
        PCP_over_USB adapter(port, true);
        if (!adapter.is_connected()) {
            std::cerr << "ERROR: could not connect to USB adapter\n";
            return 1;
        }

        PulsarActuator actuator1(adapter, addr1);
        PulsarActuator actuator2(adapter, addr2);

        actuator1_connected = actuator1.connect();
        if (actuator1_connected) {
            std::cout << "Actuator 1 -> address: 0x" << std::hex << addr1 << std::dec
                      << " | model: " << actuator1.model()
                      << " | fw: " << actuator1.firmware_version() << "\n";
        } else {
            std::cerr << "WARNING: actuator 1 not responding (address 0x"
                      << std::hex << addr1 << std::dec << ")\n";
        }

        actuator2_connected = actuator2.connect();
        if (actuator2_connected) {
            std::cout << "Actuator 2 -> address: 0x" << std::hex << addr2 << std::dec
                      << " | model: " << actuator2.model()
                      << " | fw: " << actuator2.firmware_version() << "\n";
        } else {
            std::cerr << "WARNING: actuator 2 not responding (address 0x"
                      << std::hex << addr2 << std::dec << ")\n";
        }

        if (!actuator1_connected && !actuator2_connected) {
            std::cerr << "ERROR: no actuator could be connected\n";
            adapter.close();
            return 1;
        }

        if (actuator1_connected) {
            ok1 = move_small_position_test(actuator1, "Actuator 1");
            wait_ms(500);
        }

        if (actuator2_connected) {
            ok2 = move_small_position_test(actuator2, "Actuator 2");
            wait_ms(500);
        }

        if (actuator1_connected) {
            try {
                actuator1.disconnect();
            } catch (...) {
            }
        }

        if (actuator2_connected) {
            try {
                actuator2.disconnect();
            } catch (...) {
            }
        }

        adapter.close();

        bool any_test_failed = false;
        if (actuator1_connected && !ok1) {
            any_test_failed = true;
        }
        if (actuator2_connected && !ok2) {
            any_test_failed = true;
        }

        if (!any_test_failed) {
            std::cout << "\nMotion test finished OK\n";
            return 0;
        }

        std::cerr << "\nMotion test finished with errors\n";
        return 2;
    }
    catch (const std::exception& e) {
        std::cerr << "EXCEPTION: " << e.what() << "\n";
        return 3;
    }
    catch (...) {
        std::cerr << "UNKNOWN EXCEPTION\n";
        return 4;
    }
}
```

## Example build command

Adjust the include path, library path, and library names to match your build output.

```bash
g++ -std=c++17 <filename>.cpp -I../include -L. -lpcp_api -lpthread -lserialport -o <filename>
```