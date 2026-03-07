---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "File Download Detected via Defend for Containers" prebuilt detection rule.'
---

# File Download Detected via Defend for Containers

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating File Download Detected via Defend for Containers

This rule flags an interactive session inside a Linux container that runs curl or wget to pull content from a URL or IP and immediately writes a new file, signaling hands-on retrieval of tools, payloads, or data. It matters because attackers often use on-demand downloads to stage second-phase execution and establish application-layer command-and-control without baking artifacts into images. A common pattern is an operator execing into a running container, fetching a script or binary from paste/CDN infrastructure, then saving it for rapid follow-on execution.

### Possible investigation steps

- Attribute the interactive session to an initiator by correlating the container exec/attach event with Kubernetes audit logs or Docker daemon logs to identify the user/service account, source IP, and access path.  
- Inspect the created file’s full path, size, magic/format, and hash, then retrieve it from the container or node filesystem for static analysis and malware scanning.  
- Pivot on the download destination (domain/IP/URL path) to review outbound connection telemetry, DNS/TLS indicators, and threat reputation, and determine whether the endpoint is expected for this workload.  
- Review subsequent container activity after the download for follow-on actions such as chmod, interpreter execution, new processes, cron modifications, credential access, or lateral movement attempts.  
- Validate whether the container/image and namespace normally permit interactive access and external downloads, and if not, assess for compromised credentials, exposed exec permissions, or a misconfigured runtime policy.

### False positive analysis

- A developer or SRE may exec into a running container for interactive troubleshooting and use curl or wget to fetch a diagnostic script, configuration file, or test payload from an internal HTTP endpoint, resulting in a new file creation event.  
- An operator may interactively run curl or wget to download a patch, certificate bundle, or updated artifact into the container during an emergency fix or recovery workflow, especially in minimal images lacking package managers, which can appear indistinguishable from attacker staging.

### Response and remediation

- Immediately isolate the affected pod/container by applying a deny-all egress policy and, if possible, pausing or cordoning the hosting node to stop additional downloads and outbound C2 traffic.  
- Capture and preserve the downloaded artifact(s) created by curl/wget (path, timestamps, hashes) plus the interactive shell history/command line, then delete the file(s) from the container and revoke any injected tools or scripts.  
- Terminate the interactive session and rotate credentials used to exec/attach (Kubernetes user/service account tokens, kubeconfig, SSH keys) and invalidate any newly created access (added users, API tokens, or modified secrets/config).  
- Redeploy the workload from a known-good image and configuration, then scan the node and cluster for persistence or reuse of the same URL/IP and hashes across other containers, blocking them at egress and proxy/IDS.  
- Escalate to incident response immediately if the downloaded file is executed, connects to an unapproved external host, modifies startup paths (entrypoint/cron), or if the exec user is unknown or high-privileged.  
- Harden by removing exec/attach permissions from non-admin roles, enforcing runtime policies that block interactive curl/wget and restrict outbound traffic to approved destinations, and ensuring images include required tools so ad-hoc downloads are unnecessary.
