---
description: Manage Elastic Defend endpoints, policies, exceptions, and protection settings. Configure trusted applications, event filters, blocklists, and more.
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/sec-manage-intro.html
  - https://www.elastic.co/guide/en/serverless/current/security-manage-endpoint-protection.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Manage {{elastic-defend}} [sec-manage-intro]

After deploying {{elastic-defend}}, you can manage your protected endpoints, tune policies, and create exceptions to reduce false positives — all from within {{elastic-sec}}. These management tools give you centralized control over endpoint protection across your environment.

{{elastic-sec}} provides dedicated pages for each management area. Find them in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Use them to monitor endpoint health, adjust protection policies, and define exceptions that keep {{elastic-defend}} running smoothly alongside your existing software and workflows.

## Where to start

| Your goal | Start here |
|---|---|
| View and monitor protected endpoints | [Endpoints](/solutions/security/manage-elastic-defend/endpoints.md) |
| Adjust protection settings or event collection | [Policies](/solutions/security/manage-elastic-defend/policies.md) → [Configure an integration policy](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md) |
| Reduce false positives from known software | [Trusted applications](/solutions/security/manage-elastic-defend/trusted-applications.md) → [Event filters](/solutions/security/manage-elastic-defend/event-filters.md) |
| Suppress false positive {{elastic-endpoint}} alerts | [{{elastic-endpoint}} exceptions](/solutions/security/manage-elastic-defend/elastic-endpoint-exceptions.md) |
| Block known malicious applications | [Blocklist](/solutions/security/manage-elastic-defend/blocklist.md) |
| Understand different {{elastic-endpoint}} configuration settings | [Optimize {{elastic-defend}}](/solutions/security/manage-elastic-defend/optimize-elastic-defend.md) |
| Diagnose problems with {{elastic-defend}} | [Automatic troubleshooting](/solutions/security/manage-elastic-defend/automatic-troubleshooting.md) → [Troubleshoot {{elastic-defend}}](/troubleshoot/security/elastic-defend.md) |
| Prevent users from removing {{agent}}, or remove it from a host | [Prevent {{agent}} uninstallation](/solutions/security/configure-elastic-defend/prevent-elastic-agent-uninstallation.md) → [Uninstall {{agent}}](/solutions/security/configure-elastic-defend/uninstall-elastic-agent.md) |

## Endpoints and policies

The [Endpoints](/solutions/security/manage-elastic-defend/endpoints.md) page shows every host running {{elastic-defend}}, including its status, policy assignment, and operating system. Use it to verify that endpoints are healthy, check which policy each host is using, and drill into individual endpoint details.

The [Policies](/solutions/security/manage-elastic-defend/policies.md) page lists all {{elastic-defend}} integration policies. From here, you can open a policy to adjust its protection levels, event collection settings, and advanced options.

To configure those settings, refer to [Configure an integration policy for {{elastic-defend}}](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md). To change a specific part of a policy, refer to:

- [Configure updates for protection artifacts](/solutions/security/configure-elastic-defend/configure-updates-for-protection-artifacts.md): Control how {{elastic-defend}} receives the latest threat detections, malware models, and other protection artifacts.
- [Configure Linux file system monitoring](/solutions/security/configure-elastic-defend/configure-linux-file-system-monitoring.md): Set which file systems {{elastic-defend}} monitors on Linux hosts.
- [Create an {{elastic-defend}} policy using the API](/solutions/security/configure-elastic-defend/create-an-elastic-defend-policy-using-api.md): Create and customize a policy without the UI.
- [Configure offline endpoints and air-gapped environments](/solutions/security/configure-elastic-defend/configure-offline-endpoints-air-gapped-environments.md): Keep protection artifacts up to date on hosts that can't reach Elastic's servers.

## Endpoint artifacts

[Endpoint artifacts](/solutions/security/manage-elastic-defend/endpoint-artifacts.md) let you tailor {{elastic-defend}} behavior to your environment, reducing noise without weakening protection. They include trusted applications, trusted devices, event filters, host isolation exceptions, blocklist entries, and {{elastic-endpoint}} exceptions. Each type changes a different behavior, so compare them in [Optimize {{elastic-defend}}](/solutions/security/manage-elastic-defend/optimize-elastic-defend.md) before you create one.

## Protection and security

{{elastic-defend}} includes built-in protection features and prebuilt detection rules that help secure your endpoints and prevent tampering.

- [Endpoint protection rules](/solutions/security/manage-elastic-defend/endpoint-protection-rules.md): Prebuilt detection rules that help you manage and respond to alerts generated by {{elastic-endpoint}}, including rules for malware, ransomware, memory threats, and malicious behavior.
- [{{elastic-endpoint}} self-protection](/solutions/security/manage-elastic-defend/elastic-endpoint-self-protection-features.md): Built-in tamper protection that prevents users and attackers from interfering with {{elastic-endpoint}} functionality.
- [Allowlist {{elastic-endpoint}} in third-party antivirus apps](/solutions/security/manage-elastic-defend/allowlist-elastic-endpoint-in-third-party-antivirus-apps.md): Add {{elastic-endpoint}}'s digital signatures and file paths to your antivirus software's allowlist to prevent conflicts.
- [Configure self-healing rollback for Windows endpoints](/solutions/security/configure-elastic-defend/configure-self-healing-rollback-for-windows-endpoints.md): Erase attack artifacts that a malicious process deployed before {{elastic-defend}} detected it.

## Performance and troubleshooting

Use these tools to diagnose issues, reduce resource usage, and understand how {{elastic-defend}} collects event data.

- [Automatic troubleshooting](/solutions/security/manage-elastic-defend/automatic-troubleshooting.md): Identify and resolve common issues that could prevent {{elastic-defend}} from working as intended, including policy response errors and third-party antivirus conflicts.
- [Event capture and {{elastic-defend}}](/solutions/security/manage-elastic-defend/event-capture-elastic-defend.md): Understand how {{elastic-defend}} collects, aggregates, and deduplicates system event data to balance threat detection with storage and performance overhead.
- [Troubleshoot {{elastic-defend}}](/troubleshoot/security/elastic-defend.md): Resolve common issues such as {{agent}} connectivity problems, policy failures, and malware prevention errors.
- [Turn off diagnostic data for {{elastic-defend}}](/solutions/security/configure-elastic-defend/turn-off-diagnostic-data-for-elastic-defend.md): Stop {{elastic-defend}} from streaming the diagnostic data Elastic uses to tune protection features.
- [Configure data volume](/solutions/security/configure-elastic-defend/configure-data-volume-for-elastic-endpoint.md): Change how much data {{elastic-endpoint}} processes and ingests, and understand the effect on storage and CPU usage.

## Agent lifecycle

- [Prevent {{agent}} uninstallation](/solutions/security/configure-elastic-defend/prevent-elastic-agent-uninstallation.md): Turn on agent tamper protection so users can't bypass or turn off endpoint protection.
- [Uninstall {{agent}}](/solutions/security/configure-elastic-defend/uninstall-elastic-agent.md): Remove {{agent}} from a host.

## Related pages

- [Configure endpoint protection with {{elastic-defend}}](/solutions/security/configure-elastic-defend.md): Install {{elastic-defend}} and set up integration policies.
- [Endpoint response actions](/solutions/security/endpoint-response-actions.md): Isolate hosts, run commands, and take other response actions on protected endpoints.
