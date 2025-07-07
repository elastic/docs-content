---
navigation_title: EDOT Collector
description: Troubleshooting common issues with the EDOT Collector.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Troubleshoot the EDOT Collector

Perform these checks when troubleshooting common Collector issues:

* Check logs: Review the Collector’s logs for error messages.
* Validate configuration: Use the `--dry-run` option to test configurations.
* Enable debug logging: Run the Collector with `--log-level=debug` for detailed logs.
* Check service status: Ensure the Collector is running with `systemctl status <collector-service>` (Linux) or `tasklist` (Windows).
* Test connectivity: Use `telnet <endpoint> <port>` or `curl` to verify backend availability.
* Check open ports: Run netstat `-tulnp or lsof -i` to confirm the Collector is listening.
* Monitor resource usage: Use top/htop (Linux) or Task Manager (Windows) to check CPU & memory.
* Validate exporters: Ensure exporters are properly configured and reachable.
* Verify pipelines: Use `otelctl` diagnose (if available) to check pipeline health.
* Check permissions: Ensure the Collector has the right file and network permissions.
* Review recent changes: Roll back recent config updates if the issue started after changes.

For in-depth details on troubleshooting refer to the [OpenTelemetry Collector troubleshooting documentation](https://opentelemetry.io/docs/collector/troubleshooting/).