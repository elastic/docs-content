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

* The [Attack Discovery Workflows](/solutions/security/get-started/configure-advanced-settings.md#enable-attack-discovery-workflows) advanced setting turned on.
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

For an example of this step, open **Attack discovery settings** on the [Attacks view](/solutions/security/ai/attack-discovery/configure-alert-retrieval-from-attacks-page.md#attacks-page-generation). Under **Generation**, select **View example** to open **Security - Attack discovery - Run example** (`security.attack-discovery.run`).

## Call the Attack Discovery API from a workflow step [run-ad-workflow-api-step]

If you want full control over the request body instead of using the `security.attack-discovery.run` step, add a [`kibana.request`](/explore-analyze/workflows/steps/kibana.md#kibana-request) step that posts to the [Attack Discovery generate endpoint]({{kib-apis}}operation/operation-postattackdiscoverygenerate). The step returns an `execution_uuid` that later steps can use to track the run.

The generate request requires `anonymizationFields`, which controls which alert fields are sent to the LLM. Retrieve them from the AI Assistant anonymization fields API in an earlier step, then pass them into the generation step:

```yaml
steps:
  - name: get_anonymization_fields
    type: kibana.request
    with:
      method: GET
      path: /api/security_ai_assistant/anonymization_fields/_find
      query:
        per_page: 1000

  - name: generate_discoveries
    type: kibana.request
    with:
      method: POST
      path: /api/attack_discovery/_generate
      body:
        alertsIndexPattern: .alerts-security.alerts-default
        anonymizationFields: "{{ steps.get_anonymization_fields.output.data.data }}"
        apiConfig:
          connectorId: your-connector-id
          actionTypeId: .gen-ai
        subAction: invokeAI
        size: 100
        start: now-24h
        end: now
```

To limit which alerts are analyzed, add a `filter` (an {{es}} query DSL object) to the request body. Reference the returned run ID in later steps with `{{ steps.generate_discoveries.output.data.execution_uuid }}`, or retrieve the finished discoveries with the [Attack discovery API]({{kib-apis}}group/endpoint-security-attack-discovery-api) once generation completes.

## View runs and approve detection gap proposals [run-ad-workflow-when-it-runs]

When the workflow runs, Attack Discovery uses those settings and the same analysis as manual and scheduled runs. The run opens a new {{agent-builder}} conversation. From **Workflow execution details**, select **Open conversation** to view the run or to [review and approve detection rule proposals](/solutions/security/ai/attack-discovery/run-attack-discovery-from-agent-builder.md#run-ad-conversation-gap-closure) in chat. You cannot approve those proposals inside the workflow itself.

With a synchronous run, later steps can branch on the results, including Attack triage steps for status, assignees, or tags.

## Work with built-in Attack Discovery workflows [run-ad-workflow-built-in]

Elastic provides system-managed workflows that cover retrieval, generation, and validation. Open examples from **Attack discovery settings** with **View example**. You can enable or disable built-in workflows, but you cannot edit or delete them.

## Create custom retrieval and validation workflows [run-ad-workflow-custom]

You can plug in your own workflows for alert retrieval or validation:

* **Custom retrieval**: Build a workflow that returns the alerts Attack Discovery should analyze. Select it under **Alert retrieval workflows** in the [Attack discovery settings](/solutions/security/ai/attack-discovery/configure-alert-retrieval-from-attacks-page.md#attacks-page-alert-retrieval-method) flyout, or pass it as an input to the `security.attack-discovery.run` step.
* **Custom validation**: Build a workflow that runs after generation to check, enrich, or filter discoveries before they are saved. From **Validation** in the settings flyout, select **View example** to open **Security - Attack discovery - Custom validation example**.

For a custom retrieval workflow, return the alerts as the output of the last step that produces results. In the settings flyout, select the info icon next to **Alert retrieval workflows** for a copy-pasteable example. You can also select **Create a new workflow** from that example to start from the pattern.

:::{important}
If you create a custom validation workflow, it must save the discoveries you want to keep. Otherwise they never appear as attacks.
:::
