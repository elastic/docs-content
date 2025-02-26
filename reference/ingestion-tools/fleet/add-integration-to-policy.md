---
navigation_title: "Add an integration to an {{agent}} policy"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/add-integration-to-policy.html
---

# Add an integration to an {{agent}} policy [add-integration-to-policy]


An [{{agent}} policy](/reference/ingestion-tools/fleet/agent-policy.md) consists of one or more integrations that are applied to the agents enrolled in that policy. When you add an integration, the policy created for that integration can be shared with multiple {{agent}} policies. This reduces the number of integrations policies that you need to actively manage.

To add a new integration to one or more {{agent}} policies:

1. In {{kib}}, go to the **Integrations** page.
2. The Integrations page shows {{agent}} integrations along with other types, such as {{beats}}. Scroll down and select **Elastic Agent only** to view only integrations that work with {{agent}}.
3. Search for and select an integration. You can select a category to narrow your search.
4. Click **Add <integration>**.
5. You can opt to install an {{agent}} if you haven’t already, or choose **Add integration only** to proceed.
6. In Step 1 on the **Add <integration>** page, you can select the configuration settings specific to the integration.
7. In Step 2 on the page, you have two options:

    1. If you’d like to create a new policy for your {{agent}}s, on the **New hosts** tab specify a name for the new agent policy and choose whether or not to collect system logs and metrics. Collecting logs and metrics will add the System integration to the new agent policy.
    2. If you already have an {{agent}} policy created, on the **Existing hosts** tab use the drop-down menu to specify one or more agent policies that you’d like to add the integration to.

8. Click **Save and continue** to confirm your settings.

This action installs the integration (if it’s not already installed) and adds it to the {{agent}} policies that you specified. {{fleet}} distributes the new integration policy to all {{agent}}s that are enrolled in the agent policies.

You can update the settings for an installed integration at any time:

1. In {{kib}}, go to the **Integrations** page.
2. On the **Integration policies** tab, for the integration that you like to update open the **Actions** menu and select **Edit integration**.
3. On the **Edit <integration>** page you can update any configuration settings and also update the list of {{agent}} polices to which the integration is added.

    If you clear the **Agent policies** field, the integration will be removed from any {{agent}} policies to which it had been added.

    To identify any integrations that have been "orphaned", that is, not associated with any {{agent}} policies, check the **Agent polices** column on the **Integration policies** tab. Any integrations that are installed but not associated with an {{agent}} policy are as labeled as `No agent policies`.


If you haven’t deployed any {{agent}}s yet or set up agent policies, start with one of our quick start guides:

* [Get started with logs and metrics](/solutions/observability/infra-and-hosts/get-started-with-system-metrics.md)
* [Get started with application traces and APM](/solutions/observability/apps/get-started-with-apm.md)
