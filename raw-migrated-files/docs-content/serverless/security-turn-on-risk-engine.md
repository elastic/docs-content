---
navigation_title: "Turn on risk scoring"
---

# Turn on the risk scoring engine [security-turn-on-risk-engine]


::::{admonition} Requirements
:class: note

To use entity risk scoring, you must have the appropriate user role. For more information, refer to [Entity risk scoring requirements](../../../solutions/security/advanced-entity-analytics/entity-risk-scoring-requirements.md).

::::



## Preview risky entities [security-turn-on-risk-engine-preview-risky-entities]

You can preview risky entities before installing the risk engine. The preview shows the riskiest hosts and users found in the 1000 sampled entities during the time frame selected in the date picker.

::::{note}
The preview is limited to two risk scores per serverless project.

::::


To preview risky entities, go to **Project settings** → **Management** → **Entity Risk Score**:

:::{image} ../../../images/serverless-preview-risky-entities.png
:alt: Preview of risky entities
:class: screenshot
:::


## Turn on the risk engine [security-turn-on-risk-engine-turn-on-the-risk-engine]

::::{note}
To view risk score data, you must have alerts generated in your environment.

::::


If you’re installing the risk scoring engine for the first time:

1. Go to **Project settings** → **Management** → **Entity Risk Score**.
2. On the **Entity Risk Score** page, turn the toggle on.

You can also choose to include `Closed` alerts in risk scoring calculations and specify a date and time range for the calculation.

:::{image} ../../../images/serverless-turn-on-risk-engine.png
:alt: Turn on entity risk scoring
:class: screenshot
:::
