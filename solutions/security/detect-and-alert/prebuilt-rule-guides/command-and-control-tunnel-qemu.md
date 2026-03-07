---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Traffic Tunneling using QEMU" prebuilt detection rule.'
---

# Potential Traffic Tunneling using QEMU

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Traffic Tunneling using QEMU

QEMU is a legitimate virtualization and emulation platform used for system testing and development. However, its advanced networking features can be abused to tunnel network traffic, forward ports, and create covert communication channels between systems. The detection rule identifies suspicious QEMU executions using networking-related arguments that are commonly associated with traffic forwarding and tunneling behavior.

### Possible investigation steps

- Review the process command line for the presence of networking arguments such as `-netdev`, `hostfwd=`, `connect=`, `restrict=off`, and `-nographic`.
- Confirm whether QEMU is legitimately installed and expected to run on the affected system.
- Check the parent process to determine how QEMU was launched and whether the execution chain appears suspicious.
- Investigate the user account and host context to assess whether virtualization activity is normal for that environment.
- Analyze related network activity for signs of traffic forwarding, tunneling, or unauthorized external connections.
- Correlate the event with other telemetry (process creation, persistence mechanisms, or VM artifacts) for additional context.

### False positive analysis

- Legitimate developer or research environments using QEMU for virtualization and testing may trigger this rule.
- Approved lab systems, malware analysis sandboxes, or CI/CD pipelines may use similar networking configurations.
- Internal training or testing environments may generate similar activity.

### Response and remediation

- Isolate the affected system and terminate unauthorized QEMU processes.
- Investigate for signs of lateral movement or command-and-control activity.
- Remove unauthorized VM images, configurations, and persistence mechanisms.
- Rotate credentials and assess scope of impact if tunneling activity is confirmed.
- Escalate to the SOC or incident response team for further investigation.
