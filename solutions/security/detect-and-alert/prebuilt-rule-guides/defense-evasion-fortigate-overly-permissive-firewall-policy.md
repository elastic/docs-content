---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "FortiGate Overly Permissive Firewall Policy Created" prebuilt detection rule.'
---

# FortiGate Overly Permissive Firewall Policy Created

## Triage and analysis

### Investigating FortiGate Overly Permissive Firewall Policy Created

This alert indicates that a firewall policy was created or modified on a FortiGate device with source address `all`, destination address `all`, and service `ALL`. This configuration effectively disables firewall enforcement for traffic matching the policy.

In the FG-IR-26-060 campaign, threat actors created these permissive policies to ensure their traffic could traverse the firewall without restriction.

### Possible investigation steps

- Review `source.user.name` to determine which account created or modified the policy and `fortinet.firewall.ui` for the source interface and IP address. Verify whether this administrator is authorized to make firewall policy changes.
- Examine `fortinet.firewall.cfgattr` for the full policy configuration including interfaces, NAT settings, and scheduling. Check `fortinet.firewall.cfgobj` for the affected policy ID and determine whether the policy is positioned to intercept traffic (policy ordering matters).
- Look for administrator account creation, SSO login events, or configuration exports preceding this change. Determine whether the administrator account itself was recently created.
- Identify which interfaces the policy applies to (srcintf/dstintf in cfgattr) and determine whether the policy enables inbound, outbound, or both directions of unrestricted traffic.

### False positive analysis

- Temporary troubleshooting policies created during network diagnostics (should be time-limited and removed).
- Initial device setup or lab environments where broad policies are intentionally configured.
- Migration or cutover scenarios where temporary permissive rules are needed.

### Response and remediation

- If unauthorized, immediately delete the permissive firewall policy and audit the administrator account that created it for compromise.
- Review all other firewall policies for unauthorized modifications and check for other indicators of compromise on the device (rogue admins, VPN users).
- Restore the policy configuration from a known-clean backup.
- If the activity is expected, document the business justification and ensure a removal timeline is defined. Replace with specific source/destination/service rules as soon as possible.
