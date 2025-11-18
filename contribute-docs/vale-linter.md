---
navigation_title: Vale linter
---

# Elastic style guide for Vale

[Vale](https://github.com/errata-ai/vale) is an open source prose linter that checks the content of documents in several formats against style guide rules. The goal of a prose linter is automating style guide checks in docs-as-code environments, so that style issues are detected before deploy or while editing documentation in a code editor.

The Elastic Vale package contains a set of linting rules based on the Elastic style guide and recommendations.

## Get started

Run these commands to install the Elastic style guide locally:

::::{tab-set}

:::{tab-item} macOS

```bash
curl -fsSL https://raw.githubusercontent.com/elastic/vale-rules/main/install-macos.sh | bash
```

:::

:::{tab-item} Linux

```bash
curl -fsSL https://raw.githubusercontent.com/elastic/vale-rules/main/install-linux.sh | bash
```

:::

:::{tab-item} Windows

```powershell
Invoke-WebRequest -Uri https://raw.githubusercontent.com/elastic/vale-rules/main/install-windows.ps1 -OutFile install-windows.ps1
powershell -ExecutionPolicy Bypass -File .\install-windows.ps1
```

:::
::::

:::{warning}
The installation script might overwrite your existing global Vale configuration. Install the style manually if you're using styles other than Elastic.
:::

### Install the Visual Studio Code extension

Install the [Vale VSCode](https://marketplace.visualstudio.com/items?itemName=ChrisChinchilla.vale-vscode) extension to view Vale checks when saving a document. The extension is also available for other editors that support the Open VSX Registry.

## Add the Vale action to your repo

Add the Elastic Vale linter to your repository's CI/CD pipeline using a two-workflow setup that supports fork PRs:

```yaml
# .github/workflows/vale-lint.yml
name: Vale Documentation Linting

on:
  pull_request:
    paths:
      - '**.md'
      - '**.adoc'

permissions:
  contents: read

jobs:
  vale:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v5
        with:
          fetch-depth: 0
      
      - name: Run Vale Linter
        uses: elastic/vale-rules/lint@main
```

```yaml
# .github/workflows/vale-report.yml
name: Vale Report

on:
  workflow_run:
    workflows: ["Vale Documentation Linting"]
    types:
      - completed

permissions:
  pull-requests: read

jobs:
  report:
    runs-on: ubuntu-latest
    if: github.event.workflow_run.event == 'pull_request'
    permissions:
      pull-requests: write
    
    steps:
      - name: Post Vale Results
        uses: elastic/vale-rules/report@main
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

For detailed documentation and examples, refer to [ACTION_USAGE.md](https://github.com/elastic/vale-rules/blob/main/ACTION_USAGE.md).

## Exclude content from linting

You can use HTML comments in your Markdown files to control Vale's behavior for specific sections of content. This is useful when you need to temporarily turn off checks or exclude certain content from linting.

### Turn off all Vale checks

To exclude a section of content from linting, wrap it with `vale off` and `vale on` comments:

```markdown
<!-- vale off -->

This entire section will be ignored by Vale.

<!-- vale on -->
```

### Turn off a specific rule

To turn off a specific Elastic style rule for a section, use the rule name with `= NO` and `= YES` to turn it back on:

```markdown
<!-- vale Elastic.RuleName = NO -->

This content will ignore only the specified rule.

<!-- vale Elastic.RuleName = YES -->
```

For example, to turn off the `Elastic.WordChoice` rule:

```markdown
<!-- vale Elastic.WordChoice = NO -->

This section can contain mispellings without triggering warnings.

<!-- vale Elastic.WordChoice = YES -->
```

:::{tip}
You can find the exact rule names in the [Elastic Vale rules repository](https://github.com/elastic/vale-rules/tree/main/styles/Elastic). Each rule is defined in a separate `.yml` file, and the filename (without the extension) is the rule name you use in comments.
:::

For more information about comment-based configuration, refer to the [Vale Markdown documentation](https://vale.sh/docs/formats/markdown#comments).

## Update the style guide

To update the Elastic style guide to the latest rules, rerun the installation script.

## Resources

- [Vale's official documentation](https://vale.sh/docs/vale-cli/overview/)
- [Elastic Vale rules repository](https://github.com/elastic/vale-rules)

