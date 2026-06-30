---
navigation_title: Update Integrations docs
applies_to:
  stack:
  serverless:
---

# How to update Integrations documentation

{{integrations}} documentation lives in the [elastic/integrations](https://github.com/elastic/integrations) repository and follows a specific workflow that differs from other Elastic documentation. Changes to integration docs require updating source files, bumping versions, and waiting for the package to be published to the {{package-registry}} (EPR) before they appear on the docs site.

:::{note}
Most integrations follow the workflow described on this page. However, some integrations—such as **{{elastic-defend}}**—have separate source repositories and different workflows. Refer to [Special case integrations](#special-case-integrations) for details.
:::

## Prerequisites

Before you start, ensure you have:

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
Edit the source file at `packages/{package}/docs/README.md` or `packages/{package}/_dev/build/docs/README.md`.

:::{important}
Other structures might exist. Most packages use a single README.md. A small minority use a multi-file structure, for example, one file per cloud service or component. 

<!-- If your package has multiple docs files, edit the one that corresponds to the content you're updating.  -->
If your package has doc files in both `packages/{package}/docs/README.md` _and_ `packages/{package}/_dev/build/docs/README.md`, ensure you edit the source file at `packages/{package}/_dev/build/docs/README.md`. 
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
     elastic-package changelog add --type enhancement --description "Improve documentation" --link "https://github.com/elastic/integrations/pull/123456" --next minor
     elastic-package build
     cd ../..
   done
   git add -u
   git commit -m "docs: update changelogs and build documentation"
   git push
   ```

4. Go back to your editor, and from the integrations repository root folder, paste and run the copied commands.

These commands:
- Build the generated `packages/{package}/docs/README.md` file.
- Update `changelog.yml` with the new entry.
- Update `manifest.yml` with the new version.

If you need to make subsequent edits to your PR, save your changes, then re-run the `elastic-package build` command from the package's root folder (not the integrations root folder) before you push your commits. This ensures the `packages/{package}/docs/README.md` file is updated with your new changes.

::::

::::{step} Request review and merge
Go back to your PR, request a code owner review, and merge it once approved.
::::

::::::

## After merging: When changes appear

After your PR is merged, changes don't appear immediately on the docs site. The process involves several automated steps:

1. **Package publication**: The package is published to the [{{package-registry}} (EPR)](https://github.com/elastic/package-registry). You'll know this is complete when a bot comments on your PR with a message like:

   > Package {package_name} - {version} containing this change is available at https://epr.elastic.co/package/{package_name}/{version}

2. **Docs sync**: A scheduled job in the `elastic/integration-docs` repository pulls the latest packages from EPR and opens an automated PR. This job runs once a day.

3. **Docs build**: Once the automated PR is merged, changes propagate to the docs site.

:::{tip}
If you need changes to appear sooner, you can manually trigger the [update-docs workflow](https://github.com/elastic/integration-docs/actions/workflows/run-update-docs.yml) in the integration-docs repository.
:::

## Special case integrations

Some integrations have documentation source files in repositories other than `elastic/integrations`. These integrations require different workflows.

### {{elastic-defend}}

The [{{elastic-defend}} integration](integration-docs://reference/endpoint.md) (`endpoint`) documentation lives in the [elastic/endpoint-package](https://github.com/elastic/endpoint-package) repository, not `elastic/integrations`.

#### Where to edit

| What you're editing | Repository | File location |
|---|---|---|
| Page content (intro, capabilities, field tables) | [elastic/endpoint-package](https://github.com/elastic/endpoint-package) | `doc_templates/endpoint/docs/README.md` |
| Field schema definitions | [elastic/endpoint-package](https://github.com/elastic/endpoint-package) | `custom_schemas/` directory |
| Frontmatter (`navigation_title`, `applies_to`) | `elastic/integration-docs` | `docs/reference/endpoint.md` |

:::{important}
The page content in `integration-docs/docs/reference/endpoint.md` (everything after the frontmatter) is generated and will be overwritten during the next sync. Only edit the frontmatter section directly in this file.
:::

#### Update {{elastic-defend}} docs

:::{note}
Before you update these docs, ensure you have installed [Go](https://golang.org/dl/). 
:::

::::::{stepper}

::::{step} Clone the endpoint-package repository

```bash
git clone https://github.com/elastic/endpoint-package.git
cd endpoint-package
```

::::

::::{step} Create a branch

```bash
git checkout -b docs-enhancement/my-docs-update
```

::::

::::{step} Edit the template file

Edit `doc_templates/endpoint/docs/README.md`.

This file uses `{{fields "datastream"}}` placeholders that expand into field tables during the build. Available data streams include `alerts`, `file`, `library`, `network`, `process`, `registry`, `security`, `metadata`, `metrics`, and `policy`.

::::

::::{step} Build the package

Save your changes, then run `make` from the repository root to generate the output file.

```bash
make
```

If you encounter build errors related to CGO or missing libraries, try:

```bash
CGO_ENABLED=0 make
```

The build generates `package/endpoint/docs/README.md` from your template.

::::

::::{step} Commit both files

Commit both the source template and the generated output:

```bash
git add doc_templates/endpoint/docs/README.md package/endpoint/docs/README.md
git commit -m "docs: update Elastic Defend documentation"
git push -u origin docs-enhancement/my-docs-update
```

::::

::::{step} Create a PR

Create a PR to the upstream [elastic/endpoint-package](https://github.com/elastic/endpoint-package) repository and request a review from the code owners.

::::

::::::

:::{note}
There is no local preview available from the `endpoint-package` repository. To verify your changes render correctly, wait until the package flows through EPR to the docs site, or ask a teammate with staging environment access to verify.
:::

#### After merging

After your PR merges:

1. The package is published to EPR.
2. A scheduled job in `integration-docs` pulls the updated package and opens an automated PR.
3. Once the automated PR merges, changes appear on the docs site.

## Troubleshooting

### Changes aren't appearing after merge

If your changes don't appear on the docs site after following these steps:

1. **Check for the EPR bot comment**: Look for the bot comment in your PR confirming the package was published to EPR. If you don't see it, the package hasn't been published yet.

2. **Verify the version was bumped**: Ensure your PR included updates to both `changelog.yml` and `manifest.yml`. Without these updates, a new package version won't be published.

3. **Check the integration-docs repository**: Look at recent automated update PRs in the integration-docs repository. If they're failing, your changes won't be pulled until the issues are resolved.

4. **Check version compatibility**: Check if the integration's `manifest.yml` specifies a {{kib}} version that hasn't been released yet. For example, if `^9.3.0` before 9.3 is released, the docs won't appear until that version is live.

### The edit helper check is missing

If you can't find the edit helper check on your PR, ensure your branch name follows the `docs-enhancement/` pattern.

### Build failures in integration-docs

Sometimes the automated PR in integration-docs fails due to new integrations that need to be added to `nav.yaml`. These failures block all docs updates until resolved. If you notice this, reach out to the docs team for assistance.

### My changes to integration-docs were overwritten

If you edited a file in `integration-docs/docs/reference/` directly and your changes disappeared, the file is likely generated from another source:

- **For {{elastic-defend}} (`endpoint.md`)**: Edit in [elastic/endpoint-package](https://github.com/elastic/endpoint-package) instead. Refer to [{{elastic-defend}}](#elastic-defend).
- **For other integrations**: Edit in [elastic/integrations](https://github.com/elastic/integrations). Refer to [Update the docs](#update-the-docs).

The `integration-docs` repository pulls generated content from EPR and adds frontmatter and navigation. Direct edits to generated files will be overwritten on the next sync.
