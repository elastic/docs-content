---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "FortiGate Super Admin Account Creation" prebuilt detection rule.'
---

# FortiGate Super Admin Account Creation

## Triage and analysis

### Investigating FortiGate Super Admin Account Creation

This alert indicates that an administrator account was created on a FortiGate device. Administrator creation events on these devices are generally rare and should be closely scrutinized, as they are a key persistence mechanism used in the FG-IR-26-060 campaign.

In the observed campaign, threat actors created multiple super_admin accounts (audit, backup, support, itadmin, secadmin, remoteadmin) within seconds of initial access to ensure persistent control even if individual accounts are discovered and removed.

### Possible investigation steps

- Review `fortinet.firewall.cfgobj` for the name of the newly created account and examine `fortinet.firewall.cfgattr` to determine the access profile assigned to the account (especially super_admin).
- Review `source.user.name` to determine which account performed the creation and `fortinet.firewall.ui` for the source interface and IP address. Verify whether this administrator is authorized to provision accounts.
- Check whether a login event (especially via SSO) occurred shortly before the account creation. Analyze the timing between events.
- Check `observer.name` to identify the FortiGate device and run `get system admin` to get the current administrator list. Check other FortiGate devices in the fleet for the same account name.

### False positive analysis

- Authorized provisioning of a new administrator account through an approved change management process.
- Initial device setup where administrator accounts are created as part of deployment.
- Migration or device replacement scenarios where accounts are replicated from another device.

### Response and remediation

- If unauthorized, delete the administrator account immediately and audit the creating account for compromise.
- Treat the device configuration as compromised and restore from a known-clean backup.
- Check all FortiGate devices for similar account creation and upgrade FortiOS to a patched version.
- If the activity is expected, document the provisioning activity and the business justification.
