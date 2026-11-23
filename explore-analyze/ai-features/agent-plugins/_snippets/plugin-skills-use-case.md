The plugin contains agent skills that are synced from the [elastic/agent-skills](https://github.com/elastic/agent-skills) repository.
When you install them through the plugin, these skills stay up to date. Skills that you install directly from the `agent-skills` repository stay at the version you installed.
Refer to [AI agent skills for Elastic](/explore-analyze/ai-features/agent-skills.md) for how skills work and the areas they cover.

The agent decides when to use a skill based on your request.
You can also run a skill directly by typing `/` followed by the skill name in the chat, for example {subs}`{{skill-command-example}}`.

After you install the plugin, these skills give the agent the procedural knowledge to perform common Elastic tasks without leaving {{plugin-host}}:

- Write and run {{esql}} queries against a live cluster.
- Build and manage {{kib}} dashboards, alerting rules, and workflows.
- Onboard a service into {{observability}} using {{edot}}.
- Triage {{elastic-sec}} alerts and manage cases.
- Provision {{ecloud}} resources and manage user access.

Most of these skills run their operations through the [Elastic CLI](cli://index.md), which you install and configure separately.

To compare the plugin with installing skills directly from [elastic/agent-skills](https://github.com/elastic/agent-skills), refer to [Elastic plugins for AI agents](/explore-analyze/ai-features/agent-plugins.md#plugins-compared-to-installing-skills-directly).
