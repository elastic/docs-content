---
navigation_title: Create and manage notification policies
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Create, configure, and manage Kibana alerting v2 notification policies — matching conditions, grouping, throttling, destinations, and snooze."
---

# Create and manage Kibana alerting v2 notification policies [create-manage-notification-policies-v2]

Create notification policies to control which alerts trigger notifications, how alerts are grouped, how frequently notifications are sent, and where they are routed.

## Create a notification policy

1. Navigate to **Management > Alerts and Insights > Rules V2 > Notification Policies**.
2. Click **Create policy**.
3. Configure the policy settings described below.
4. Click **Save**.

You can also create policies from within the rule form when linking a policy to a rule.

### Policy name and description

Give the policy a descriptive name (required) and an optional description that explains the policy's intent.

### Matching conditions

Define which alerts the policy applies to using KQL matching conditions. Matching supports:

- **Equality**: `severity: "critical"`
- **AND/OR logic**: `severity: "critical" AND tags: "production"`
- **Membership**: `rule.name: ("cpu-alert" OR "memory-alert")`
- **Prefix matching**: `service.name: "checkout*"`
- **Field existence**: `data.host.name: *`

If no matcher is set, the policy matches every alert from its linked rules (catch-all).

### Grouping

Configure how related alerts are batched into a single notification:

- **Group by field** — group alerts by `host.name`, `service.name`, `severity`, or any alert field.
- **No grouping** — each alert produces its own notification.

Grouping is always scoped per rule. Alerts from different rules are never grouped into the same notification, even if they share the same grouping field values.

### Frequency and throttling

Control how often notifications are sent:

- **Immediate** — every matching alert triggers a notification.
- **Throttled** — at most one notification per interval (for example, every 15 minutes). The first alert always fires. Subsequent alerts within the throttle window are suppressed.
- **Summary digest** — a periodic summary of all matching alerts, sent at a configured interval.

The throttle interval is configurable in seconds, minutes, or hours.

### Destinations

Select one or more workflow destinations for the policy. Destinations are workflows configured in the Workflows management area:

- Slack channels
- PagerDuty services
- Email recipients
- Custom webhooks

### Policy status

Policies can be enabled or disabled. A disabled policy does not evaluate or send notifications.

## Manage notification policies

### Policy list

The notification policies list shows all policies with:

- Policy name and description
- Status (enabled, disabled, or snoozed)
- Matching conditions summary
- Destination icons
- Linked rule count
- Last triggered timestamp
- Last updated by

### Filter and search

- **Filter** by status, destination type, rule name, last updated by, and tags.
- **Sort** by name, last triggered, status, last updated by, or linked rule count.
- **Search** across all policy attributes.

### Inline actions

From the policy list, you can:

- **View details** — navigate to the full policy details page.
- **Edit** — open the policy form.
- **Enable/Disable** — toggle the policy on or off.
- **Clone** — duplicate the policy as a starting point for a new one.
- **Snooze/Unsnooze** — temporarily suppress notifications.
- **Delete** — remove the policy.
- **Update API key** — refresh the API key used for workflow authentication.

### Bulk actions

Select multiple policies to:

- Enable or disable in bulk.
- Unsnooze in bulk.
- Delete in bulk.
- Update API keys in bulk.

## Snooze a policy

Snooping temporarily suppresses all notifications from the policy while alerts continue to fire and be recorded:

1. Open the policy from the list.
2. Click **Snooze**.
3. Select a duration (for example, 3 minutes, 5 hours, 1 week) or set a specific end time.
4. Notifications are suppressed until the snooze expires.

Snooze auto-expires. After expiration, notifications resume automatically.

## Policy details page

The policy details page shows:

- **Policy information**: name, description, status, created by, last updated by, last triggered.
- **Configuration**: matching conditions, grouping, frequency, suppression settings, destinations.
- **Linked rules**: all rules assigned to this policy with name, description, and status. Clicking a rule navigates to its detail page.
- **Maintenance windows**: active or scheduled maintenance windows with name, schedule, and status.
- **Execution history**: when the policy evaluated, how many alerts matched, how many notifications were sent, delivery status, and failure reasons. Filter by time range, delivery status, and destination.
