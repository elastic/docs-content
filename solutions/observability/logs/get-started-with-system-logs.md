---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/observability-get-started-with-logs.html
---

# Get started with system logs [observability-get-started-with-logs]

::::{admonition} Required role
:class: note

The **Admin** role or higher is required to onboard log data. To learn more, refer to [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/manage-users.md#general-assign-user-roles).

::::


In this guide you’ll learn how to onboard system log data from a machine or server, then observe the data in **Logs Explorer**.

To onboard system log data:

1. [Create a new {{obs-serverless}} project](../get-started/create-an-observability-project.md), or open an existing one.
2. In your {{obs-serverless}} project, go to **Add data**.
3. Under **What do you want to monitor?**, select **Host** → **Elastic Agent: Logs & Metrics**.
4. Follow the in-product steps to auto-detect your logs and install and configure the {{agent}}.

After the agent is installed and successfully streaming log data, you can view the data in the UI:

1. From the navigation menu, go to **Discover** and select the **Logs Explorer** tab. The view shows all log datasets. Notice you can add fields, change the view, expand a document to see details, and perform other actions to explore your data.
2. Click **All log datasets** and select **System** → **syslog** to show syslog logs.

:::{image} ../../../images/serverless-log-explorer-select-syslogs.png
:alt: Screen capture of the Logs Explorer showing syslog dataset selected
:class: screenshot
:::


## Next steps [observability-get-started-with-logs-next-steps]

Now that you’ve added system logs and explored your data, learn how to onboard other types of data:

* [Stream any log file](stream-any-log-file.md)
* [Get started with traces and APM](../apps/get-started-with-apm.md)

To onboard other types of data, select **Add Data** from the main menu.
