---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Tampering with RUNNER_TRACKING_ID in GitHub Actions Runners" prebuilt detection rule.'
---

# Tampering with RUNNER_TRACKING_ID in GitHub Actions Runners

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Tampering with RUNNER_TRACKING_ID in GitHub Actions Runners

This rule surfaces processes launched by GitHub Actions runners where RUNNER_TRACKING_ID is deliberately set to a non-default value. Attackers do this to break runner job tracking and cleanup on self-hosted runners, enabling long‑lived or hidden workloads. A common pattern is a workflow step that exports a custom RUNNER_TRACKING_ID and then spawns bash or node to fetch and execute a script via curl|bash or npm install scripts, keeping the process alive after the job finishes to run mining or exfil tasks.

### Possible investigation steps

- Correlate the event to its GitHub Actions run/job and workflow YAML, identify the repository and actor (commit/PR), and verify whether RUNNER_TRACKING_ID was explicitly set in the workflow or injected by a step script.
- On the runner host, determine if the spawned process persisted beyond job completion by checking for orphaning or reparenting to PID 1, sustained CPU/memory usage, and timestamps relative to the runner process exit.
- Review nearby telemetry for fetch-and-execute patterns (curl|bash, wget, node/npm lifecycle scripts), unexpected file writes under /tmp or actions-runner/_work, and outbound connections to non-GitHub endpoints.
- Enumerate persistence artifacts created during the run, including crontab entries, systemd unit files, pm2 or nohup sessions, and changes to authorized_keys or rc.local, and tie them back to the suspicious process.
- Assess blast radius by listing secrets and tokens available to the job, checking audit logs for their subsequent use from the runner IP or unusual repositories, and decide whether to revoke or rotate credentials.

### False positive analysis

- A self-hosted runner bootstrap script or base image intentionally sets a fixed RUNNER_TRACKING_ID for internal log correlation or debugging, causing all runner-spawned processes to inherit a non-github_* value.
- A composite action or reusable workflow accidentally overrides RUNNER_TRACKING_ID through env mapping or variable expansion (for example templating it from the run ID), resulting in benign non-default values during standard jobs.

### Response and remediation

- Quarantine the self-hosted runner by stopping Runner.Listener, removing the runner from the repository/organization, and terminating any Runner.Worker children or orphaned processes (PID 1) that carry a non-default RUNNER_TRACKING_ID.
- Purge persistence by removing artifacts created during the run, including systemd unit files under /etc/systemd/system, crontab entries in /var/spool/cron, pm2/nohup sessions, edits to ~/.ssh/authorized_keys or /etc/rc.local, and files under /tmp and actions-runner/_work linked to the tampered process.
- Revoke and rotate credentials exposed to the job (GITHUB_TOKEN, personal access tokens, cloud keys), delete leftover containers and caches in actions-runner/_work, invalidate the runner registration, and redeploy the runner from a clean, patched image.
- Escalate to incident response if you observe outbound connections to non-GitHub endpoints, processes persisting after job completion, modifications to ~/.ssh/authorized_keys or /etc/systemd/system, or repeated RUNNER_TRACKING_ID tampering across runners or repositories.
- Harden by restricting self-hosted runners to trusted repositories and actors, enforcing ephemeral per-job runners with egress allowlisting to github.com, setting strict job timeouts, and adding a workflow guard step that exits if RUNNER_TRACKING_ID does not start with github_.
