# Quickstart Tutorial: No-Code Desktop App for Real Actuator

This page walks you through running a Real Actuator connected via USB without needing to do any coding, using the [PULSAR HRI Desktop App](../control/desktop_app/desktop_app.md), which can be downloaded from [HERE](../download/download_app.md).

## 👣 Step-By-Step Guide
1. Make sure your actuator is set up and connected via USB, as per the [Quickstart Tutorial: Set up Real Actuator and connect via USB](../quickstarts/quickstart_set_up_usb.md) 

2. Launch the [PULSAR HRI Desktop App](../control/desktop_app/desktop_app.md): you should be able to see the actuator connected via USB in the "Devices" dropdown. Upon selecting it, a popup will inform you of the successful connection and the actuator's address will be shown 
> *the Actuator Address is useful for example to connect via CAN Bus instead of USB, but this will be covered in another guide*

    ![GUI to connect](../assets/images/GUI_to_connect.png)
    ![GUI connected](../assets/images/GUI_connected.png)
    !!! warning
        You successfully connected to the actuator, which is now ready to move, that's great!!
        But, as they say, with great power come great responsibilities: 
        **be mindful to keep the actuator's operating area clear of any object** that might get caught or collide with any moving parts.

3. As a first example, we'll run the actuator in **Speed Control** mode: 
    - select **Speed Control** mode under **Control Type**
    - check that the setpoint in rad/s is currently zero
    - hit the **play button**: the actuator won't move as you're telling it to move at zero speed. 
    ![Speed Ctrl Zero](../assets/images/GUI_speed_zero.png)
    - you can now change the setpoint speed either by typing the desired rad/s value in the textbox, or by moving the slider
    - you'll see the actuator moving and the live plot of the position at the bottom of the GUI being updated accordingly

4. We can now move to try **Position Control** mode:
    - select **Positon Control** mode under **Control Type**
    - click on the **SET 0 POSITION** button, this will store the current position (output angle) of the actuator as the zero. 
        - If you skip setting the zero position, it will use the latest zero position that was set and written to memory 
    ![Position Ctrl Zero](../assets/images/GUI_position_control_zero.png)
    - hit the **play button**: the actuator won't move as you're telling it to hold the zero position you just set.
    ![Position Ctrl Move](../assets/images/GUI_position_control_move.png)
    - you can now **change the setpoint position** either by typing the desired rad value in the textbox, or by moving the slider
    - you'll see the actuator moving and the live plot of the position at the bottom of the GUI being updated accordingly

5. You can now try changing the values of **actuator limits** and of the **control parameters** associated to different [available Actuator Control Modes](../control/control_modes_explained/control_modes_overview.md)
    - Continuing from the previous point we can try changing the control parameter associated to Position control, **Position Kp**
        - increasing this parameter essentially makes the actuator more responsive but, if set too high, it will at some point lead to overshooting setpoints and eventually instable behaviour
    !!! warning
        When changing control parameters such as Kp Position, introduce small gradual changes at a time to avoid unexpected and potentially unsafe behaviour of the actuator. For example you can try going from 0.5 to 1 and see how the change impact the behaviour of the actuator, don't go e.g. from 0.5 to 5
    - Upon changing the value of Position Kp, for it to take effect you will need to click the **Apply** button
    - This same process can be applied when selecting other modes, changing their respective control parameters.
        - The **Torque** and the **Speed** control loops also have some preset control parameters that can be simply sleected form the respective dropdown menus
    - You can then try to set some position and torque limts from **Set Limits** and see how that impacts the behaviour of the actuator.

6. If you have a mechanical shaft that you can attach to the output shaft of the actuator (such as those printable from [here](../set_up/hardware_interfaces/mechanical_interfaces.md))
    - you could try fastening a shaft to the output of the actuator and try interacting with it in different contorl modes, for example:
        - get the actuator to hold a position setpoint in **Position Control** mode and try to move the output shaft manually: you will feel the actuator opposing your force, the highest the Position Kp, the stronger it will oppose you
        - starting with a low value, e.g. 2Nm, set a torque setpoint in **Torque Control**: the actuator will start spinnging producing such torque at the output: if you grab the output shaft, this will stop as soon as you exert a countertorque of the same amount. You can try changing the torque setpoint from there or the torque loop control parameters.

!!! success
    Well done! You’ve successfully powered on a PULSAR actuator, switched control modes, and observed how it responds. You’ve already covered a lot 🚀
    
    Where can you go from here?

    - If you’re comfortable with Python and want **deeper control or multi-actuator setups**, continue with the [Quickstart Tutorial: Python API for Real Actuator](../quickstarts/quickstart_python_api.md) 
        
    - If you're interested in **simulating PULSAR actuators** without needing hardware, explore [how to create Virtual Actuators with the AUGUR Digital Twin](../set_up/set_up_virtual.md).

!!! question
    Need help or something doesn’t work? Head over to the [Support page](../support.md): we’ve got your back.
