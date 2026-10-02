# CAN Bus Utilization Tool

Estimate the theoretical CAN FD bus load for a group of PULSAR actuators. Adjust the controls to see how actuator count, feedback, command frequency, and data bitrate affect utilization.

<div class="bus-utilization" id="bus-utilization-tool">
  <div class="bus-utilization__controls">
    <label class="bus-utilization__control" for="bus-actuators">
      <span>Actuators <output id="bus-actuators-value" for="bus-actuators">6</output></span>
      <input id="bus-actuators" type="range" min="1" max="10" value="6">
      <small>1–10 actuators on one bus</small>
    </label>

    <label class="bus-utilization__control" for="bus-feedback-items">
      <span>Feedback items per actuator <output id="bus-feedback-items-value" for="bus-feedback-items">4</output></span>
      <input id="bus-feedback-items" type="range" min="1" max="10" value="4">
      <small>Each item uses a 1-byte identifier and a 4-byte value</small>
    </label>

    <div class="bus-utilization__control">
      <span>
        <label for="bus-feedback-hz">Feedback frequency</label>
        <label class="bus-utilization__number" for="bus-feedback-hz-number"><input id="bus-feedback-hz-number" type="number" min="1" max="2000" value="500" step="1"><span>Hz</span></label>
      </span>
      <input id="bus-feedback-hz" type="range" min="1" max="2000" value="500" step="1">
      <small>Sent by each actuator</small>
    </div>

    <div class="bus-utilization__control">
      <span>
        <label for="bus-command-hz">Command frequency</label>
        <label class="bus-utilization__number" for="bus-command-hz-number"><input id="bus-command-hz-number" type="number" min="1" max="2000" value="500" step="1"><span>Hz</span></label>
      </span>
      <input id="bus-command-hz" type="range" min="1" max="2000" value="500" step="1">
      <small>Sent by the host to each actuator</small>
    </div>

    <label class="bus-utilization__control" for="bus-control-mode">
      <span>Control mode
        <select id="bus-control-mode">
          <option value="torque">Torque</option>
          <option value="speed">Speed</option>
          <option value="position">Position</option>
          <option value="impedance" selected>Impedance</option>
        </select>
      </span>
      <small>Determines the maximum command parameters</small>
    </label>

    <label class="bus-utilization__control" for="bus-command-parameters">
      <span>Command parameters <output id="bus-command-parameters-value" for="bus-command-parameters">8 / 8</output></span>
      <input id="bus-command-parameters" type="range" min="1" max="8" value="8">
      <small>Includes the setpoint; each parameter is a float32</small>
    </label>

    <fieldset class="bus-utilization__rate">
      <legend>CAN FD data bitrate</legend>
      <label><input type="radio" name="bus-data-rate" value="1"> <span>1 Mbps</span></label>
      <label><input type="radio" name="bus-data-rate" value="5" checked> <span>5 Mbps</span></label>
    </fieldset>
  </div>

  <section class="bus-utilization__result" aria-labelledby="bus-utilization-heading">
    <h2 id="bus-utilization-heading">Estimated utilization</h2>
    <div class="bus-utilization__gauge" id="bus-utilization-gauge" role="meter" aria-label="Estimated bus utilization" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">
      <div class="bus-utilization__gauge-center">
        <strong id="bus-utilization-value" aria-live="polite">0.0%</strong>
        <span>of bus capacity</span>
      </div>
    </div>
    <p class="bus-utilization__status" id="bus-utilization-status"></p>

    <div class="bus-utilization__breakdown">
      <div>
        <span>Feedback</span><strong id="bus-feedback-load">0.0%</strong>
        <i><b id="bus-feedback-bar"></b></i>
      </div>
      <div>
        <span>Commands</span><strong id="bus-command-load">0.0%</strong>
        <i><b id="bus-command-bar"></b></i>
      </div>
    </div>

    <dl class="bus-utilization__details">
      <div><dt>Feedback frame</dt><dd id="bus-feedback-frame">—</dd></div>
      <div><dt>Command frame</dt><dd id="bus-command-frame">—</dd></div>
      <div><dt>Total frames</dt><dd id="bus-total-frames">—</dd></div>
    </dl>
  </section>
</div>

## How the estimate is calculated

Each feedback item occupies **5 data bytes**: a 1-byte PCP item identifier and a 4-byte value. The combined data is rounded up to the next valid CAN FD payload size: 0–8, 12, 16, 20, 24, 32, 48, or 64 bytes. Firmware currently supports up to 10 configured high-rate feedback items.

Each command contains a 1-byte action identifier followed by the selected number of 4-byte parameters. The setpoint is always included. Torque and Speed support up to 5 parameters, Position up to 6, and Impedance up to 8. The resulting data is rounded up to the next valid CAN FD payload size.

Both directions use 29-bit extended CAN identifiers; source and target addresses are carried in that identifier rather than the data payload. The calculation assumes a 1 Mbps nominal/arbitration bitrate, applies the selected bitrate to the CAN FD data phase, and includes protocol overhead, inter-frame spacing, and worst-case bit stuffing.

!!! note
    This is a theoretical upper-bound estimate for periodic traffic. Real systems need additional headroom for arbitration, configuration and error messages, retransmissions, clock tolerance, adapter/host timing, and non-periodic traffic. Values at or above 100% cannot fit on the bus; lower values are not a guarantee of real-time performance.
