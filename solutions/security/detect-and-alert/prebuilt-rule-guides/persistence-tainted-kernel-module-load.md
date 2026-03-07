---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Tainted Kernel Module Load" prebuilt detection rule.'
---

# Tainted Kernel Module Load

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Tainted Kernel Module Load

Kernel modules extend the functionality of the Linux kernel, allowing dynamic loading of code. While beneficial, they can be exploited by adversaries to introduce malicious code, bypassing security measures. Attackers may load unsigned or improperly signed modules, leading to a "tainted" kernel state. The detection rule identifies such events by monitoring syslog for specific error messages, signaling potential unauthorized module loads, thus aiding in early threat detection and system integrity maintenance.

### Possible investigation steps

- Review the syslog entries around the time of the alert to gather additional context and identify any other suspicious activities or related events.
- Investigate the specific kernel module mentioned in the syslog message to determine its origin, legitimacy, and whether it is expected on the system.
- Check the system for any recent changes or installations that could have introduced the unsigned or improperly signed module, including software updates or new applications.
- Analyze the system for signs of compromise, such as unexpected network connections, unusual process activity, or unauthorized user accounts, which may indicate a broader security incident.
- Consult with system administrators or relevant personnel to verify if the module load was authorized or part of a legitimate operation, and document any findings or justifications provided.

### False positive analysis

- Custom kernel modules: Organizations often use custom or proprietary kernel modules that may not be signed. These can trigger false positives. To manage this, maintain a list of known, trusted custom modules and create exceptions for them in the monitoring system.
- Outdated or unsupported hardware drivers: Some older hardware drivers may not have signed modules, leading to false positives. Regularly update drivers and, if necessary, exclude specific drivers that are known to be safe but unsigned.
- Development and testing environments: In environments where kernel module development occurs, unsigned modules may be loaded frequently. Implement separate monitoring rules or exceptions for these environments to avoid unnecessary alerts.
- Vendor-provided modules: Certain vendors may provide modules that are not signed. Verify the legitimacy of these modules with the vendor and consider excluding them if they are confirmed to be safe.
- Temporary testing modules: During troubleshooting or testing, temporary modules might be loaded without proper signing. Ensure these are removed after testing and consider temporary exceptions during the testing phase.

### Response and remediation

- Immediately isolate the affected system from the network to prevent potential lateral movement by the attacker.
- Verify the integrity of the kernel and loaded modules by comparing them against known good versions or using a trusted baseline.
- Unload the suspicious kernel module if possible, and replace it with a verified, signed version to restore system integrity.
- Conduct a thorough forensic analysis of the affected system to identify any additional signs of compromise or persistence mechanisms.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if other systems are affected.
- Implement enhanced monitoring and logging for kernel module loads and other critical system activities to detect similar threats in the future.
- Review and update system and network access controls to ensure only authorized personnel can load kernel modules, reducing the risk of unauthorized changes.
