:::{note}
If your organization uses firewalls, you need to provide access to port 443 and allow the agent to send data to the following URLs:
* `https://api.elastic-cloud.com`
* `https://otel-collector.auto-ops.${region}.${csp}.cloud.elastic.co/`

Replace `${region}` and `${csp}` with the region and CSP you have selected as your [metrics storage location](../autoops/cc-connect-self-managed-to-autoops.md#metrics-storage-location).

Learn more about [defining an Elastic IP address](/deploy-manage/monitor/autoops/ec-autoops-faq.md#elastic-ip-address) for AutoOps in self-managed clusters.
:::