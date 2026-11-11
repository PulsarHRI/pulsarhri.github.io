(() => {
  const selector = ".md-version";
  const labelClass = "md-version-label";

  function addDocsVersionLabel() {
    const versionSelector = document.querySelector(selector);
    if (!versionSelector) {
      return false;
    }

    if (versionSelector.parentElement?.querySelector(`.${labelClass}`)) {
      versionSelector.setAttribute("aria-labelledby", "md-version-label");
      return true;
    }

    const label = document.createElement("span");
    label.className = labelClass;
    label.textContent = "SDK version:";
    label.id = "md-version-label";
    versionSelector.parentElement.insertBefore(label, versionSelector);
    versionSelector.setAttribute("aria-labelledby", label.id);
    return true;
  }

  function addDocsVersionLabelWhenAvailable() {
    if (addDocsVersionLabel()) {
      return;
    }

    const observer = new MutationObserver(() => {
      if (addDocsVersionLabel()) {
        observer.disconnect();
      }
    });

    observer.observe(document.documentElement, { childList: true, subtree: true });

    // Close the gap between the initial lookup and observer registration.
    if (addDocsVersionLabel()) {
      observer.disconnect();
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", addDocsVersionLabelWhenAvailable, { once: true });
  } else {
    addDocsVersionLabelWhenAvailable();
  }
})();
