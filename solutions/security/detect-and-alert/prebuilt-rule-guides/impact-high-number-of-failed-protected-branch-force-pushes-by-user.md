---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Several Failed Protected Branch Force Pushes by User" prebuilt detection rule.'
---

# Several Failed Protected Branch Force Pushes by User

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Several Failed Protected Branch Force Pushes by User

This rule flags a single user generating multiple failed force push attempts to protected branches within a short span, indicating attempts to rewrite commit history and bypass branch protections. An attacker with a compromised maintainer role repeatedly tries to roll back a security fix, delete prior commits, and erase history entries before pushing a malicious revision. This activity threatens code integrity, disrupts pipelines, and can propagate harmful changes across repositories.

### Possible investigation steps

- Pull audit entries for the rejected updates to confirm the rejection reasons and the exact org/repo/branch targets, then reconstruct the timeline and sequence of attempts.
- Verify the user's current and recent permissions, team membership, and role changes, and confirm whether any admin or ownership transfers occurred before the attempts.
- Correlate the attempts with authentication and token activity (SSO logins, PAT/SSH key usage, IP/device fingerprints, geo), flagging any new or unusual sources.
- Review branch protection settings and recent edits (require status checks, linear history, admin enforcement, force push exemptions) to detect policy tampering or misconfiguration.
- Identify the specific commits the force pushes sought to overwrite by diffing the attempted ref against the protected branch head, prioritizing impacts to security fixes, release branches, or signed commits.

### False positive analysis

- During a repository migration or history cleanup, a maintainer runs a local script that loops through branches and tries to push rewritten commits with --force, but newly tightened branch protection rejects each attempt, resulting in multiple failures.
- A developer who previously had a force-push exemption on a protected release branch loses that permission during a role or team change and continues their usual rebase-and-force-push workflow, causing several rapid rejected ref updates.

### Response and remediation

- Immediately block the user in the GitHub organization, revoke all active personal access tokens and SSH keys from their account, and force sign-out to stop further push attempts.
- On each affected repository and branch (e.g., main, release/*), remove any force-push exemptions, enable “Include administrators,” require signed commits and status checks, and restrict push access to specific teams.
- Purge staging artifacts by deleting any branches or tags the user created around the attempts, rotate the user’s password and regenerate PATs/SSH keys, and remove newly registered keys or OAuth apps added during the window.
- Validate recovery by confirming the protected branch HEAD matches the last known good signed commit SHA, re-running CI for impacted repos, and creating a restore point tag for rapid rollback.
- Escalate to incident response if any attempts targeted main or release branches, originated from a newly created PAT/SSH key or an unrecognized IP/device, or the user holds repo admin/organization owner rights.
- Harden long term by enforcing org-wide 2FA/SSO, removing all standing force-push exemptions, requiring CODEOWNERS approvals on protected branches, and enabling audit alerts for branch protection edits and new credential creation.
