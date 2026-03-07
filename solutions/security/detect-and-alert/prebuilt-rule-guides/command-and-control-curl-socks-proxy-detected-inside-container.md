---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Curl SOCKS Proxy Detected via Defend for Containers" prebuilt detection rule.
---

# Curl SOCKS Proxy Detected via Defend for Containers

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Curl SOCKS Proxy Detected via Defend for Containers

This detection flags interactive curl invocations inside Linux containers that use SOCKS proxy options, indicating traffic tunneling to evade egress controls and enable data exfiltration or C2 communications. A common pattern is an operator with shell access launching curl -x socks5h://localhost:1080 or --socks5-hostname via a dynamically created SSH -D port, then fetching payloads, beaconing to external endpoints, or posting stolen data through the proxy.

### Possible investigation steps

- Retrieve the full curl command line to extract the SOCKS proxy host:port, target URLs, and signs of uploads or auth (e.g., -d/--data, -T/--upload-file, -H Authorization), then pivot those IOCs across container and cluster telemetry.
- If the proxy points to localhost or an internal address, confirm a SOCKS listener in the container or node network namespace and identify the owning process to reveal the tunneling mechanism.
- Examine the process ancestry and same TTY/session context to attribute the action and spot precursor activity such as ssh -D, chisel, cloudflared, tor, or 3proxy establishing the proxy.
- Correlate Kubernetes metadata (pod, namespace, service account, node, image) and kube-apiserver audit logs for exec/attach to identify the actor, verify legitimacy, and find similar events in sibling pods or earlier revisions.
- Review network flows and DNS from this container through the proxy to external destinations to quantify data volume and destination reputation, and check for access to sensitive internal services.

### False positive analysis

- A developer troubleshooting from an interactive shell inside a container runs curl with -x/--proxy socks5 options to validate egress or reach internal endpoints through an approved proxy (e.g., localhost or an internal host), generating a benign match.
- Shell profiles or container environment configuration automatically route curl through --preproxy/--socks5-hostname to access internal APIs or artifact mirrors during interactive checks, causing expected activity to be flagged.

