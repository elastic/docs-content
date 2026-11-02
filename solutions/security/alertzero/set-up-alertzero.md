---
description: "Turn on AlertZero in an Elastic Security space, then use onboarding to start its Workers."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# Set up {{alertzero}} [alertzero-set-up]

{{alertzero}} is off by default, and you set it up separately in each space. First turn on its advanced setting, then let onboarding guide you through starting the {{az-workers}}.

## Before you begin [alertzero-set-up-before]

Every setup needs the same privileges and an AI model. What else you need depends on which {{az-workers}} you run.

### Required for every setup [alertzero-set-up-before-all]

You need all of the following:

- **All** for **Advanced Settings**, to turn on the {{alertzero}} setting.
- The `manage_security` cluster privilege, to start the {{az-workers}}. None of the {{serverless-short}} predefined roles includes it.
- At least one AI model in the space, to start the {{az-workers}}. Refer to [Connect to an LLM](/solutions/security/ai/set-up-ai-features.md#set-up-ai-llm).

If you don't have `manage_security`, ask an administrator who does to start the {{az-workers}}. Don't grant it only for {{alertzero}}, because it also lets anyone who has it manage users and roles for the whole cluster. For all {{alertzero}} privileges, refer to [](alertzero-privileges.md).

% After elastic/docs-content#9115 merges, link the privileges reference to alertzero-privileges.md#alertzero-privileges-configure.

### Required for specific {{az-workers}} [alertzero-set-up-before-workers]

Each {{az-worker}} works from different data, and some need extra setup, such as [{{context-engine}}](/explore-analyze/ai-features/context-engine.md). Check what each {{az-worker}} you plan to run needs:

| {{az-worker}} | Works from | Also needs |
| --- | --- | --- |
| [{{az-alert-triage}}](watches-and-workers.md#alertzero-triage-watch) | Alerts from your detection rules that are waiting to be triaged | The [Alert analysis workflow](/explore-analyze/workflows/use-cases/security/automate-security-operations/alert-analysis-workflow.md) turned on |
| [{{az-attack-discovery}}](watches-and-workers.md#alertzero-triage-watch) | Alerts from your detection rules | The [**Attack Discovery Workflows**](kibana://reference/advanced-settings.md#kibana-siem-settings) advanced setting turned on in the space, and {{context-engine}} |
| [{{az-continuous-threat-hunt}}](watches-and-workers.md#alertzero-hunt-watch) | Events in the indices that the [`securitySolution:defaultIndex`](kibana://reference/advanced-settings.md#kibana-siem-settings) advanced setting lists. If you added index patterns to that setting, it can read only the ones that match the setting's default patterns, such as `logs-*`. | {{context-engine}}, outbound HTTPS access from {{kib}} to the [supported threat feeds](watches-and-workers.md#alertzero-hunt-watch), and a model selected for **Efficient models** and **Frontier models** in [**Feature Settings**](/explore-analyze/ai-features/manage-access-to-ai-assistant.md) in the default space |
| [{{az-rule-tuning}}](watches-and-workers.md#alertzero-detection-watch) | Alerts marked as false positives, by {{az-alert-triage}} or by your analysts | Nothing else |
| [{{az-rule-coverage}}](watches-and-workers.md#alertzero-detection-watch) | Detection gaps that {{az-continuous-threat-hunt}} records | {{context-engine}} |
| [{{az-endpoint-analysis}}](watches-and-workers.md#alertzero-forensics-watch) | Attacks that {{az-attack-discovery}} hands off | {{elastic-defend}} and {{context-engine}} |

% After elastic/docs-content#9144 merges, link each Worker to its own anchor (for example, watches-and-workers.md#alertzero-alert-triage) and the threat feeds to watches-and-workers.md#alertzero-threat-feeds.

{{az-rule-coverage}} and {{az-endpoint-analysis}} only work on what other {{az-workers}} produce, so turn those {{az-workers}} on too.

If you haven't added data to {{elastic-sec}} yet, onboarding links to where you can add it. Refer to [](/solutions/security/get-started/ingest-data-to-elastic-security.md).

## Turn on {{alertzero}} for a space [alertzero-turn-on]

1. In the space where you want {{alertzero}}, find **Advanced Settings** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the **Security Solution** section, turn on the **{{alertzero}}** setting (`securitySolution:enableAlertZero`).
3. Select **Save changes**, then select **Reload page**.

% For the setting's details, refer to the [advanced settings reference](kibana://reference/advanced-settings.md#securitysolution-enablealertzero).

**{{alertzero}}**, **{{az-escalations-cap}}**, and **{{az-watches}}** appear in the {{elastic-sec}} navigation menu.

## Start the {{az-workers}} [alertzero-turn-on-workers]

1. In the navigation menu, select **{{alertzero}}**. The first time you open it in a space, onboarding starts.
2. Follow the onboarding steps, and turn off any {{az-workers}} you decided not to run. All of them start out selected, and at least one has to stay selected. Onboarding flags any {{az-worker}} that's missing {{context-engine}}.
3. Select **Enable and run**.

The {{az-workers}} start their first run right away, and {{alertzero}} opens the **{{az-proposed-actions-cap}}** page. That's where their {{az-proposed-actions}} appear when they need your decision.

To change which {{az-workers}} run later, refer to [](configure-worker-settings.md).

% After elastic/docs-content#9144 merges, link configure-worker-settings.md#configure-worker-settings-enabled.

## Next steps [alertzero-set-up-next]

- [](alertzero-privileges.md): Give your team the privileges they need to view and decide {{az-proposed-actions}}.
- [](use-alertzero.md): Find the {{az-proposed-actions}} that need your decision.
- [](configure-worker-settings.md): Change {{az-worker}} settings, such as {{az-autonomy}} and schedule.
