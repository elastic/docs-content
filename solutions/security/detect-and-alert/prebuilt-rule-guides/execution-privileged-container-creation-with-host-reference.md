---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Privileged Container Creation with Host Directory Mount" prebuilt detection rule.'
---

# Privileged Container Creation with Host Directory Mount

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Privileged Container Creation with Host Directory Mount

This rule flags creation of a privileged container that bind-mounts host directories into the container filesystem, breaking isolation and granting direct access to host files and devices. An attacker on a compromised node starts a privileged container via the runtime, bind-mounts the host root (/:) inside it, then chroots and alters critical files or services to seize host control, persist, and pivot.

### Possible investigation steps

- Retrieve the full process tree and execution context (user, controlling TTY, parent, remote source IP) to identify who initiated the container and whether it aligns with a sanctioned change.
- Run runtime introspection to confirm the container’s mounts and privileges (e.g., docker ps/inspect or CRI equivalents), capturing the container ID, exact hostPath mappings, image, entrypoint, and start time.
- If orchestrated, correlate with Kubernetes events and kubelet logs at the same timestamp to find any Pod using privileged: true with hostPath volumes, recording the namespace, service account, controller, and requestor.
- Review audit and file integrity telemetry after container start for host-impacting actions such as chroot into the mount, nsenter into host namespaces, or writes to critical paths (/etc/passwd, /etc/sudoers, /root/.ssh, /var/lib/kubelet, and systemd unit directories).
- Assess image provenance and intent by resolving the image digest and registry, reviewing history/entrypoint for post-start tooling, and validating with service owners or allowlists whether this privileged host-mount is expected on this node.

### False positive analysis

- An administrator uses docker run --privileged with -v /:/host during a break-glass or troubleshooting session to edit host files or restart services, matching the pattern but aligned with an approved maintenance procedure.
- Automated provisioning or upgrade workflows intentionally start a privileged container that bind-mounts / to apply system configuration, install packages, or manage kernel modules during node bootstrap, producing an expected event.

### Response and remediation

- Immediately stop and remove the privileged container by its ID using docker, cordon the node to prevent scheduling, and temporarily disable the Docker/CRI socket to block further privileged runs.
- Preserve forensic artifacts (docker inspect output, container image and filesystem, bash history, /var/log) and remediate by diffing and restoring critical paths (/etc, /root/.ssh, /etc/systemd/system, /var/lib/kubelet), removing rogue users, SSH keys, and systemd units.
- Rotate credentials potentially exposed by the host mount (SSH keys, kubelet certs, cloud tokens under /var/lib/kubelet or /root), patch the container runtime, and uncordon or rejoin the node only after verifying privileged runs and host-root mounts are blocked.
- Escalate to incident response if the mount included "/" or if evidence shows chroot or nsenter into host namespaces or writes to /etc/passwd, /etc/sudoers, or systemd unit files, and initiate host reimage and broader fleet scoping.
- Enforce controls that deny --privileged and hostPath of "/" via admission policy (Pod Security Standards, Kyverno, OPA Gatekeeper), drop CAP_SYS_ADMIN with seccomp/AppArmor, enable Docker userns-remap and no-new-privileges, and restrict membership in the docker group.
- Establish a break-glass approval workflow and an allowlist for legitimate host mounts, enable file integrity monitoring on /etc and kubelet directories, and add runtime rules to alert and block future docker run -v /:/host attempts.
