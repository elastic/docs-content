---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Curl or Wget Egress Network Connection via LoLBin" prebuilt detection rule.
---

# Curl or Wget Egress Network Connection via LoLBin

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Curl or Wget Egress Network Connection via LoLBin

This detects outbound connections from curl or wget when they are launched via living-off-the-land binaries that can execute shell commands, signaling proxy execution to mask activity. It matters because attackers abuse trusted utilities to fetch payloads, stage command-and-control, or exfiltrate while evading simple controls. Example: an attacker uses awk or busybox to run curl to an external host, downloads a script into /tmp, pipes it to sh, or saves a binary and runs it under the proxy’s context.

### Possible investigation steps

- Pull the full process tree around the event and review the parent LoLBin’s command line for signs of proxy execution such as pipelines to a shell, write-to-file flags (-o/-O), exfil options (--data/--upload-file), or TLS bypass (-k), noting working directory and effective user for context.
- Identify any paths or filenames used by the transfer and inspect the filesystem for newly created or modified artifacts in temp locations, recording hashes, timestamps, permission changes (e.g., chmod +x), and any immediate execution or persistence actions.
- Correlate the outbound destination with threat intelligence and internal allowlists, examine DNS/SNI/certificate details, and flag unusual ports or use of proxies/TOR that suggest evasion.
- Validate whether the parent LoLBin and its execution path align with legitimate software or maintenance workflows on the host, and broaden the search for similar executions across hosts within the same timeframe.
- Hunt for follow-on activity including new listeners, reverse shells, additional outbound beacons, or other GTFOBins invoking curl/wget, and tie findings back to the same domains/IPs or dropped filesystem artifacts.

### False positive analysis

- During legitimate dependency installation or build workflows, pip/npm/gem/bundler/yarn may run post-install hooks that invoke curl/wget to fetch supplemental files from public mirrors, with the package manager as the parent process.
- Operations or maintenance tasks may use watch/busybox/run-parts/awk to proxy execution of curl/wget for external availability checks or bootstrap downloads in init scripts, producing short-lived egress that matches the LoLBin-parent pattern.

### Response and remediation

- Immediately isolate the affected Linux host or apply an outbound block, terminate active curl/wget and their invoking LoLBins (e.g., awk, busybox, run-parts), and add temporary firewall/DNS rules to deny the contacted domain/IP and port.
- Enumerate and delete files fetched via curl/wget (-o/-O) in /tmp, /var/tmp, /dev/shm, and user home (including scripts piped to sh), remove any persistence added (new cron entries, systemd units, rc.local edits), and record hashes/paths for evidence.
- Rotate credentials or tokens exposed via -u/--header or ~/.netrc, purge malicious proxy settings and config files (http_proxy/https_proxy environment, ~/.wgetrc, ~/.curlrc), and revoke SSH keys or cookies discovered alongside the downloads.
- Restore the system by reimaging or reinstalling if tampering is suspected, re-enable egress only after validation, verify application functionality, and re-enroll the endpoint with EDR while limiting curl/wget usage to approved service accounts.
- Escalate to incident response if curl/wget is piped to a shell (e.g., curl https://... | sh), a downloaded binary is made executable and run (chmod +x followed by execution), the destination matches known malicious infrastructure, or torify/torsocks/proxy chaining is used.
- Harden by mounting /tmp, /var/tmp, and /dev/shm with noexec/nosuid/nodev, enforcing AppArmor/SELinux to restrict curl/wget network access and file writes, constraining GTFOBins from spawning shells, and requiring egress via a proxy allowlist with TLS validation (disallow --insecure/-k).

