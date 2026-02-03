After you apply the policy changes, validate that both the ECS-based logs and the OTel-based metrics are flowing in.

:::::::{stepper}

::::::{step} Validate the log collection

1. In {{kib}}, go to **Discover**, then filter the results using the KQL search bar.
2. Search for NGINX data stream datasets such as `nginx.access` and `nginx.error`, or enter:

   ```
   data_stream.dataset : "nginx.access" or "nginx.error"
   ```

3. Go to **Dashboards**, then select **[Logs Nginx] Access and error logs** to view the dashboard installed with the Nginx integration.

::::::

::::::{step} Validate the metrics collection

Go to **Dashboards**, then select **[Metrics Nginx OTEL] Overview** to view the dashboard for visualizing OTel-based metrics.

This dashboard is provided by the NGINX OpenTelemetry Assets content package, installed automatically when data is ingested through the NGINX OpenTelemetry Input Package.

::::::

:::::::
