function setExternalLinksToNewTab() {
  document.querySelectorAll("a[href]").forEach(function (link) {
    var rawHref = link.getAttribute("href");

    if (!rawHref || rawHref.startsWith("#")) {
      return;
    }

    var url;

    try {
      url = new URL(rawHref, window.location.href);
    } catch (_) {
      return;
    }

    if (url.protocol !== "http:" && url.protocol !== "https:") {
      return;
    }

    if (url.origin === window.location.origin) {
      return;
    }

    link.setAttribute("target", "_blank");
    link.setAttribute("rel", "noopener noreferrer");
  });
}

if (typeof document$ !== "undefined") {
  document$.subscribe(setExternalLinksToNewTab);
} else {
  document.addEventListener("DOMContentLoaded", setExternalLinksToNewTab);
}
