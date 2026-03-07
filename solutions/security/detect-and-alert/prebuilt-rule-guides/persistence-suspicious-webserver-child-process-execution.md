---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Web Server Child Shell Spawn Detected via Defend for Containers" prebuilt detection rule.'
---

# Web Server Child Shell Spawn Detected via Defend for Containers

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Web Server Child Shell Spawn Detected via Defend for Containers

This rule flags Linux container activity where a web server (or typical web-service account) spawns an interactive shell to run a command string, a strong indicator of web app exploitation rather than normal request handling. It matters because this pattern commonly marks initial foothold and post-exploitation execution that can lead to persistence and lateral movement from the service container. A typical attacker flow drops a web shell or abuses RCE to launch `sh -c` and pull or run a secondary payload (e.g., reverse shell).

### Possible investigation steps

- Capture the full executed command line and decode/normalize any obfuscation (base64, hex, URL encoding) to determine the operator intent and any payload retrieval or reverse-shell behavior.  
- Correlate the execution timestamp with web access/error logs and ingress/WAF events to identify the triggering request path, parameters, and source IP/user-agent indicating RCE or web-shell invocation.  
- Inspect recent file and permission changes in the container’s application and web directories (including temp and upload paths) to identify newly dropped scripts/binaries, cron entries, or modified server configs.  
- Review container and orchestration context (image tag/digest, recent deploys, exec sessions, and Kubernetes events) to determine whether the activity aligns with a legitimate rollout or represents in-container compromise.  
- Check network telemetry for the container around the event for suspicious outbound connections, DNS lookups, or downloads, then pivot to any contacted hosts to assess command-and-control or staging infrastructure.

### False positive analysis

- A web application or server-side script running under the web-service account legitimately invokes `sh -c` (e.g., to run maintenance tasks like log rotation, cache rebuilds, file conversions, or templating/asset compilation) from a web directory such as `/var/www/*`, causing the web server to spawn a shell child process.  
- During container startup or a deployment/health-check routine, the web server process launches a shell via `sh -c` to perform initialization (e.g., environment substitution, dynamic configuration generation, permission fixes, or calling bundled helper scripts), which can resemble exploitation when the parent is a web server and the child is a shell.

### Response and remediation

- Immediately isolate the affected container/pod from inbound and outbound traffic (quarantine namespace/security group or apply a deny-all NetworkPolicy) and stop the workload to prevent further `sh -c` execution and potential C2.  
- Preserve evidence by exporting the container filesystem and logs (web access/error logs, application logs, and process output) and capture the exact shell command string and any downloaded payloads or newly created files in web roots, temp, and upload directories.  
- Eradicate by removing any identified web shells/backdoors and reverting unauthorized changes, then rebuild and redeploy the service from a known-good image digest while rotating secrets exposed to the container (service tokens, database creds, API keys).  
- Recover by validating application integrity and behavior post-redeploy (no unexpected shell spawns, no abnormal outbound connections, clean health checks) and monitor the previously contacted IPs/domains for further callbacks from other workloads.  
- Escalate to incident response and platform security immediately if the shell command indicates payload retrieval, reverse shell activity, credential access, or if similar `sh -c` executions are observed across multiple containers/namespaces.  
- Harden by removing shell binaries from runtime images where feasible, enforcing non-root and read-only filesystems, restricting egress to required destinations only, disabling risky interpreter execution paths in the web app, and adding WAF/RCE protections for the identified vulnerable endpoint.
