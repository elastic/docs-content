---
description: Turn on the entity risk scoring engine in Elastic Security to calculate risk scores for hosts, users, and services, and preview risky entities first.
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

# Turn on risk scoring


::::{important}
To use entity risk scoring, your role must have the appropriate user role or privileges. For more information, refer to [Entity analytics requirements](/solutions/security/advanced-entity-analytics/entity-analytics-requirements.md).
::::


## Preview risky entities [_preview_risky_entities]

You can preview risky entities before turning on risk scoring. The preview shows the riskiest hosts, users, and services found in the 1000 sampled entities during the time frame selected in the date picker.

::::{note}
The preview is limited to two risk scores per {{kib}} instance or serverless project.
::::


::::{applies-switch}

:::{applies-item} { stack: ga 9.4+, serverless: ga }
To preview risky entities, go to the **Entity Analytics** management page. Accessing this page differs based on the [solution view](/deploy-manage/manage-spaces.md#spaces-managing) that you're using:
  * **Security solution view**: Find **{{stack-manage-app}} → Entity Analytics** in the navigation menu.
  * **Classic view**: Find **Manage → Entity Analytics** in the navigation menu.
:::

:::{applies-item} { stack: ga 9.0-9.3 }
To preview risky entities, find **Entity risk score** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
:::

::::


## Turn on risk scoring [_turn_on_the_latest_risk_engine]

::::{note}
* To view risk score data, you must have alerts generated in your environment.
* In {{stack}}, if you previously installed the original user and host risk score modules, and you’re upgrading to {{stack}} version 9.0 or later, refer to [Upgrade to the latest risk engine](/solutions/security/advanced-entity-analytics/turn-on-risk-scoring-engine.md#upgrade-risk-engine).
::::



:::::{applies-switch}

::::{applies-item} { stack: ga 9.4+, serverless: ga }

:::{important}
Turning on risk scoring and entity store on deployments with less than 4 GB of memory is not recommended, as the cluster might become heavily loaded by the processes required to run Entity Analytics. For optimal performance, we recommend at least 8 GB of memory.
:::

In the default {{kib}} space, both risk scoring and entity store are enabled automatically.

For non-default spaces, if you're enabling risk scoring for the first time:

1. Go to the **Entity Analytics** management page. Accessing this page differs based on the [solution view](/deploy-manage/manage-spaces.md#spaces-managing) that you're using:
    * **Security solution view**: Find **{{stack-manage-app}} → Entity Analytics** in the navigation menu.
    * **Classic view**: Find **Manage → Entity Analytics** in the navigation menu.
2. Turn the toggle on.

   :::{note}
   The toggle activates both risk scoring and the [entity store](/solutions/security/advanced-entity-analytics/entity-store.md).
   :::

3. In the **Entity Risk Score** tab, choose whether to retain the [last calculated risk scores](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md#residual-risk-score).
4. Optionally, specify a date and time range for the calculation.
5. Choose whether to include closed alerts in risk scoring calculations.
6. Optionally, filter out alerts by defining conditions for the entity types or attributes that you want to exclude from the calculation. For example, if you don't want to calculate risk scores for users with a **Low impact** asset criticality level, enter `not user.asset.criticality: "low_impact"`.
::::

::::{applies-item} { stack: ga 9.0-9.3 }
1. Find **Entity Risk Score** in the navigation menu or using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Turn the toggle on.
3. {applies_to}`stack: ga 9.2-9.3` Choose whether to retain the [last calculated risk scores](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md#residual-risk-score).
4. Optionally, specify a date and time range for the calculation.
5. Choose whether to include closed alerts in risk scoring calculations.
6. {applies_to}`stack: ga =9.3` Optionally, filter out alerts by defining conditions for the entity types or attributes that you want to exclude from the calculation. For example, if you don't want to calculate risk scores for users with a **Low impact** asset criticality level, enter `not user.asset.criticality: "low_impact"`.
::::

:::::

:::{image} /solutions/images/security-turn-on-risk-scoring.png
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

::::{applies-switch}

:::{applies-item} { stack: ga 9.4+ }
1. Click **Manage** in the upgrade prompt, or find the **Entity Analytics** management page in the navigation menu.
2. Click **Start update** next to the **Update available** label.
3. On the confirmation message, click **Yes, update now**. The old transform is removed and the latest risk engine is installed.
4. When the installation is complete, confirm that the **Entity Risk Score** toggle is on.
:::

:::{applies-item} { stack: ga 9.0-9.3 }
1. Click **Manage** in the upgrade prompt, or find **Entity risk score** in the navigation menu.
2. Click **Start update** next to the **Update available** label.
3. On the confirmation message, click **Yes, update now**. The old transform is removed and the latest risk engine is installed.
4. When the installation is complete, confirm that the **Entity risk score** toggle is on.
:::

::::


::::{note}
Previous risk score data is retained when you upgrade to the latest risk engine.
::::
