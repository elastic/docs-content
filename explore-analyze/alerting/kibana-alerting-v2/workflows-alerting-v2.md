---
navigation_title: Workflows
applies_to:
  stack: ga 9.4, preview 9.3
  serverless: ga
products:
  - id: kibana
description: "How workflows connect to {{alerting-v2}} action policies and rule automation, and where to configure them."
---

# Workflows for {{alerting-v2}} [workflows-v2]

$$$workflows-v2$$$

In {{alerting-v2}}, [Workflows](../../workflows.md) are how notifications get delivered. Action policies invoke workflows to send messages, trigger automation, or run other steps when an alert episode matches.


Before creating an action policy, make sure the workflows you want to use already exist in your space. Policies store references to workflow IDs, so a destination workflow must exist before you can select it. For workflow authoring and permissions, refer to [Workflows](../../workflows.md).

::::{note}
Only manual triggers are supported for workflows used with action policies.
::::

You can also attach workflows directly to a rule for automation that runs regardless of policy matching. To set up an action policy that references a workflow as a destination, refer to [Create and configure an action policy](notifications/create-configure-action-policy-v2.md).

## Runtime execution order [runtime-execution-order]

After a rule produces or updates alert episodes, processing follows this sequence:

```
Rule → Alert → Action Policy → Workflow → Notification
```

1. The rule runs its {{esql}} evaluation and writes to `.rule-events`.
2. In Alert mode, alert documents and episodes represent the ongoing issue.
3. Action policies in the same space are evaluated against episodes (matcher, suppression, grouping, throttling).
4. For each dispatch, the policy invokes its configured workflows.
5. Notifications are the outcome: Email, chat, webhook, and so on.

The policy evaluates matchers and throttling before any workflow step runs, even though you created the workflow before the policy. That's why configuration order (workflow first, then policy, then rule) is the reverse of runtime order.

[CONTENT NEEDED for M2: Two M2 changes affect what the dispatcher sends in the workflow payload:

1. **`group_hash` → `series.key` + `series.tracked_by`**: The current dispatch payload includes `group_hash` as the series identifier — an opaque hash that means nothing to a workflow author. M2 replaces it with `series.key` (the same hash, renamed) and adds `series.tracked_by` (for example, `{"service.name": "checkout", "environment": "production"}`). Update this page and any workflow payload documentation to show `series.tracked_by` as the human-readable context for which series triggered the workflow.

2. **`episode.severity` + `episode.severity_max`**: Once severity is first-class, the dispatch payload will include these fields. Workflow authors will be able to reference them in message templates, routing logic, or conditional steps. Document the fields and show example usage once M2 ships.]

