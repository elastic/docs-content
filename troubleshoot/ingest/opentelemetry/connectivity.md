---
navigation_title: Connectivity issues
description: Troubleshoot connectivity issues between EDOT SDKs, the EDOT Collector, and Elastic.
applies_to:
  serverless: ga
  product:
      edot_collector: ga  
products:
  - id: observability
  - id: edot-collector
  - id: edot-sdk
---

# Connectivity issues with EDOT

Connectivity problems occur when the EDOT SDKs or the EDOT Collector can't reach Elastic. Even with correct proxy settings, network restrictions such as blocked ports or firewalls can prevent data from flowing.

:::{tip}
If you're sending EDOT SDK telemetry directly to {{apm-server}}'s OTel intake, note that this flow is not supported. Send data to an [EDOT Collector Gateway](elastic-agent://reference/edot-collector/modes.md#edot-collector-as-gateway) or [Managed OTel intake](opentelemetry://reference/motlp.md) instead.
:::


## Symptoms

You might see one or more of the following error messages:

- `connection refused`
- `network unreachable`
- `i/o timeout`
- `tls: handshake failure`

These errors might appear either in application logs (from the SDK) or in the Collector logs.

Example (Collector):

```text
2024-09-15T12:44:30Z error exporterhelper/queued_retry.go:149 Exporting failed. Rejecting data. Error: context deadline exceeded
```

Example (Python SDK):

```text
opentelemetry.sdk ERROR OTLPSpanExporter - Failed to export spans: [Errno 111] Connection refused
```

## Causes

Connectivity errors usually trace back to one of the following issues:

- **Firewall or port blocking**  

  Outbound traffic may be blocked by corporate firewalls or network policies. 

  Check that the required protocol and port combination is allowed:

  - OTLP/HTTP: TCP 4318  
  - OTLP/gRPC: TCP 4317  
  - {{es}} (over HTTPS): 443  
  - {{es}}: 9200  

  Also confirm whether your environment uses IPv4 or IPv6, as routing and firewall rules may differ.


- **Endpoint errors**  
  
  The endpoint is unreachable or not listening on the specified port: 
  
  - `connection refused`: endpoint not listening  
  - `network unreachable`: VPN, routing, or DNS failure  
  - `timeout`: traffic dropped by firewall, proxy, or load balancer

- **Proxy misconfiguration**  
  
  Proxy environment variables (`HTTP_PROXY`, `HTTPS_PROXY`) might be set correctly but the proxy itself lacks access to Elastic or restricts ports. Refer to [Proxy settings](opentelemetry://reference/edot-collector/config/proxy.md) for more information.


### Differences between SDK and Collector issues

Errors can look similar whether they come from an SDK or the Collector. Identifying the source helps you isolate the problem.

:::{note}
Note: Some SDKs support setting a proxy directly (for example, using `HTTPS_PROXY`). Refer to [Proxy settings for EDOT SDKs](/troubleshoot/ingest/opentelemetry/edot-sdks/proxy.md) for details.
:::

#### SDK

Application logs report failures when the SDK cannot send data to the Collector or directly to Elastic. These often appear as `connection refused` or `timeout` messages. If seen, verify that the Collector endpoint is reachable.

For guidance on enabling logs in your SDK, refer to [Enable SDK debug logging](/troubleshoot/ingest/opentelemetry/edot-sdks/enable-debug-logging.md).

Example (Java SDK):

```text
io.opentelemetry.exporter.otlp.internal.grpc.OkHttpGrpcExporter - Failed to export spans. Error: UNAVAILABLE: io exception
```

#### The Collector

Collector logs show export failures when it cannot forward data to Elastic. Look for messages like `cannot send spans` or `failed to connect to <endpoint>`. If present, confirm the Collector’s exporters configuration and network access.


## Resolution

Before you dig into SDK or Collector configuration, confirm that your environment can reach the Elastic endpoint. 

:::{note}
The examples below use command syntax from Linux and macOS. On Windows or when testing IPv6, the equivalent tooling or syntax may differ (for example, `Test-NetConnection` in PowerShell).
:::

:::::{stepper}

::::{step} Verify DNS resolution

Make sure the hostname for your Elastic endpoint resolves correctly:  

```bash
nslookup <your-endpoint>
```

::::

::::{step} Test network reachability

```bash
ping <your-endpoint>
```

::::

::::{step} Check open ports

Test whether the required OTLP ports are open (default `443` for HTTPS):

```bash
nc -vz <your-endpoint> 443
```

::::

::::{step} Verify TLS/SSL

Check that TLS certificates can be validated:

```bash
openssl s_client -connect <your-endpoint>:443
```

::::

:::::

If any of these steps fail, the issue is likely caused by network infrastructure rather than your SDK or Collector configuration.


### Next steps

If basic checks and configuration look correct but issues persist, collect more details before escalating:

* Review proxy settings. For more information, refer to [Proxy settings](opentelemetry://reference/edot-collector/config/proxy.md).

* If ports are confirmed open but errors persist, [enable debug logging in the SDK](/troubleshoot/ingest/opentelemetry/edot-sdks/enable-debug-logging.md) or [in the Collector](/troubleshoot/ingest/opentelemetry/edot-collector/enable-debug-logging.md) for more detail.

* Contact your network administrator with test results if you suspect firewall restrictions.