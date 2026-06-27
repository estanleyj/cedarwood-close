(function () {
  const canonicalHost = "cedarwood.vc";
  const redirectHosts = new Set(["www.cedarwood.vc", "c-c.vc", "www.c-c.vc", "cedarwoodclose.com", "www.cedarwoodclose.com"]);

  if (redirectHosts.has(window.location.hostname)) {
    const target = new URL(window.location.href);
    target.protocol = "http:";
    target.hostname = canonicalHost;
    window.location.replace(target.toString());
  }
})();
