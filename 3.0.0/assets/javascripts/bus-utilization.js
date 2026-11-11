(function () {
  "use strict";

  var CAN_FD_PAYLOAD_SIZES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 16, 20, 24, 32, 48, 64];
  var CONTROL_MODE_MAX_PARAMETERS = { torque: 5, speed: 5, position: 6, impedance: 8 };

  function dlcFor(bytes) {
    return CAN_FD_PAYLOAD_SIZES.find(function (size) { return size >= bytes; });
  }

  // ISO CAN FD extended frame with worst-case stuffing and a 1 Mbps nominal phase.
  function frameTiming(payloadBytes, dataRateMbps) {
    var dlc = dlcFor(payloadBytes);
    var dynamicRegionBits = 41 + 8 * dlc;
    var dynamicStuffBits = Math.floor((dynamicRegionBits - 1) / 4);
    var nominalStuffBits = 8;
    var crcSectionBits = dlc <= 16 ? 28 : 33;
    var nominalBits = 36 + nominalStuffBits + 1 + 9 + 3;
    var dataBits = 5 + 8 * dlc + dynamicStuffBits - nominalStuffBits + crcSectionBits - 1;

    return {
      dlc: dlc,
      microseconds: nominalBits + dataBits / dataRateMbps
    };
  }

  function calculateBusLoad(options) {
    var feedback = frameTiming(options.feedbackItems * 5, options.dataRateMbps);
    var commandPayloadBytes = 1 + options.commandParameters * 4;
    var command = frameTiming(commandPayloadBytes, options.dataRateMbps);
    var feedbackLoad = options.actuators * options.feedbackHz * feedback.microseconds / 10000;
    var commandLoad = options.actuators * options.commandHz * command.microseconds / 10000;

    return {
      utilization: feedbackLoad + commandLoad,
      feedbackLoad: feedbackLoad,
      commandLoad: commandLoad,
      feedbackDlc: feedback.dlc,
      feedbackMicroseconds: feedback.microseconds,
      commandPayloadBytes: commandPayloadBytes,
      commandDlc: command.dlc,
      commandMicroseconds: command.microseconds,
      framesPerSecond: options.actuators * (options.feedbackHz + options.commandHz)
    };
  }

  function initializeBusUtilizationTool() {
    var root = document.getElementById("bus-utilization-tool");
    if (!root || root.dataset.initialized) return;
    root.dataset.initialized = "true";

    var actuators = document.getElementById("bus-actuators");
    var feedbackItems = document.getElementById("bus-feedback-items");
    var feedbackHz = document.getElementById("bus-feedback-hz");
    var feedbackHzNumber = document.getElementById("bus-feedback-hz-number");
    var commandHz = document.getElementById("bus-command-hz");
    var commandHzNumber = document.getElementById("bus-command-hz-number");
    var controlMode = document.getElementById("bus-control-mode");
    var commandParameters = document.getElementById("bus-command-parameters");
    var gauge = document.getElementById("bus-utilization-gauge");
    var value = document.getElementById("bus-utilization-value");
    var status = document.getElementById("bus-utilization-status");
    var displayedUtilization = 0;
    var animationFrame;
    var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function animateValue(target) {
      cancelAnimationFrame(animationFrame);
      if (reducedMotion) {
        displayedUtilization = target;
        value.textContent = target.toFixed(1) + "%";
        return;
      }

      var start = displayedUtilization;
      var startedAt = performance.now();
      function step(now) {
        var progress = Math.min((now - startedAt) / 280, 1);
        displayedUtilization = start + (target - start) * (1 - Math.pow(1 - progress, 3));
        value.textContent = displayedUtilization.toFixed(1) + "%";
        if (progress < 1) animationFrame = requestAnimationFrame(step);
      }
      animationFrame = requestAnimationFrame(step);
    }

    function update() {
      var maximumParameters = CONTROL_MODE_MAX_PARAMETERS[controlMode.value];
      commandParameters.max = maximumParameters;
      if (Number(commandParameters.value) > maximumParameters) commandParameters.value = maximumParameters;

      var options = {
        actuators: Number(actuators.value),
        feedbackItems: Number(feedbackItems.value),
        feedbackHz: Number(feedbackHz.value),
        commandHz: Number(commandHz.value),
        commandParameters: Number(commandParameters.value),
        dataRateMbps: Number(root.querySelector('input[name="bus-data-rate"]:checked').value)
      };
      var result = calculateBusLoad(options);
      var level = result.utilization >= 100 ? "over" : result.utilization >= 80 ? "high" : result.utilization >= 60 ? "medium" : "low";

      document.getElementById("bus-actuators-value").textContent = options.actuators;
      document.getElementById("bus-feedback-items-value").textContent = options.feedbackItems;
      document.getElementById("bus-command-parameters-value").textContent = options.commandParameters + " / " + maximumParameters;
      actuators.setAttribute("aria-valuetext", options.actuators + " actuators");
      feedbackItems.setAttribute("aria-valuetext", options.feedbackItems + " feedback items");
      commandParameters.setAttribute("aria-valuetext", options.commandParameters + " of " + maximumParameters + " parameters");
      feedbackHz.setAttribute("aria-valuetext", options.feedbackHz + " hertz");
      commandHz.setAttribute("aria-valuetext", options.commandHz + " hertz");

      gauge.dataset.level = level;
      gauge.style.setProperty("--utilization", Math.min(result.utilization, 100));
      gauge.setAttribute("aria-valuenow", Math.min(result.utilization, 100).toFixed(1));
      gauge.setAttribute("aria-valuetext", result.utilization.toFixed(1) + " percent estimated bus utilization");
      animateValue(result.utilization);

      status.textContent = level === "over" ? "Traffic exceeds the theoretical bus capacity."
        : level === "high" ? "Very little theoretical headroom remains."
        : level === "medium" ? "The bus is busy; leave margin for non-periodic traffic."
        : "The estimate leaves theoretical headroom.";

      document.getElementById("bus-feedback-load").textContent = result.feedbackLoad.toFixed(1) + "%";
      document.getElementById("bus-command-load").textContent = result.commandLoad.toFixed(1) + "%";
      document.getElementById("bus-feedback-bar").style.width = Math.min(result.feedbackLoad, 100) + "%";
      document.getElementById("bus-command-bar").style.width = Math.min(result.commandLoad, 100) + "%";
      document.getElementById("bus-feedback-frame").textContent = (options.feedbackItems * 5) + " B data → " + result.feedbackDlc + " B DLC · " + result.feedbackMicroseconds.toFixed(1) + " µs";
      document.getElementById("bus-command-frame").textContent = controlMode.options[controlMode.selectedIndex].text + " · " + result.commandPayloadBytes + " B data → " + result.commandDlc + " B DLC · " + result.commandMicroseconds.toFixed(1) + " µs";
      document.getElementById("bus-total-frames").textContent = result.framesPerSecond.toLocaleString() + " frames/s";
    }

    function bindFrequency(range, number) {
      range.addEventListener("input", function () {
        number.value = range.value;
        update();
      });
      number.addEventListener("input", function () {
        if (number.validity.valid && number.value !== "") {
          range.value = number.value;
          update();
        }
      });
      number.addEventListener("change", function () {
        number.value = Math.min(Number(number.max), Math.max(Number(number.min), Math.round(Number(number.value)) || Number(number.min)));
        range.value = number.value;
        update();
      });
    }

    actuators.addEventListener("input", update);
    feedbackItems.addEventListener("input", update);
    controlMode.addEventListener("change", update);
    commandParameters.addEventListener("input", update);
    root.querySelectorAll('input[name="bus-data-rate"]').forEach(function (input) {
      input.addEventListener("input", update);
    });
    bindFrequency(feedbackHz, feedbackHzNumber);
    bindFrequency(commandHz, commandHzNumber);
    update();
  }

  if (typeof module !== "undefined") {
    module.exports = { dlcFor: dlcFor, frameTiming: frameTiming, calculateBusLoad: calculateBusLoad };
    if (require.main === module) {
      var check = calculateBusLoad({ actuators: 1, feedbackItems: 1, feedbackHz: 1, commandHz: 1, commandParameters: 8, dataRateMbps: 1 });
      console.assert(dlcFor(50) === 64, "50-byte payload must use the 64-byte DLC");
      console.assert(check.commandDlc === 48, "Impedance command must use the 48-byte DLC");
      console.assert(Math.abs(check.utilization - 0.0717) < 1e-9, "Unexpected one-actuator utilization");
      console.log("Bus utilization self-check passed");
    }
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(initializeBusUtilizationTool);
  } else if (typeof document !== "undefined") {
    document.addEventListener("DOMContentLoaded", initializeBusUtilizationTool);
  }
}());
