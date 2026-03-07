---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Statistical Model Detected C2 Beaconing Activity" prebuilt detection rule.
---

# Statistical Model Detected C2 Beaconing Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Statistical Model Detected C2 Beaconing Activity

Statistical models analyze network traffic patterns to identify anomalies indicative of C2 beaconing, a tactic used by attackers to maintain covert communication with compromised systems. Adversaries exploit this by sending periodic signals to C2 servers, often mimicking legitimate traffic. The detection rule leverages statistical analysis to flag unusual beaconing while excluding known benign processes, thus highlighting potential threats without overwhelming analysts with false positives.

### Possible investigation steps

- Review the network traffic logs to identify the source and destination IP addresses associated with the beaconing activity flagged by the statistical model.
- Cross-reference the identified IP addresses with threat intelligence databases to determine if they are associated with known malicious C2 servers.
- Analyze the frequency and pattern of the beaconing signals to assess whether they mimic legitimate traffic or exhibit characteristics typical of C2 communication.
- Investigate the processes running on the source system to identify any suspicious or unauthorized applications that may be responsible for the beaconing activity.
- Check for any recent changes or anomalies in the system's configuration or installed software that could indicate a compromise.
- Examine the historical network activity of the source system to identify any other unusual patterns or connections that may suggest a broader compromise.

### False positive analysis

- The rule may flag legitimate processes that exhibit periodic network communication patterns similar to C2 beaconing. Processes like "metricbeat.exe" and "packetbeat.exe" are known to generate regular network traffic for monitoring purposes.
- Users can manage these false positives by adding exceptions for these known benign processes in the detection rule, ensuring they are not flagged as threats.
- Regularly review and update the list of excluded processes to include any new legitimate applications that may mimic beaconing behavior, reducing unnecessary alerts.
- Consider implementing a whitelist approach for processes that are verified as non-threatening, allowing the statistical model to focus on truly anomalous activities.
- Engage with network and security teams to understand the normal traffic patterns of your environment, which can help in refining the detection rule and minimizing false positives.

### Response and remediation

- Isolate the affected system from the network to prevent further communication with the C2 server and limit potential data exfiltration.
- Terminate any suspicious processes identified by the alert that are not part of the known benign list, ensuring that any malicious activity is halted.
- Conduct a thorough scan of the isolated system using updated antivirus and anti-malware tools to identify and remove any malicious software or files.
- Review and analyze network logs to identify any other systems that may have communicated with the same C2 server, and apply similar containment measures to those systems.
- Restore the affected system from a known good backup to ensure that any persistent threats are removed, and verify the integrity of the restored system.
- Implement network segmentation to limit the ability of compromised systems to communicate with critical infrastructure and sensitive data.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional measures are needed to prevent recurrence.
