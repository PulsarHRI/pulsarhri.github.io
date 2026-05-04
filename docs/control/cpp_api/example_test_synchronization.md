# Evaluating Synchronization Between Two Actuators

This tutorial shows how to evaluate the synchronization between two PULSAR HRI actuators by sending coordinated position commands and comparing their measured response times.

Unlike the basic multi-actuator control tutorial, this example is not about continuous operation. It is a measurement-oriented test that estimates how closely two actuators respond to the same motion command.

The example connects to two actuators, reads their initial positions, applies the same relative position step to both, captures feedback samples during the motion, and estimates synchronization error from the time each actuator reaches 50% of the commanded move.

!!! warning
    Make sure both actuators can move freely and safely before starting the example.

## Requirements

Before running the example, make sure:

- the C++ API is built,
- the adapter is connected and reachable,
- both actuators are powered and reachable,
- the user has permission to access the communication device,
- the commanded position step is safe for your setup.

## Include files

The following headers are required for this example:

```cpp
#include <pcp_api/pcp_api.hpp>
#include <chrono>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <limits>
#include <optional>
#include <string>
#include <thread>
#include <unordered_map>
#include <vector>

using namespace pcp_api;
using Clock = std::chrono::steady_clock;
```

## Overview

This example performs the following steps:

1. Connects to one adapter and two actuators.
2. Reads the initial position of each actuator.
3. Computes a relative target for each actuator.
4. Configures position mode, feedback rate, and temporary motion limits.
5. Arms both actuators and sends the target commands with minimal delay.
6. Captures feedback samples during the motion.
7. Sends return commands to the initial positions.
8. Computes the 50% crossing time for each actuator.
9. Estimates synchronization error from the difference between the two crossing times.

## Define a sample structure

Each captured sample stores the measurement time and selected feedback values for both actuators.

```cpp
struct Sample {
    double t_s;
    float pos1 = std::numeric_limits<float>::quiet_NaN();
    float pos2 = std::numeric_limits<float>::quiet_NaN();
    float spd1 = std::numeric_limits<float>::quiet_NaN();
    float spd2 = std::numeric_limits<float>::quiet_NaN();
};
```

## Helper function to wait until a time point

This helper is used to arm the test and fire both commands at a known time.

```cpp
static void sleep_until(Clock::time_point tp)
{
    while (Clock::now() < tp) {
        std::this_thread::sleep_for(std::chrono::milliseconds(1));
    }
}
```

## Helper function to read feedback items safely

This helper extracts a feedback value from a map and returns a fallback value if the item is missing.

```cpp
static float get_item(
    const std::unordered_map<PulsarActuator::PCP_Items, float>& feedback,
    PulsarActuator::PCP_Items item,
    float fallback = std::numeric_limits<float>::quiet_NaN())
{
    auto it = feedback.find(item);
    if (it == feedback.end()) {
        return fallback;
    }
    return it->second;
}
```

## Estimate the 50% crossing time

This helper scans the captured samples and returns the first time at which the actuator position crosses 50% of the commanded step.

```cpp
static std::optional<double> crossing_time_50pct(
    const std::vector<Sample>& samples,
    bool for_first_actuator,
    float start_pos,
    float target_pos)
{
    const float threshold = start_pos + 0.5f * (target_pos - start_pos);

    for (const auto& s : samples) {
        const float pos = for_first_actuator ? s.pos1 : s.pos2;
        if (std::isnan(pos)) {
            continue;
        }

        if (target_pos >= start_pos) {
            if (pos >= threshold) {
                return s.t_s;
            }
        } else {
            if (pos <= threshold) {
                return s.t_s;
            }
        }
    }

    return std::nullopt;
}
```

## Configure the adapter and actuator addresses

This example uses one direct USB actuator and one CAN actuator on the same adapter.

```cpp
const std::string port = "";   // "" = auto-detect, or set an explicit port such as "/dev/ttyACM0"
const int addr1 = 0;           // direct USB actuator
const int addr2 = 0x36;        // CAN actuator
```

## Configure the test parameters

These values define the step size and the timing of the measurement.

```cpp
const float delta = 1.5f;

const auto pre_arm_delay = std::chrono::seconds(2);
const auto capture_time = std::chrono::seconds(3);
const auto poll_period = std::chrono::milliseconds(20);
```

