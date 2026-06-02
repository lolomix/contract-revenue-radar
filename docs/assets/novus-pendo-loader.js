(function () {
  var config = window.REVIEW_ROOM_PENDO_CONFIG || {};
  var apiKey = String(config.apiKey || "").trim();
  if (!apiKey || apiKey === "PENDO_API_KEY") {
    window.reviewRoomPendoStatus = "not_configured";
    return;
  }

  (function (p, e, n, d, o) {
    var v;
    var w;
    var x;
    var y;
    var z;
    o = p[d] = p[d] || {};
    o._q = o._q || [];
    v = ["initialize", "identify", "updateOptions", "pageLoad", "track"];
    for (w = 0, x = v.length; w < x; ++w) {
      (function (m) {
        o[m] = o[m] || function () {
          o._q[m === v[0] ? "unshift" : "push"]([m].concat([].slice.call(arguments, 0)));
        };
      })(v[w]);
    }
    y = e.createElement(n);
    y.async = true;
    y.src = "https://cdn.pendo.io/agent/static/" + apiKey + "/pendo.js";
    z = e.getElementsByTagName(n)[0];
    z.parentNode.insertBefore(y, z);
  })(window, document, "script", "pendo");

  window.pendo.initialize({
    visitor: {
      id: String(config.visitorId || "review-room-public-visitor"),
      role: "hackathon-judge-or-user",
      product: "Revenue Review Room",
    },
    account: {
      id: String(config.accountId || "contract-revenue-radar"),
      type: "public-demo",
    },
  });

  window.reviewRoomPendoStatus = "initialized";
})();
