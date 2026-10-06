---
navigation_title: Manage
description: Manage Elastic Security after setup, including Elastic Defend policies and exceptions, cloud workload protection, feature privileges, and workspace settings.
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Manage {{elastic-sec}}

After you deploy {{elastic-sec}}, you return to these tasks as your environment and team change. Tune protection policies, manage exceptions, control who can use each feature, and decide which data the {{security-app}} shows.

For one-time deployment tasks, such as installing {{elastic-defend}} or connecting your cloud accounts, refer to [Set up](/solutions/security/set-up.md).

## Where your settings apply

{{elastic-sec}} settings apply at different levels, so a change in one place can affect more than one host or user:

- **Integration policies** control protection on your hosts and workloads. {{elastic-defend}} and Defend for Containers policies are part of {{agent}} policies, so each change applies to every host that uses that policy.
- **Roles** control what each user can view and do. Each feature has its own privileges, and you assign them to roles.
- **Spaces** separate your security content. Detection rules, exceptions, alerts, Timelines, and cases in one {{kib}} space aren't visible in other spaces. {applies_to}`stack: preview 9.1` You can also scope {{elastic-defend}} policies, artifacts, and response actions by space.
- **{{data-sources-cap}}** control which indices the {{security-app}} reads in each space.

## Where to start

| Your goal | Start here |
|---|---|
| Monitor protected endpoints, tune policies, or reduce false positives from {{elastic-defend}} | [Manage {{elastic-defend}}](/solutions/security/manage-elastic-defend.md) |
| Detect and block threats on Linux VMs and Kubernetes workloads at runtime | [Manage cloud workload protection](/solutions/security/manage/manage-cloud-workload-protection.md) |
| Give users the access they need for each feature | [Access control](/solutions/security/manage/access-control.md) |
| Organize security content into spaces, or change which data the {{security-app}} shows | [Configure workspace settings](/solutions/security/manage/configure-workspace-settings.md) |

## Next steps

After you configure your environment, you can:

- [Detect and alert](/solutions/security/detect-and-alert.md) on threats with prebuilt and custom detection rules.
- [Respond and contain](/solutions/security/respond-and-contain.md) threats by triaging alerts and isolating hosts.
- [Troubleshoot {{elastic-defend}}](/troubleshoot/security/elastic-defend.md) if you run into installation, connectivity, or policy issues.
