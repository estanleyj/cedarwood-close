(function () {
  const canonicalHost = "cedarwood.vc";
  const redirectHosts = new Set(["www.cedarwood.vc", "c-c.vc", "www.c-c.vc", "cedarwoodclose.com", "www.cedarwoodclose.com"]);

  if (redirectHosts.has(window.location.hostname)) {
    const target = new URL(window.location.href);
    target.protocol = "https:";
    target.hostname = canonicalHost;
    window.location.replace(target.toString());
    return;
  }

  const year = document.getElementById("year");
  if (year) {
    year.textContent = String(new Date().getFullYear());
  }
})();
