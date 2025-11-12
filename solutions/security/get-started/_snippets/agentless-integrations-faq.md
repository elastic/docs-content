Frequently asked questions and troubleshooting steps for {{elastic-sec}}'s agentless CSPM integration.


## When I make a new integration, when will I see the agent appear on the Integration Policies page? [_when_i_make_a_new_integration_when_will_i_see_the_agent_appear_on_the_integration_policies_page]

After you create a new agentless integration, the new integration policy may show a button that says **Add agent** instead of the associated agent for several minutes during agent enrollment. No action is needed other than refreshing the page once enrollment is complete.

## Why isn't my agentless agent appearing in Fleet?

```{applies_to}
  stack: ga 9.1
  serverless: ga
```

Agentless agents (which run on Elastic's infrastructure to enable agentless integrations) do not appear on the **Fleet** page by default. To view them on this page:


::::{applies-switch}

:::{applies-item} { stack: ga 9.2, serverless: }
Go to the **Settings** tab of the **Fleet** page. Navigate to the **Advanced Settings** section, and enable **Show agentless resources**.
:::

:::{applies-item} stack: ga 9.1
Add the following query to the end of the **Fleet** page's URL: `?showAgentless=true`. 
:::

::::


## How do I troubleshoot an `Offline` agent? [_how_do_i_troubleshoot_an_offline_agent]

For agentless integrations to successfully connect to {{elastic-sec}}, the {{fleet}} server host value must be the default. Otherwise, the agent status on the {{fleet}} page will be `Offline`, and logs will include the error `[elastic_agent][error] Cannot checkin in with fleet-server, retrying`.

To troubleshoot this issue:

1. Find **{{fleet}}** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Go to the **Settings** tab.
2. Under **{{fleet}} server hosts**, click the **Actions** button for the policy named `Default`. This opens the Edit {{fleet}} Server flyout. The policy named `Default` should have the **Make this {{fleet}} server the default one** setting enabled. If not, enable it, then delete your integration and create it again.

If the **Make this {{fleet}} server the default one** setting was already enabled but problems persist, it’s possible someone changed the default {{fleet}} server’s **URL** value. In this case, contact Elastic Support to find out what the original **URL** value was, update the settings to match this value, then delete your integration and create it again.

::::{note}
:applies_to: ess: ga
In {{ech}} deployments on {{stack}} versions prior to 9.1.6, the connection between agentless integrations and {{fleet-server}} can break if the default {{fleet-server}} host URL value in {{fleet}} is modified or if a different host URL is set as the default.

This issue is resolved in {{stack}} 9.1.6. In this and later versions, agentless integration policies are assigned to a default managed {{fleet-server}} host which cannot be modified.
::::

## Why can't I upgrade my agentless integration to a newer version?

On versions of {{stack}} before v9.2, agentless integrations can't be upgraded to newer versions of the integration. To get a newer version in your {{stack}} environment, upgrade to {{stack}} v9.2+ or delete and re-install the desired integration.


## How do I troubleshoot an `Unhealthy` agent? [_how_do_i_troubleshoot_an_unhealthy_agent]

On the **{{fleet}}** page, agents associated with agentless integrations have names that begin with `agentless`. To troubleshoot an `Unhealthy` agent:

1. Go to the **Settings** tab of the **Fleet** page. Go to the **Advanced Settings** section, and turn on the **Show agentless resources** toggle.
2. In {{fleet}}, select the unhealthy agent. 
3. From the **Actions** menu, select **Request diagnostics .zip**. 
4. Download and unzip the [diagnostics bundle](/troubleshoot/ingest/fleet/common-problems.md#trb-collect-agent-diagnostics). Refer to [Common problems with {{fleet}} and {{agent}}](/troubleshoot/ingest/fleet/common-problems.md) for more information.

## How do I delete an agentless integration? [_how_do_i_delete_an_agentless_integration]

::::{note}
Deleting your integration will remove all associated resources and stop data ingestion.
::::


When you create a new agentless CSPM integration, a new agent policy appears within the **Agent policies** tab on the **{{fleet}}** page, but you can’t use the **Delete integration** button on this page. Instead, you must delete the integration from the CSPM Integration’s **Integration policies** tab.

1. Find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then search for and select `CSPM`.
2. Go to the CSPM Integration’s **Integration policies** tab.
3. Find the integration policy for the integration you want to delete. Click **Actions**, then **Delete integration**.
4. Confirm by clicking **Delete integration** again.

## Can agentless integrations use a specific range of static IP addresses for configuring allow and deny rules for traffic?

No, agentless integrations can not use a specific range of static IP addresses for configuring ingress and egress allow and deny rules.