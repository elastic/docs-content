---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "DNS Request for IP Lookup Service via Unsigned Binary" prebuilt detection rule.'
---

# DNS Request for IP Lookup Service via Unsigned Binary

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating DNS Request for IP Lookup Service via Unsigned Binary

This detects an unsigned or untrusted process on macOS performing DNS lookups for common “what is my public IP” and geolocation services, a frequent reconnaissance step before external communications. It matters because malware uses the host’s external IP and region to choose C2 infrastructure, gate payload delivery, or evade sandboxing. A typical pattern is a dropped, unsigned Mach-O or script resolving api.ipify.org or ipinfo.io immediately after execution, then initiating outbound beacons.

### Possible investigation steps

- Identify the initiating process and parent chain, then validate whether the binary is expected for the host/user and whether it is actually unsigned versus a transient signature collection issue.  
- Review the same process’s near-term network activity for follow-on HTTP(S) requests to the resolved service and any subsequent connections to rare/new domains or IPs that could indicate C2 staging.  
- Pivot from the resolved domain to other endpoints to determine prevalence and timing, then prioritize isolated single-host hits with recent first-seen binaries.  
- Examine how the binary was introduced by correlating with recent downloads, archive mounts, installer executions, or quarantine/Gatekeeper events around the process start time.  
- Acquire and analyze the binary (hash reputation, static strings, entitlements, persistence mechanisms, and launch agents/daemons) to confirm intent and scope of compromise.

### False positive analysis

- A developer-built or locally compiled macOS utility/script (run from a user directory) performs a “what is my public IP” DNS lookup for telemetry, diagnostics, or environment detection, and is flagged because it lacks a trusted code signature.  
- An unsigned helper binary dropped by a legitimate installer/updater workflow briefly runs during setup to validate external connectivity or geolocation by resolving an IP-lookup domain, and is detected before the binary is signed or placed in its final trusted location.

### Response and remediation

- Isolate the affected macOS host from the network if the unsigned process continues to resolve IP-lookup domains (e.g., api.ipify.org, ipinfo.io) or initiates new outbound connections immediately after the lookup.  
- Quarantine the unsigned executable and any associated scripts from disk (preserving path, hashes, and a copy for analysis) and remove its persistence artifacts such as newly created LaunchAgents/LaunchDaemons, login items, or cron entries tied to the same binary.  
- Block the observed IP-lookup domains used by the unsigned process at DNS/web egress and add temporary deny rules for any follow-on suspicious destinations the process contacted after resolution.  
- Reset compromised credentials and invalidate active sessions for the logged-in user if the process originated from user-writable locations (Downloads, Desktop, /tmp) or if additional discovery/collection behavior is found on the host.  
- Reimage or restore the endpoint from a known-good state when persistence or tampering is confirmed, then verify Gatekeeper/XProtect status, re-enable security tooling, and monitor for recurrence of the same binary hash or domain pattern.  
- Escalate to the incident response team if the unsigned binary is newly seen in the environment, appears on multiple hosts, or is followed by connections to rare domains/IPs indicative of staging or command-and-control.
