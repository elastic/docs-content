# Analyze unassigned shards using the Kibana UI [ech-analyze_shards_with-kibana]

If you are shipping logs and metrics to a monitoring deployment, go through the following steps.

1. Select your deployment from the {{es}} Service panel and navigate to the **Logs and metrics** page.
2. Click **Enable**.
3. Choose the deployment where to send your logs and metrics.
4. Click **Save**. It might take a few minutes to apply the configuration changes.
5. Click **View** to open the Kibana UI and get more details on metrics and logs.

:::{image} ../../../images/cloud-heroku-ec-logs-metrics-page.png
:alt: Log and metrics page
:::

The unhealthy indices appear with a red or yellow status.

:::{image} ../../../images/cloud-heroku-ec-red-yellow-indices.png
:alt: Unhealthy indices in red or yellow status
:::

