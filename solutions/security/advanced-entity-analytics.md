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
| {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` Manage watchlists and factor membership into risk scoring | [](/solutions/security/advanced-entity-analytics/watchlists.md) |
| {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` Link entity records representing the same real-world identity | [](/solutions/security/advanced-entity-analytics/entity-resolution.md) |
| {applies_to}`stack: preview 9.4+` {applies_to}`serverless: preview` Hunt for threats using AI-generated leads | [](/solutions/security/advanced-entity-analytics/overview.md) |
| {applies_to}`stack: preview 9.4+` {applies_to}`serverless: preview` Investigate entity connections and relationships in a graph | [Visualizations](/solutions/security/advanced-entity-analytics/view-entity-details.md#visualizations) |
| {applies_to}`stack: removed =9.4, ga =9.3, preview 9.1-9.2` Monitor privileged user activity | [](/solutions/security/advanced-entity-analytics/privileged-user-monitoring.md) |

## How entity analytics works

Entity analytics operates continuously across several stages:

1. **Collects data:** Risk scoring ingests several [risk inputs](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md#security-entity-risk-scoring-risk-scoring-inputs) from across your {{elastic-sec}} deployment.
2. **Scores risk:**  Risk scores (0–100) are calculated for hosts, users, and services based on alert severity, frequency, and asset criticality. Scores are recalculated on a recurring interval.
3. **Detects anomalies:** Prebuilt {{ml}} jobs identify unusual patterns in user and host behavior that may indicate compromise or insider threats.
4. **Enriches entities:** The [entity store](/solutions/security/advanced-entity-analytics/entity-store.md) reconciles data from ingested logs, identity providers, and risk scores into a unified view of each entity.

    {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` The entity store resolves entities using shared identity matching across sources, so a single real-world entity observed across multiple identity providers appears as one deduplicated record.

## Key capabilities

Entity analytics provides the following core capabilities that work together to give you a complete picture of entity risk across your environment.

### Entity risk scoring

Assign risk scores to hosts, users, and services based on detection alerts and asset criticality. Risk scoring runs on a recurring interval, using a weighted sum to calculate scores from 0 (lowest risk) to 100 (highest risk). Use risk scores to identify which entities require immediate attention and track how risk changes over time.

### Advanced behavioral detections

Use {{ml}} anomaly detection to identify suspicious behavior patterns — such as unusual login locations, atypical process execution, or abnormal network activity — that rule-based detections might miss. Prebuilt {{ml}} jobs are tailored to common security use cases.

### Watchlists
```yaml {applies_to}
stack: ga 9.4+
serverless: ga
```

Define custom groups of entities — such as executives or critical infrastructure hosts — and factor watchlist membership directly into entity risk scoring. A built-in **Privileged Users** watchlist automatically pulls in administrative users from [Active Directory](integration-docs://reference/entityanalytics_ad.md) and [Okta](integration-docs://reference/entityanalytics_okta.md)integrations.

### Entity resolution
```yaml {applies_to}
stack: ga 9.4+
serverless: ga
```

Link multiple entity records that represent the same real-world identity into a resolution group. The primary entity aggregates risk scores from all linked records, giving you a consolidated view across identity providers such as Okta, Active Directory, and Entra ID.

### Graph visualization
```yaml {applies_to}
stack: preview 9.4+
serverless: preview
```

Investigate entity connections and relationships directly from the entity details flyout. The overview panel shows a graph preview of the entity's connections over the last 30 days, and the **Graph View** tab in the expanded panel provides a full interactive investigation experience. Graph visualization requires [entity store](/solutions/security/advanced-entity-analytics/entity-store.md) to be enabled and populated in the active space.

### Privileged user monitoring
```yaml {applies_to}
stack: removed =9.4, ga =9.3, preview 9.1-9.2
```

Track the activity of users with elevated permissions, such as system administrators or users with access to sensitive data. Identify suspicious activities like over-provisioning of rights or potential insider threats before they cause damage.

## Next steps

- [Turn on risk scoring](/solutions/security/advanced-entity-analytics/turn-on-risk-scoring-engine.md) to begin calculating entity risk scores.
- [Enable the entity store](/solutions/security/advanced-entity-analytics/entity-store.md) for centralized entity management.
- [Set up anomaly detection](/solutions/security/advanced-entity-analytics/anomaly-detection.md) to identify behavioral threats.
- [Assign asset criticality](/solutions/security/advanced-entity-analytics/asset-criticality.md) to prioritize high-value entities.
- Use the [Entity analytics page](/solutions/security/advanced-entity-analytics/overview.md) to review risk scores, surface anomalies, and prioritize investigations.
- {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` [Create watchlists](/solutions/security/advanced-entity-analytics/watchlists.md) to factor entity group membership into risk scoring.
- [Explore host, user, and network data](/solutions/security/advanced-entity-analytics/explore.md) across your environment.