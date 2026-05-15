---
navigation_title: Workflows
applies_to:
  stack: ga 9.4, preview 9.3
  serverless: ga
products:
  - id: kibana
description: "How workflows connect to the experimental alerting features action policies and rule automation, and where to configure them."
---

# Workflows for the experimental alerting features [workflows]


Workflows are part of the experimental alerting features in Kibana. Without a workflow, an action policy has nowhere to send notifications. [Workflows](../../workflows.md) are the delivery layer. They define the actual steps that run when a policy matches an episode: sending a message, calling a webhook, triggering automation, or any combination. Setting up a workflow is what connects the experimental alerting features to the tools your team already uses for incident response.

Before creating an action policy, make sure the workflows you want to use already exist in your space. Policies store references to workflow IDs, so a destination workflow must exist before you can select it. 

::::{note}
Only manual triggers are supported for workflows used with action policies.
::::

## Runtime execution order [runtime-execution-order]

After a rule produces or updates alert episodes, processing follows this sequence:

```
Rule → Alert → Action Policy → Workflow → Notification
```

1. The rule runs its {{esql}} evaluation and writes to `.rule-events`.
2. In Alert mode, alert documents and episodes represent the ongoing issue.
3. Action policies in the same space are evaluated against episodes (matcher, suppression, grouping, frequency).
4. For each dispatch, the policy invokes its configured workflows.
5. Notifications are the outcome: Email, chat, webhook, and so on.

The policy evaluates matchers and **frequency** limits before any workflow step runs, even though you created the workflow before the policy. That's why configuration order (workflow first, then policy, then rule) is the reverse of runtime order.

