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

## Resolution

<!-- REQUIRED

Provide clear, actionable steps to resolve the issue.

- Numbered instructions that begin with imperative verb phrases
- Keep each step focused on a single action
- Use the stepper component

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

Explain how to avoid this issue in the future. Use bullet points.
-->

## Resources

<!-- OPTIONAL 

Link to related documentation for deeper context. These links are supplementary — all information required to fix the issue should already be on this page. 
-->

- [Related documentation link]
- [Contrib/upstream reference]