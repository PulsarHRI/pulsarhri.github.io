# Home

Welcome to the **PULSAR HRI Ecosystem Documentation**!

Whether you're a researcher, developer, or engineer, the content on this website will help you get up and running with PULSAR products: 
PULSAR HRI develops best-in-class actuation systems and surrounding ecosystem, to enable next-generation robotics.

### ⚡ First Time Here?

If you really can't wait to get hands-on, just go straight to the [**Quickstart No-Code Guide**](quickstarts/quickstart_desktop_app.md) to set up, power your actuator and get moving in minutes!

!!! tip
    Make sure to read the following short section: it will allow you to easily find what you need in the website

## 🧭 Ecosystem Overview

At a glance, these are the main elements of the PULSAR HRI ecosystem:

![High-level ecosystem diagram](assets/images/high_level_diagram_ecosystem.png)

- **REAL** ACTUATORS which, once [set up](set_up/set_up_real.md), offer the following [hardware communication interfaces](communicate/communicate_real.md): 
    - Direct **USB** connection
    - **CAN** communication 
<br><br>
- **VIRTUAL** ACTUATORS closely matching their Real counterparts behaviour. These [Virtual Actuators can be set up](set_up/set_up_virtual.md) thanks to:
    - 🚧 **AUGUR Digital Twin**, UNDER DEVELOPMENT - modeling the physics of the real actuator and running the exact same control algorithms
<br><br>
- **CONTROL INTERFACES** of different kinds and for different needs, to control *both Real and Virtual Actuators*:
    - [**Desktop Application**](control/desktop_app/desktop_app.md), no-code GUI for single actuator testing, for [the easiest quickstart experience](quickstarts/quickstart_desktop_app.md) and to get familiar with PULSAR HRI actuators and their control
    - [**Python API**](control/python_api/install_python_api.md), simple but powerful scripting to control multiple actuators for robotics prototypes and to leverage Python libraries such as for **ML, AI** applications
        - 🚧 **ROS2 Python Node**, UNDER DEVELOPMENT
    - 🚧 **C++ API**, UNDER DEVELOPMENT - to control multiple actuators in demanding applications with strict real-time requirements, where latency is a blocker
        - 🚧 **ROS2 C++ Node**, UNDER DEVELOPMENT

!!! note
    A quick alignment on naming we use:
    
    - **Motors** = Direct-drive units without transmission  
    - **Actuators** = Motors with integrated transmission

A question we often hear is: 
>*"How are you different from the other actuator companies?"*

Glad you asked: check out [PULSAR HRI's website](https://pulsarhri.com/technology/) for answers!

---

### 🆘 Need help? 
Visit our [Support page](support.md) or check the [FAQ](faq.md).

---
![Pulsar](assets/images/P98_01.jpg){ loading=lazy }

