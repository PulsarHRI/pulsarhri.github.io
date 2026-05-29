# Which Control Parameters Can Be Used in Each Mode?

!!! note
    This table describes Python API 2.0.0 control-mode terminology and the matching actuator firmware family. It is aligned with the public real and virtual actuator API stubs.

Not all public control parameters are relevant to every control mode. The table below summarizes parameters that directly tune mode behavior. For runnable examples, follow the [Python API Examples](../python_api/examples.md); the examples repository includes dedicated notebooks for real and virtual actuators covering mode changes and control-parameter changes.

Special-purpose voltage-injection and debug modes are intentionally not documented here.

<div class="pulsar-table-scroll">
  <table class="pulsar-parameter-table">
    <thead>
      <tr>
        <th>Parameter or setpoint argument</th>
        <th>Public API name</th>
        <th>Torque (<code>Mode.TORQUE</code>)</th>
        <th>Speed (<code>Mode.SPEED</code>)</th>
        <th>Position (<code>Mode.POSITION</code>)</th>
        <th>Impedance (<code>Mode.IMPEDANCE</code>)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Main setpoint</td>
        <td><code>SETPOINT</code>, <code>change_setpoint(...)</code></td>
        <td><span class="pulsar-yes">Yes</span>, torque in Nm</td>
        <td><span class="pulsar-yes">Yes</span>, speed in rad/s</td>
        <td><span class="pulsar-yes">Yes</span>, position in rad</td>
        <td><span class="pulsar-yes">Yes</span>, position in rad</td>
      </tr>
      <tr>
        <td>Torque performance preset</td>
        <td><code>TORQUE_PERFORMANCE</code>, <code>set_torque_performance(...)</code></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
      </tr>
      <tr>
        <td>Speed performance preset</td>
        <td><code>SPEED_PERFORMANCE</code>, <code>set_speed_performance(...)</code></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-no">No</span></td>
      </tr>
      <tr>
        <td>Current-loop gains</td>
        <td><code>id_Kp</code>, <code>id_Ki</code>, <code>iq_Kp</code>, <code>iq_Ki</code> in <code>change_torque_setpoint(...)</code></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-no">No</span></td>
      </tr>
      <tr>
        <td>Speed-loop gains</td>
        <td><code>KP_SPEED</code>, <code>KI_SPEED</code>, <code>spd_Kp</code>, <code>spd_Ki</code></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-no">No</span></td>
      </tr>
      <tr>
        <td>Position-loop gain</td>
        <td><code>KP_POSITION</code>, <code>pos_Kp</code></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-no">No</span></td>
      </tr>
      <tr>
        <td>Impedance stiffness</td>
        <td><code>K_STIFFNESS</code>, <code>K_stiff</code></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
      </tr>
      <tr>
        <td>Impedance damping</td>
        <td><code>K_DAMPING</code>, <code>K_damp</code></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
      </tr>
      <tr>
        <td>Impedance inertia</td>
        <td><code>J_imp</code></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
      </tr>
      <tr>
        <td>Feed-forward torque</td>
        <td><code>TORQUE_FF</code>, <code>ref_ff_torque</code></td>
        <td><span class="pulsar-na">N/A</span>, main setpoint is torque</td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
      </tr>
      <tr>
        <td>Feed-forward gain</td>
        <td><code>FF_GAIN</code></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
      </tr>
      <tr>
        <td>Symmetric torque limit</td>
        <td><code>LIM_TORQUE</code>, <code>PROFILE_TORQUE_MAX_NM</code></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
      </tr>
      <tr>
        <td>Speed limits</td>
        <td><code>LIM_SPEED_MAX</code>, <code>LIM_SPEED_MIN</code></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-no">No</span></td>
      </tr>
      <tr>
        <td>Position limits</td>
        <td><code>LIM_POSITION_MAX</code>, <code>LIM_POSITION_MIN</code></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
      </tr>
      <tr>
        <td>Position-profile speed limits</td>
        <td><code>PROFILE_POSITION_MAX</code>, <code>PROFILE_POSITION_MIN</code></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-no">No</span></td>
      </tr>
      <tr>
        <td>Speed-profile acceleration limits</td>
        <td><code>PROFILE_SPEED_MAX</code>, <code>PROFILE_SPEED_MIN</code></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-no">No</span></td>
      </tr>
      <tr>
        <td>Maximum profile speed</td>
        <td><code>PROFILE_SPEED_MAX_RAD_S</code></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-no">No</span></td>
      </tr>
      <tr>
        <td>Speed filter cutoff</td>
        <td><code>PCP_PARAM_SPEED_CUTOFF</code></td>
        <td><span class="pulsar-no">No</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
      </tr>
      <tr>
        <td>Current filter cutoff</td>
        <td><code>PCP_PARAM_CURRENT_CUTOFF</code></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
        <td><span class="pulsar-yes">Yes</span></td>
      </tr>
    </tbody>
  </table>
</div>

The API also exposes mode-agnostic or device-level parameters. These are not mode-tuning parameters, so they are not included in the compatibility matrix above:

- `MODE`
- `INVERT_FLAG`
- `FIRMWARE_VERSION`
- `PCP_ADDRESS`
- `SERIAL_NUMBER`
- `DEVICE_MODEL`
- `CONTROL_VERSION`
- `CAN_HIGH_SPEED`
