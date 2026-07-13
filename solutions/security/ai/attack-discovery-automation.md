---
navigation_title: Automate Attack Discovery
description: Run Attack Discovery on a schedule, from an Elastic Workflow, or from an Agent Builder chat, and migrate existing schedules to the skill-augmented pipeline.
applies_to:
  stack: ga 9.5
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Automate Attack Discovery [automate-attack-discovery]

Beyond running Attack Discovery manually from the [Attack Discovery](/solutions/security/ai/attack-discovery.md) page, you can automate it so it runs continuously or as part of a larger response process. Every automated path—a schedule, a workflow step, or a chat request—triggers the same audited pipeline as a manual run.

The following table can help you choose an automated path:

| Method | Use when | Where it runs |
|---|---|---|
| Schedule | You want continuous, hands-off coverage | Alerting framework |
| Workflow step | You're embedding Attack Discovery in a larger SOC automation | [Elastic Workflows](/explore-analyze/workflows.md) |
| Chat | You want Attack Discovery on demand during an investigation | {{agent-builder}} |


## Before you begin [automate-ad-before-you-begin]

- You need the same privileges as manual Attack Discovery use. Refer to [Role-based access control (RBAC) for Attack Discovery](/solutions/security/ai/attack-discovery.md#attack-discovery-rbac).

  <!-- TODO(writer): confirm whether Workflows and Agent Builder triggers require additional Kibana privileges beyond the base Attack Discovery RBAC (for example, a Workflows execute privilege), and add them here. -->

- Enable the `securitySolution.attackDiscoveryWorkflowsEnabled` advanced setting, which is off by default.
- Have a working [LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md).
- To run Attack Discovery from a workflow, make sure you meet the [Workflows prerequisites](/explore-analyze/workflows/get-started.md).


## Schedule recurring discoveries [schedule-ad]

Set a schedule once, and a skill-augmented run kicks off automatically every N hours. Discoveries land on the [Attack Discovery](/solutions/security/ai/attack-discovery.md) and [Attacks](/solutions/security/ai/attacks-page.md) pages, and notifications route to any Alerting Framework connector you've configured, such as Slack, Microsoft Teams, PagerDuty, ServiceNow, Jira, email, or a webhook.

For setup steps, refer to [Schedule discoveries](/solutions/security/ai/attack-discovery.md#schedule-discoveries).

<!-- TODO(writer): confirm the exact connector list—the source issue lists Slack, ServiceNow, Jira, PagerDuty, Cases, Email, and Webhook, but flags it as "to be confirmed." Verify against the shipped Alerting Framework connector list before publishing. -->


## Run Attack Discovery from a workflow [run-ad-from-workflow]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

You can call Attack Discovery from an [Elastic Workflow](/explore-analyze/workflows.md) using a built-in step, so you can embed it in a larger SOC automation—for example, triggering a run when an alert threshold is met, then acting on the resulting discoveries in the same workflow.

<!-- TODO(writer): confirm the exact step type ID and its YAML usage against the Kibana source before publishing. The source issue names it `security.attack-discovery.run`, but other built-in Workflows steps documented in explore-analyze/workflows/steps/kibana.md use PascalCase action names within a namespace (for example, `kibana.SetAlertsStatus`), not hyphenated lowercase—the final ID may not match the issue's shorthand. -->

```yaml
- name: run_attack_discovery
  type: security.attack-discovery.run
  with:
    connector_id: <your-llm-connector-id>
```

Refer to [Workflow steps](/explore-analyze/workflows/steps.md) for how built-in steps work, and to [Compose workflows](/explore-analyze/workflows/authoring-techniques/compose-workflows.md) for combining Attack Discovery with other steps.


## Run Attack Discovery from a chat [run-ad-from-chat]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

You can trigger an Attack Discovery run conversationally, from an {{agent-builder}} chat, without leaving your investigation. Conversations that trigger a run are stored in {{agent-builder}}, alongside its other chat history.

<!-- TODO(writer): document the conversation-visibility limitation once confirmed—the source issue notes there's currently no way to control who can see a conversation that triggered a run, and that a per-space visibility setting is still in development. Don't publish a workaround until that setting ships or is confirmed out of scope for 9.5. -->

Refer to [{{agent-builder}}](/solutions/security/ai/agent-builder/agent-builder.md) for how to start and manage chats.


## View system workflows [ad-system-workflows]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

Attack Discovery's default retrieval and validation logic runs as a system workflow. You can view these workflows—including their steps—from the workflow run step, but you can't edit them through the workflow editor or API. If you have questions about what a system workflow does, ask about it in the chat panel.


## Customize retrieval and validation workflows [customize-ad-workflows]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

You can author your own workflows to customize two parts of the Attack Discovery pipeline:

- **Retrieval**—supply your own alert-retrieval logic using the **Alert retrieval workflows** toggle. Refer to [Flexible alert retrieval](/solutions/security/ai/attack-discovery.md#set-up-attack-discovery).
- **Validation**—add final verification or enrichment before discoveries are persisted, conceptually similar to a detection rule's actions.

<!-- TODO(writer): confirm the 9.5 status of natural-language workflow authoring for this use case—the source issue notes NL authoring is tech preview and may not be usable to author system-workflow replacements yet. -->


## Migrate to the new Attack Discovery experience [migrate-ad]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

Enabling `securitySolution.attackDiscoveryWorkflowsEnabled` layers skill-augmented retrieval, corroboration, and raw-log enrichment onto your existing Attack Discovery setup. It doesn't disrupt anything already running:

- Your existing schedules keep running on the previous retrieval path until you migrate them.
- Existing discoveries, connectors, and sharing settings are unaffected.

<!-- TODO(writer): this section is largely blocked pending migration-flow clarification from engineering—the source issue flags the migration steps themselves, and what happens to existing discoveries/settings during migration, as open items. Do not publish prescriptive migration steps until confirmed. Once available, document: (1) how to migrate an existing schedule, (2) what changes for end users after migrating, (3) when/whether the pre-9.5 retrieval path will be removed. -->


## Next steps [automate-ad-next-steps]

- [Generate discoveries manually](/solutions/security/ai/attack-discovery.md#attack-discovery-generate-discoveries)
- [Triage and manage attacks](/solutions/security/ai/attacks-page.md)
- [Elastic Workflows](/explore-analyze/workflows.md)
- [{{agent-builder}}](/solutions/security/ai/agent-builder/agent-builder.md)
- [AI-driven alert triage workflow](/explore-analyze/workflows/use-cases/security/automate-security-operations/ai-driven-alert-triage.md)
