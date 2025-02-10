---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/agentless-integrations.html
  - https://www.elastic.co/guide/en/serverless/current/agentless-integration-troubleshooting.html
---

# Agentless integrations FAQ [agentless-integration-troubleshooting]

Frequently asked questions and troubleshooting steps for {{elastic-sec}}'s agentless CSPM integration.


## When I make a new integration, when will I see the agent appear on the Integration Policies page? [_when_i_make_a_new_integration_when_will_i_see_the_agent_appear_on_the_integration_policies_page]

After you create a new agentless integration, the new integration policy may show a button that says **Add agent** instead of the associated agent for several minutes during agent enrollment. No action is needed other than refreshing the page once enrollment is complete.


## How do I troubleshoot an `Offline` agent? [_how_do_i_troubleshoot_an_offline_agent]

For agentless integrations to successfully connect to {{elastic-sec}}, the {{fleet}} server host value must be the default. Otherwise, the agent status on the {{fleet}} page will be `Offline`, and logs will include the error `[elastic_agent][error] Cannot checkin in with fleet-server, retrying`.

To troubleshoot this issue:

1. Find **{{fleet}}** in the navigation menu or use the [global search field](../../get-started/the-stack.md#kibana-navigation-search). Go to the **Settings** tab.
2. Under **{{fleet}} server hosts**, click the **Actions** button for the policy named `Default`. This opens the Edit {{fleet}} Server flyout. The policy named `Default` should have the **Make this {{fleet}} server the default one** setting enabled. If not, enable it, then delete your integration and create it again.

::::{note}
If the **Make this {{fleet}} server the default one** setting was already enabled but problems persist, it’s possible someone changed the default {{fleet}} server’s **URL** value. In this case, contact Elastic Support to find out what the original **URL** value was, update the settings to match this value, then delete your integration and create it again.
::::



## How do I troubleshoot an `Unhealthy` agent? [_how_do_i_troubleshoot_an_unhealthy_agent]

On the **{{fleet}}** page, the agent associated with an agentless integration has a name that begins with `agentless`. To troubleshoot an `Unhealthy` agent:

* Confirm that you entered the correct credentials for the cloud provider you’re monitoring. The following is an example of an error log resulting from using incorrect AWS credentials:

    ```
    [elastic_agent.cloudbeat][error] Failed to update registry: failed to get AWS accounts: operation error Organizations: ListAccounts, get identity: get credentials: failed to refresh cached credentials, operation error STS: AssumeRole, https response error StatusCode: 403, RequestID: XXX, api error AccessDenied: User: XXX is not authorized to perform: sts:AssumeRole on resource:XXX
    ```


For instructions on checking {{fleet}} logs, refer to [{{fleet}} troubleshooting](../ingest/fleet/common-problems.md).


## How do I delete an agentless integration? [_how_do_i_delete_an_agentless_integration]

::::{note}
Deleting your integration will remove all associated resources and stop data ingestion.
::::


When you create a new agentless CSPM integration, a new agent policy appears within the **Agent policies** tab on the **{{fleet}}** page, but you can’t use the **Delete integration** button on this page. Instead, you must delete the integration from the CSPM Integration’s **Integration policies** tab.

1. Find **Integrations** in the navigation menu or use the [global search field](../../get-started/the-stack.md#kibana-navigation-search), then search for and select `CSPM`.
2. Go to the CSPM Integration’s **Integration policies** tab.
3. Find the integration policy for the integration you want to delete. Click **Actions**, then **Delete integration**.
4. Confirm by clicking **Delete integration** again.
