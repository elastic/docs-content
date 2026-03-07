---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "BPF filter applied using TC" prebuilt detection rule.'
---

# BPF filter applied using TC

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating BPF filter applied using TC

BPF (Berkeley Packet Filter) is a powerful tool for network traffic analysis and control, often used with the `tc` command to manage traffic on Linux systems. Adversaries may exploit this by setting BPF filters to manipulate or monitor network traffic covertly. The detection rule identifies suspicious use of `tc` to apply BPF filters, flagging potential misuse by checking for specific command patterns and excluding legitimate processes.

### Possible investigation steps

- Review the process execution details to confirm the presence of the `/usr/sbin/tc` command with arguments "filter", "add", and "bpf" to ensure the alert is not a false positive.
- Investigate the parent process of the `tc` command to determine if it is a known legitimate process or if it appears suspicious, especially since the rule excludes `/usr/sbin/libvirtd`.
- Check the user account associated with the process execution to assess if it is a privileged account and whether the activity aligns with the user's typical behavior.
- Analyze network traffic logs around the time of the alert to identify any unusual patterns or connections that may indicate malicious activity.
- Correlate this event with other security alerts or logs to identify if this is part of a broader attack pattern or campaign, such as the use of the TripleCross threat.
- Review system logs for any other suspicious activities or anomalies that occurred before or after the alert to gather additional context.

### False positive analysis

- Legitimate use of tc by virtualization software like libvirtd can trigger the rule. To handle this, exclude processes where the parent executable is /usr/sbin/libvirtd, as indicated in the rule.
- Network administrators may use tc with BPF filters for legitimate traffic management tasks. Identify and document these use cases, then create exceptions for specific command patterns or user accounts involved in these activities.
- Automated scripts or system management tools that configure network interfaces might use tc with BPF filters. Review these scripts and tools, and if they are verified as safe, exclude their process signatures from triggering the rule.
- Regular audits of network configurations can help distinguish between legitimate and suspicious use of BPF filters. Implement a process to regularly review and update exceptions based on these audits to minimize false positives.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further manipulation or monitoring of network traffic by the adversary.
- Terminate the suspicious `tc` process to stop any ongoing malicious activity related to the BPF filter application.
- Conduct a thorough review of network traffic logs to identify any unauthorized data exfiltration or communication with known malicious IP addresses.
- Restore the affected system from a known good backup to ensure that no malicious configurations or software persist.
- Implement network segmentation to limit the potential impact of similar threats in the future, ensuring critical systems are isolated from less secure areas.
- Escalate the incident to the security operations center (SOC) for further investigation and to determine if additional systems are compromised.
- Update and enhance endpoint detection and response (EDR) solutions to improve monitoring and alerting for similar suspicious activities involving `tc` and BPF filters.
