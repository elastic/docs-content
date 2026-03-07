---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Hping Process Activity" prebuilt detection rule.
---

# Hping Process Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Hping Process Activity

Hping is a versatile command-line tool used for crafting and analyzing network packets, often employed in network security testing. Adversaries may exploit Hping to perform reconnaissance, such as scanning networks or probing firewalls, to gather system information. The detection rule identifies Hping's execution on Linux systems by monitoring specific process start events, helping to flag potential misuse indicative of discovery tactics.

### Possible investigation steps

- Review the process start event details to confirm the execution of Hping, focusing on the process.name field to ensure it matches "hping", "hping2", or "hping3".
- Identify the user account associated with the Hping process by examining the user context in the event data to determine if the activity aligns with expected behavior for that user.
- Analyze the command line arguments used with the Hping process to understand the intent of the execution, such as specific network targets or options that indicate scanning or probing activities.
- Check the timing and frequency of the Hping process execution to assess whether it aligns with routine network testing schedules or if it appears anomalous.
- Investigate the source and destination IP addresses involved in the Hping activity to identify potential targets and assess whether they are internal or external to the organization.
- Correlate the Hping activity with other security events or alerts from the same host or network segment to identify any related suspicious activities or patterns.
- Consult with the system owner or network security team to verify if the Hping activity was authorized as part of legitimate security testing or if it requires further investigation.

### False positive analysis

- Routine network testing by IT teams may trigger the rule when using Hping for legitimate purposes. To manage this, create exceptions for known IP addresses or user accounts involved in regular network audits.
- Automated scripts or cron jobs that utilize Hping for monitoring network performance can lead to false positives. Identify these scripts and exclude their execution paths or associated user accounts from the detection rule.
- Security training exercises or penetration testing activities might involve Hping usage. Coordinate with security teams to whitelist these activities by specifying time windows or specific user roles.
- Development or testing environments where Hping is used for application testing can cause alerts. Exclude these environments by filtering based on hostnames or network segments associated with non-production systems.

### Response and remediation

- Immediately isolate the affected Linux host from the network to prevent further reconnaissance or potential lateral movement by the adversary.
- Terminate any active Hping processes on the affected host to stop ongoing packet crafting or network probing activities.
- Conduct a thorough review of network logs and firewall configurations to identify any unauthorized access or anomalies that may have been exploited using Hping.
- Perform a comprehensive scan of the affected system for additional indicators of compromise, such as unauthorized user accounts or unexpected changes to system files.
- Reset credentials and review access permissions for accounts on the affected host to ensure no unauthorized access persists.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Update detection and monitoring systems to enhance visibility and alerting for similar reconnaissance activities, ensuring rapid response to future threats.
