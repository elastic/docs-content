---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "GitHub Private Repository Turned Public" prebuilt detection rule.'
---

# GitHub Private Repository Turned Public

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating GitHub Private Repository Turned Public

This rule flags when a previously private repository is made public, a high-risk change that can expose proprietary code, credentials, and internal documentation. Attackers who hijack a maintainer’s account often flip visibility via the UI or API, then immediately fork or mirror the repo to an external account to retain access and harvest embedded secrets even if the org reverts the change.

### Possible investigation steps

- Identify the actor and authentication method used for the visibility change, verify their repository role, and confirm the action against an approved change request or ticket.
- Pull a time-bounded audit trail around the event for the actor and repository to surface related risky operations such as forking, transfers, collaborator additions, webhook edits, branch protection changes, or archive downloads.
- Enumerate forks, mirrors, stars, and watchers added after the change via the repository network graph and correlate with external accounts or suspicious clusters.
- Inspect GitHub Actions runs, deployments, and webhooks triggered post-change for workflows that export code or secrets to external destinations.
- Perform rapid secret scanning across the repository history and HEAD, triage any exposed credentials, and initiate rotation while mapping impacted services and environments.

### False positive analysis

- A planned, approved open-source release where a maintainer intentionally flips a sanitized repository from private to public as part of a documented change.
- Bulk visibility changes during an organization-wide cleanup or migration that publishes templates, sample repos, or empty scaffolds, executed by an authorized service account.

### Response and remediation

- Immediately revert the repository to private, remove outside collaborators, lock access to the core maintainers team, disable GitHub Actions and webhooks, and delete any release assets or packages published during the exposure window.
- Enumerate new forks, mirrors, stars, and watchers created after the visibility change and file takedown requests with GitHub Trust & Safety for unauthorized public copies while removing any deploy keys and uninstalling suspicious GitHub App installations added around the event.
- Run a rapid secret scan across the repository history and HEAD, rotate exposed credentials (cloud keys, API tokens, SSH keys), invalidate compromised service accounts, and purge cached artifacts or container images built from the public commit range.
- Restore secure settings from baseline by re-applying branch protection rules, CODEOWNERS, required reviews, signed commits, and protected environments, then re-enable workflows only after reviewing job steps and outputs for any export of code or secrets.
- Escalate to Security IR and Legal if the actor denies making the change, the repo network graph shows new public forks under unknown accounts, regulated data is present, or external users downloaded source zips or release archives during the public period.
- Restrict who can change repository visibility to organization owners, enforce SSO and 2FA for maintainers, disable forking of private repositories, limit Actions to trusted runners and verified actions, and enable secret scanning with push protection across the organization.
