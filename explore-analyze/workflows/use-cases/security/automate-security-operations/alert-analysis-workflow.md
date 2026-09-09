---
navigation_title: Alert analysis workflow
applies_to:
  stack: experimental 9.5+
  serverless: experimental
description: Configure the Elastic-managed Security alert analysis workflow that classifies alerts with AI, writes verdicts to notes and tags, and can auto-close high-confidence false positives.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
  - id: security
---

# Alert analysis workflow [workflows-alert-analysis-workflow]

The **Alert analysis workflow** is a [managed workflow](/explore-analyze/workflows/managed-workflows.md) for {{elastic-sec}}. When a detection rule that has the workflow attached generates an alert, or when you run the workflow manually, the workflow gathers related context, sends it to an {{agent-builder}} agent, and writes a classification verdict (true positive, false positive, or inconclusive) back to the alert, including confidence and rationale.

Elastic installs a single shared workflow definition that's available in every {{kib}} space, including spaces created later. Elastic maintains the YAML, and you configure how the workflow runs per space on the **Alert analysis workflow** settings page.

## Before you begin [workflows-alert-analysis-prereqs]

You must have the appropriate subscription. Refer to the subscription page for [Elastic Cloud](https://www.elastic.co/subscriptions/cloud) and [Elastic Stack/self-managed](https://www.elastic.co/subscriptions) for the breakdown of available features and their associated subscription tiers.

To open and save the **Alert analysis workflow** settings page, you also need the following [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md):

- `All` for **Management → Advanced Settings**.
- `All` for **Security → Rules and Exceptions**.
- **Update managed workflows** under **Analytics → Workflows → Managed Workflows Actions**.

You also need a configured [AI connector](/deploy-manage/manage-connectors.md) for the agent to call.

To view the managed workflow itself on the **Workflows** page, turn on the [**Show managed workflows**](kibana://reference/advanced-settings.md#kibana-workflows-settings) advanced setting and grant managed read privileges. Refer to [Show managed workflows](/explore-analyze/workflows/get-started/setup.md#workflows-managed-visibility).


## How it works [workflows-alert-analysis-how-it-works]

For each alert it analyzes, the workflow:

1. Gathers context such as related alerts, rule and MITRE details, how similar alerts were closed, and how noisy the rule is.
2. Sends that context to an LLM through {{agent-builder}}.
3. Writes a started note on the alert's notes, then updates it with a verdict (true positive, false positive, or inconclusive, with confidence and rationale) or an error note if analysis fails.
4. Adds workflow tags to the alert. The tag prefix is configurable and defaults to `alert-analysis`.
5. Auto-closes the alert when the verdict is a high-confidence false positive within the configured confidence range (on by default; range defaults to 0.85–1).
6. Creates an {{agent-builder}} conversation and links it from the verdict note (on by default).


## Set up the workflow [workflows-alert-analysis-setup]

To configure the **Alert analysis workflow** in the current space and attach it to detection rules, follow these steps:

:::::{stepper}

::::{step} Open the settings page
Find **Alert analysis workflow** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::{tip}
In the page description, you can select **View workflow** to open the managed workflow definition. The YAML is read-only.
:::

::::

::::{step} Configure the workflow
Set how the workflow runs in the current space:

| Setting | Description |
|---------|-------------|
| **Workflow enabled** | Turns the workflow on or off everywhere it is configured, including for any rules it is attached to. Defaults to on. |
| **AI connector** | The AI connector used to classify alerts. |
| **Agent** | The {{agent-builder}} agent that analyzes alerts. Defaults to the built-in Elastic AI Agent. The list includes that default plus your custom agents. |
| **Create conversation** | When on, the agent creates a new conversation for each alert analysis. Defaults to on. Turn off to avoid accumulating large numbers of conversations. |
| **Auto-close alerts classified as false positives** | When on, the workflow automatically closes alerts classified as false positives within the configured confidence range. Defaults to on. |
| **Auto-close minimum confidence score** | Lowest false-positive confidence score (0–1) that can auto-close an alert. Defaults to `0.85`. Must be lower than the maximum when auto-close is on. |
| **Auto-close maximum confidence score** | Highest false-positive confidence score (0–1) that can auto-close an alert. Defaults to `1`. |
| **Alert tag prefix** | Prefix for tags the workflow adds to analyzed alerts (default `alert-analysis`). Example: `alert-analysis.classification.false_positive`. The field can't be empty. If you change the prefix, alerts tagged under the old prefix are no longer recognized as already analyzed. |

Click **Save alert analysis workflow settings** to persist changes for the current space.
::::

::::{step} Attach the workflow to detection rules
The settings page includes a **Detection rules** section, where you can search rules by name, filter them by attachment status, and bulk attach or remove the workflow from rules.

You can also attach the workflow from the rule settings, the same way as any other workflow. Refer to [](/explore-analyze/workflows/triggers/alert-triggers.md#configure-the-alert-rule) for more information.
::::

:::::

## Run the workflow [workflows-alert-analysis-run]

After you attach the workflow to detection rules, it runs automatically when those rules generate alerts. You can also [run it on demand](/explore-analyze/workflows/authoring-techniques/manage-workflows.md#workflow-run) from the **Workflows** page.

## Where results appear [workflows-alert-analysis-results]

After the workflow runs, look in these places for the classification output and execution details:

| Result | Where to look |
|--------|----------------|
| Started, verdict, or error note | **Alerts** → alert details → **Notes**. If a conversation was created, the verdict note links to it. |
| Workflow tags | Alert tags (`kibana.alert.workflow_tags`) on the alert, for example in the alert details **Table** tab. |
| Auto-close | Alert status and close reason, when the verdict is a false positive within your confidence range. |
| Execution history | **Workflows** → open the workflow → **Executions**. |

## Related pages [workflows-alert-analysis-related]

- [View detection alert details](/solutions/security/detect-and-alert/view-detection-alert-details.md): Find notes, tags, and other alert fields after a run.
- [Triage alerts with an AI agent](/explore-analyze/workflows/use-cases/security/automate-security-operations/ai-driven-alert-triage.md): Build your own AI triage workflow.
