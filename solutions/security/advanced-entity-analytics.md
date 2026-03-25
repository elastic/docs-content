---
navigation_title: Entity analytics
description: Assess entity risk for hosts, users, and services, detect behavioral anomalies with machine learning, and monitor privileged users in Elastic Security.
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/advanced-entity-analytics-overview.html
  - https://www.elastic.co/guide/en/serverless/current/security-advanced-entity-analytics.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Entity analytics [advanced-entity-analytics-overview]

Entity analytics helps security teams detect emerging threats by assessing the risk posture of hosts, users, and services across your environment. It combines the SIEM detection engine with {{ml}} to score entity risk, identify anomalous behavior, and surface insider threats, so you can prioritize investigations and respond faster.

Rather than triaging alerts one at a time, entity analytics continuously evaluates risk using detection alerts, asset criticality assignments, and behavioral anomalies. You can focus on the entities that pose the greatest risk and investigate the full pattern of activity behind each score.

## Where to start

| Your goal | Start here |
|-----------|------------|
| Set up entity risk scoring for the first time | [](/solutions/security/advanced-entity-analytics/entity-risk-scoring-requirements.md) → [](/solutions/security/advanced-entity-analytics/turn-on-risk-scoring-engine.md) |
| Monitor risk scores for hosts, users, and services | [](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md) → [](/solutions/security/advanced-entity-analytics/view-analyze-risk-score-data.md) |
| Detect behavioral anomalies with machine learning | [](/solutions/security/advanced-entity-analytics/advanced-behavioral-detections.md) → [Anomaly detection](/solutions/security/advanced-entity-analytics/anomaly-detection.md) |
| Prioritize high-value assets | [](/solutions/security/advanced-entity-analytics/asset-criticality.md) |
| Monitor privileged user activity | [](/solutions/security/advanced-entity-analytics/privileged-user-monitoring.md) |

## How entity analytics works

Entity analytics operates continuously across several stages:

1. **Collect data:** The risk scoring engine ingests detection alerts, asset criticality levels, and privileged user designations from across your {{elastic-sec}} deployment.
2. **Score risk:** The engine calculates risk scores (0–100) for hosts, users, and services based on alert severity, frequency, and asset criticality. Scores are recalculated on a recurring interval.
3. **Detect anomalies:** Prebuilt {{ml}} jobs identify unusual patterns in user and host behavior that may indicate compromise or insider threats.
4. **Enrich entities:** The [entity store](/solutions/security/advanced-entity-analytics/entity-store.md) reconciles data from ingested logs, identity providers, and risk scores into a unified view of each entity.
5. **Investigate and respond:** The [Entity analytics overview page](/solutions/security/advanced-entity-analytics/overview.md) surfaces the highest-risk entities, anomalies, and KPIs so you can triage and investigate efficiently.

## Key capabilities

Entity analytics provides the following core capabilities that work together to give you a complete picture of entity risk across your environment.

### Entity risk scoring

Assign risk scores to hosts, users, and services based on detection alerts and asset criticality. The risk scoring engine runs on a recurring interval, using a weighted sum to calculate scores from 0 (lowest risk) to 100 (highest risk). Use risk scores to identify which entities require immediate attention and track how risk changes over time.

### Advanced behavioral detections

Use {{ml}} anomaly detection to identify suspicious behavior patterns — such as unusual login locations, atypical process execution, or abnormal network activity — that rule-based detections might miss. Prebuilt {{ml}} jobs are tailored to common security use cases.

### Privileged user monitoring
```yaml {applies_to}
stack: preview 9.1-9.2, ga 9.3+
serverless: ga
```

Track the activity of users with elevated permissions, such as system administrators or users with access to sensitive data. Identify suspicious activities like over-provisioning of rights or potential insider threats before they cause damage.

## Next steps

- [Turn on the risk scoring engine](/solutions/security/advanced-entity-analytics/turn-on-risk-scoring-engine.md) to begin calculating entity risk scores.
- [Enable the entity store](/solutions/security/advanced-entity-analytics/entity-store.md) for centralized entity management.
- [Set up anomaly detection](/solutions/security/advanced-entity-analytics/anomaly-detection.md) to identify behavioral threats.
- [Assign asset criticality](/solutions/security/advanced-entity-analytics/asset-criticality.md) to prioritize high-value entities.
- [Explore host, user, and network data](/solutions/security/advanced-entity-analytics/explore.md) across your environment.