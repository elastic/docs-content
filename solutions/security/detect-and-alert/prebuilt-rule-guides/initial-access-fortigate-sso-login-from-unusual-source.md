---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "FortiGate FortiCloud SSO Login from Unusual Source" prebuilt detection rule.'
---

# FortiGate FortiCloud SSO Login from Unusual Source

## Triage and analysis

### Investigating FortiGate FortiCloud SSO Login from Unusual Source

This alert indicates that a FortiCloud SSO login was observed from a source IP address not previously seen authenticating via SSO in the last 5 days. This is a high-value signal because it filters out routine SSO access from known management IPs and only fires on novel source addresses.

CVE-2026-24858 (FG-IR-26-060) allows attackers with a FortiCloud account and a registered device to craft SAML assertions that authenticate them as administrators on other FortiGate devices when FortiCloud SSO is enabled. This vulnerability has been actively exploited in the wild.

### Possible investigation steps

- Check `source.ip` against known corporate management networks, VPN egress points, and jump hosts. Investigate the IP's ASN and geolocation, as attacker IPs have been observed from The Constant Company LLC, BL Networks, Kaopu Cloud HK Limited, and Cloudflare-protected ranges.
- Determine whether this IP has been seen in any other authentication context across the environment.
- Check `Esql.user_values` for the SSO account name (typically an email address) and verify the account belongs to the organization. Compare against known attacker email IOCs: cloud-noc@mail.io, cloud-init@mail.io, heltaylor.12@tutamail.com, support@openmail.pro.
- Check `Esql.observer_name_values` to identify which FortiGate device was accessed and confirm whether FortiCloud SSO is intentionally enabled on the device.
- Look for local administrator account creation, configuration exports, firewall policy changes, or VPN user/group creation immediately following the SSO login. The observed attack pattern involves rogue admin creation within seconds of login.

### False positive analysis

- Administrators connecting from a new office location, hotel, or home network for the first time may trigger this alert.
- FortiCloud SSO access after IP address changes such as ISP rotation or VPN egress changes can appear as a new source IP.
- First login after FortiCloud SSO is initially enabled on a device will fire since no historical SSO logins exist.

### Response and remediation

- If the activity is unauthorized, disable FortiCloud SSO immediately using `config system global` > `set admin-forticloud-sso-login disable`.
- Audit all administrator accounts for unauthorized additions and review and restore configuration from a known-clean backup.
- Rotate all credentials including any LDAP/AD accounts connected to the device.
- Upgrade FortiOS to a patched version.
- If the activity is expected, document the new source IP and consider adding an exception if it represents a new management location.
