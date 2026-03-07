---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual City for an Azure Activity Logs Event" prebuilt detection rule.
---

# Unusual City for an Azure Activity Logs Event

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual City for an Azure Activity Logs Event

This rule highlights Azure Activity Logs activity executed from a city atypical for the action, indicating use of valid accounts from a different geography. A common pattern is a threat actor using stolen user or service principal credentials to add privileged role assignments and rapidly spin up compute to stage data exfiltration or mining from overseas. Location–action mismatch surfaces stealthy account abuse before persistence and broader impact.

### Possible investigation steps

- Identify the principal behind the operation and validate legitimate presence in the region by contacting the user/owner and reviewing travel or business justification.
- Enrich the source IP with ASN, hosting/cloud provider, VPN/Tor indicators, reverse DNS, and threat intel to determine whether it originates from anonymizing or compute infrastructure.
- Correlate Entra ID sign-in logs for the principal around the timestamp to check impossible travel, MFA usage or bypass, device compliance state, and atypical user-agent strings.
- Review adjacent Azure Resource Manager activity by the same principal for privileged changes such as role assignments, policy updates, access key or secret actions, and rapid compute/network provisioning.
- Determine whether the actor is a user or service principal, and if a service principal, inspect recent secret/certificate changes, unexpected consent or role grants, and potential credential exposure in CI/CD or repositories.

### False positive analysis

- A legitimate admin traveling or connecting via a VPN or newly configured egress/NAT gateway can geolocate to an unexpected city while performing routine Azure Activity Logs actions.
- Service principal or managed identity automation executing from a different Azure region due to multi-region deployment or failover can egress from a city unusual for the action yet still be authorized.

### Response and remediation

- Immediately revoke active sessions and refresh tokens for the implicated user or service principal, disable the account or application, and block the observed source IP/CIDR at Azure Firewall and NSGs to contain activity.
- Reset the user's password and force MFA re-registration, or for a service principal rotate all client secrets/certificates and remove any recent admin consent grants to eradicate credential reuse.
- Revert changes executed from the unusual city by removing newly added role assignments, deleting unexpected VMs/VNets or policy updates, and rotating Storage account keys and Key Vault secrets if they were accessed.
- After containment, verify business justification (travel or new egress) and restore any required resources from ARM/Bicep templates or backups, then re-enable access behind Conditional Access with known egress IPs only.
- Escalate to Incident Response if the actor performs privileged role grants, Key Vault secret retrieval, Storage key listing, or rapid compute provisioning within the same session, or if sign-in shows impossible travel or missing MFA.
- Harden by enforcing PIM for Owner/Contributor/User Access Administrator roles, configuring Conditional Access with country allowlists and named egress IP ranges, restricting service principals to certificate-only auth and Private Link on Key Vault/Storage, and enabling continuous geolocation anomaly alerts in Microsoft Sentinel.

