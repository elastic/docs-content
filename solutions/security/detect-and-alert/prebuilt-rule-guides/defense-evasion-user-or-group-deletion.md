---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Linux User or Group Deletion" prebuilt detection rule.
---

# Linux User or Group Deletion

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Linux User or Group Deletion

This rule surfaces successful deletions of Linux users or groups—activity that can erase evidence, hide persistence, or disrupt access control. A common pattern is an attacker with root rights running userdel -r to remove a temporary privileged account they used for access, deleting its home directory and mail spool to strip artifacts. Correlate with recent privilege escalation and changes to sudoers/wheel to identify whether this was malicious cleanup versus routine deprovisioning.

### Possible investigation steps

- Correlate with auth and sudo logs to identify the actor, session (TTY/SSH), and source IP that executed the deletion and confirm whether root was obtained via sudo or another escalation path.
- Inspect the process tree and command line to see if userdel/groupdel used -r to remove the home/mail spool and whether it was launched from an interactive shell, SSH session, or automation tooling.
- Validate expected deprovisioning by checking HR/ticketing/IdM and configuration-management activity around the time, and escalate if the deleted identity was privileged or part of sudo/wheel.
- Build a timeline around the event to find adjacent actions such as account creation, password or key changes, group membership edits, and modifications to /etc/passwd, /etc/group, /etc/shadow, or sudoers.
- Assess impact and persistence by locating services, cron/systemd units, files, ACLs, or running processes still referencing the deleted UID/GID, attempt recovery of the home/mail from backups, and look for wtmp/btmp/lastlog tampering.

### False positive analysis

- Scheduled deprovisioning or baseline enforcement where administrators intentionally remove stale local users or groups associated with retired projects, decommissioned systems, or role changes during maintenance.
- Package uninstall or system maintenance scripts that add a service account during setup and later remove it during cleanup, causing legitimate user/group deletion events.

### Response and remediation

- If the deletion is unauthorized, immediately isolate the host and restrict interactive access by setting PermitRootLogin no and tightening AllowUsers/AllowGroups in /etc/ssh/sshd_config, then systemctl restart sshd to apply.
- Review and clean authorization and persistence by inspecting /etc/sudoers and /etc/sudoers.d for unauthorized rules, checking wheel/sudo memberships in /etc/group, and purging cron or systemd units that reference the deleted UID/GID.
- Recover the identity if legitimate by recreating the user/group with the original UID/GID from /var/backups/{passwd,group,shadow}, restoring the corresponding /home directory and /var/spool/mail from backups, and reassigning orphaned files using find -nouser -nogroup to a valid account.
- Rotate credentials associated with the deleted identity by replacing SSH keys and secrets found in ~/.ssh/authorized_keys and application configs, and invalidate cached tokens and service account credentials that may have been shared.
- Escalate to incident response if the deleted account was privileged (present in wheel/sudo groups), userdel/groupdel used -r to remove the home/mail spool, or evidence of log tampering exists such as truncated /var/log/auth.log or altered wtmp/btmp/lastlog.
- Harden by centralizing local account lifecycle in IdM/LDAP, enforcing visudo-managed sudo changes, enabling auditd watches on /usr/sbin/userdel,/usr/sbin/groupdel and writes to /etc/passwd,/etc/group,/etc/shadow, and deploying AIDE to monitor integrity of /etc.

