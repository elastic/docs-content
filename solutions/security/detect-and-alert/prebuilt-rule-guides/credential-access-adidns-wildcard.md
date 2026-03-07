---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential ADIDNS Poisoning via Wildcard Record Creation" prebuilt detection rule.'
---

# Potential ADIDNS Poisoning via Wildcard Record Creation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential ADIDNS Poisoning via Wildcard Record Creation

Active Directory Integrated DNS (ADIDNS) is crucial for maintaining domain consistency by storing DNS zones as AD objects. However, its default permissions allow authenticated users to create DNS records, which adversaries can exploit by adding wildcard records. This enables them to redirect traffic and perform Man-in-the-Middle attacks. The detection rule identifies such abuse by monitoring specific directory service changes indicative of wildcard record creation.

### Possible investigation steps

- Review the event logs on the affected Windows host to confirm the presence of event code 5137, which indicates a directory service object modification.
- Examine the ObjectDN field in the event data to identify the specific DNS zone where the wildcard record was created, ensuring it starts with "DC=*," to confirm the wildcard nature.
- Check the user account associated with the event to determine if it is a legitimate account or potentially compromised, focusing on any unusual or unauthorized activity.
- Investigate recent changes in the DNS zone to identify any other suspicious modifications or patterns that could indicate further malicious activity.
- Correlate the event with network traffic logs to detect any unusual or redirected traffic patterns that could suggest a Man-in-the-Middle attack.
- Assess the permissions and access controls on the DNS zones to ensure they are appropriately configured and restrict unnecessary modifications by authenticated users.

### False positive analysis

- Routine administrative changes to DNS records by IT staff can trigger alerts. To manage this, create exceptions for known administrative accounts or specific ObjectDN patterns that correspond to legitimate changes.
- Automated systems or scripts that update DNS records as part of regular maintenance may cause false positives. Identify these systems and exclude their activity from triggering alerts by filtering based on their unique identifiers or event sources.
- Software installations or updates that modify DNS settings might be flagged. Monitor and document these activities, and consider excluding them if they are part of a recognized and secure process.
- Changes made by trusted third-party services that integrate with ADIDNS could be misinterpreted as threats. Verify these services and whitelist their actions to prevent unnecessary alerts.
- Temporary testing environments that mimic production settings might generate alerts. Ensure these environments are clearly documented and excluded from monitoring if they are known to perform non-threatening wildcard record creations.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further exploitation or data exfiltration.
- Revoke any potentially compromised credentials associated with the affected system or user accounts involved in the alert.
- Conduct a thorough review of DNS records in the affected zone to identify and remove any unauthorized wildcard entries.
- Implement stricter access controls on DNS record creation, limiting permissions to only necessary administrative accounts.
- Monitor network traffic for signs of Man-in-the-Middle activity, focusing on unusual DNS queries or redirections.
- Escalate the incident to the security operations center (SOC) for further investigation and to assess the potential impact on other systems.
- Update detection mechanisms to include additional indicators of compromise related to ADIDNS abuse, enhancing future threat detection capabilities.
