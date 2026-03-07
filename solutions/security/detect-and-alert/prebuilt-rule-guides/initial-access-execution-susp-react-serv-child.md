---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious React Server Child Process" prebuilt detection rule.'
---

# Suspicious React Server Child Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious React Server Child Process

This rule flags suspicious shell or system utility processes spawned by a React or Next.js server application—clear evidence of CVE-2025-55182 or CVE-2025-66478 exploitation enabling arbitrary code execution. An attacker sends a specially crafted RSC Flight protocol payload to a vulnerable Next.js or React Server Components endpoint, causing the server to deserialize untrusted data and execute attacker-controlled JavaScript, which then spawns shell commands or system utilities to establish initial access and persistence.

### Possible investigation steps

- Extract the parent Node.js process command line and working directory to identify the React or Next.js application, then check package.json or package-lock.json for React version (19.0-19.2) and Next.js version (14.3.0-canary, 15.x, 16.x) to confirm vulnerability.
- Review web server access logs (Nginx, Apache, ALB) for suspicious POST requests to RSC endpoints (/_next/data/, /.next/, /api/) in the minutes before the shell spawn, focusing on requests with unusual Content-Type headers (text/x-component, application/rsc) or large payload sizes.
- Analyze the spawned child process command line, arguments, working directory, and any downloaded files or scripts to identify the payload type (reverse shell, data exfiltration, credential theft, persistence mechanism) and compute file hashes for threat intelligence correlation.
- Pivot on the source IP address from web logs across other hosts and applications to identify additional compromised servers, and check for lateral movement attempts or scanning activity from the compromised host to internal networks.
- Examine the host for post-exploitation artifacts including new cron jobs, modified .bashrc/.profile files, SSH authorized_keys additions, new user accounts, unusual network connections to external IPs, files in /tmp or /var/tmp directories, and container escape attempts (nsenter, docker socket access).

### False positive analysis

- Legitimate build or deployment scripts triggered by CI/CD pipelines may cause Next.js build workers (jest-worker/processChild.js) to spawn shell commands; filter these by excluding processes with --node-ipc flags or running in /builds/, /workspace/, or other CI directories.
- Development servers (next dev, expo start, react-scripts start) running on developer workstations may spawn legitimate shells for tooling; consider excluding NODE_ENV=development or processes running from user home directories if appropriate for your environment.
- Server-side rendering (SSR) frameworks may legitimately invoke system utilities for image processing, PDF generation, or other server-side tasks; maintain an allowlist of expected child processes and their arguments for known applications.

### Response and remediation

- Immediately isolate the affected host to prevent lateral movement, terminate the Node.js parent process and all child processes spawned from the React/Next.js server, and block the source IP address at the firewall and WAF level.
- Remove any persistence mechanisms installed by the attacker including cron jobs (check crontab -l for all users), modified shell initialization files (~/.bashrc, ~/.profile, /etc/profile.d/), SSH keys in ~/.ssh/authorized_keys, and systemd timers or service units.
- Rotate all credentials and secrets accessible to the compromised application including database passwords, API keys, cloud service credentials (AWS/Azure/GCP), and session tokens, assuming they may have been exfiltrated.
- Collect forensic artifacts including memory dumps of the Node.js process (if still running), packet captures of the malicious HTTP request, web server access and error logs, application logs from the React/Next.js server, and copies of any files created in /tmp, /var/tmp, or the application directory.
- Escalate to incident command if the attacker achieved container escape (nsenter usage detected), accessed sensitive data or credentials, established C2 communication to external infrastructure, or if multiple hosts show similar exploitation patterns from the same source.
- Patch immediately by upgrading React to version 19.0.1+, 19.1.2+, or 19.2.1+, and Next.js to versions 14.3.0-canary.88+, 15.0.5+, 15.1.9+, 15.2.6+, 15.3.6+, 15.4.8+, 15.5.7+, or 16.0.7+ depending on your major version, and deploy WAF rules to block malformed RSC payloads at the application edge.
