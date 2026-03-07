---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Password Spraying Attack via SSH" prebuilt detection rule.
---

# Potential Password Spraying Attack via SSH

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Password Spraying Attack via SSH

This rule flags bursts of failed SSH logins coming from the same network origin against many different Linux accounts within a short window, indicating password spraying that can precede account compromise. It matters because attackers try a small set of common passwords across broad user lists to evade lockouts and find one weak credential. A typical pattern is an external VPS rapidly trying passwords like “Welcome123” or “Spring2024!” against 30+ usernames (e.g., admin, test, ubuntu, devops) over five minutes via SSH on a single server.

### Possible investigation steps

- Check for any successful SSH authentications from the same source IP within a short window around the failures and, if found, pivot to session details such as interactive TTY use, sudo activity, and modifications like authorized_keys updates.
- Enrich the source IP with geolocation, ASN, reputation, and cloud-provider attribution and verify whether it is observed attempting SSH across multiple hosts to confirm a broad spray pattern.
- Compare the attempted usernames against your directory to identify valid and privileged or service accounts and confirm whether lockouts, password resets, or MFA challenges were triggered.
- Determine if the affected host is internet-exposed and which port SSH is reachable on, then review current SSH authentication settings (password vs key-based, PAM/MFA) to assess risk of compromise.
- Correlate the source IP with approved scanners, bastion hosts, or change tickets and maintenance windows to quickly rule out sanctioned testing or misconfigured monitoring.

### False positive analysis

- A misconfigured internal automation or admin script on a management or jump host sequentially attempts SSH to many accounts with an outdated password, producing more than 10 distinct usernames and at least 30 failures from a single source IP within five minutes.
- Legitimate users behind a shared NAT or bastion host concurrently attempt SSH with expired credentials during a password rotation or temporary authentication issue, making failures across many distinct usernames appear to come from one IP.

### Response and remediation

- Immediately block the spraying source IP(s) at host firewalls (iptables/nftables) and edge controls, and temporarily restrict SSH (port 22) to approved bastion/jump host CIDRs only.
- If any login succeeded or an sshd session from the same IP is active, terminate it, remove any newly added ~/.ssh/authorized_keys entries, and force password resets with MFA for the targeted users.
- Before restoring normal access, verify no persistence by checking for changes to /etc/ssh/sshd_config, sudoers, or cron jobs and reviewing /var/log/auth.log and lastlog for anomalies, then re-enable only required accounts.
- Escalate to incident response if privileged or service accounts were targeted, the spray spanned multiple servers, or there is evidence of sudo activity, file changes under /root or /etc, or a successful login, and preserve auth logs, bash histories, and firewall block artifacts.
- Harden SSH by disabling PasswordAuthentication, enforcing key-based auth with PAM MFA, setting conservative MaxAuthTries and LoginGraceTime, enabling fail2ban or equivalent bans, and restricting access via AllowUsers/AllowGroups and security group rules.

