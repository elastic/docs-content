---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual File Operation by dns.exe" prebuilt detection rule.
---

# Unusual File Operation by dns.exe

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual File Operation by dns.exe

The rule flags Windows DNS Server (dns.exe) creating, changing, or deleting files that aren’t typical DNS zone or log files, which signals exploitation for code execution or abuse to stage payloads for lateral movement. After gaining execution in dns.exe via DNS RPC or parsing bugs, attackers often write a malicious EXE into System32 and register a new service, leveraging the trusted service context on a domain controller to persist and pivot.

### Possible investigation steps

- Validate the modified file’s full path, type, and provenance, prioritizing writes in %SystemRoot%\System32, NETLOGON, or SYSVOL, and confirm signature, hash reputation, and compile timestamp to rapidly classify the artifact.
- Pivot to persistence telemetry around the same timestamp by hunting for new services or scheduled tasks (e.g., SCM 7045, Security 4697, TaskScheduler 106/200) and registry autoruns that reference the file.
- Correlate with DNS service network activity and logs for unusual RPC calls, authenticated connections from non-admin hosts, or spikes in failures/crashes that could indicate exploitation.
- Inspect the service’s runtime state for injection indicators by reviewing recent module loads, unsigned DLLs, suspicious memory sections, and ETW/Sysmon events mapping threads that performed the write.
- If the file is executable or a script or placed in execution-friendly locations, detonate it in a sandbox and scope the blast radius by pivoting on its hash, filename, and path across the fleet.

### False positive analysis

- DNS debug logging configured to write to a file with a non-.log extension (e.g., .txt) causes dns.exe to legitimately create or rotate that file during troubleshooting.
- An administrator exports a zone to a custom-named file with a nonstandard extension (e.g., .txt or .xml), leading dns.exe to create or modify that file as part of routine maintenance.

### Response and remediation

- Isolate the host by removing it from DNS rotation and restricting network access to management-only, then capture and quarantine any files dns.exe created or modified outside %SystemRoot%\System32\Dns or with executable extensions.
- Delete or quarantine suspicious artifacts written by dns.exe (e.g., .exe, .dll, .ps1, .js) in %SystemRoot%\System32, NETLOGON, or SYSVOL, record their hashes, and block them fleetwide via EDR or application control.
- Remove persistence by disabling and deleting any new or altered Windows services, scheduled tasks, or Run/Autorun registry entries that reference the dns.exe-written file path, and restore legitimate service ImagePath values.
- Recover by repairing system files with SFC/DISM, restoring affected directories from known-good backups, and restarting the DNS service, then validate zone integrity, AD replication, and client name-resolution.
- Immediately escalate to incident response if dns.exe wrote an executable or script into NETLOGON or SYSVOL or if a service binary path was changed to point to a newly dropped file, indicating probable domain controller compromise and lateral movement.
- Harden by applying the latest Windows Server DNS patches, enforcing WDAC/AppLocker to block execution from SYSVOL/NETLOGON and restrict dns.exe writes to the DNS and log directories, and enable auditing on service creation and file writes in System32/NETLOGON/SYSVOL.

