---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Openssl Client or Server Activity" prebuilt detection rule.
---

# Openssl Client or Server Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Openssl Client or Server Activity

OpenSSL is a widely-used toolkit for implementing secure communication via SSL/TLS protocols. In Linux environments, it can function as a client or server to encrypt data transmissions. Adversaries may exploit OpenSSL to establish encrypted channels for data exfiltration or command and control. The detection rule identifies suspicious OpenSSL usage by monitoring process execution patterns, specifically targeting atypical client-server interactions, while excluding known benign processes.

### Possible investigation steps

- Review the process execution details to confirm the presence of the "openssl" process with arguments indicating client or server activity, such as "s_client" with "-connect" or "s_server" with "-port".
- Check the parent process of the "openssl" execution to determine if it is a known benign process or if it is potentially suspicious, especially if it is not in the excluded list (e.g., "/pro/xymon/client/ext/awsXymonCheck.sh", "/opt/antidot-svc/nrpe/plugins/check_cert").
- Investigate the network connections established by the "openssl" process to identify the remote server's IP address and port, and assess whether these are known or potentially malicious.
- Analyze the timing and frequency of the "openssl" executions to determine if they align with normal operational patterns or if they suggest unusual or unauthorized activity.
- Correlate the "openssl" activity with other security events or logs to identify any related suspicious behavior, such as data exfiltration attempts or command and control communications.

### False positive analysis

- Known benign processes such as "/pro/xymon/client/ext/awsXymonCheck.sh" and "/opt/antidot-svc/nrpe/plugins/check_cert" are already excluded to reduce false positives. Ensure these paths are accurate and up-to-date in your environment.
- Regularly review and update the list of excluded parent processes to include any additional internal scripts or monitoring tools that frequently use OpenSSL for legitimate purposes.
- Monitor for any internal applications or services that may use OpenSSL in a similar manner and consider adding them to the exclusion list if they are verified as non-threatening.
- Implement logging and alerting to track the frequency and context of OpenSSL usage, which can help identify patterns that are consistently benign and warrant exclusion.
- Engage with system administrators to understand routine OpenSSL usage patterns in your environment, which can inform further refinement of the detection rule to minimize false positives.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further data exfiltration or command and control activities.
- Terminate the suspicious OpenSSL process identified by the alert to halt any ongoing unauthorized encrypted communications.
- Conduct a forensic analysis of the affected system to identify any additional indicators of compromise, such as unusual network connections or unauthorized file access.
- Review and update firewall rules to block unauthorized outbound connections from the affected system, focusing on the ports and IP addresses involved in the suspicious activity.
- Reset credentials and review access permissions for accounts on the affected system to prevent unauthorized access.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if the threat has spread to other systems.
- Implement enhanced monitoring and logging for OpenSSL usage across the network to detect similar activities in the future, ensuring that alerts are promptly reviewed and acted upon.
