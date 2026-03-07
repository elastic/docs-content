---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Perl Outbound Network Connection" prebuilt detection rule.'
---

# Perl Outbound Network Connection

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Perl Outbound Network Connection

This rule detects Perl starting on macOS and then initiating an outbound connection to a public (non-private) IP, a pattern that stands out because Perl rarely performs direct network reach-outs in normal macOS workflows. Attackers often abuse Perl as a built-in “living off the land” runtime to beacon to external command-and-control over HTTP/S or to fetch and execute a second-stage payload from an internet host.

### Possible investigation steps

- Review the full command line, parent/child process tree, execution context (user, TTY, working directory), and referenced script/module paths to determine whether the run was expected or suspicious.  
- Pivot on the external destination (IP, port, and any resolved domain from DNS telemetry) to assess reputation, hosting characteristics, and whether other endpoints have recently contacted the same infrastructure.  
- Examine connection characteristics (protocol, TLS SNI/certificate, HTTP headers/user-agent, data volume, and timing) to identify staged downloads or beacon-like periodicity.  
- Correlate nearby file activity for newly created or modified scripts, temp artifacts, or downloaded payloads, and validate them via hashes, signatures, and known-good baselines.  
- Check for follow-on behavior consistent with persistence or lateral movement, such as new launchd/cron items, suspicious login items, or additional interpreters and shells spawned from the same lineage.

### False positive analysis

- A legitimate Perl script run by an administrator or scheduled maintenance task (e.g., log rotation, health checks, or API polling) may connect to a public service endpoint over HTTP/S, matching the Perl exec followed by a non-private destination IP pattern.  
- A developer workflow that uses Perl one-liners or project scripts to fetch dependencies, query internet-hosted resources, or validate external URLs can generate outbound connections to public IPs that appear unusual on endpoints without an established baseline for Perl network use.

### Response and remediation

- Isolate the affected macOS host from the network (or block the specific destination IP/port at the egress firewall) and terminate the suspicious `perl` process to stop any active command-and-control or payload download.  
- Collect and preserve the Perl command line, referenced script paths, current working directory, any newly written files (especially in `/tmp`, `/var/tmp`, and the user’s `~/Library`), and the full process tree for forensic review before cleanup.  
- Remove or quarantine the identified Perl script and any downloaded payloads, then eradicate persistence by deleting malicious `launchd` agents/daemons, cron entries, and suspicious Login Items created around the time of the outbound connection.  
- Reimage or restore the endpoint from a known-good source if integrity cannot be confidently validated, rotate credentials used on the device, and invalidate active sessions/tokens that may have been exposed to the Perl process.  
- Escalate to IR/forensics immediately if the destination infrastructure is contacted by multiple hosts, the Perl process runs under a privileged context, or you observe repeated beacon-like connections or evidence of persistence beyond a single script execution.  
- Harden by restricting interpreter execution (Perl, Python, Ruby) via endpoint controls, enforcing outbound allowlisting/proxying for user endpoints, and adding detections for Perl launching network tools or writing executable content into user-writable directories.
