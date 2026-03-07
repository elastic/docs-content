---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Web Server Command Execution" prebuilt detection rule.
---

# Unusual Web Server Command Execution

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Web Server Command Execution

This rule detects shells invoked by web server processes on Linux to run one-off commands, surfacing command lines the server has never executed before. Attackers exploit vulnerable apps or dropped webshells to launch bash -c from web roots, e.g., download a payload with wget/curl into /opt or /tmp, chmod +x and execute it, or open a reverse shell (nc -e sh) to implant services or cron-like tasks and persist under the web server account.

### Possible investigation steps

- Reconstruct the process tree around the event to identify the shell payload and parent service, determine if it chains downloads, reverse shells, or archive extraction, and hash/snapshot any referenced files.
- Pivot to web server access and error logs at the timestamp to identify the request path, client IP, user agent, and HTTP verb that triggered execution, noting anomalies like POST uploads, long query strings, or 500s.
- List and diff newly created or recently modified files under common web roots and application directories around the event time, looking for webshells, chmod+x artifacts, .php/.jsp backdoors, or systemd/cron writes by the same user.
- Correlate with network telemetry to see if the web tier opened outbound connections or listeners (nc, bash -i, curl/wget), and capture any active sockets and destinations for rapid containment.
- Validate whether the command matches expected maintenance tasks for the application (e.g., wkhtmltopdf or image processing), and if not, isolate the process and host while scoping for the same pattern across other servers and preserving volatile evidence.

### False positive analysis

- A legitimate web-admin workflow (plugin/module install, content import, or cache warmup) spawns sh -c from an apache/nginx parent in /var/www to run tar/chmod/chown steps, producing a command line the host has not previously executed under www-data.
- A recently deployed application feature performs server-side document or image processing and rotates logs by calling sh -c from a framework parent (flask/rails/php) with a working directory in /opt or /usr/share/nginx, making the specific shell invocation a new term for this server.

### Response and remediation

- Quarantine the affected web server by removing it from the load balancer, stopping apache/nginx/httpd, and killing the spawned shell (e.g., bash -c) while capturing /proc/<pid>/cmdline and /proc/<pid>/environ, lsof, and active sockets for evidence.
- Block outbound egress from the web server account and immediately deny destinations contacted by curl/wget or reverse shells (nc, bash -i to /dev/tcp), and rotate exposed API keys or credentials referenced in the command line.
- Eradicate persistence by deleting newly dropped or modified files under /var/www, /usr/share/nginx, /srv/http, /opt, or /home/*/public_html (webshells, .php backdoors), removing downloaded binaries from /tmp or /opt, and cleaning cron/systemd units created by www-data/nginx.
- Recover by restoring web content and application code from known-good backups or images, verifying file ownership and permissions, and restarting the service with monitored command allowlists and file integrity checks.
- Escalate to full incident response and forensic imaging if any reverse shell artifacts (nc -e sh, bash -i >& /dev/tcp/*), privileged writes (/etc/systemd/system/*.service, /var/spool/cron/*), or sudo execution by the web server user are observed.
- Harden by disabling risky exec paths (PHP exec/system/shell_exec and unsafe plugins), enforcing noexec,nodev,nosuid mounts on web roots, applying SELinux/AppArmor confinement to web processes, narrowing outbound egress, and deploying WAF/mod_security rules for upload and RCE vectors.

