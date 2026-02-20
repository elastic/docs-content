---
navigation_title: Update Integrations docs
applies_to:
  stack:
  serverless:
---

# How to update Integrations documentation

{{integrations}} documentation lives in the [elastic/integrations](https://github.com/elastic/integrations) repository and follows a specific workflow that differs from other Elastic documentation. Changes to integration docs require updating source files, bumping versions, and waiting for the package to be published to the {{package-registry}} (EPR) before they appear on the docs site.

## Prerequisites

Before you start, make sure you have:

- Write access to the [elastic/integrations](https://github.com/elastic/integrations) repository (for Elastic contributors).
- The [`elastic-package`](https://github.com/elastic/elastic-package) tool installed locally.

## Update the docs

::::::{stepper}

::::{step} Create a branch
Create a branch with the pattern `docs-enhancement/{desired_branch_name}`:

```bash
git checkout -b docs-enhancement/my-docs-update
```
::::

::::{step} Edit the README source file
Edit the source file at `packages/{package}/docs/README.md` or `packages/{package}/_dev/build/docs/README.md` .

:::{important}
Other structures might occur. Most packages use a single README.md. A small minority use a multi-file structure, for example, one file per cloud service or component. 

If your package has multiple docs files, edit the one that corresponds to the content you're updating.
:::

::::

::::{step} Commit and push your changes
Commit and push your changes to the remote repository:

```bash
git add .
git commit -m "docs: update {package} documentation"
git push -u origin docs-enhancement/my-docs-update
```
::::

::::{step} Create a PR and wait for checks
Create a PR to the upstream [elastic/integrations](https://github.com/elastic/integrations) repository.

Wait for the **Documentation edit helper** check to complete. This check generates the commands you'll need in the next step.
::::

::::{step} Copy and run the generated commands
1. In your PR, select the **Documentation edit helper** check.
2. Select **Summary** in the top left.
3. Copy the commands from the **Documentation follow-up** panel. The commands look similar to this:

   ```bash
   for pkg in docker; do
     cd packages/$pkg
     elastic-package changelog add --type enhancement --description "Improve documentation" --link "https://github.com/elastic/integrations/pull/123456" --next patch
     elastic-package build
     cd ../..
   done
   git add -u
   git commit -m "docs: update changelogs and build documentation"
   git push
   ```

4. Go back to your editor and, from the integrations repository root folder, paste and run the copied commands.

These commands:
- Build the generated `packages/{package}/docs/README.md` file.
- Update `changelog.yml` with the new entry.
- Update `manifest.yml` with the new version.
::::

::::{step} Request review and merge
Go back to your PR, request a code owner review, and merge it once approved.
::::

::::::

## After merging: When changes appear

After your PR is merged, changes don't appear immediately on the docs site. The process involves several automated steps:

1. **Package publication**: The package is published to the [{{package-registry}} (EPR)](https://github.com/elastic/package-registry). You'll know this is complete when a bot comments on your PR with a message like:

   > Package {package_name} - {version} containing this change is available at https://epr.elastic.co/package/{package_name}/{version}

2. **Docs sync**: A scheduled job in the [elastic/integration-docs](https://github.com/elastic/integration-docs) repository pulls the latest packages from EPR and opens an automated PR. This job runs once a day.

3. **Docs build**: Once the automated PR is merged, changes propagate to the docs site.

:::{tip}
If you need changes to appear sooner, you can manually trigger the [update-docs workflow](https://github.com/elastic/integration-docs/actions/workflows/run-update-docs.yml) in the integration-docs repository.
:::

## Troubleshooting

### Changes aren't appearing after merge

If your changes don't appear on the docs site after following these steps:

1. **Check for the EPR bot comment**: Look for the bot comment in your PR confirming the package was published to EPR. If you don't see it, the package hasn't been published yet.

2. **Verify the version was bumped**: Ensure your PR included updates to both `changelog.yml` and `manifest.yml`. Without these updates, a new package version won't be published.

3. **Check the integration-docs repository**: Look at recent automated update PRs in the integration-docs repository. If they're failing, your changes won't be pulled until the issues are resolved.

4. **Check version compatibility**: If the integration's `manifest.yml` specifies a {{kib}} version that hasn't been released yet. For example, if `^9.3.0` before 9.3 is released, the docs won't appear until that version is live.

### The edit helper check is missing

If you can't find the edit helper check on your PR, ensure your branch name follows the `docs-enhancement/` pattern.

### Build failures in integration-docs

Sometimes the automated PR in integration-docs fails due to new integrations that need to be added to `nav.yaml`. These failures block all docs updates until resolved. If you notice this, reach out to the docs team for assistance.
