---
navigation_title: AI agent skills
description: Install and use official Elastic agent skills to help AI coding agents work with the Elastic stack more accurately and efficiently.
applies_to:
  stack: ga
  serverless: ga
---

# AI agent skills for Elastic [elastic-agent-skills]

```{applies_to}
product: preview
```

The [elastic/agent-skills](https://github.com/elastic/agent-skills) repository provides official, open-source skill packages that help AI coding agents work with the Elastic stack. Built on the [Agent Skills](https://agentskills.io/) open standard, they give agents like Claude Code, Cursor, GitHub Copilot, and others the specialized knowledge they need to perform Elastic-specific tasks more accurately and efficiently.

Skills cover areas such as interacting with {{es}} APIs, building {{kib}} dashboards, configuring {{fleet}} policies, and working with {{observability}} and {{elastic-sec}} workflows.

## What are AI agent skills?

AI agent skills are a lightweight, open format for extending AI agent capabilities with specialized knowledge. Each skill is a self-contained folder with a `SKILL.md` file containing metadata and instructions. 

Agents discover available skills at startup by reading their `name` and `description` fields, then load full instructions on demand when a matching task is detected.

This approach keeps agents fast by default while giving them access to deep, procedural knowledge when needed.

For more background on the standard, refer to [agentskills.io](https://agentskills.io/).

## Available skills

Skills in the [elastic/agent-skills](https://github.com/elastic/agent-skills) repository focus on Elastic products and the Elastic stack:

- Interacting with {{es}} APIs (search, indexing, cluster management).
- Building and managing {{kib}} dashboards, saved objects, and visualizations.
- Configuring {{fleet}} policies, {{agent}} integrations, and {{beats}} pipelines.
- Patterns for {{observability}}, {{elastic-sec}}, and {{product.apm}} workflows.

## Installation

Follow the instructions below to install AI agent skills.

### npx (recommended)

The fastest way to install skills is with the `skills` CLI. Run the following command to launch an interactive prompt where you can select skills and target agents:

```bash
npx skills add elastic/agent-skills
```

Install a specific skill by name:

```bash
npx skills add elastic/agent-skills --skill elasticsearch-esql
```

Or use the `@` shorthand:

```bash
npx skills add elastic/agent-skills@elasticsearch-esql
```

Install to specific agents:

```bash
npx skills add elastic/agent-skills -a cursor -a claude-code
```

List available skills without installing:

```bash
npx skills add elastic/agent-skills --list
```

Install all skills to all agents without prompts:

```bash
npx skills add elastic/agent-skills --all
```

| Flag | Description |
| --- | --- |
| `-a, --agent` | Target specific agents. |
| `-s, --skill` | Install specific skills by name. |
| `-g, --global` | Install to user home instead of project directory. |
| `-y, --yes` | Skip confirmation prompts. |
| `--all` | Install all skills to all agents without prompts. |
| `--list` | List available skills without installing. |

### Local clone

If you prefer to work from a local checkout, or your environment does not have Node.js or npx, clone the repository and use the bundled bash installer:

```bash
git clone https://github.com/elastic/agent-skills.git
cd agent-skills
./scripts/install-skills.sh add -a <agent>
```

The script requires bash 3.2+ and standard Unix utilities (`awk`, `find`, `cp`, `rm`, `mkdir`).

| Flag | Description |
| --- | --- |
| `-a, --agent` | Target agent (repeatable). |
| `-s, --skill` | Install specific skills by name. |
| `-f, --force` | Overwrite already-installed skills. |
| `-y, --yes` | Skip confirmation prompts. |

## Supported agents

The following AI coding agents are compatible with the Agent Skills format:

| Agent | Install directory |
| --- | --- |
| Claude Code | `.claude/skills` |
| Cursor | `.agents/skills` |
| Codex | `.agents/skills` |
| OpenCode | `.agents/skills` |
| Windsurf | `.windsurf/skills` |
| Roo | `.roo/skills` |
| Cline | `.agents/skills` |
| GitHub Copilot | `.agents/skills` |
| Gemini CLI | `.agents/skills` |

## Keep skills up to date

Skills are copied into your project or home directory at install time. When the repository is updated with new instructions, bug fixes, or additional resources, those changes are not automatically synced to your local copies.

### Using npx

Check whether any installed skills have changed upstream:

```bash
npx skills check
```

Pull the latest versions of all installed skills:

```bash
npx skills update
```

:::{tip}
The default npx installation uses symlinks, so every agent points to a single canonical copy. Updating once refreshes all agents at the same time.
:::

### Using a local clone

Re-run the installer with `--force` to overwrite existing skills:

```bash
git pull
./scripts/install-skills.sh add -a <agent> --force
```

Without `--force`, the script skips skills that are already installed.

## Issues and feedback

Found a problem or have a suggestion? [Open an issue](https://github.com/elastic/agent-skills/issues/new) on the `elastic/agent-skills` repository.
