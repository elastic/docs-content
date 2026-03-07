---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious StartupItem Plist Creation" prebuilt detection rule.
---

# Suspicious StartupItem Plist Creation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious StartupItem Plist Creation

StartupItems are a deprecated macOS persistence mechanism that predates LaunchDaemons and was phased out after OS X Mavericks. Despite deprecation, the StartupItem infrastructure still functions on modern macOS versions for backward compatibility. Because legitimate software no longer uses StartupItems, the creation of a StartupParameters.plist file in /Library/StartupItems/ or /System/Library/StartupItems/ is highly anomalous and strongly indicates malicious activity seeking persistence through an overlooked mechanism.

### Possible investigation steps

- Examine the file.path to identify the specific StartupItem directory and verify that it was newly created versus modified.
- Review the StartupParameters.plist contents using plutil to identify the Description, Provides, OrderPreference, and other configuration values.
- Locate the StartupItem script in the same directory (typically named after the item) and analyze its contents for malicious commands.
- Check the process.executable that created the StartupItem to understand the initial delivery mechanism.
- Review file creation timestamps to correlate the StartupItem creation with other suspicious activity on the system.
- Search for additional files or binaries that may have been deployed alongside the StartupItem.
- Check for corresponding entries in /etc/rc files that may interact with the StartupItem.

### False positive analysis

- Very old legacy applications may use StartupItems for backward compatibility. Verify the software's legitimacy and whether it is still supported.
- Some enterprise or industrial software may not have been updated to use modern persistence mechanisms. Confirm with IT operations if legacy software is expected.
- Apple's shove process is already excluded in the query as it may interact with StartupItem directories during system maintenance.

### Response and remediation

- Remove the entire StartupItem directory containing the malicious StartupParameters.plist and associated scripts.
- Verify that the StartupItem was not successfully executed by checking system logs for execution evidence.
- Reboot the system to confirm the StartupItem has been fully removed and no longer executes.
- Investigate the initial access vector that allowed creation of the StartupItem.
- Search for other deprecated persistence mechanisms on the system that may indicate comprehensive malware deployment.
- Review other systems in the environment for similar StartupItem creations.
- Monitor the /Library/StartupItems/ directory for future unauthorized file creation.
- Consider implementing file integrity monitoring on persistence directories to detect future modifications.

