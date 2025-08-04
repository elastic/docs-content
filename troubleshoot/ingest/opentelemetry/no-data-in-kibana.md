---
navigation_title: No data visible in Kibana
description: Learn what to check when no data (logs, metrics, traces) appears in Kibana after setting up EDOT.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_collector: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# No logs, metrics, or traces visible in Kibana

If the EDOT Collector or SDKs appear to be running, but you see no logs, metrics, or traces in the {{kib}} UI, try to use these solutions to identify and resolve the issue.

## Symptoms

* Collector process is consuming CPU/memory but no telemetry data is visible in {{kib}}
* APM services don’t show up in {{kib}}
* Dashboards appear empty or partially loaded
* The Collector is running without crash logs

## Causes

This issue is typically caused by one or more of the following:

* Incorrect export endpoint
* Missing or invalid API key/token
* Network issues, such as proxy misconfigurations
* TLS verification failures
* Misconfigured pipelines or disabled signals
* Incomplete setup — to capture all telemetry data, you must use the EDOT Collector together with an appropriate EDOT SDK

## Resolution

Use the following checks to identify and fix common configuration or connectivity issues that can prevent telemetry data from reaching {{kib}}.

### Check export endpoint

Make sure the Collector is configured to send data to the correct Elastic endpoint. 

To confirm:

1. Open {{kib}} for your deployment.
2. In the top right, select **Add data**.
3. Select **Application** > **OpenTelemetry**.
4. In the **APM Agents** panel, locate **OpenTelemetry**.
5. Ensure the `endpoint` in your Collector configuration matches exactly.

If you’re using the managed OTLP endpoint, confirm the region and cluster ID are correct.

### Verify authentication headers

Ensure the Collector or SDK includes an API key in the `Authorization` header:

```yaml
headers:
  Authorization: ApiKey <your-api-key>
```

If you’re using environment variables, confirm the key is set correctly in the runtime context.

### Review logs for export errors

Common log messages include:

```
permanent error: rpc error: code = Unavailable desc = connection refused
```

Also look for:

* TLS handshake failures
* Invalid character errors, which may indicate proxy or HTML redirect instead of JSON

Increase verbosity using `--log-level=debug` for deeper insights. <!--Refer to [Enable debug logging] for more information.-->

### Test network connectivity

You can validate connectivity using `curl`:

```bash
curl -v https://<endpoint> -H "Authorization: ApiKey <your-key>"
```

Or use `telnet` or `nc` to verify port 443 is reachable.

<!--### Check proxy environment variables

Ensure environment variables are correctly set in your deployment. Refer to [EDOT proxy settings] for more information relevant to your configuration.

In Kubernetes or container environments, pass these as `env:` entries.
-->

### Validate signal configuration

Check that each pipeline is defined properly in your configuration:

```yaml
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [...]
      exporters: [otlp]
```

If only logs are configured, metrics and traces will not be sent.