## Connect to the adapter and actuators

Create the adapter, verify the connection, and then attempt to connect to both actuators.

```cpp
PCP_over_USB adapter(port, true);
if (!adapter.is_connected()) {
    std::cerr << "ERROR: could not connect to adapter\n";
    return 1;
}

PulsarActuator actuator1(adapter, addr1);
PulsarActuator actuator2(adapter, addr2);

bool actuator1_connected = actuator1.connect();
bool actuator2_connected = actuator2.connect();
```

Print basic information as soon as each connection succeeds.

```cpp
if (actuator1_connected) {
    std::cout << "A1 connected -> addr=0x" << std::hex << addr1 << std::dec
              << " model=" << actuator1.model()
              << " fw=" << actuator1.firmware_version() << "\n";
} else {
    std::cerr << "WARNING: actuator 1 not responding (addr=0x"
              << std::hex << addr1 << std::dec << ")\n";
}

if (actuator2_connected) {
    std::cout << "A2 connected -> addr=0x" << std::hex << addr2 << std::dec
              << " model=" << actuator2.model()
              << " fw=" << actuator2.firmware_version() << "\n";
} else {
    std::cerr << "WARNING: actuator 2 not responding (addr=0x"
              << std::hex << addr2 << std::dec << ")\n";
}
```

## Read the initial positions

Read the initial feedback of each actuator and compute the target position as a relative step from the starting position.

```cpp
std::vector<PulsarActuator::PCP_Items> items = {
    PulsarActuator::PCP_Items::POSITION_FB,
    PulsarActuator::PCP_Items::SPEED_FB,
    PulsarActuator::PCP_Items::TORQUE_FB
};

float pos1_0 = std::numeric_limits<float>::quiet_NaN();
float pos2_0 = std::numeric_limits<float>::quiet_NaN();
float target1 = std::numeric_limits<float>::quiet_NaN();
float target2 = std::numeric_limits<float>::quiet_NaN();

if (actuator1_connected) {
    auto feedback1_0 = actuator1.getItemsBlocking(items, 1.0f);
    pos1_0 = get_item(feedback1_0, PulsarActuator::PCP_Items::POSITION_FB);
    if (std::isnan(pos1_0)) {
        std::cerr << "WARNING: could not read initial position for A1, skipping A1 test\n";
        actuator1.disconnect();
        actuator1_connected = false;
    } else {
        target1 = pos1_0 + delta;
    }
}

if (actuator2_connected) {
    auto feedback2_0 = actuator2.getItemsBlocking(items, 1.0f);
    pos2_0 = get_item(feedback2_0, PulsarActuator::PCP_Items::POSITION_FB);
    if (std::isnan(pos2_0)) {
        std::cerr << "WARNING: could not read initial position for A2, skipping A2 test\n";
        actuator2.disconnect();
        actuator2_connected = false;
    } else {
        target2 = pos2_0 + delta;
    }
}
```

## Configure position mode and temporary motion limits

Switch the connected actuators to `POSITION` mode, configure the feedback rate, and apply temporary position limits and profile settings for the test.

```cpp
if (actuator1_connected) {
    actuator1.change_mode(PulsarActuator::Mode::POSITION);
}
if (actuator2_connected) {
    actuator2.change_mode(PulsarActuator::Mode::POSITION);
}
std::this_thread::sleep_for(std::chrono::milliseconds(100));

if (actuator1_connected) {
    actuator1.setFeedbackItems(items);
    actuator1.setFeedbackRate(PulsarActuator::Rates::RATE_50HZ);
    actuator1.set_parameters({
        {PulsarActuator::PCP_Parameters::LIM_POSITION_MIN, pos1_0 - 0.5f},
        {PulsarActuator::PCP_Parameters::LIM_POSITION_MAX, pos1_0 + 0.5f},
        {PulsarActuator::PCP_Parameters::PROFILE_POSITION_MAX, 0.8f},
        {PulsarActuator::PCP_Parameters::PROFILE_POSITION_MIN, -0.8f}
    });
}

if (actuator2_connected) {
    actuator2.setFeedbackItems(items);
    actuator2.setFeedbackRate(PulsarActuator::Rates::RATE_50HZ);
    actuator2.set_parameters({
        {PulsarActuator::PCP_Parameters::LIM_POSITION_MIN, pos2_0 - 0.5f},
        {PulsarActuator::PCP_Parameters::LIM_POSITION_MAX, pos2_0 + 0.5f},
        {PulsarActuator::PCP_Parameters::PROFILE_POSITION_MAX, 0.8f},
        {PulsarActuator::PCP_Parameters::PROFILE_POSITION_MIN, -0.8f}
    });
}
```

