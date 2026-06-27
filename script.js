(function () {
  const canonicalHost = "cedarwoodclose.com";
  const redirectHosts = new Set(["cedarwood.vc", "www.cedarwood.vc", "c-c.vc", "www.c-c.vc", "www.cedarwoodclose.com"]);

  if (redirectHosts.has(window.location.hostname)) {
    const target = new URL(window.location.href);
    target.protocol = "http:";
    target.hostname = canonicalHost;
    window.location.replace(target.toString());
  }
})();
