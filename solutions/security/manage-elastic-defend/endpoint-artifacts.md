---
description: Use endpoint artifacts to adapt Elastic Defend to your environment, including trusted applications, event filters, blocklist entries, and Elastic Endpoint exceptions.
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Endpoint artifacts

Use endpoint artifacts to adapt {{elastic-defend}} to the software, devices, and network traffic in your environment. With artifacts, you can stop false positive alerts, avoid conflicts with other security tools, store less event data in {{es}}, and block applications that you know are malicious.

Each artifact type changes a different part of how {{elastic-endpoint}} handles activity on the host. Some types prevent alerts, some prevent monitoring, and some keep {{es}} from storing events. Before you create an artifact, check which type fits your goal.

## How endpoint artifacts work

Keep these points in mind when you create artifacts:

- **Artifacts apply to all hosts by default**: A new artifact applies to every host running {{elastic-defend}}. To limit it to some hosts, assign it to specific {{elastic-defend}} integration policies instead. {{elastic-endpoint}} exceptions support per-policy assignment only after you [opt in](/solutions/security/manage-elastic-defend/elastic-endpoint-exceptions.md#endpoint-exceptions-opt-in).
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` **One page lists every artifact type**: Go to the **Artifacts** page, then select the tab for the artifact type that you want to manage.
- {applies_to}`stack: preview 9.1+` **Spaces control who can edit an artifact**: Global artifacts appear in every space. A per-policy artifact belongs to the space where you create it, and only users in that space or with the **Global artifact management** privilege can edit it. To learn more, refer to the [Spaces and {{elastic-defend}} FAQ](/solutions/security/get-started/spaces-defend-faq.md#spaces-security-faq-endpoint-artifacts).

## Where to start

| Your goal | Start here |
|---|---|
| Compare the artifact types and find the one that fits your goal | [Optimize {{elastic-defend}}](/solutions/security/manage-elastic-defend/optimize-elastic-defend.md) |
| Stop {{elastic-endpoint}} from generating alerts for activity that you expect | [{{elastic-endpoint}} exceptions](/solutions/security/manage-elastic-defend/elastic-endpoint-exceptions.md) |
| Avoid conflicts with other antivirus or endpoint security software | [Trusted applications](/solutions/security/manage-elastic-defend/trusted-applications.md) |
| {applies_to}`serverless: ga` {applies_to}`stack: ga 9.2+` Allow specific USB storage devices to connect to protected hosts | [Trusted devices](/solutions/security/manage-elastic-defend/trusted-devices.md) |
| Keep {{es}} from storing high-volume or low-value endpoint events | [Event filters](/solutions/security/manage-elastic-defend/event-filters.md) |
| Let isolated hosts communicate with specific IP addresses | [Host isolation exceptions](/solutions/security/manage-elastic-defend/host-isolation-exceptions.md) |
| Prevent known malicious applications from running | [Blocklist](/solutions/security/manage-elastic-defend/blocklist.md) |
| Check how to enter file paths and other values for each exception type | [Exception types and value syntax](/solutions/security/manage-elastic-defend/exception-types-and-syntax.md) |

## Next steps

After you create artifacts, you can:

- Give users the [{{elastic-defend}} feature privileges](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md) they need to view or manage each artifact type.
- Review [endpoint protection rules](/solutions/security/manage-elastic-defend/endpoint-protection-rules.md) to understand the alerts that {{elastic-endpoint}} exceptions can prevent.
