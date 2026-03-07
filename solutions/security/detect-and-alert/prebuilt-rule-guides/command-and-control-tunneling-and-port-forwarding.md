---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Tunneling and/or Port Forwarding Detected via Defend for Containers" prebuilt detection rule.'
---

# Tunneling and/or Port Forwarding Detected via Defend for Containers

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Tunneling and/or Port Forwarding Detected via Defend for Containers

This detects tunneling or port-forwarding tools launched inside Linux containers, which attackers use to create hidden pathways for command-and-control, data theft, or lateral movement across the container network. A common pattern is running SSH with local/remote/dynamic forwarding or tools like chisel/socat to expose an internal service (e.g., database or kube API) through an external relay, bypassing normal network controls and segmentation.

### Possible investigation steps

- Identify the owning workload (pod/deployment/cronjob), image tag, and recent rollout or configuration changes to determine whether the tunnel/forwarding behavior is expected for that service.  
- Review the full executed command line, environment variables, and process ancestry to confirm what local/remote addresses and ports are being bridged and whether execution originated from an interactive session or startup script.  
- Enumerate active listeners and established connections from the container/node at the time of the alert to find externally reachable forwards, unexpected egress destinations, and any traffic to known C2 or relay infrastructure.  
- Correlate container network telemetry with DNS queries and outbound proxy usage to detect protocol tunneling patterns (e.g., long-lived sessions, high-entropy subdomains, unusual ports) and identify the initial ingress path.  
- Check for follow-on actions in the container and cluster (new binaries dropped, modified entrypoints, created secrets/serviceaccounts, or lateral access attempts) that would indicate persistence or pivoting beyond simple debugging.

### False positive analysis

- A developer or SRE launches `ssh` with `-L`/`-R`/`-D` options from inside a container during troubleshooting to temporarily reach an internal service (e.g., database or API) from their workstation through the container network.  
- A containerized service legitimately embeds proxying/forwarding behavior (e.g., `socat`, `3proxy`, `frps`, or `proxychains`) to expose or bridge ports as part of its normal runtime configuration, causing expected long-lived listeners and relayed connections that match tunnel/forwarding patterns.

### Response and remediation

- Isolate the affected pod/container by scaling the workload to zero or cordoning/quarantining the node and applying a deny-all egress policy to stop the active tunnel/forward while preserving artifacts for collection.  
- Terminate the tunneling process (e.g., ssh with -L/-R/-D, socat TCP4-LISTEN, chisel client/server, ngrok) and remove any dropped binaries or modified entrypoints/startup scripts that re-launch the forwarder.  
- Capture and review the running command line, parent process chain, active listeners, and established connections to identify exposed internal services and block the destination IPs/domains/ports used by the tunnel at the network edge and cluster egress controls.  
- Rotate potentially exposed credentials (Kubernetes service account tokens, cloud/API keys, database passwords) and validate RBAC/service account usage for unauthorized access originating from the affected workload.  
- Rebuild and redeploy from a known-good image, pin image digests, and add admission controls to block images containing tunneling utilities or starting processes with port-forwarding arguments unless explicitly approved.  
- Escalate to incident response immediately if the tunnel connects to external infrastructure, forwards access to sensitive services (e.g., kube-apiserver, etcd, databases), or similar tunneling behavior appears in multiple pods/namespaces.
