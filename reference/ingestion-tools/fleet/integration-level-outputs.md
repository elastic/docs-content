---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/integration-level-outputs.html
---

# Set integration-level outputs [integration-level-outputs]

If you have an `Enterprise` [{{stack}} subscription](https://www.elastic.co/subscriptions), you can configure {{agent}} data to be sent to different outputs for different integration policies. Note that the output clusters that you send data to must also be on the same subscription level.

Integration-level outputs are very useful for certain scenarios. For example:

* You can may want to send security logs monitored by an {{agent}} to one {{ls}} output, while informational logs are sent to a another {{ls}} output.
* If you operate multiple {{beats}} on a system and want to migrate these to {{agent}}, integration-level outputs enable you to maintain the distinct outputs that are currently used by each Beat.


## Order of precedence [_order_of_precedence]

For each {{agent}}, the agent policy configures sending data to the following outputs in decreasing order of priority:

1. The output set in the [integration policy](/reference/ingestion-tools/fleet/add-integration-to-policy.md).
2. The output set in the integration’s parent [{{agent}} policy](/reference/ingestion-tools/fleet/agent-policy.md). This includes the case where an integration policy belongs to multiple {{agent}} policies.
3. The global, default data output set in the [{{fleet}} settings](/reference/ingestion-tools/fleet/fleet-settings.md).


## Configure the output for an integration policy [_configure_the_output_for_an_integration_policy]

To configure an integration-level output for {{agent}} data:

1. In {{kib}}, go to **Integrations**.
2. On the **Installed integrations** tab, select the integration that you’d like to update.
3. Open the **Integration policies** tab.
4. From the **Actions** menu next to the integration, select **Edit integration**.
5. In the **integration settings** section, expand **Advanced options**.
6. Use the **Output** dropdown menu to select an output specific to this integration policy.
7. Click **Save and continue** to confirm your changes.


## View the output configured for an integration [_view_the_output_configured_for_an_integration]

To view which {{agent}} output is set for an integration policy:

1. In {{fleet}}, open the **Agent policies** tab.
2. Select an {{agent}} policy.
3. On the **Integrations** tab, the **Output** column indicates the output used for each integration policy. If data is configured to be sent to either the global output defined in {{fleet}} settings or to the integration’s parent {{agent}} policy, this is indicated in a tooltip.
