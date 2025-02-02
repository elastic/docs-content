# Turn off diagnostic data for {{elastic-defend}} [security-endpoint-diagnostic-data]

By default, {{elastic-defend}} streams diagnostic data to your cluster, which Elastic uses to tune protection features. You can stop producing this diagnostic data by configuring the advanced settings in the {{elastic-defend}} integration policy.

::::{note}
{{elastic-sec}} also collects usage telemetry, which includes {{elastic-defend}} diagnostic data. You can modify telemetry preferences in [Advanced Settings](https://www.elastic.co/guide/en/kibana/current/telemetry-settings-kbn.html).

::::


1. Go to **Assets** → **Endpoints** to view the Endpoints list.
2. Locate the endpoint for which you want to disable diagnostic data, then click the integration policy in the **Policy** column.
3. Scroll down to the bottom of the policy and click **Show advanced settings**.
4. Enter `false` for these settings:

    * `windows.advanced.diagnostic.enabled`
    * `linux.advanced.diagnostic.enabled`
    * `mac.advanced.diagnostic.enabled`

5. Click **Save**.
