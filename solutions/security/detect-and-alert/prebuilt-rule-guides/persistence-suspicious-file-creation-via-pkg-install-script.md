---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious File Creation via Pkg Install Script" prebuilt detection rule.
---

# Suspicious File Creation via Pkg Install Script

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious File Creation via Pkg Install Script

macOS installer packages (.pkg) can include pre-install and post-install scripts that execute with elevated privileges during installation. While legitimate software uses these scripts for proper setup, threat actors abuse this capability to deploy malware, establish persistence, or stage additional payloads under the guise of legitimate software installation. This detection rule identifies when pkg install scripts copy executables or scripts to suspicious locations outside standard installation directories.

### Possible investigation steps

- Examine the process.args to identify the specific pkg install script path and determine which package triggered the alert.
- Review the file.path to understand where files were copied and assess whether the destination is a known malware staging location or persistence directory.
- Analyze the file.Ext.header_bytes to confirm the file type (Mach-O binary indicated by cffaedfe or cafebabe, or script files like .py, .sh, .js).
- Locate the original installer package if still available and examine its contents, including the preinstall and postinstall scripts using pkgutil --expand.
- Check the package's code signature and notarization status using pkgutil --check-signature and spctl --assess to determine if it passed Apple's security review.
- Review the download source or delivery mechanism for the installer package to understand how it reached the system.
- Search for the same package hash across other systems in the environment to identify potential widespread deployment.

### False positive analysis

- Legitimate software installers may deploy helper tools or scripts to /usr/local/bin/ or other locations. Verify the package's origin and signing status.
- Development tools and frameworks may install additional components to various directories during setup. Confirm with development teams if installations were expected.
- Enterprise software deployment may use installer scripts that deploy files to custom locations. Review with IT operations to document expected installation patterns.
- Temporary files during complex installations may appear in /tmp/ or /var/folders/ briefly. These typically don't persist after installation completes.

### Response and remediation

- Terminate any suspicious processes that were spawned by the malicious installer script.
- Remove the files that were copied to suspicious locations, including any persistence mechanisms like LaunchAgents or LaunchDaemons.
- Quarantine the original installer package for forensic analysis and submission to Apple for notarization revocation if appropriate.
- Review system logs for all actions taken during the malicious installation to identify the full scope of changes.
- Scan the system for additional malware components or persistence mechanisms that may have been deployed.
- Report the malicious package to Apple at reportaproblem.apple.com to request notarization revocation.
- Check other systems that may have installed the same package and remediate accordingly.
- Review endpoint security policies to prevent future execution of unsigned or revoked installer packages.

