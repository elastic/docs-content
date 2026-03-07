---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "GitHub Actions Unusual Bot Push to Repository" prebuilt detection rule.
---

# GitHub Actions Unusual Bot Push to Repository

## Triage and analysis

### Investigating GitHub Actions Unusual Bot Push to Repository

This rule detects when the GitHub Actions bot pushes to a repository where it hasn't pushed to in a certain time interval. While this can be
legitimate automation, it may also indicate a supply chain attack where malicious code executes during CI and attempts
to modify repository contents.

### Possible investigation steps

- Review the `github.repo` field to identify the affected repository.
- Check recent workflow runs in the repository to identify which workflow triggered the push.
- Examine the repository's commit history to see what files were modified by the bot push.
- Look for newly added or modified files in `.github/workflows/` directory.
- Review the repository's dependencies for recently added or updated packages with preinstall/postinstall hooks.
- Check if the repository has legitimate automation that would explain bot pushes (Dependabot, Renovate, release automation).
- Correlate with `protected_branch.rejected_ref_update` events to see if workflow injection was blocked.
- Search for other repositories in the organization with similar suspicious activity.

### False positive analysis

- Repositories with auto-commit workflows (formatting, changelog generation, version bumps) will trigger on first run.
- Dependabot or Renovate auto-merge configurations cause legitimate bot pushes.
- GitHub Pages deployment workflows may push to gh-pages branches.
- Release automation that updates version files or generates artifacts.

### Response and remediation

- If the push is unexpected, immediately review the commit contents for malicious files.
- Check for suspicious workflow files (e.g., `discussion_*.yaml`, `formatter_*.yml`).
- Audit all dependencies in the affected repository for malicious packages.
- Rotate any secrets that may have been exposed during the workflow run.
- Enable branch protection rules to require PR reviews for all changes.
- Consider restricting GITHUB_TOKEN permissions in workflow files using `permissions:` key.

