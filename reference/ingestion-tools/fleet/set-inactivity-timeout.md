---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/set-inactivity-timeout.html
---

# Set inactivity timeout [set-inactivity-timeout]

The inactivity timeout moves {{agent}}s to inactive status after being offline for a set amount of time. Inactive {{agent}}s are still valid {{agent}}s, but are removed from the main {{fleet}} UI allowing you to better manage {{agent}}s and declutter the {{fleet}} UI.

When {{fleet-server}} receives a check-in from an inactive {{agent}}, it returns to healthy status.

For example, if an employee is on holiday with their laptop off, the {{agent}} will transition to offline then inactive once the inactivity timeout limit is reached. This prevents the inactive {{agent}} from cluttering the {{fleet}} UI. When the employee returns, the {{agent}} checks in and returns to healthy status with valid API keys.

If an {{agent}} is no longer valid, you can manually [unenroll](/reference/ingestion-tools/fleet/unenroll-elastic-agent.md) inactive {{agent}}s to revoke the API keys. Unenrolled agents need to be re-enrolled to be operational again.

For more on {{agent}} statuses, see [view agent status](/reference/ingestion-tools/fleet/monitor-elastic-agent.md#view-agent-status).


## Set the inactivity timeout [setting-inactivity-timeout]

Set the inactivity timeout in the {{agent}} policy to the amount of time after which you want an offline {{agent}} to become inactive.

To set the inactivity timeout:

1. In **{{fleet}}**, select **Agent policies**.
2. Click the policy name, then click **Settings**.
3. In the **Inactivity timeout** field, enter a value in seconds. The default value is 1209600 seconds or two weeks.

