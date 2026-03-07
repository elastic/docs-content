---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Web Server Suspicious User Agent Requests" prebuilt detection rule.
---

# Web Server Suspicious User Agent Requests

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Web Server Suspicious User Agent Requests

This rule flags surges of web requests that advertise scanner or brute-force tool user agents, signaling active reconnaissance against your web servers and applications. A common pattern is dirsearch or gobuster sweeping for hidden paths, firing hundreds of rapid GETs across diverse URLs from one host and probing admin panels, backup folders, and robots.txt.

### Possible investigation steps

- Verify whether the activity aligns with approved scanners or uptime checks by cross-referencing inventories, allowlists, change windows, and egress ranges; otherwise enrich the originating IP with ASN, geolocation, and threat reputation to gauge risk.
- Sample representative requests to identify targeted paths and payloads (e.g., admin panels, .git/.env, backups, traversal, SQLi/XSS markers) and note any successful responses or downloads that indicate information exposure.
- Analyze request rate, methods, and status-code distribution to separate noisy recon from successful discovery or brute-force patterns, highlighting any POST/PUT with nontrivial bodies.
- Correlate the same client across hosts and security layers (application/auth logs, WAF/CDN, IDS) to determine whether it is scanning multiple services, triggering signatures, or attempting credential stuffing.
- Assess user-agent authenticity and evasiveness by comparing HTTP header order/values and TLS fingerprints (JA3/JA4) to expected clients, and verify true client identity via forwarded-for headers if behind a proxy or CDN.

### False positive analysis

- Legitimate, scheduled vulnerability assessments by internal teams (e.g., Nessus, Nikto, or OpenVAS) can generate large volumes of requests with those user-agent strings across many paths.
- Developer or QA testing using discovery/fuzzing or intercept-proxy tools (Dirsearch, Gobuster, Ffuf, Burp, or OWASP ZAP) may unintentionally target production hosts, producing a short-lived spike with diverse URLs.

### Response and remediation

- Immediately contain by blocking or rate-limiting the originating IPs at the WAF/CDN and edge firewall, and add temporary rules to drop or challenge requests that advertise tool user agents such as "nikto", "sqlmap", "dirsearch", "wpscan", "gobuster", or "burp".
- If traffic is proxied (CDN/reverse proxy), identify the true client via forwarded headers and extend blocks at both layers, enabling bot management or JS challenges on swept paths like /admin, /.git, /.env, /backup, and common discovery endpoints.
- Eradicate exposure by removing or restricting access to sensitive files and directories uncovered by the scans, rotating any credentials or API keys found, invalidating active sessions, and disabling public access to administrative panels until hardened.
- Recover by verifying no unauthorized changes or data exfiltration occurred, tuning per-IP and per-path rate limits to prevent path-sweeps while preserving legitimate traffic, and reintroducing normal rules only after fixes are deployed and stability is confirmed.
- Escalate to incident response if sensitive files are successfully downloaded (HTTP 200/206 on /.git, /.env, or backups), any login or account creation succeeds, multiple hosts or environments are targeted, or activity persists after blocking via UA spoofing or rapid IP rotation.
- Harden long term by enforcing WAF signatures for known scanner UAs and path patterns, denying directory listing and direct access to /.git, /.env, /backup and similar artifacts, requiring MFA/VPN for /admin and management APIs, and deploying auto-ban controls like fail2ban or mod_security.

