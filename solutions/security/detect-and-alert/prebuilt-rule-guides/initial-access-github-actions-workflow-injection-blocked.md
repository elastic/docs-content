---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "GitHub Actions Workflow Modification Blocked" prebuilt detection rule.
---

# GitHub Actions Workflow Modification Blocked

## Triage and analysis

### Investigating GitHub Actions Workflow Modification Blocked

This rule detects attempts to push workflow files to a GitHub repository from within a GitHub Actions workflow that are blocked by GitHub's security controls. This is a key indicator of supply chain attacks where malicious code attempts to establish persistence by injecting backdoor workflows.

### Possible investigation steps

- Review the `github.repo` field to identify which repository was targeted.
- Examine the `github.actor_id` to determine if the action was triggered by a bot (`github-actions[bot]`) or a user account (PAT-based).
- Check recent workflow runs in the repository for suspicious activity, especially in jobs that run `npm install` or other package manager commands.
- Review the repository's dependencies for recently added or updated packages that may contain malicious preinstall/postinstall hooks.
- Examine the `github.reasons.message` field for details on which workflow file was being created or modified.
- Search for other repositories in the organization that may have the same malicious dependency.
- Review GitHub audit logs for successful workflow file modifications that may have occurred before protections were enabled.

### False positive analysis

- Legitimate automation tools that manage workflow files may trigger this alert. Verify if the repository uses tools like Dependabot, Renovate, or custom automation that modifies workflows.
- CI/CD pipelines that intentionally update workflow files should use a PAT with the 'workflows' scope and be documented.

### Response and remediation

- If this is a confirmed attack attempt, immediately audit all dependencies in the affected repository.
- Remove any suspicious packages and regenerate lock files.
- Rotate any secrets that may have been exposed during the CI run.
- Review and revoke any PATs that may have been compromised.
- Enable branch protection rules requiring pull request reviews for workflow file changes.
- Consider implementing CODEOWNERS for `.github/workflows/` directory.
- Search for indicators of compromise such as unexpected workflow files (e.g., `discussion_*.yaml`, `formatter_*.yml`).

