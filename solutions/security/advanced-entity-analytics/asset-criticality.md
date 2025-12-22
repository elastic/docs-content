---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/asset-criticality.html
  - https://www.elastic.co/guide/en/serverless/current/security-asset-criticality.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Asset criticality [asset-criticality]

::::{admonition} Requirements
To view and assign asset criticality, you must have the appropriate user role. For more information, refer to [Entity risk scoring requirements](entity-risk-scoring-requirements.md).

::::


The asset criticality feature allows you to classify your organization’s entities based on various operational factors that are important to your organization. Through this classification, you can improve your threat detection capabilities by focusing your alert triage, threat-hunting, and investigation activities on high-impact entities.

You can assign one of the following asset criticality levels to your entities, based on their impact:

* Low impact
* Medium impact
* High impact
* Extreme impact

For example, you can assign **Extreme impact** to business-critical entities, or **Low impact** to entities that pose minimal risk to your security posture.


## View and assign asset criticality [_view_and_assign_asset_criticality]

Entities do not have a default asset criticality level. You can either assign asset criticality to your entities individually, or [bulk assign](#bulk-assign-asset-criticality) it to multiple entities by importing a text file. Alternatively, you can assign and manage asset criticality records through the [Asset criticality API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-security-entity-analytics-api).

When you assign, change, or unassign an individual entity’s asset criticality level, that entity’s risk score is immediately recalculated.

::::{note}
If you assign asset criticality using the file import feature, risk scores are **not** immediately recalculated. However, you can trigger an immediate recalculation by clicking **Recalculate entity risk scores now**. Otherwise, the newly assigned or updated asset criticality levels will be factored in during the next hourly risk scoring calculation.
::::


You can view, assign, change, or unassign asset criticality from the following places in the {{elastic-sec}} app:

* The [host details page](../explore/hosts-page.md#host-details-page) and [user details page](../explore/users-page.md#user-details-page):

    :::{image} /solutions/images/security-assign-asset-criticality-host-details.png
    :alt: Assign asset criticality from the host details page
    :screenshot:
    :::

* The [entity details flyout](/solutions/security/advanced-entity-analytics/view-entity-details.md#entity-details-flyout):

    :::{image} /solutions/images/security-assign-asset-criticality-host-flyout.png
    :alt: Assign asset criticality from the host details flyout
    :screenshot:
    :::

* The entity details flyout in [Timeline](../investigate/timeline.md):

    :::{image} /solutions/images/security-assign-asset-criticality-timeline.png
    :alt: Assign asset criticality from the host details flyout in Timeline
    :screenshot:
    :::


If you have enabled the [entity store](entity-store.md), you can also view asset criticality assignments in the **Entities** section on the following pages:

* {applies_to}`stack: ga 9.1` {applies_to}`serverless: ga` [Entity analytics](/solutions/security/advanced-entity-analytics/overview.md)
* [Entity analytics dashboard](/solutions/security/dashboards/entity-analytics-dashboard.md)

:::{image} /solutions/images/security-entities-section.png
:alt: Entities section
:screenshot:
:::


### Bulk assign asset criticality [bulk-assign-asset-criticality]

You can bulk assign asset criticality to multiple entities by importing a CSV, TXT or TSV file from your asset management tools.

The file must contain three columns, with each entity record listed on a separate row:

1. The first column should indicate whether the entity is a `host`, `user`, or `service`.
2. The second column should specify the entity’s `host.name`, `user.name`, or `service.name`.
3. The third column should specify one of the following asset criticality levels:

    * `extreme_impact`
    * `high_impact`
    * `medium_impact`
    * `low_impact`
    * {applies_to}`stack: ga 9.1` `unassigned`


The maximum file size is 1 MB.

File structure example:

```txt
user,user-001,low_impact
user,user-002,medium_impact
host,host-001,extreme_impact
service,service-001,extreme_impact
```

To import a file:

1. Find **Entity Store** in the main menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select or drag and drop the file you want to import.

    ::::{note}
    The file validation step highlights any lines that don’t follow the required file structure. The asset criticality levels for those entities won’t be assigned. We recommend that you fix any invalid lines and re-upload the file.
    ::::

3. Click **Assign**.

This process overwrites any previously assigned asset criticality levels for the entities included in the imported file. The newly assigned or updated asset criticality levels are immediately visible within all asset criticality workflows.

You can trigger an immediate recalculation of entity risk scores by clicking **Recalculate entity risk scores now**. Otherwise, the newly assigned or updated asset criticality levels will be factored in during the next hourly risk scoring calculation.


## Improve your security operations [_improve_your_security_operations]

With asset criticality, you can improve your security operations by:

* [Prioritizing open alerts](#prioritize-open-alerts)
* [Monitoring an entity’s risk](#monitor-entity-risk)


### Prioritize open alerts [prioritize-open-alerts]

You can use asset criticality as a prioritization factor when triaging alerts and conducting investigations and response activities.

Once you assign a criticality level to an entity, all subsequent alerts related to that entity are enriched with its criticality level. This additional context allows you to [prioritize alerts associated with business-critical entities](view-analyze-risk-score-data.md#triage-alerts-associated-with-high-risk-or-business-critical-entities).


### Monitor an entity’s risk [monitor-entity-risk]

The risk scoring engine dynamically factors in an entity’s asset criticality, along with `Open` and `Acknowledged` detection alerts to [calculate the entity’s overall risk score](entity-risk-scoring.md#how-is-risk-score-calculated). This dynamic risk scoring allows you to monitor changes in the risk profiles of your most sensitive entities, and quickly escalate high-risk threats.

To view the impact of asset criticality on an entity’s risk score, follow these steps:

1. Open the [entity details flyout](/solutions/security/advanced-entity-analytics/view-entity-details.md#entity-details-flyout). The risk summary section shows asset criticality’s contribution to the overall risk score.
2. Click **View risk contributions** to open the flyout’s left panel.
3. In the **Risk contributions** section, verify the entity’s criticality level from the time the alert was generated.

:::{image} /solutions/images/security-asset-criticality-impact.png
:alt: View asset criticality impact on host risk score
:screenshot:
:::

