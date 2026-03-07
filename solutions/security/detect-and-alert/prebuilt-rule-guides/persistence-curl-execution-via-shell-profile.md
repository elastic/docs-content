---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Curl Execution via Shell Profile" prebuilt detection rule.'
---

# Curl Execution via Shell Profile

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Curl Execution via Shell Profile

Shell profile scripts (.zshrc, .bashrc, .bash_profile, .zprofile) execute automatically when users open new terminal sessions, making them valuable persistence mechanisms. Threat actors inject curl commands into these profiles to download and execute additional payloads each time the user opens a terminal, creating a reliable beacon mechanism that persists across system reboots. This detection rule identifies curl execution with download flags that originates directly from shell profile execution at login.

### Possible investigation steps

- Review the shell profile files (.zshrc, .bashrc, .bash_profile, .zprofile) for the affected user to identify the injected curl command and its destination URL.
- Analyze the process.args to determine the full curl command including output destination (-o, --output) and any other flags used.
- Investigate the destination URL in threat intelligence databases to determine if it is associated with known malicious infrastructure.
- Review the file modification timestamps of the shell profile files to determine when the malicious entry was added.
- Check browser history, email attachments, and download logs to understand how the attacker initially gained access to modify the profile.
- Examine the user.name associated with the modified profile to assess the scope of potential data access.
- Search for downloaded files on the system that may have been retrieved by the curl command and analyze their contents.

### False positive analysis

- Developers may add curl commands to shell profiles for convenience, such as fetching daily updates or checking API endpoints. Verify the URL destination and purpose with the user.
- Some shell customization frameworks and plugins use curl to update themselves on shell startup. Review common frameworks like Oh My Zsh for expected behavior.
- Enterprise tools may configure shell profiles for authentication or environment setup. Confirm with IT operations if such configurations are expected.
- Elastic infrastructure URLs are already excluded in the query to reduce noise from legitimate Elastic tooling.

### Response and remediation

- Remove the malicious curl command from the affected shell profile file immediately.
- Block the destination URL at the network perimeter to prevent payload delivery.
- Search for any files that were downloaded by the curl command and quarantine or remove them.
- Review user credentials and tokens that may have been exposed, as shell sessions often contain sensitive environment variables.
- Investigate how the shell profile was modified to identify the initial access vector.
- Check other user accounts on the system for similar shell profile modifications.
- Reset the user's shell profile from a known-good backup or template if available.
- Monitor for curl execution from shell profiles across the environment to identify additional compromised systems.
