---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "High Number of Closed Pull Requests by User" prebuilt detection rule.'
---

# High Number of Closed Pull Requests by User

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating High Number of Closed Pull Requests by User

This rule flags a single user rapidly closing many pull requests in a short window, a disruptive pattern that suppresses review history, delays releases, and masks unauthorized changes. An attacker with stolen maintainer access mass-closes pull requests across multiple repositories, then force-pushes branches and opens new pull requests that sidestep earlier review threads, making malicious edits appear routine amid churn.

### Possible investigation steps

- Determine if the actor is a bot or sanctioned maintenance by confirming account type, scheduled workflows, and change advisories from repo/org owners.
- Open a sample of the closed PRs to review comments, labels, linked issues, and whether closure coincided with branch deletions, force-pushes, or unusual commit history in the target branches.
- Correlate the closure burst with audit events for permission changes, role assignments, repository settings edits, or protection rule modifications to detect potential sabotage.
- Validate the actor’s IPs, geolocation, and user agents against baselines and check for recent PAT creations, OAuth app grants, or SSO anomalies indicating credential theft.
- Identify whether closed PRs were immediately replaced by new PRs carrying similar diffs that bypass prior review threads and required checks, and verify branch protection remained enforced.

### False positive analysis

- A maintainer or org-owned bot performs scheduled backlog hygiene, closing stale, duplicate, or superseded PRs across multiple repositories after a default branch rename or policy update, resulting in a high closure count from one account.
- During a planned migration or archival, a release manager closes PRs tied to deprecated branches and consolidates work into new targets, legitimately generating a burst of closures attributed to a single user.

### Response and remediation

- Immediately contain by removing the user from teams with Triage/Write permissions on affected repositories, revoking their personal access tokens from Tokens & keys, and tightening branch protection by disallowing force-pushes and restricting who can push to main and release branches.
- Trigger escalation to Security Incident Response if closed pull requests span more than five repositories within one hour, coincide with branch deletions or forced pushes, or originate from a new user agent/IP, and disable the account at the identity provider while contacting GitHub Support.
- Eradicate impact by reopening legitimate PRs via each closed PR URL, using Restore branch or recreating the head branch from the last known commit SHA, and reapplying required labels and reviewers.
- Recover repository state by comparing diffs of closed PRs to any newly opened PRs by the same user, reverting unauthorized commits in target branches with git revert, and re-running required status checks before merging.
- Harden controls by enforcing branch protection rules (require two approvals, restrict who can dismiss reviews, require signed commits), enabling CODEOWNERS for critical paths, and turning off Allow deletions on default and release branches.
- Prevent recurrence by disabling classic PATs and requiring short-lived fine-grained PATs, revoking unusual OAuth app grants, mandating SSO with hardware-backed MFA, and installing a GitHub App/Action that notifies on PR closures with PR URLs, repos, and branches and requires a reason-coded label per policy.
