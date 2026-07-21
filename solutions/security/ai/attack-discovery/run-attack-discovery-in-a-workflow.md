---
navigation_title: Run from a workflow
description: "For automation builders: run Attack Discovery as a step inside an Elastic workflow."
applies_to:
  stack: ga 9.5+
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Run Attack Discovery from a workflow [run-attack-discovery-in-a-workflow]

You can run Attack Discovery as a step in an Elastic workflow (`security.attack-discovery.run`). The step uses the same analysis as manual and scheduled runs, so you can fold Attack Discovery into larger automations, for example analyzing alerts from an earlier step, then branching on discovery count or status without a person in the loop.

This page explains the inputs and run modes for that step, how built-in and custom retrieval or validation workflows fit in, and where to open a working example. If you are investigating in chat instead, use [Run Attack Discovery from {{agent-builder}}](/solutions/security/ai/attack-discovery/run-attack-discovery-from-agent-builder.md).

## Before you begin [run-ad-workflow-before-you-begin]

To run Attack Discovery from a workflow, you need:

* The [**Attack Discovery Workflows**](/solutions/security/get-started/configure-advanced-settings.md#enable-attack-discovery-workflows) advanced setting turned on.
* Access to [Elastic Workflows](/explore-analyze/workflows/get-started/setup.md). Building, viewing, and running workflows requires the **Analytics > Workflows** {{kib}} privilege, which is separate from Attack Discovery access. Serverless roles include this privilege by default. On self-managed and Elastic Cloud Hosted deployments, add it explicitly to custom roles.
* The privileges described in [Grant access to Attack Discovery](/solutions/security/ai/attack-discovery/grant-access.md).

## How it works [run-ad-workflow-how-it-works]

The `security.attack-discovery.run` step takes structured inputs and runs the same analysis steps used by every other Attack Discovery trigger. Typical inputs include:

* How to collect alerts (alerts already selected by the skill, an {{esql}} query, or a custom query)
* A time range and filter
* An optional connector override
* A validation workflow

You can pass alerts from an earlier workflow step into this step, then use the discovery count or status to decide what happens next.

Choose how the step runs:

* **Synchronously**: the workflow waits briefly for the run to finish so later steps can use the discoveries right away.
* **Asynchronously**: the step returns immediately with a run ID, and discoveries keep saving in the background.

Even without a live chat, Attack Discovery still verifies and enriches the evidence in the background. Each time the Attack Discovery skill runs, {{agent-builder}} opens a new conversation for that run. You can open that conversation from the workflow execution details flyout for audit purposes.

:::{note}
There is no interactive approval step inside the workflow. If the skill finds an uncovered step in an attack chain, it drafts a detection rule proposal. A person must review and approve that proposal from the run's execution details, not from within the workflow itself.
:::

## Built-in workflows [run-ad-workflow-built-in]

Elastic provides system-managed workflows that cover retrieval, generation, and validation. These workflows are hidden from the main workflow list by default. You can still open them directly by URL.

* You cannot edit built-in workflows through the UI or the standard API. Attempting to change one shows a message that only enabling or disabling is allowed.
* A separate privilege can unlock editing for administrators who need it. That privilege is distinct from base Workflows access. Refer to [Grant access to Attack Discovery](/solutions/security/ai/attack-discovery/grant-access.md#attack-discovery-workflows-privileges).
  <!-- FLAG: Confirm the exact privilege name for editing built-in Attack Discovery workflows. -->
* Deletion is always blocked. There is no way to override this.

## Custom retrieval and validation workflows [run-ad-workflow-custom]

You can plug in your own workflows for alert retrieval or validation:

* **Custom retrieval**: Build a workflow that returns the alerts Attack Discovery should analyze. Select it under **Alert retrieval workflows** in the [Attack discovery settings](/solutions/security/ai/attack-discovery/configure-alert-retrieval-from-attacks-page.md#attacks-page-alert-retrieval-method) flyout, or pass it as an input to the `security.attack-discovery.run` step.
* **Custom validation**: Build a workflow that runs after generation to check, enrich, or filter discoveries before they are saved.

:::{important}
A custom validation workflow must explicitly save its discoveries. If it does not, discoveries are dropped silently. You see only a log warning, not a visible error in the UI.
:::

Start from a working example in the **Attack discovery settings** flyout (**View example** under **Generation** or **Validation**), then adapt it for your environment.

Next, [try an example](#run-ad-workflow-example).

## Try an example [run-ad-workflow-example]

A working example workflow is available from the **Attack discovery settings** flyout on the [Attacks view](/solutions/security/ai/attack-discovery/configure-alert-retrieval-from-attacks-page.md#attacks-page-generation) (**Detections > Views > Attacks**). In the **Generation** section, select **View example**. The **Validation** section also includes **View example** and **Create a new workflow**.

After the workflow saves discoveries, [manage them from the Attacks view](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md).
