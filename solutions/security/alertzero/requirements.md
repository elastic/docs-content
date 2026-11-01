---
navigation_title: Requirements
description: "Check what every space needs before you set up AlertZero in Elastic Security, and what specific Workers need."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# {{alertzero}} requirements [alertzero-requirements]

Check these requirements before you [set up {{alertzero}}](set-up-alertzero.md). {{alertzero}} requires the Security Analytics Complete [feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md#elastic-sec-project-features) in {{serverless-short}} or an Enterprise [subscription](https://www.elastic.co/subscriptions) on {{stack}}.

Not everything on this page applies to you:

- [What every space needs](#alertzero-requirements-every-space): Complete these in each space before you set up {{alertzero}}.
- [What specific {{az-workers}} need](#alertzero-requirements-specific-workers): Complete only the parts for the {{az-workers}} you plan to turn on.

## What every space needs [alertzero-requirements-every-space]

Complete these in each space where you want to use {{alertzero}}, before you set it up. You turn on {{alertzero}} itself later, during [setup](set-up-alertzero.md#alertzero-turn-on).

### Security solution view [alertzero-requirements-space]
```{applies_to}
serverless: unavailable
```

{{alertzero}} works only in spaces that use the **Security** solution view. In any other view, including **Classic**, the message "{{alertzero}} is not available in this space" appears instead. To set a space's solution view, refer to [Create a space](/deploy-manage/manage-spaces.md#spaces-managing).

### AI model [alertzero-requirements-ai-model]

The space needs at least one AI model that {{alertzero}} can use, such as an [Elastic Managed LLM](kibana://reference/connectors-kibana/elastic-managed-llm.md) or an [External Inference](/explore-analyze/elastic-inference/external.md) model. You can't turn on {{az-workers}} until a model is available. To connect a model, refer to [Connect to an LLM](/solutions/security/ai/set-up-ai-features.md#set-up-ai-llm).

Choosing a model for each kind of task is optional, and you can do it later. Find **Feature Settings** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). In the **{{alertzero}}** section, set **{{az-efficient-models}}**, **{{az-balanced-models}}**, **{{az-frontier-models}}**, and **{{az-cyber-domain-models}}**. Refer to [Feature settings](/explore-analyze/ai-features/manage-access-to-ai-assistant.md#feature-settings).

### Security data [alertzero-requirements-security-data]

{{az-workers}} analyze the security data you ingest. If the space has no data yet, add it before you set up {{alertzero}}, or the {{az-workers}} have nothing to analyze. Refer to [](/solutions/security/get-started/ingest-data-to-elastic-security.md).

### Privileges to set up {{alertzero}} [alertzero-requirements-setup-access]

Setting up {{alertzero}} needs privileges that most roles don't include, so you might need an administrator to do it. Refer to [](alertzero-privileges.md).

## What specific {{az-workers}} need [alertzero-requirements-specific-workers]

Some {{az-workers}} need more than every space does. Complete only the parts for the {{az-workers}} you plan to turn on, and skip the rest. If the {{az-workers}} you turn on are missing something, their {{az-watch}} pages show a warning, so you can also come back to this section then.

### Settings that are off by default [alertzero-requirements-worker-settings]

Turn on these settings in each space where the {{az-workers}} run:

| {{az-worker}} | Turn on |
| --- | --- |
| {{az-alert-triage}} | The [Alert analysis workflow](/explore-analyze/workflows/use-cases/security/automate-security-operations/alert-analysis-workflow.md) |
| {{az-attack-discovery}} | Attack Discovery workflows (`securitySolution:enableAttackDiscoveryWorkflows`) and [{{context-engine}}](/explore-analyze/ai-features/context-engine.md) (`contextEngine:enabled`) |
| {{az-continuous-threat-hunt}}, {{az-rule-coverage}}, and {{az-endpoint-analysis}} | [{{context-engine}}](/explore-analyze/ai-features/context-engine.md) (`contextEngine:enabled`) |

The {{az-workers}} that need {{context-engine}} use it to pass detection gaps and forensics handoffs to each other. Refer to [](watches-and-workers.md).

% After elastic/docs-content#9118 merges, link "Refer to" above to watches-and-workers.md#alertzero-context-engine.

### Data that specific {{az-workers}} need [alertzero-requirements-data]

- **Detection alerts and rules:** The {{az-alert-triage}} and {{az-attack-discovery}} {{az-workers}} analyze the alerts your detection rules create, and the {{az-detection-watch}} improves the rules themselves. Refer to [](/solutions/security/detect-and-alert/turn-on-detections.md).
- **{{elastic-defend}} data:** The {{az-endpoint-analysis}} {{az-worker}} needs {{elastic-defend}} data from the hosts it analyzes. Refer to [](/solutions/security/configure-elastic-defend/install-elastic-defend.md).

### {{az-workers}} that need other {{az-workers}} [alertzero-requirements-dependencies]

Some {{az-workers}} work on what another {{az-worker}} produces. For each {{az-worker}} you turn on in the first column, turn on the {{az-worker}} it needs too.

| {{az-worker}} | Needs | Why |
| --- | --- | --- |
| {{az-rule-coverage}} | {{az-continuous-threat-hunt}} | It works on the detection gaps that {{az-continuous-threat-hunt}} finds. |
| {{az-endpoint-analysis}} | {{az-attack-discovery}} | It analyzes only the attacks that {{az-attack-discovery}} hands off. |
| {{az-attack-discovery}} | {{az-endpoint-analysis}} | It hands off attacks it can't rule out as false positives. If {{az-endpoint-analysis}} is off, those attacks stay unanalyzed, and their {{az-investigations}} stay open. |

To turn {{az-workers}} on or off after setup, refer to [](configure-worker-settings.md#alertzero-worker-on-off).
