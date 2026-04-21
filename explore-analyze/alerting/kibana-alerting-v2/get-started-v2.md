---
navigation_title: Get started
applies_to:
  serverless: preview
products:
  - id: kibana
  - id: cloud-serverless
description: "Get {{alerting-v2}} running in your space: enable the UI, confirm data streams, then understand spaces, API keys, and privileges."
---

# Get started [alerting-get-started-v2]

$$$alerting-get-started-v2$$$

This page walks you through enabling {{alerting-v2}} and understanding what you need before authoring rules and policies.

**In this guide**

- [Set up and verify](#alerting-set-up-v2): Enable the feature and confirm it's working
- [Spaces and API keys](#spaces-and-api-keys-for-alerting-v2): How objects and keys are scoped

For privilege requirements ({{kib}} feature access and {{es}} index access), refer to [{{alerting-v2}} privileges](alerting-v2-privileges.md).

## Set up and verify [alerting-set-up-v2]

$$$alerting-set-up-v2$$$

### Enable {{alerting-v2}}

{{alerting-v2}} is available in {{stack}} 9.4 and later. When it is enabled for your deployment, use **{{manage-app}} > V2 Alerting Preview** to open the v2 rules list and author rules. If **V2 Alerting Preview** does not appear in the navigation, ask your administrator whether alerting v2 is enabled in your environment.

### Where alert data is stored

{{alerting-v2}} automatically creates and manages these data streams:

- `.rule-events`: signal and alert event documents for each rule run (append-only).
- `.alert-actions`: records for acknowledge, snooze, deactivate, fire, suppress, and related audit or suppression tracking.

You do not create these indices yourself. Mappings are applied when the first rule runs.

## Spaces and API keys for alerting [spaces-and-api-keys-for-alerting-v2]

### Spaces

Rules and action policies are space-scoped: objects you create in one space are not visible in another. Alert events are stored globally, but the UI filters what you see by space.

### API keys

Saving a rule or policy creates an API key used for execution. It inherits the saving user's privileges. If privileges drift, update the key from the rule or policy management UI when your team's process calls for it.

## Privileges and roles [alerting-privileges-v2]

For {{kib}} feature access and {{es}} index privilege requirements, refer to [{{alerting-v2}} privileges](alerting-v2-privileges.md).

## What's next

When you are ready to go further, your next steps depend on what you want to set up first. These can be done in any order:

- [Author rules](rules/author-rules.md): Write the {{esql}} query that defines what to detect, choose Detect or Alert mode, and set up grouping and thresholds in [Configure a rule](rules/configure-a-rule.md).
- [Set up workflows](workflows-alerting-v2.md): Configure the automation objects that deliver messages (email, Slack, webhook). You'll need at least one workflow before action policies can send anything.
- [Create action policies](notifications/create-configure-action-policy.md): Define who gets notified, how often, and under what conditions. Policies use KQL matchers to pick up the right episodes and route them to your workflows.