## Arm the test and send the position commands

Start the actuators, wait until the armed fire time, and then send the target commands with minimal delay.

```cpp
if (actuator1_connected) {
    actuator1.start();
}
if (actuator2_connected) {
    actuator2.start();
}
std::this_thread::sleep_for(std::chrono::milliseconds(200));

const auto t0 = Clock::now();
const auto fire_time = t0 + pre_arm_delay;

std::cout << "Armed. Sending available setpoints in ~2 seconds...\n";
sleep_until(fire_time);

std::optional<Clock::time_point> send1;
std::optional<Clock::time_point> send2;

if (actuator1_connected) {
    send1 = Clock::now();
    actuator1.change_setpoint(target1);
}

if (actuator2_connected) {
    send2 = Clock::now();
    actuator2.change_setpoint(target2);
}
```

If both actuators are active, the difference between `send2` and `send1` provides a rough estimate of the command issue gap.

## Capture feedback samples

Capture position and speed samples for both actuators during the motion window.

```cpp
std::vector<Sample> samples;
const auto capture_start = Clock::now();

while (Clock::now() - capture_start < capture_time) {
    std::unordered_map<PulsarActuator::PCP_Items, float> feedback1;
    std::unordered_map<PulsarActuator::PCP_Items, float> feedback2;

    if (actuator1_connected) {
        feedback1 = actuator1.getItemsBlocking(items, 0.2f);
    }
    if (actuator2_connected) {
        feedback2 = actuator2.getItemsBlocking(items, 0.2f);
    }

    Sample sample{};
    sample.t_s = std::chrono::duration<double>(Clock::now() - fire_time).count();

    if (actuator1_connected) {
        sample.pos1 = get_item(feedback1, PulsarActuator::PCP_Items::POSITION_FB);
        sample.spd1 = get_item(feedback1, PulsarActuator::PCP_Items::SPEED_FB);
    }
    if (actuator2_connected) {
        sample.pos2 = get_item(feedback2, PulsarActuator::PCP_Items::POSITION_FB);
        sample.spd2 = get_item(feedback2, PulsarActuator::PCP_Items::SPEED_FB);
    }

    samples.push_back(sample);
    std::this_thread::sleep_for(poll_period);
}
```

## Return the actuators to the starting positions

After the capture window, send the return commands and wait for the motion to finish.

```cpp
if (actuator1_connected) {
    actuator1.change_setpoint(pos1_0);
}
if (actuator2_connected) {
    actuator2.change_setpoint(pos2_0);
}

std::this_thread::sleep_for(std::chrono::seconds(2));

if (actuator1_connected) {
    actuator1.stop();
}
if (actuator2_connected) {
    actuator2.stop();
}
```

## Estimate synchronization error

Compute the 50% crossing time for each actuator and estimate synchronization error from their difference.

```cpp
std::optional<double> t50_1;
std::optional<double> t50_2;

if (actuator1_connected) {
    t50_1 = crossing_time_50pct(samples, true, pos1_0, target1);
}
if (actuator2_connected) {
    t50_2 = crossing_time_50pct(samples, false, pos2_0, target2);
}

if (actuator1_connected && actuator2_connected && t50_1.has_value() && t50_2.has_value()) {
    const double sync_error_ms = std::abs(*t50_1 - *t50_2) * 1000.0;
    std::cout << "Estimated sync error (50% crossing): "
              << sync_error_ms << " ms\n";
}
```

## Complete example

The following program is a complete example that can be copied into a `.cpp` file and compiled directly.

