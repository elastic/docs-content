---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Script Interpreter Connection to Non-Standard Port" prebuilt detection rule.
---

# Script Interpreter Connection to Non-Standard Port

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Script Interpreter Connection to Non-Standard Port

This rule detects a macOS script interpreter launch (Python, Node, or Ruby) quickly followed by an outbound connection to a raw IP address over a non-standard port. It matters because implants and initial access scripts often bypass domain-based controls and blend into developer tooling while using unusual ports for C2. A common pattern is a one-liner Python or Node stager that beacons directly to an external IP on a high-but-not-ephemeral port (e.g., 4444/8081) to fetch or execute a second stage.

### Possible investigation steps

- Review the interpreter’s full command line, parent/ancestry, execution path, and working directory to determine whether this was an interactive developer action, a scheduled task, or a hidden launcher.  
- Identify the script/module being executed (including any temp paths or inline code), collect it for analysis, and check for obfuscation, encoded payloads, or remote-fetch logic.  
- Pivot on the destination IP and port to assess reputation, hosting/ASN, geolocation, and whether the host has contacted the same endpoint before or other endpoints on the same unusual port.  
- Correlate around the event time for follow-on activity such as file downloads, new processes, credential access attempts, persistence creation (LaunchAgents/LaunchDaemons), or security tool tampering.  
- Validate the initiating user context and host posture (new user/login, recent software installs, unsigned binaries, quarantine attributes, or MDM exceptions) to decide on containment and scoping to peer endpoints.

### False positive analysis

- A developer runs a short Python/Node/Ruby script with a single argument to test a service by connecting directly to a public IP on an application-specific port (e.g., staging APIs, custom web services, or test listeners), resulting in a raw-IP outbound connection outside common ports.  
- An administrative or diagnostic script (e.g., a quick health check or connectivity probe) executed via an interpreter uses an IP literal for reliability and targets a non-standard port for internal tooling exposed to the internet, producing the same interpreter-to-raw-IP network pattern without malicious intent.

### Response and remediation

- Isolate the affected macOS host from the network (or block only the observed destination IP:port at the firewall) and terminate the Python/Node/Ruby process that initiated the outbound raw-IP connection.  
- Acquire volatile and on-disk artifacts including the interpreter command line, referenced script file, current working directory contents, recent downloads, and any temporary directories used at execution time, then submit the script and any fetched payloads for malware analysis.  
- Hunt for persistence and re-infection by checking for new or modified LaunchAgents/LaunchDaemons, cron entries, login items, and recently added executable files, and remove/rollback any items tied to the interpreter or the suspicious IP:port.  
- Reset potentially impacted credentials and revoke active tokens for the initiating user if the script accessed keychain material, SSH keys, browser sessions, or cloud CLIs near the event time.  
- Restore the endpoint from a known-good snapshot or reimage if the script/payload cannot be confidently eradicated, then validate recovery by confirming no further connections to the same IP:port and no recurrence of the interpreter one-liner.  
- Escalate to IR leadership and initiate broader scoping if multiple hosts contact the same external IP:port, the destination is confirmed malicious, or persistence/credential theft is detected, and harden by restricting script interpreter execution via MDM, enforcing full disk access controls, and adding egress allow-listing for non-standard ports.

