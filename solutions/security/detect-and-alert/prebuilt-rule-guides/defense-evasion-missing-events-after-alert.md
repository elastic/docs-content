---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Elastic Defend Alert Followed by Telemetry Loss" prebuilt detection rule.'
---

# Elastic Defend Alert Followed by Telemetry Loss

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Elastic Defend Alert Followed by Telemetry Loss

This rule identifies situations where an Elastic Defend alert is generated on a host and is not followed by
any normal endpoint activity events within a short time window. This may indicate agent tampering, sensor
disablement, host shutdown, system crash, or defense evasion behavior.

### Possible investigation steps

- Review the original `endpoint.alert` event and identify the detection that triggered the alert.
- Check the host’s online status, uptime, and reboot history.
- Verify the health and status of the Elastic Defend agent and related services.
- Look for evidence of agent tampering, service stops, or security control modifications.
- Correlate with activity immediately preceding the alert for signs of exploitation or evasion.
- Determine if similar alert → silence patterns are occurring on other hosts.

### False positive analysis

- Legitimate system reboots or shutdowns
- Network connectivity loss
- Elastic Agent upgrades or restarts
- Endpoint service crashes
- Maintenance or IT operations

### Response and remediation

- Validate host and agent availability.
- Reconnect or re-enroll the agent if telemetry is missing.
- Isolate the host if malicious activity is suspected.
- Investigate for security control tampering.
- Perform broader environment hunting for similar patterns.
