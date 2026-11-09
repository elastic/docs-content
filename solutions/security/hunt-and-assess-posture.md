---
navigation_title: Hunt and assess posture
description: Review Elastic Security dashboards, cloud posture findings, and entity risk scores to find risks before they become incidents.
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Hunt and assess posture

Find risks in your environment before they become incidents. Review dashboards, cloud posture findings, and entity risk scores to decide where to look first, and come back regularly to see what changed since your last review.

These tools summarize the data that your other {{elastic-sec}} features collect. When a score or finding needs a closer look, use the tools in [Investigate](/solutions/security/investigate.md), such as Timeline, Discover, and {{esql}}, to hunt through the events behind it.

## How dashboards, findings, and risk scores work together

Each tool shows a different view of your risk:

- **Dashboards**: Give you a summary of alerts, cloud posture, entity risk, rule health, and data quality. Use them to see trends and to find the area that needs attention.
- **Cloud Security**: Findings show which cloud and Kubernetes resources fail Center for Internet Security (CIS) benchmark checks, and which AWS EC2 Linux workloads have known vulnerabilities. Cloud Security Posture Management (CSPM) and Kubernetes Security Posture Management (KSPM) find the misconfigurations, and Cloud Native Vulnerability Management (CNVM) finds the vulnerabilities. Each misconfiguration finding includes steps to fix it.
- **Entity analytics**: Scores the risk of each host, user, and service, based on its detection alerts and its asset criticality. It also uses {{ml}} to find unusual behavior. Use it to find the entities to investigate first.

## Where to start

| Your goal | Start here |
|---|---|
| See a summary of alerts, posture, and risk in your environment | [Dashboards](/solutions/security/dashboards.md) → [Overview dashboard](/solutions/security/dashboards/overview-dashboard.md) |
| Find and fix misconfigured cloud and Kubernetes resources | [Cloud Security](/solutions/security/cloud.md) → [CSPM findings](/solutions/security/cloud/findings-page.md) or [KSPM findings](/solutions/security/cloud/findings-page-2.md) |
| Find known vulnerabilities on AWS EC2 Linux workloads | [Cloud Native Vulnerability Management](/solutions/security/cloud/cloud-native-vulnerability-management.md) → [CNVM findings](/solutions/security/cloud/findings-page-3.md) |
| Find the hosts, users, and services with the highest risk | [Entity risk scoring](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md) → [View and analyze risk score data](/solutions/security/advanced-entity-analytics/view-analyze-risk-score-data.md) |
| Find unusual behavior with {{ml}} | [Advanced behavioral detections](/solutions/security/advanced-entity-analytics/advanced-behavioral-detections.md) |
| Check that your detection rules and data are healthy | [Detection rule monitoring dashboard](/solutions/security/dashboards/detection-rule-monitoring-dashboard.md) → [Data Quality dashboard](/solutions/security/dashboards/data-quality-dashboard.md) |

## Next steps

After you find a risk, you can:

- [Investigate](/solutions/security/investigate.md) the events behind it with Timeline, Discover, and {{esql}}.
- [Respond and contain](/solutions/security/respond-and-contain.md) threats that you confirm.
- [Write custom detection rules](/solutions/security/detect-and-alert/author-rules.md) so that {{elastic-sec}} alerts you when the same risk appears again.
