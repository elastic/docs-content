---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "FortiGate Configuration File Downloaded" prebuilt detection rule.'
---

# FortiGate Configuration File Downloaded

## Triage and analysis

### Investigating FortiGate Configuration File Downloaded

This alert indicates that a FortiGate device configuration file was downloaded. Configuration files contain highly sensitive information including administrator credentials, LDAP/RADIUS secrets, VPN pre-shared keys, certificate private keys, and the complete network topology.

In the FG-IR-26-060 campaign, threat actors exported the full device configuration shortly after creating rogue administrator accounts, using the harvested credentials for lateral movement and to maintain access through alternative channels.

### Possible investigation steps

- Review `source.user.name` to determine which account initiated the download and `fortinet.firewall.ui` for the source interface and IP address (e.g., GUI, CLI, or API). Verify whether this administrator is authorized to export device configurations.
- Check whether a scheduled backup process or configuration management tool performed this action. Look for preceding SSO login events or administrator account creation events on the same device and determine whether the downloading account was recently created.
- Check `observer.name` to identify which device had its configuration exported and search for configuration download events across other FortiGate devices in the fleet.
- Check for firewall policy changes, VPN configuration modifications, or additional admin account creation after the download. Determine whether any credentials from the configuration have been used for lateral movement.

### False positive analysis

- Scheduled configuration backups performed by FortiManager, Ansible, or other automation tools.
- Administrator-initiated backups during planned maintenance or before firmware upgrades.
- Configuration audits or compliance checks that require config export.

### Response and remediation

- If unauthorized, treat all credentials in the configuration as compromised. Rotate all passwords, pre-shared keys, LDAP bind credentials, and RADIUS secrets contained in the configuration.
- Revoke and reissue any certificates whose private keys were included in the export.
- Audit the administrator account that performed the download for compromise and check for other indicators of compromise on the device (rogue admins, policy changes).
- If the activity is expected, document the backup activity and verify it was performed through an authorized process. Ensure configuration backups are stored securely with appropriate access controls.