```cpp
#include <pcp_api/pcp_api.hpp>
#include <chrono>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <limits>
#include <optional>
#include <string>
#include <thread>
#include <unordered_map>
#include <vector>

using namespace pcp_api;
using Clock = std::chrono::steady_clock;

struct Sample {
    double t_s;
    float pos1 = std::numeric_limits<float>::quiet_NaN();
    float pos2 = std::numeric_limits<float>::quiet_NaN();
    float spd1 = std::numeric_limits<float>::quiet_NaN();
    float spd2 = std::numeric_limits<float>::quiet_NaN();
};

static void sleep_until(Clock::time_point tp)
{
    while (Clock::now() < tp) {
        std::this_thread::sleep_for(std::chrono::milliseconds(1));
    }
}

static float get_item(
    const std::unordered_map<PulsarActuator::PCP_Items, float>& feedback,
    PulsarActuator::PCP_Items item,
    float fallback = std::numeric_limits<float>::quiet_NaN())
{
    auto it = feedback.find(item);
    if (it == feedback.end()) {
        return fallback;
    }
    return it->second;
}

static std::optional<double> crossing_time_50pct(
    const std::vector<Sample>& samples,
    bool for_first_actuator,
    float start_pos,
    float target_pos)
{
    const float threshold = start_pos + 0.5f * (target_pos - start_pos);

    for (const auto& s : samples) {
        const float pos = for_first_actuator ? s.pos1 : s.pos2;
        if (std::isnan(pos)) {
            continue;
        }

        if (target_pos >= start_pos) {
            if (pos >= threshold) {
                return s.t_s;
            }
        } else {
            if (pos <= threshold) {
                return s.t_s;
            }
        }
    }

    return std::nullopt;
}

int main()
{
    const std::string port = "";   // "" = auto-detect, or set an explicit port such as "/dev/ttyACM0"
    const int addr1 = 0;           // direct USB actuator
    const int addr2 = 0x36;        // CAN actuator

    const float delta = 1.5f;

    const auto pre_arm_delay = std::chrono::seconds(2);
    const auto capture_time = std::chrono::seconds(3);
    const auto poll_period = std::chrono::milliseconds(20);

    bool actuator1_connected = false;
    bool actuator2_connected = false;

    try {
        PCP_over_USB adapter(port, true);
        if (!adapter.is_connected()) {
            std::cerr << "ERROR: could not connect to adapter\n";
            return 1;
        }

        PulsarActuator actuator1(adapter, addr1);
        PulsarActuator actuator2(adapter, addr2);

        actuator1_connected = actuator1.connect();
        if (actuator1_connected) {
            std::cout << "A1 connected -> addr=0x" << std::hex << addr1 << std::dec
                      << " model=" << actuator1.model()
                      << " fw=" << actuator1.firmware_version() << "\n";
        } else {
            std::cerr << "WARNING: actuator 1 not responding (addr=0x"
                      << std::hex << addr1 << std::dec << ")\n";
        }

        actuator2_connected = actuator2.connect();
        if (actuator2_connected) {
            std::cout << "A2 connected -> addr=0x" << std::hex << addr2 << std::dec
                      << " model=" << actuator2.model()
                      << " fw=" << actuator2.firmware_version() << "\n";
        } else {
            std::cerr << "WARNING: actuator 2 not responding (addr=0x"
                      << std::hex << addr2 << std::dec << ")\n";
        }

        if (!actuator1_connected && !actuator2_connected) {
            std::cerr << "ERROR: no actuator could be connected\n";
            adapter.close();
            return 1;
        }

        std::vector<PulsarActuator::PCP_Items> items = {
            PulsarActuator::PCP_Items::POSITION_FB,
            PulsarActuator::PCP_Items::SPEED_FB,
            PulsarActuator::PCP_Items::TORQUE_FB
        };

        float pos1_0 = std::numeric_limits<float>::quiet_NaN();
        float pos2_0 = std::numeric_limits<float>::quiet_NaN();
        float target1 = std::numeric_limits<float>::quiet_NaN();
        float target2 = std::numeric_limits<float>::quiet_NaN();

        if (actuator1_connected) {
            auto feedback1_0 = actuator1.getItemsBlocking(items, 1.0f);
            pos1_0 = get_item(feedback1_0, PulsarActuator::PCP_Items::POSITION_FB);
            if (std::isnan(pos1_0)) {
                std::cerr << "WARNING: could not read initial position for A1, skipping A1 test\n";
                actuator1.disconnect();
                actuator1_connected = false;
            } else {
                target1 = pos1_0 + delta;
            }
        }

        if (actuator2_connected) {
            auto feedback2_0 = actuator2.getItemsBlocking(items, 1.0f);
            pos2_0 = get_item(feedback2_0, PulsarActuator::PCP_Items::POSITION_FB);
            if (std::isnan(pos2_0)) {
                std::cerr << "WARNING: could not read initial position for A2, skipping A2 test\n";
                actuator2.disconnect();
                actuator2_connected = false;
            } else {
                target2 = pos2_0 + delta;
            }
        }

        if (!actuator1_connected && !actuator2_connected) {
            std::cerr << "ERROR: no actuator available after initial feedback check\n";
            adapter.close();
            return 2;
        }

        std::cout << std::fixed << std::setprecision(6);
        if (actuator1_connected) {
            std::cout << "Initial pos A1: " << pos1_0 << " rad\n";
            std::cout << "Target  pos A1: " << target1 << " rad\n";
        }
        if (actuator2_connected) {
            std::cout << "Initial pos A2: " << pos2_0 << " rad\n";
            std::cout << "Target  pos A2: " << target2 << " rad\n";
        }

        if (actuator1_connected) {
            actuator1.change_mode(PulsarActuator::Mode::POSITION);
        }
        if (actuator2_connected) {
            actuator2.change_mode(PulsarActuator::Mode::POSITION);
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(100));

        if (actuator1_connected) {
            actuator1.setFeedbackItems(items);
            actuator1.setFeedbackRate(PulsarActuator::Rates::RATE_50HZ);
            actuator1.set_parameters({
                {PulsarActuator::PCP_Parameters::LIM_POSITION_MIN, pos1_0 - 0.5f},
                {PulsarActuator::PCP_Parameters::LIM_POSITION_MAX, pos1_0 + 0.5f},
                {PulsarActuator::PCP_Parameters::PROFILE_POSITION_MAX, 0.8f},
                {PulsarActuator::PCP_Parameters::PROFILE_POSITION_MIN, -0.8f}
            });
        }

        if (actuator2_connected) {
            actuator2.setFeedbackItems(items);
            actuator2.setFeedbackRate(PulsarActuator::Rates::RATE_50HZ);
            actuator2.set_parameters({
                {PulsarActuator::PCP_Parameters::LIM_POSITION_MIN, pos2_0 - 0.5f},
                {PulsarActuator::PCP_Parameters::LIM_POSITION_MAX, pos2_0 + 0.5f},
                {PulsarActuator::PCP_Parameters::PROFILE_POSITION_MAX, 0.8f},
                {PulsarActuator::PCP_Parameters::PROFILE_POSITION_MIN, -0.8f}
            });
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(200));

        if (actuator1_connected) {
            actuator1.start();
        }
        if (actuator2_connected) {
            actuator2.start();
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(200));

        const auto t0 = Clock::now();
        const auto fire_time = t0 + pre_arm_delay;

        std::cout << "Armed. Sending available setpoints in ~2 seconds...\n";
        sleep_until(fire_time);

        std::optional<Clock::time_point> send1;
        std::optional<Clock::time_point> send2;

        if (actuator1_connected) {
            send1 = Clock::now();
            actuator1.change_setpoint(target1);
        }

        if (actuator2_connected) {
            send2 = Clock::now();
            actuator2.change_setpoint(target2);
        }

        if (send1.has_value() && send2.has_value()) {
            const double command_gap_ms =
                std::chrono::duration<double, std::milli>(*send2 - *send1).count();
            std::cout << "Command gap between A1 and A2 sends: "
                      << command_gap_ms << " ms\n";
        } else {
            std::cout << "Only one actuator active: no inter-actuator command gap available\n";
        }

        std::vector<Sample> samples;
        const auto capture_start = Clock::now();
        while (Clock::now() - capture_start < capture_time) {
            std::unordered_map<PulsarActuator::PCP_Items, float> feedback1;
            std::unordered_map<PulsarActuator::PCP_Items, float> feedback2;

            if (actuator1_connected) {
                feedback1 = actuator1.getItemsBlocking(items, 0.2f);
            }
            if (actuator2_connected) {
                feedback2 = actuator2.getItemsBlocking(items, 0.2f);
            }

            Sample sample{};
            sample.t_s = std::chrono::duration<double>(Clock::now() - fire_time).count();

            if (actuator1_connected) {
                sample.pos1 = get_item(feedback1, PulsarActuator::PCP_Items::POSITION_FB);
                sample.spd1 = get_item(feedback1, PulsarActuator::PCP_Items::SPEED_FB);
            }
            if (actuator2_connected) {
                sample.pos2 = get_item(feedback2, PulsarActuator::PCP_Items::POSITION_FB);
                sample.spd2 = get_item(feedback2, PulsarActuator::PCP_Items::SPEED_FB);
            }

            samples.push_back(sample);
            std::this_thread::sleep_for(poll_period);
        }

        std::optional<Clock::time_point> back1;
        std::optional<Clock::time_point> back2;

        if (actuator1_connected) {
            back1 = Clock::now();
            actuator1.change_setpoint(pos1_0);
        }
        if (actuator2_connected) {
            back2 = Clock::now();
            actuator2.change_setpoint(pos2_0);
        }

        if (back1.has_value() && back2.has_value()) {
            const double return_gap_ms =
                std::chrono::duration<double, std::milli>(*back2 - *back1).count();
            std::cout << "Return command gap between A1 and A2 sends: "
                      << return_gap_ms << " ms\n";
        } else {
            std::cout << "Only one actuator active: no inter-actuator return gap available\n";
        }

        std::this_thread::sleep_for(std::chrono::seconds(2));

        if (actuator1_connected) {
            actuator1.stop();
        }
        if (actuator2_connected) {
            actuator2.stop();
        }

        std::optional<double> t50_1;
        std::optional<double> t50_2;

        if (actuator1_connected) {
            t50_1 = crossing_time_50pct(samples, true, pos1_0, target1);
        }
        if (actuator2_connected) {
            t50_2 = crossing_time_50pct(samples, false, pos2_0, target2);
        }

        std::cout << "\n=== Summary ===\n";

        if (actuator1_connected) {
            if (t50_1.has_value()) {
                std::cout << "A1 50% crossing time: " << *t50_1 << " s\n";
            } else {
                std::cout << "A1 50% crossing time: not reached\n";
            }
        } else {
            std::cout << "A1: not connected / not tested\n";
        }

        if (actuator2_connected) {
            if (t50_2.has_value()) {
                std::cout << "A2 50% crossing time: " << *t50_2 << " s\n";
            } else {
                std::cout << "A2 50% crossing time: not reached\n";
            }
        } else {
            std::cout << "A2: not connected / not tested\n";
        }

        if (actuator1_connected && actuator2_connected && t50_1.has_value() && t50_2.has_value()) {
            const double sync_error_ms = std::abs(*t50_1 - *t50_2) * 1000.0;
            std::cout << "Estimated sync error (50% crossing): "
                      << sync_error_ms << " ms\n";
        } else {
            std::cout << "Estimated sync error: not available\n";
        }

        std::cout << "\nCaptured samples: " << samples.size() << "\n";
        std::cout << "First 10 samples:\n";
        for (size_t i = 0; i < samples.size() && i < 10; ++i) {
            const auto& s = samples[i];
            std::cout << "t=" << s.t_s
                      << " | p1=" << s.pos1
                      << " p2=" << s.pos2
                      << " | v1=" << s.spd1
                      << " v2=" << s.spd2 << "\n";
        }

        if (actuator1_connected) {
            actuator1.disconnect();
        }
        if (actuator2_connected) {
            actuator2.disconnect();
        }
        adapter.close();
        return 0;
    }
    catch (const std::exception& e) {
        std::cerr << "EXCEPTION: " << e.what() << "\n";
        return 10;
    }
    catch (...) {
        std::cerr << "UNKNOWN EXCEPTION\n";
        return 11;
    }
}
```

## Example build command

Adjust the include path, library path, and library names to match your build output.

```bash
g++ -std=c++17 <filename>.cpp -I../include -L. -lpcp_api -lpthread -lserialport -o <filename>
```