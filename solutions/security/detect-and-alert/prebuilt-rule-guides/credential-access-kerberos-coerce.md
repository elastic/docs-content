---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Kerberos Coercion via DNS-Based SPN Spoofing" prebuilt detection rule.'
---

# Potential Kerberos Coercion via DNS-Based SPN Spoofing

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Kerberos Coercion via DNS-Based SPN Spoofing

### Possible investigation steps

- Review the event logs on the affected Windows host to confirm the presence of event code 5137, which indicates a directory service object modification.
- Inspect the ObjectDN field to identify the full distinguished name of the created DNS record. Look for entries containing Base64-encoded segments matching UWhRCA...BAAAA, which are indicative of an embedded CREDENTIAL_TARGET_INFORMATION payload used in SPN spoofing.
- Validate the associated user or computer account responsible for the DNS record creation. Investigate whether the account has legitimate administrative access to modify DNS zones or whether it may have been compromised.
- Correlate with DNS query logs and network telemetry to determine if the suspicious DNS hostname was later queried or resolved by other hosts on the network. A match suggests the attacker moved forward with the coercion attempt.
- Assess the permissions and access controls on the DNS zones to ensure they are appropriately configured and restrict unnecessary modifications by authenticated users.

### False positive analysis

- This activity is unlikely to happen legitimately.

### Response and remediation

- Review and remove the malicious DNS record containing the embedded CREDENTIAL_TARGET_INFORMATION Base64 payload (UWhRCA...BAAAA). Ensure that no additional coercion records exist in the same DNS zone.
- Identify the source of the DNS modification by correlating the event with user context and host activity. Investigate whether the account used was compromised or misused.
- Audit Kerberos ticket activity following the DNS record creation. Look for suspicious service ticket requests (Event ID 4769) or authentication attempts that could indicate a relay or privilege escalation attempt.
- Temporarily isolate involved systems if signs of compromise or lateral movement are detected, especially if the record was successfully resolved and used for coercion.
- Monitor network traffic for signs of Man-in-the-Middle activity, focusing on unusual DNS queries or redirections.
- Escalate the incident to the security operations center (SOC) for further investigation and to assess the potential impact on other systems.
