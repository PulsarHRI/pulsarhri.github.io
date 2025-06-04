# Feedback Configuration from the Pulsar Actuator
To efficiently manage data flow and avoid saturating the CAN bus, the PulsarActuator API supports two feedback channels with configurable update rates:

* High-Frequency Feedback: For fast-changing signals (e.g., torque, speed).
* Low-Frequency Feedback: For slower or less critical signals (e.g., temperature, voltage).
Each channel allows you to specify:
* Which feedback items to receive.
* The rate at which they are updated.

## 🔁 High-Frequency Feedback
### setHighFreqFeedbackItems(items: list)
Sets the list of feedback items to be sent at high frequency.

* Parameters: `items` A list of PulsarActuator.PCP_Items enums (see Table 1).
### setHighFreqFeedbackRate(rate: Rates)
Sets the update rate for high-frequency feedback.

* Parameters: `rate` A value from the PulsarActuator.Rates enum (see Table 2).

## 🕒 Low-Frequency Feedback
### setLowFreqFeedbackItems(items: list)
Sets the list of feedback items to be sent at low frequency.

* Parameters: `items` A list of PulsarActuator.PCP_Items enums.
### setLowFreqFeedbackRate(rate: Rates)
Sets the update rate for low-frequency feedback.

* Parameters: `rate` A value from the PulsarActuator.Rates enum.

## 📡 Receiving Feedback
To handle incoming feedback, you can register a callback function.
### set_feedback_callback(callback: callable) -> None
Registers a function to be called whenever new feedback is received.
* Parameters: `callback` A callable that will be executed with each feedback update.

## 📘 Table 1 – Configurable Feedback Items (`PCP_Items` Enum)

| Enum Name              | Code   | Description |
|------------------------|--------|-------------|
| `ENCODER_INT`          | 0x41   | Internal encoder position (rads) |
| `ENCODER_INT_RAW`      | 0x42   | Raw internal encoder value (uint32) |
| `ENCODER_EXT`          | 0x43   | External encoder position (rads) |
| `ENCODER_EXT_RAW`      | 0x44   | Raw external encoder value (uint32) |
| `SPEED_FB`             | 0x45   | Output speed (rad/s) |
| `IA`, `IB`, `IC`       | 0x46–0x48 | Phase currents A, B, C (Amps) |
| `TORQUE_SENS`          | 0x49   | Measured torque (Nm) |
| `TORQUE_SENS_RAW`      | 0x4A   | Raw torque sensor value (uint32) |
| `POSITION_REF`         | 0x4B   | Position mode command (rads) |
| `POSITION_FB`          | 0x4C   | Actual position (rads) |
| `SPEED_REF`            | 0x4D   | Speed mode command (rad/s) |
| `ID_REF`, `ID_FB`      | 0x4F–0x50 | Direct current reference and feedback (Amps) |
| `IQ_REF`, `IQ_FB`      | 0x51–0x52 | Quadrature current reference and feedback (Amps) |
| `VD_REF`, `VQ_REF`     | 0x53–0x54 | DVI mode voltage references (Volts) |
| `TORQUE_REF`, `TORQUE_FB` | 0x55–0x56 | Torque command and feedback (Nm) |
| `ENABLE`               | 0x57   | Actuator enabled state (0/1) |
| `ERRORS_ENCODER_INT`   | 0x60   | Internal encoder error count |
| `ERRORS_ENCODER_EXT`   | 0x61   | External encoder error count |
| `ERRORS_OVERRUN`       | 0x62   | Loop overrun count |
| `VBUS`                 | 0x70   | Bus voltage |
| `TEMP_PCB`             | 0x71   | PCB temperature |
| `TEMP_MOTOR`           | 0x72   | Motor winding temperature |

---

## ⏱️ Table 2 – Feedback Rates (`Rates` Enum)

| Enum Name     | Value   | Update Frequency |
|---------------|---------|------------------|
| `DISABLED`    | 0       | Disabled |
| `RATE_1KHZ`   | 10      | 1,000 Hz |
| `RATE_100HZ`  | 100     | 100 Hz |
| `RATE_50HZ`   | 200     | 50 Hz |
| `RATE_10HZ`   | 1,000   | 10 Hz |
| `RATE_5HZ`    | 2,000   | 5 Hz |
| `RATE_2HZ`    | 5,000   | 2 Hz |
| `RATE_1HZ`    | 10,000  | 1 Hz |

---

!!! important
    To optimize CAN bus performance, only enable the feedback items and rates necessary for your application.
