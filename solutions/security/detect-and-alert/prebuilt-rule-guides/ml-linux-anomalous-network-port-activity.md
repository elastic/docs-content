---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Linux Network Port Activity" prebuilt detection rule.
---

# Unusual Linux Network Port Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Linux Network Port Activity

In Linux environments, network ports facilitate communication between applications and services. Adversaries may exploit rarely used ports for covert command-and-control, persistence, or data exfiltration, bypassing standard monitoring. The 'Unusual Linux Network Port Activity' detection rule leverages machine learning to identify anomalies in port usage, flagging potential unauthorized access or threat actor activity by highlighting deviations from typical network behavior.

### Possible investigation steps

- Review the alert details to identify the specific unusual destination port and the associated source and destination IP addresses.
- Check historical network logs to determine if the identified port has been used previously and assess the frequency and context of its usage.
- Investigate the source IP address to determine if it is associated with known internal systems or if it is an external or unexpected source.
- Analyze the destination IP address to verify if it is a legitimate endpoint within the network or an external entity that requires further scrutiny.
- Correlate the unusual port activity with any recent changes or updates in the network environment that might explain the anomaly.
- Examine any related process or application logs on the involved Linux systems to identify the application or service responsible for the network activity.
- Consider reaching out to the system owner or administrator for additional context or to verify if the activity is expected or authorized.

### False positive analysis

- Routine administrative tasks may trigger alerts when using non-standard ports for legitimate purposes. Users can create exceptions for known administrative tools and scripts that consistently use these ports.
- Internal applications or services might use uncommon ports for inter-service communication. Identify these applications and whitelist their port usage to prevent unnecessary alerts.
- Security tools and monitoring solutions sometimes scan or probe network ports as part of their operations. Recognize these tools and exclude their activities from the rule to avoid false positives.
- Development and testing environments often experiment with various port configurations. Establish a separate monitoring profile for these environments to reduce noise in production alerts.
- Custom or legacy applications may operate on non-standard ports due to historical configurations. Document these applications and adjust the rule to accommodate their expected behavior.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Conduct a thorough review of the system's network connections and terminate any suspicious or unauthorized connections.
- Analyze system logs to identify any malicious processes or scripts that may have been executed, and remove or quarantine any identified threats.
- Change all credentials associated with the affected system, especially if there is any indication of credential compromise.
- Restore the system from a known good backup if any unauthorized changes or malware are detected.
- Implement network segmentation to limit the exposure of critical systems to potential threats and reduce the risk of lateral movement.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
