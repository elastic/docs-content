---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "GitHub Exfiltration via High Number of Repository Clones by User" prebuilt detection rule.'
---

# GitHub Exfiltration via High Number of Repository Clones by User

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating GitHub Exfiltration via High Number of Repository Clones by User

This rule flags a single user rapidly cloning dozens of repositories, a strong indicator of bulk source code exfiltration. Mass cloning enables quick siphoning of proprietary code, embedded secrets, and build artifacts across teams before defenses can respond. A typical pattern is a stolen personal access token used in a script to enumerate org repositories and clone them in rapid succession from a CI runner or cloud VM, including private and internal repos, to stage data for off-platform transfer.

### Possible investigation steps

- Validate whether the actor is a known automation or service account with a documented need to mass-clone, and quickly confirm intent with the account owner and affected repo admins.
- Enumerate the cloned repositories and their visibility, deprioritizing activity dominated by public repos while fast-tracking private/internal codebases with sensitive content across orgs.
- Pivot on the token identifier to determine the token owner, scopes, and creation/last-use details, compare to normal usage patterns, and revoke/reset credentials if anomalous.
- Analyze the user agent and agent identifier to attribute the activity to a specific host or CI runner, correlating with pipeline logs and login locations/times for anomalies.
- Correlate with endpoint/network telemetry from the originating host for large outbound transfers, external Git remotes, or bulk archiving indicating off-platform exfiltration following the clones.

### False positive analysis

- A developer rebuilding a workstation or creating an approved local mirror may legitimately clone dozens of repositories in a short window, especially when activity is dominated by public or low-sensitivity repos.
- A shared automation/service account running scheduled builds or org-wide maintenance tasks can trigger fresh clones across many repositories due to pipeline configuration or cache resets, inflating counts without exfiltration intent.

### Response and remediation

- Immediately revoke the GitHub token used for the clones, force sign out, require password reset and 2FA re-verification for the user, and suspend the account if unauthorized.
- Block and quarantine the originating host or CI runner by revoking its runner registration, removing its SSH keys/credentials, and firewalling its IP until imaged.
- On the cloned private/internal repositories, remove the user from teams, rotate or disable deploy keys and GitHub App installations, and enforce SAML SSO.
- Rotate repository and organization secrets present in those repos (Actions secrets, PATs, SSH keys, cloud access keys) and invalidate any secrets found in commit history.
- Recover by restoring only minimal access after owner approval, issuing a new fine-grained PAT with least privilege and expiry, and re-enabling builds while monitoring for further clone bursts.
- Escalate to incident response leadership and Legal if any private or export-controlled repos were cloned or cloning continues post-revocation, and harden by enforcing org-wide SSO, disallowing classic PATs, IP allowlisting for PAT use, enabling secret scanning with push protection, and alerting on burst git clone patterns from runners and unusual user agents.
