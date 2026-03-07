---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Kerberos SPN Spoofing via Suspicious DNS Query" prebuilt detection rule.
---

# Potential Kerberos SPN Spoofing via Suspicious DNS Query

## Triage and analysis

### Investigating Potential Kerberos SPN Spoofing via Suspicious DNS Query

> **Note**:
> This investigation guide uses the [Investigate Markdown Plugin](https://www.elastic.co/guide/en/security/current/interactive-investigation-guides.html) introduced in Elastic Stack version 8.8.0. Older Elastic Stack versions will display unrendered Markdown in this guide.

### Possible investigation steps

- Identify the system that issued the DNS query for the suspicious hostname. Determine whether it is a server or an end user device. This technique is typically only relevant against server systems, but queries originating from workstations may indicate compromise or misuse.
- Identify attacker-controlled system by getting the IP addresses (`dns.resolved_ip`) that this DNS query resolved to by looking for the related `lookup_result` events.
    - $investigate_0
- If this alert was triggered on a domain controller, escalate the investigation to involve the incident response team to determine the full scope of the breach as soon as possible.

### False positive analysis

- This activity is unlikely to happen legitimately.

### Response and remediation

- Review and remove malicious DNS records containing the embedded CREDENTIAL_TARGET_INFORMATION Base64 payload (UWhRCA...BAAAA). Ensure that no additional coercion records exist in the same DNS zone.
- Isolate involved systems if signs of compromise or lateral movement are detected, especially if the record was successfully resolved and used for coercion.
- Monitor network traffic for signs of Man-in-the-Middle activity, focusing on unusual DNS queries or redirections.
- Escalate the incident to the security operations center (SOC) for further investigation and to assess the potential impact on other systems.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

