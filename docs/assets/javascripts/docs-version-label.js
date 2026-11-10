(() => {
  const selector = ".md-version";
  const labelClass = "md-version-label";

  function addDocsVersionLabel() {
    const versionSelector = document.querySelector(selector);
    if (!versionSelector || versionSelector.parentElement?.querySelector(`.${labelClass}`)) {
      return;
    }

    const label = document.createElement("span");
    label.className = labelClass;
    label.textContent = "Docs version:";
    label.id = "md-version-label";
    versionSelector.parentElement.insertBefore(label, versionSelector);
    versionSelector.setAttribute("aria-labelledby", label.id);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", addDocsVersionLabel, { once: true });
  } else {
    addDocsVersionLabel();
  }
})();
