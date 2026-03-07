---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Web Server Potential Spike in Error Response Codes" prebuilt detection rule.
---

# Web Server Potential Spike in Error Response Codes

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Web Server Potential Spike in Error Response Codes

This rule detects bursts of 5xx errors (500–504) from GET traffic, highlighting abnormal server behavior that accompanies active scanning or fuzzing and exposes fragile code paths or misconfigured proxies. Attackers sweep common and generated endpoints while mutating query params and headers—path traversal, template syntax, large payloads—to repeatedly force backend exceptions and gateway timeouts, enumerate which routes fail, and pinpoint inputs that leak stack traces or crash components for follow-on exploitation.

### Possible investigation steps

- Plot error rates per minute by server and client around the alert window to confirm the spike, determine scope, and separate a single noisy client from a platform-wide issue.
- Aggregate the failing URL paths and query strings from the flagged client and look for enumeration sequences, traversal encoding, template injection markers, or oversized inputs indicative of fuzzing.
- Examine User-Agent, Referer, header mix, and TLS JA3 for generic scanner signatures or reuse across multiple clients, and enrich the originating IP with reputation and hosting-provider attribution.
- Correlate the timeframe with reverse proxy/WAF/IDS and application error logs or stack traces to identify which routes threw exceptions or timeouts and whether they align with the client’s input patterns.
- Validate backend and dependency health (upstreams, databases, caches, deployments) to rule out infrastructure regressions, then compare whether only the suspicious client experiences disproportionate failures.

### False positive analysis

- A scheduled deployment or upstream dependency issue can cause normal GET traffic to fail with 502/503/504, and many users egressing through a shared NAT or reverse proxy may be aggregated as one source IP that triggers the spike.
- An internal health-check, load test, or site crawler running from a single host can rapidly traverse endpoints and induce 500 errors on fragile routes, mimicking scanner-like behavior without malicious intent.

### Response and remediation

- Immediately rate-limit or block the originating client(s) at the edge (reverse proxy/WAF) using the observed source IPs, User-Agent/TLS fingerprints, and the failing URL patterns generating 5xx bursts.
- Drain the origin upstream(s) showing repeated 500/502/503/504 on the probed routes, roll back the latest deployment or config change for those services, and disable any unstable endpoint or plugin that is crashing under input fuzzing.
- Restart affected application workers and proxies, purge bad cache entries, re-enable traffic gradually with canary percentage, and confirm normal response rates via synthetic checks against the previously failing URLs.
- Escalate to Security Operations and Incident Response if 5xx spikes persist after blocking or if error pages expose stack traces, credentials, or admin route disclosures, or if traffic originates from multiple global hosting ASNs.
- Deploy targeted WAF rules for path traversal and injection markers seen in the URLs, enforce per-IP and per-route rate limits, tighten upstream timeouts/circuit breakers, and replace verbose error pages with generic responses that omit stack details.
- Add bot management and IP reputation blocking at the CDN/edge, lock down unauthenticated access to admin/debug routes, and instrument alerts that trigger on sustained 5xx bursts per client and per route with automatic edge throttling.

