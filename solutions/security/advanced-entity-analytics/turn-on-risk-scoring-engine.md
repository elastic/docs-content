---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/turn-on-risk-engine.html
  - https://www.elastic.co/guide/en/serverless/current/security-turn-on-risk-engine.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Turn on the risk scoring engine


::::{important}
To use entity risk scoring, your role must have the appropriate user role or privileges. For more information, refer to [Entity risk scoring requirements](/solutions/security/advanced-entity-analytics/entity-risk-scoring-requirements.md).
::::


## Preview risky entities [_preview_risky_entities]

You can preview risky entities before installing the latest risk engine. The preview shows the riskiest hosts, users, and services found in the 1000 sampled entities during the time frame selected in the date picker.

::::{note}
The preview is limited to two risk scores per {{kib}} instance or serverless project.
::::


To preview risky entities, find **Entity risk score** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).


## Turn on the latest risk engine [_turn_on_the_latest_risk_engine]

::::{note}
* To view risk score data, you must have alerts generated in your environment.
* In {{stack}}, if you previously installed the original user and host risk score modules, and you’re upgrading to {{stack}} version 9.0 or later, refer to [Upgrade to the latest risk engine](/solutions/security/advanced-entity-analytics/turn-on-risk-scoring-engine.md#upgrade-risk-engine).

::::


If you’re installing the risk scoring engine for the first time:

1. Find **Entity risk score** in the navigation menu or using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. On the **Entity risk score** page, turn the toggle on.
3. {applies_to}`stack: ga 9.2+` {applies_to}`serverless: ga` Choose whether to retain [residual risk scores](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md#residual-risk-score).
4. Optionally, specify a date and time range for the calculation.
5. Choose whether to include `Closed` alerts in risk scoring calculations.
6. {applies_to}`stack: ga 9.3+` {applies_to}`serverless: ga` Optionally, filter out alerts by defining conditions for the entity types or attributes that you want to exclude from the calculation. For example, if you don't want to calculate risk scores for users with a **Low impact** asset criticality level, enter `not user.asset.criticality: "low_impact"`.

:::{image} /solutions/images/security-turn-on-risk-engine.png
:alt: Turn on entity risk scoring
:screenshot:
:::


## Upgrade to the latest risk engine [upgrade-risk-engine]
```yaml {applies_to}
stack:
```

If you upgraded to 9.0 or later from an earlier {{stack}} version, and you have the original risk engine installed, you can upgrade to the latest risk engine. You will be prompted to upgrade in places where risk score data exists, such as:

* The Entity Analytics dashboard
* The **User risk** tab on the Users page
* The **User risk** tab on a user’s details page
* The **Host risk** tab on the Hosts page
* The **Host risk** tab on a host’s details page

:::{image} /solutions/images/security-risk-engine-upgrade-prompt.png
:alt: Prompt to upgrade to the latest risk engine
:screenshot:
:::

1. Click **Manage** in the upgrade prompt, or find **Entity risk score** in the navigation menu.
2. On the Entity Risk Score page, click **Start update** next to the **Update available** label.

    :::{image} /solutions/images/security-risk-score-start-update.png
    :alt: Start the risk engine upgrade
    :screenshot:
    :::

3. On the confirmation message, click **Yes, update now**. The old transform is removed and the latest risk engine is installed.
4. When the installation is complete, confirm that the **Entity risk score** toggle is on.

    :::{image} /solutions/images/security-turn-on-risk-engine.png
    :alt: Turn on entity risk scoring
    :screenshot:
    :::


::::{note}
Previous risk score data is retained when you upgrade to the latest risk engine.
::::
