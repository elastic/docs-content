---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/entity-risk-scoring.html
  - https://www.elastic.co/guide/en/serverless/current/security-entity-risk-scoring.html
applies_to:
  stack: all
  serverless:
    security: all
---

# Entity risk scoring [security-entity-risk-scoring]

Entity risk scoring is an advanced {{elastic-sec}} analytics feature that helps security analysts detect changes in an entity’s risk posture, hunt for new threats, and prioritize incident response.

Entity risk scoring allows you to monitor risk score changes of hosts, users, and services in your environment. When generating advanced scoring analytics, the risk scoring engine utilizes threats from its end-to-end XDR use cases, such as SIEM, cloud, and endpoint. It leverages the Elastic SIEM detection engine to generate host, user, and service risk scores from the last 30 days.

It also generates risk scores on a recurring interval, and allows for easy onboarding and management. The engine is built to factor in risks from all {{elastic-sec}} use cases, and allows you to customize and control how and when risk is calculated.


## Risk scoring inputs [security-entity-risk-scoring-risk-scoring-inputs]

Entity risk scores are determined by the following risk inputs:

| Risk input | Storage location |
| --- | --- |
| [Alerts](../detect-and-alert/manage-detection-alerts.md) | `.alerts-security.alerts-<space-id>` index alias |
| [Asset criticality level](asset-criticality.md) | `.asset-criticality.asset-criticality-<space-id>` index alias |

The resulting entity risk scores are stored in the `risk-score.risk-score-<space-id>` data stream alias, and the latest score for each entity is stored in `risk-score.risk-score-latest-<space-id>`.

::::{note}
Entities without any alerts, or with only `Closed` alerts, are not assigned a risk score.

::::



## How is risk score calculated? [how-is-risk-score-calculated]

1. The risk scoring engine runs hourly to aggregate `Open` and `Acknowledged` alerts from the last 30 days. For each entity, the engine processes up to 10,000 alerts.

    ::::{note}
    When [turning on the risk engine](turn-on-risk-scoring-engine.md), you can choose to also include `Closed` alerts in risk scoring calculations.
    ::::

2. The engine groups alerts by `host.name`, `user.name`, or `service.name`, and aggregates the individual alert risk scores (`kibana.alert.risk_score`) such that alerts with higher risk scores contribute more than alerts with lower risk scores. The resulting aggregated risk score is assigned to the **Alerts** category in the entity’s [risk summary](/solutions/security/advanced-entity-analytics/view-entity-details.md#entity-risk-summary).
3. The engine then verifies the entity’s [asset criticality level](asset-criticality.md). If there is no asset criticality assigned, the entity risk score remains equal to the aggregated score from the **Alerts** category. If a criticality level is assigned, the engine calculates the risk score based on the default risk weight for each criticality level. The asset criticality risk input is assigned to the **Asset Criticality** category in the entity’s risk summary.

    | Asset criticality level | Default risk weight |
    | --- | --- |
    | Low impact | 0.5 |
    | Medium impact | 1 |
    | High impact | 1.5 |
    | Extreme impact | 2 |

    ::::{note}
    Asset criticality levels and default risk weights are subject to change.

    ::::

4. Based on the two risk inputs, the risk scoring engine generates a single entity risk score of 0-100. It assigns a risk level by mapping the risk score to one of these levels:

    | Risk level | Risk score |
    | --- | --- |
    | Unknown | < 20 |
    | Low | 20-40 |
    | Moderate | 40-70 |
    | High | 70-90 |
    | Critical | > 90 |

The risk score is updated every hour based on the configured date and time range, which defaults to 30 days. Each update generates a new score, calculated independently of any previous scores.

::::{dropdown} Click for a risk score calculation example
This example shows how the risk scoring engine calculates the user risk score for `User_A`, whose asset criticality level is **Extreme impact**.

There are 5 open alerts associated with `User_A`:

* Alert 1 with alert risk score 21
* Alert 2 with alert risk score 45
* Alert 3 with alert risk score 21
* Alert 4 with alert risk score 70
* Alert 5 with alert risk score 21

To calculate the user risk score, the risk scoring engine:

1. Sorts the associated alerts in descending order of alert risk score:

    * Alert 4 with alert risk score 70
    * Alert 2 with alert risk score 45
    * Alert 1 with alert risk score 21
    * Alert 3 with alert risk score 21
    * Alert 5 with alert risk score 21

2. Generates an aggregated risk score of 36.16, and assigns it to `User_A`'s **Alerts** risk category.
3. Looks up `User_A`'s asset criticality level, and identifies it as **Extreme impact**.
4. Generates a new risk input under the **Asset Criticality** risk category, with a risk contribution score of 16.95.
5. Adds the asset criticality risk contribution score (16.95) to the aggregated risk score (36.16), and generates a user risk score of 53.11.
6. Assigns `User_A` a **Moderate** user risk level.

If `User_A` had no asset criticality level assigned, the user risk score would remain unchanged at 36.16.

::::


Learn how to [turn on the risk scoring engine](turn-on-risk-scoring-engine.md).
