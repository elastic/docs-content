---
navigation_title: Alerting privileges
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Required privileges for creating and managing Kibana alerting v2 rules, notification policies, and alert actions."
---

# Kibana alerting v2 privileges [alerting-privileges-v2]

Kibana alerting v2 uses {{es}} index-level security to control access to alert data, combined with {{kib}} feature privileges for rule and policy management.

## Required privileges

### Rule management

To create, edit, and manage Kibana alerting v2 rules, you need:

- **{{kib}} feature privilege**: `Rules V2` with the appropriate access level (read, create, edit, or all).
- **{{es}} index privileges**: Read access to the source indices your rules query (for example, `logs-*`, `metrics-*`).

Rule execution uses the API key of the user who created or last updated the rule. This means the rule runs with the privileges of that user. If the user's privileges change, rule execution reflects those changes.

### Notification policy management

To create and manage notification policies, you need:

- **{{kib}} feature privilege**: `Rules V2` with create or edit access.
- **Workflow permissions**: To add a workflow as a destination on a policy, you need permissions for that workflow. This prevents privilege escalation through policy configuration.

### Alert management

To view and take actions on alerts (acknowledge, snooze, tag, assign), you need:

- **{{kib}} feature privilege**: `Rules V2` with at least read access.
- **{{es}} index privileges**: Read access to `.rule-events` for viewing alerts. Write access to `.alert-actions` for taking alert actions.

### Discover and dashboard access

Because Kibana alerting v2 alert events are stored in standard {{es}} indices, any user with read access to `.rule-events` can query them in Discover and use them in dashboards. No additional {{kib}} privileges are required beyond the standard Discover feature access.

## Space boundaries

Rule and notification policy management respects {{kib}} space boundaries. Rules created in one space are not visible in another. Alert events are indexed globally, but UI access is filtered by space.

## API key management

Rules and notification policies use API keys for execution:

- An API key is created when a rule or policy is saved.
- The API key inherits the privileges of the user who created it.
- You can update the API key from the rule or policy management page if the original user's privileges change.
