# Predefined Performance Profiles for Actuator Control

The actuator provides a set of predefined performance profiles for both **torque** and **speed** control loops. These profiles allow users to easily configure the system's responsiveness without manually tuning low-level control parameters. Each profile adjusts the **bandwidth** and **stability** of the inner control loops, which is essential for achieving optimal behavior in dynamic or high-precision applications.

---

## Torque Control Loop Performance

This setting determines how quickly and aggressively the actuator responds to torque commands. The available profiles are:

### AGGRESSIVE
- **Bandwidth**: ~1000 Hz  
- **Behavior**: Maximizes responsiveness and torque application speed.  
- **Use Case**: Ideal for dynamic tasks such as impedance control or joint torque control.  
- **Trade-off**: May reduce steady-state precision.

### BALANCED
- **Bandwidth**: ~500 Hz  
- **Behavior**: Offers a compromise between responsiveness and stability.  
- **Use Case**: Suitable for general-purpose applications.

### SOFT
- **Bandwidth**: ~100 Hz  
- **Behavior**: Prioritizes smoothness and precision over speed.  
- **Use Case**: Best for tasks requiring high torque fidelity and low noise.  
- **Trade-off**: Lower responsiveness.

### CUSTOM *(if supported)*
- **Behavior**: Allows manual tuning of control gains.  
- **Use Case**: For advanced users with specialized requirements.

#### API Command
```python
set_torque_performance(self, performance: TorquePerformance)
```
- **Parameter**: `performance`  
  - **Type**: `PulsarActuator.TorquePerformance`  
  - **Description**: Sets the desired torque control profile.

### Table 4 – `TorquePerformance` (Enum)

| Name       | Value | Bandwidth (Hz) | Description                                 |
|------------|-------|----------------|---------------------------------------------|
| AGGRESSIVE | 1     | ~1000 Hz       | Fast response, less precision in steady state |
| BALANCED   | 2     | ~500 Hz        | Balanced between response and stability     |
| SOFT       | 3     | ~100 Hz        | Stable and quiet, low responsiveness        |


## Speed Loop Performance

The speed control loop uses the same predefined profiles as the torque loop, ensuring consistent behavior tuning across both control domains.

### AGGRESSIVE
- **Behavior**: Enables rapid speed tracking with minimal delay and short settling time.
- **Use Case**: High-speed applications where quick velocity changes are required.

### BALANCED
- **Behavior**: Provides a well-rounded compromise between speed and stability.
- **Use Case**: Suitable for general-purpose motion control tasks.

### SOFT
- **Behavior**: Emphasizes smooth, accurate motion over speed.
- **Use Case**: Ideal for applications requiring low noise and precise velocity regulation.

### CUSTOM
- **Behavior**: Grants full control over PI controller gains.
- **Use Case**: Advanced tuning for specialized systems or experimental setups.


### API Command

To configure the speed loop performance, use the following API method:

```bash
set_speed_performance(self, performance: SpeedPerformance)
```

### Parameter: `performance`

- **Type**: `PulsarActuator.SpeedPerformance`
- **Description**: Sets the desired speed control profile.

### Table 5 – `SpeedPerformance` (Enum)

| Name       | Value | Description                      |
|------------|-------|----------------------------------|
| AGGRESSIVE | 1     | Aggressive speed control profile |
| BALANCED   | 2     | Balanced speed control profile   |
| SOFT       | 3     | Soft speed control profile       |
| CUSTOM     | 4     | Custom-defined profile           |

