---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Default Cobalt Strike Team Server Certificate" prebuilt detection rule.'
---

# Default Cobalt Strike Team Server Certificate

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Default Cobalt Strike Team Server Certificate

Cobalt Strike is a tool used for simulating advanced cyber threats, often employed by security teams to test defenses. However, adversaries can exploit its default server certificate to establish covert command and control channels. The detection rule identifies this misuse by monitoring network traffic for specific cryptographic hashes associated with the default certificate, flagging potential unauthorized Cobalt Strike activity.

### Possible investigation steps

- Review the network traffic logs to identify any connections associated with the specific cryptographic hashes: MD5 (950098276A495286EB2A2556FBAB6D83), SHA1 (6ECE5ECE4192683D2D84E25B0BA7E04F9CB7EB7C), or SHA256 (87F2085C32B6A2CC709B365F55873E207A9CAA10BFFECF2FD16D3CF9D94D390C).
- Identify the source and destination IP addresses involved in the flagged network traffic to determine the potential origin and target of the Cobalt Strike activity.
- Correlate the identified IP addresses with known assets in the network to assess if any internal systems are potentially compromised.
- Check for any other suspicious or anomalous network activities around the same time as the alert to identify potential lateral movement or additional command and control channels.
- Investigate any associated processes or user accounts on the involved systems to determine if there are signs of compromise or unauthorized access.
- Review historical data to see if there have been previous alerts or similar activities involving the same cryptographic hashes or IP addresses, which might indicate a persistent threat.

### False positive analysis

- Legitimate security testing activities by internal teams using Cobalt Strike may trigger the rule. Coordinate with security teams to whitelist known testing IP addresses or certificate hashes.
- Some commercial penetration testing services may use Cobalt Strike with default certificates. Verify the legitimacy of such services and exclude their traffic from detection by adding their certificate hashes to an exception list.
- Network appliances or security tools that simulate adversary behavior for training purposes might use similar certificates. Identify these tools and configure exceptions for their specific network traffic patterns.
- In environments where Cobalt Strike is used for authorized red team exercises, ensure that the default certificate is replaced with a custom one to avoid false positives.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further communication with the potential Cobalt Strike server.
- Conduct a thorough forensic analysis of the isolated system to identify any malicious payloads or additional indicators of compromise.
- Revoke any compromised credentials and enforce a password reset for affected accounts to prevent unauthorized access.
- Update and patch all systems to the latest security standards to mitigate vulnerabilities that could be exploited by similar threats.
- Implement network segmentation to limit the lateral movement of threats within the network.
- Enhance monitoring and logging to capture detailed network traffic and endpoint activity, focusing on the identified cryptographic hashes.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and coordination with external threat intelligence sources if necessary.

## Threat intel

While Cobalt Strike is intended to be used for penetration tests and IR training, it is frequently used by actual threat actors (TA) such as APT19, APT29, APT32, APT41, FIN6, DarkHydrus, CopyKittens, Cobalt Group, Leviathan, and many other unnamed criminal TAs. This rule uses high-confidence atomic indicators, so alerts should be investigated rapidly.
