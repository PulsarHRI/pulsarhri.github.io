# CAN bus utilization

Estimate the theoretical CAN FD load for a group of PULSE actuators. Adjust actuator count, telemetry selection, command rate, and data bitrate before configuring a high-rate system.

<div class="bus-utilization" id="bus-utilization-tool">
  <div class="bus-utilization__controls">
    <label class="bus-utilization__control" for="bus-actuators">
      <span>Actuators <output id="bus-actuators-value" for="bus-actuators">6</output></span>
      <input id="bus-actuators" type="range" min="1" max="10" value="6">
      <small>1–10 actuators on one bus</small>
    </label>

    <label class="bus-utilization__control" for="bus-feedback-items">
      <span>Telemetry items per actuator <output id="bus-feedback-items-value" for="bus-feedback-items">4</output></span>
      <input id="bus-feedback-items" type="range" min="1" max="12" value="4">
      <small>Each item uses a 1-byte identifier and a 4-byte value</small>
    </label>

    <div class="bus-utilization__control">
      <span>
        <label for="bus-feedback-hz">Telemetry frequency</label>
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
          <option value="speed">Velocity</option>
          <option value="position">Position</option>
          <option value="impedance" selected>Impedance</option>
        </select>
      </span>
      <small>Determines the maximum command parameters</small>
    </label>

    <label class="bus-utilization__control" for="bus-command-parameters">
      <span>Command parameters <output id="bus-command-parameters-value" for="bus-command-parameters">8 / 8</output></span>
      <input id="bus-command-parameters" type="range" min="1" max="8" value="8">
      <small>Includes the command; each parameter is a float32</small>
    </label>

    <fieldset class="bus-utilization__rate">
      <legend>CAN FD data bitrate</legend>
      <label><input type="radio" name="bus-data-rate" value="1"> <span>1 Mbit/s</span></label>
      <label><input type="radio" name="bus-data-rate" value="5" checked> <span>5 Mbit/s</span></label>
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
      <div><span>Telemetry</span><strong id="bus-feedback-load">0.0%</strong><i><b id="bus-feedback-bar"></b></i></div>
      <div><span>Commands</span><strong id="bus-command-load">0.0%</strong><i><b id="bus-command-bar"></b></i></div>
    </div>

    <dl class="bus-utilization__details">
      <div><dt>Telemetry frame</dt><dd id="bus-feedback-frame">—</dd></div>
      <div><dt>Command frame</dt><dd id="bus-command-frame">—</dd></div>
      <div><dt>Total frames</dt><dd id="bus-total-frames">—</dd></div>
    </dl>
  </section>
</div>

## Calculation

Each telemetry item occupies five data bytes: a one-byte identifier and a four-byte value. Payloads are rounded to a valid CAN FD size. Pulsar SDK permits at most 12 configured telemetry items.

Each command contains an action identifier followed by mode-specific float32 values. The estimate includes extended identifiers, protocol overhead, inter-frame spacing, and worst-case bit stuffing.

!!! note
    This is a theoretical upper-bound estimate. Leave headroom for arbitration, configuration, diagnostics, retransmissions, clock tolerance, adapter timing, and other non-periodic traffic. A value below 100% is not a real-time guarantee.
