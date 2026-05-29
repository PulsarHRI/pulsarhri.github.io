# PCP ROS 2 Bridge Tutorials

This [PCP ROS 2 package](https://github.com/cconejob-arc/pcp_ros2_bridge) includes tutorial documentation and Python/C++ examples:

| Tutorial | Goal |
|---|---|
| **Tutorial 1** | Discover the namespaced API |
| **Tutorial 2** | Read live actuator state |
| **Tutorial 3** | Use services: get info and trigger |
| **Tutorial 4** | Send commands and build a minimal client |
| **Tutorial 5** | Run a motion and parameter-change test |

## Tutorial 1: Discover the `pcp_ros2_bridge` package

This tutorial shows how to verify that `pcp_ros2_bridge` is running and that its ROS2 API is visible to client software.It does not enable, disable, or move the actuator.

The purpose is to understand the basic architecture:

<p align="center">
  <img src="/assets/images/pcp_ros2_bridge_high_level.png" alt="High-level ecosystem diagram" width="70%">
</p>

!!! note
    Client software should not use `pcp_api` directly. Client software should communicate with the bridge through ROS2 topics and services.

!!! success
    After this tutorial, the user should understand:
    
    - the bridge is a ROS2 API layer over `pcp_api`
    - clients communicate through ROS2 topics and services
    - `/actuators/state` is used for feedback
    - `/actuators/command` is used for commands
    - `/actuators/get_info` is used for on-demand actuator information
    - `/actuators/trigger` is used for discrete actions such as enable and disable

## Tutorial 2: Read Live Actuator State

This tutorial shows how client software reads live actuator feedback from `pcp_ros2_bridge`.

The bridge publishes continuous actuator feedback on:

```text
/actuators/state
```

!!! note
    This tutorial is safe. It only subscribes to actuator state. It does not enable, disable, or move the actuator.

!!! success
    After this tutorial, the user should understand:

    - continuous feedback is read from `/actuators/state`
    - state subscribers should use compatible QoS
    - named fields are the main client-facing state API
    - generic feedback arrays can expose additional actuator-specific values
    - state reading does not require direct `pcp_api` access

## Tutorial 3: Use Services: Get Info, Enable, Disable, Reset Fault

This tutorial shows how client software uses ROS2 services exposed by `pcp_ros2_bridge`.

It covers two service patterns:

1. Request actuator information on demand with `/actuators/get_info`.
2. Send discrete actuator actions with `/actuators/trigger`.

!!! warning
    Unlike Tutorial 1 and Tutorial 2, this tutorial can change actuator state if you send `enable`, `disable`, or `reset_fault`. 

!!! success
    After this tutorial, the user should understand:

    - services are used for request/response operations
    - `/actuators/get_info` is for on-demand information
    - `/actuators/trigger` is for discrete actions
    - enabling/disabling is done through the bridge, not through direct `pcp_api` calls

## Tutorial 4: Send Commands and Build a Minimal Client

This tutorial shows how a client sends actuator commands through `pcp_ros2_bridge`.

Commands are published on:

```text
/actuators/command
```

This tutorial also shows the minimal client pattern:

1. Subscribe to `/actuators/state`.
2. Optionally call `/actuators/trigger` to enable or disable.
3. Publish one command to `/actuators/command`.
4. Monitor state.

!!! warning
    This tutorial can move the actuator if you enable command publishing and the actuator is enabled.

!!! success
    After this tutorial, the user should understand:

    - command messages are published to `/actuators/command`
    - commands are targeted by `actuator_name`
    - state should be monitored before and after commands
    - enabling/disabling should be handled through `/actuators/trigger`
    - clients still do not use `pcp_api` directly

## Tutorial 5: Motion and Parameter Restore Test

This tutorial shows how a client application can coordinate a complete actuator test through `pcp_ros2_bridge`.

The test demonstrates how to:

1. Read and store the original actuator parameters.
2. Disable the actuator.
3. Set the current position as home.
4. Apply an initial parameter set.
5. Enable the actuator.
6. Command speed mode at `0.75 rad/s`.
7. Change the command to `0.25 rad/s`.
8. Modify selected parameters during the test.
9. Disable the actuator.
10. Restore the original parameters.
11. Verify the restored values.

!!! note
    The client does **not** call `pcp_api` directly. It only uses ROS2 topics and services exposed by `pcp_ros2_bridge`.

!!! warning
    This tutorial can move real actuator hardware. Before running with motion enabled:

    - Make sure the actuator is mechanically safe to move.
    - Make sure the output shaft is free or properly constrained.
    - Keep an emergency stop strategy available.
    - Start with conservative values.