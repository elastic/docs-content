---
navigation_title: "[Short title that works in the context of existing navigation folders]"
description: "[Describe the user-visible problem this page helps resolve, suitable for search results and tooltips]."
type: troubleshooting
applies_to:
  stack:
  serverless:
products:
  - id:
---

<!--
Copy and paste this template to get started writing your troubleshooting page, deleting the instructions and comments from your final page.

For complete guidance, refer to [the troubleshooting guide](https://www.elastic.co/docs/contribute-docs/content-types/troubleshooting).
-->

# [Problem statement written from the user’s perspective]

<!-- REQUIRED

Describe the problem users are experiencing.

Example: EDOT Collector doesn't propagate client metadata
-->

<!-- REQUIRED

Introduction

A brief summary of what the page helps users resolve. Keep it concise and focused on the problem, not the solution. Help users quickly confirm they're in the right place by describing the issue they're experiencing.
-->

## Symptoms

<!-- REQUIRED

Describe what users observe when the problem occurs. Focus on the symptoms themselves, not their causes. Use bullet points. If applicable, include:

- Error messages
- Log output
- Missing or unexpected behavior
- Timeouts or performance issues
-->

## Diagnosis

<!-- OPTIONAL

Use a Diagnosis section when you need to help users narrow down the problem from an initial symptom before providing the resolution. This is especially useful when:

- The initial symptom requires diagnostic steps to identify the specific cause
- Multiple resolutions depend on diagnostic findings
- The same symptom can have multiple root causes

Use numbered steps or bullet points to guide users through the diagnostic process.
-->

## Resolution

<!-- REQUIRED

Provide clear, actionable steps to resolve the issue.

- Order steps from most common to least common to resolve the issue
- Numbered instructions that begin with imperative verb phrases
- Keep each step focused on a single action
- Use the stepper component
- Avoid diagnostic branching unless the problem cannot be resolved linearly.

For complex scenarios, consider these patterns:

- Multiple resolutions or "combo" resolutions: When multiple solutions can be applied together or independently, present them as a list of options (users can choose one or combine multiple approaches).

- Resolutions that differ by deployment type: When steps differ significantly by deployment type ({{ecloud}} versus self-managed versus ECK), organize by deployment type using clear headings.

- Separating diagnosis from causes and resolution: When multiple resolutions depend on diagnostic findings, use a separate Diagnosis section before Resolution to help users identify their specific situation first.

For more information about the stepper component, refer to [the syntax guide](https://elastic.github.io/docs-builder/syntax/stepper/).
-->

```markdown
:::::{stepper}

::::{step} [Step title]
[Step description or instruction - begin with an imperative verb]
::::

::::{step} [Step title]
[Step description or instruction - begin with an imperative verb]
::::

::::{step} [Step title]
[Step description or instruction - begin with an imperative verb]
::::

:::::
```

## Best practices

<!-- OPTIONAL BUT RECOMMENDED 

Explain how to avoid this issue in the future. Use bullet points. Do not restate general product best practices or guidance that applies broadly beyond this issue.
-->

## Resources

<!-- OPTIONAL 

Link to related documentation for deeper context. These links are supplementary — all information required to fix the issue should already be on this page.

Avoid linking to GitHub issues, pull requests, or internal discussions. Resources should be stable, user-facing documentation.
-->

- [Related documentation link]
- [Contrib/upstream reference]

## Contact support

<!-- OPTIONAL

Use this section only if there is no dedicated "Contact support" page available in the troubleshooting folder.
-->

## Contact us

If you have an [Elastic subscription](https://www.elastic.co/pricing), then you can contact Elastic support for assistance. You can reach us in the following ways:

* Through the [Elastic Support Portal](https://support.elastic.co/home). The Elastic Support Portal is the central place where you can access all of your cases, subscriptions, and licenses. Within a few hours after subscribing, you receive an email with instructions on how to log in to the Support Portal, where you can track both current and archived cases.

  You can access the portal [directly](https://support.elastic.co/home), or by clicking on the life preserver icon on any page in {{ecloud}}.

* By email: support@elastic.co

:::{tip}
If you contact us by email, use the email address that you registered with so that we can help you more quickly. If you are using a distribution list as your registered email, you can also register a second email address with us. Just open a case to let us know the name and email address you want to add.
:::