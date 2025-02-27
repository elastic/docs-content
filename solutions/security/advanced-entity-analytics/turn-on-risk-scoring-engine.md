---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/turn-on-risk-engine.html
  - https://www.elastic.co/guide/en/serverless/current/security-turn-on-risk-engine.html
---

# Turn on the risk scoring engine


::::{important}
To use entity risk scoring, your role must have the appropriate user role or privileges. For more information, refer to [Entity risk scoring requirements](/solutions/security/advanced-entity-analytics/entity-risk-scoring-requirements.md).
::::


## Preview risky entities [_preview_risky_entities]

You can preview risky entities before installing the latest risk engine. The preview shows the riskiest hosts and users found in the 1000 sampled entities during the time frame selected in the date picker.

::::{note}
The preview is limited to two risk scores per {{kib}} instance or serverless project.
::::


To preview risky entities, find **Entity Risk Score** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::{image} ../../../images/security-preview-risky-entities.png
:alt: Preview of risky entities
:class: screenshot
:::


## Turn on the latest risk engine [_turn_on_the_latest_risk_engine]

::::{note}
* To view risk score data, you must have alerts generated in your environment.
* In {{stack}}, if you previously installed the original user and host risk score modules, and you’re upgrading to {{stack}} version 8.11 or newer, refer to [Upgrade to the latest risk engine](/solutions/security/advanced-entity-analytics/turn-on-risk-scoring-engine.md#upgrade-risk-engine).

::::


If you’re installing the risk scoring engine for the first time:

1. Find **Entity Risk Score** in the navigation menu.
2. On the **Entity Risk Score** page, turn the toggle on.

You can also choose to include `Closed` alerts in risk scoring calculations and specify a date and time range for the calculation.

:::{image} ../../../images/security-turn-on-risk-engine.png
:alt: Turn on entity risk scoring
:class: screenshot
:::


## Upgrade to the latest risk engine [upgrade-risk-engine]
```yaml {applies_to}
stack:
```

If you upgraded to 8.11 from an earlier {{stack}} version, and you have the original risk engine installed, you can upgrade to the latest risk engine. You will be prompted to upgrade in places where risk score data exists, such as:

* The Entity Analytics dashboard
* The **User risk** tab on the Users page
* The **User risk** tab on a user’s details page
* The **Host risk** tab on the Hosts page
* The **Host risk** tab on a host’s details page

:::{image} ../../../images/security-risk-engine-upgrade-prompt.png
:alt: Prompt to upgrade to the latest risk engine
:class: screenshot
:::

1. Click **Manage** in the upgrade prompt, or find **Entity Risk Score** in the navigation menu.
2. On the Entity Risk Score page, click **Start update** next to the **Update available** label.

    :::{image} ../../../images/security-risk-score-start-update.png
    :alt: Start the risk engine upgrade
    :class: screenshot
    :::

3. On the confirmation message, click **Yes, update now**. The old transform is removed and the latest risk engine is installed.
4. When the installation is complete, confirm that the **Entity risk score** toggle is on.

    :::{image} ../../../images/security-turn-on-risk-engine.png
    :alt: Turn on entity risk scoring
    :class: screenshot
    :::


::::{note}
Previous risk score data is retained when you upgrade to the latest risk engine.
::::
