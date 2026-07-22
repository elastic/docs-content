---
navigation_title: Run from a workflow
description: "Run Attack Discovery as a step inside an Elastic workflow."
applies_to:
  stack: ga 9.5+
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Run Attack Discovery from a workflow [run-attack-discovery-in-a-workflow]

You can run Attack Discovery as a step in an Elastic workflow (`security.attack-discovery.run`). The step uses the same analysis as manual and scheduled runs, so you can fold it into larger automations and branch later steps on how many discoveries were created.

`security.attack-discovery.run` generates discoveries. It does not set status, assignees, or tags on alerts or attacks. Those triage actions use separate Attack triage steps such as `security.setAttackStatus`, `security.assignAttack`, and `security.setAttackTags`.
<!-- FLAG: Uncomment after docs-content#7449 merges: Refer to [Attack triage action steps](/explore-analyze/workflows/steps/attack-triage.md). -->

For chat-based investigation, use [Run Attack Discovery from {{agent-builder}}](/solutions/security/ai/attack-discovery/run-attack-discovery-from-agent-builder.md).

## Before you begin [run-ad-workflow-before-you-begin]

To run Attack Discovery from a workflow, you need:

* The [**Attack Discovery Workflows**](/solutions/security/get-started/configure-advanced-settings.md#enable-attack-discovery-workflows) advanced setting turned on.
* A role with the [index privileges](/solutions/security/ai/attack-discovery/grant-access.md#ad-index-privileges) required to generate and read discoveries, and these [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md#adding_kibana_privileges) at minimum:
  * **Security > Attack discovery**: `All`
  * **Security > Rules and Exceptions**: `Read`
  * **Security > Alerts**: `Read`
  * **Analytics > Workflows**: `All`

## Configure the Attack Discovery step [run-ad-workflow-configure-step]

When you add `security.attack-discovery.run` to a workflow, you set the same kinds of options in the step that you would set in the **Attack discovery settings** flyout. You define them once in the Workflows editor (or in the step's YAML `with` block). On each run, the step uses those values. You can hardcode them in the step, or fill them from an earlier step or workflow variable.

For example, the step can specify:

* Which alerts to analyze (alerts from an earlier step, the skill, an {{esql}} query, or a custom query)
* The time range and filter for that analysis
* Which LLM connector to use, if you want to override the default
* Which validation workflow to run after generation

Along with those options, choose whether Attack Discovery runs synchronously or asynchronously:

* **Synchronously**: The workflow waits briefly for the run to finish so later steps can use the discoveries right away. Use this when the next step depends on the results, such as branching on discovery count or updating attack status.
* **Asynchronously**: The step returns immediately with a run ID, and discoveries keep saving in the background. Use this when you only need to start the analysis and don't need the discoveries in later steps of this workflow.

## Audit runs and approve detection gap proposals [run-ad-workflow-when-it-runs]

When the workflow runs, Attack Discovery uses those settings and the same analysis as manual and scheduled runs. Each time the Attack Discovery skill runs, {{agent-builder}} opens a new conversation for that run. Open that conversation from the workflow execution details to audit the run or to [review and approve detection rule proposals](/solutions/security/ai/attack-discovery/run-attack-discovery-from-agent-builder.md#run-ad-conversation-gap-closure) in chat. You cannot approve those proposals inside the workflow itself.

With a synchronous run, later steps can branch on the results, including Attack triage steps for status, assignees, or tags.

## Work with built-in Attack Discovery workflows [run-ad-workflow-built-in]

Elastic provides system-managed workflows that cover retrieval, generation, and validation. These workflows are hidden from the main workflow list by default. You can still open them directly by URL.

You can enable or disable built-in workflows, but you cannot edit or delete them.

## Create custom retrieval and validation workflows [run-ad-workflow-custom]

You can plug in your own workflows for alert retrieval or validation:

* **Custom retrieval**: Build a workflow that returns the alerts Attack Discovery should analyze. Select it under **Alert retrieval workflows** in the [Attack discovery settings](/solutions/security/ai/attack-discovery/configure-alert-retrieval-from-attacks-page.md#attacks-page-alert-retrieval-method) flyout, or pass it as an input to the `security.attack-discovery.run` step.
* **Custom validation**: Build a workflow that runs after generation to check, enrich, or filter discoveries before they are saved.

:::{important}
A custom validation workflow must explicitly save its discoveries. If it does not, discoveries are dropped silently. You see only a log warning, not a visible error in the UI.
:::

## Open a workflow example from Attack Discovery settings [run-ad-workflow-example]

From the **Attack discovery settings** flyout on the [Attacks view](/solutions/security/ai/attack-discovery/configure-alert-retrieval-from-attacks-page.md#attacks-page-generation), select **View example** under **Generation** or **Validation**. Adapt the example for your environment.

After the workflow saves discoveries, [manage them from the Attacks view](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md).
<!-- FLAG: Uncomment after docs-content#7449 merges: or continue in the same workflow with [Attack triage action steps](/explore-analyze/workflows/steps/attack-triage.md). -->
