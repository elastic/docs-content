---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "FortiGate Administrator Account Creation from Unusual Source" prebuilt detection rule.'
---

# FortiGate Administrator Account Creation from Unusual Source

## Triage and analysis

### Investigating FortiGate Administrator Account Creation from Unusual Source

This alert indicates that an administrator account was created on a FortiGate device from a source IP address that has not been observed performing configuration changes in the recent history window. This is a behavioral indicator of compromise, as threat actors exploiting SSO bypass vulnerabilities typically operate from infrastructure not previously associated with the device.

### Possible investigation steps

- Review `source.ip` to determine whether the IP address belongs to a known management network or authorized administrator location. Check against known threat infrastructure from The Constant Company LLC, BL Networks, and Kaopu Cloud HK Limited.
- Examine `fortinet.firewall.cfgobj` for the name of the newly created account and `fortinet.firewall.cfgattr` for the access profile assigned (especially super_admin).
- Check `source.user.name` to identify the account that performed the creation and verify whether it was recently created itself or accessed via SSO.
- Look for other configuration changes from the same source IP, including firewall policy modifications, configuration exports, or VPN user creation.
- Run `get system admin` on the affected FortiGate to list all current administrator accounts and compare against the authorized list.

### False positive analysis

- Authorized administrators connecting from a new location (VPN, travel, new office).
- Initial device setup or migration where configuration changes come from temporary infrastructure.
- Managed service providers performing authorized administration from rotating IP addresses.

### Response and remediation

- If unauthorized, immediately delete the newly created administrator account and audit the source account for compromise.
- Block the source IP at the perimeter and check other FortiGate devices for activity from the same IP.
- Restore configuration from a known-clean backup and rotate all credentials including LDAP/AD accounts connected to the device.
- Upgrade FortiOS to a patched version and disable FortiCloud SSO if not required.
