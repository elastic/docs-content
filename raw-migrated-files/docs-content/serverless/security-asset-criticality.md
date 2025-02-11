# Asset criticality [security-asset-criticality]

::::{admonition} Requirements
:class: note

To view and assign asset criticality, you must have the appropriate user role. For more information, refer to [Entity risk scoring prerequisites](../../../solutions/security/advanced-entity-analytics/entity-risk-scoring-requirements.md).

::::


The asset criticality feature allows you to classify your organization’s entities based on various operational factors that are important to your organization. Through this classification, you can improve your threat detection capabilities by focusing your alert triage, threat-hunting, and investigation activities on high-impact entities.

You can assign one of the following asset criticality levels to your entities, based on their impact:

* Low impact
* Medium impact
* High impact
* Extreme impact

For example, you can assign **Extreme impact** to business-critical entities, or **Low impact** to entities that pose minimal risk to your security posture.


## View and assign asset criticality [security-asset-criticality-view-and-assign-asset-criticality]

Entities do not have a default asset criticality level. You can either assign asset criticality to your entities individually, or [bulk assign](../../../solutions/security/advanced-entity-analytics/asset-criticality.md#security-asset-criticality-bulk-assign-asset-criticality) it to multiple entities by importing a text file.

When you assign, change, or unassign an individual entity’s asset criticality level, that entity’s risk score is immediately recalculated.

::::{note}
If you assign asset criticality using the file import feature, risk scores are **not** immediately recalculated. However, you can trigger an immediate recalculation by clicking **Recalculate entity risk scores now**. Otherwise, the newly assigned or updated asset criticality levels will be factored in during the next hourly risk scoring calculation.

::::


You can view, assign, change, or unassign asset criticality from the following places in the {{elastic-sec}} app:

* The [host details page](../../../solutions/security/explore/hosts-page.md#host-details-page) and [user details page](../../../solutions/security/explore/users-page.md#security-users-page-user-details-page):

    :::{image} ../../../images/serverless--assign-asset-criticality-host-details.png
    :alt: Assign asset criticality from the host details page
    :class: screenshot
    :::

* The [host details flyout](../../../solutions/security/explore/hosts-page.md#security-hosts-overview-host-details-flyout) and [user details flyout](../../../solutions/security/explore/users-page.md#security-users-page-user-details-flyout):

    :::{image} ../../../images/serverless--assign-asset-criticality-host-flyout.png
    :alt: Assign asset criticality from the host details flyout
    :class: screenshot
    :::

* The host details flyout and user details flyout in [Timeline](../../../solutions/security/investigate/timeline.md):

    :::{image} ../../../images/serverless--assign-asset-criticality-timeline.png
    :alt: Assign asset criticality from the host details flyout in Timeline
    :class: screenshot
    :::



### Bulk assign asset criticality [security-asset-criticality-bulk-assign-asset-criticality]

You can bulk assign asset criticality to multiple entities by importing a CSV, TXT or TSV file from your asset management tools.

The file must contain three columns, with each entity record listed on a separate row:

1. The first column should indicate whether the entity is a `host` or a `user`.
2. The second column should specify the entity’s `host.name` or `user.name`.
3. The third column should specify one of the following asset criticality levels:

    * `extreme_impact`
    * `high_impact`
    * `medium_impact`
    * `low_impact`


The maximum file size is 1 MB.

File structure example:

```txt
user,user-001,low_impact
user,user-002,medium_impact
host,host-001,extreme_impact
```

To import a file:

1. Go to **Project Settings** → **Stack Management** → **Entity Store**.
2. Select or drag and drop the file you want to import.

    ::::{note}
    The file validation step highlights any lines that don’t follow the required file structure. The asset criticality levels for those entities won’t be assigned. We recommend that you fix any invalid lines and re-upload the file.

    ::::

3. Click **Assign**.

This process overwrites any previously assigned asset criticality levels for the entities included in the imported file. The newly assigned or updated asset criticality levels are immediately visible within all asset criticality workflows.

You can trigger an immediate recalculation of entity risk scores by clicking **Recalculate entity risk scores now**. Otherwise, the newly assigned or updated asset criticality levels will be factored in during the next hourly risk scoring calculation.


## Improve your security operations [security-asset-criticality-improve-your-security-operations]

With asset criticality, you can improve your security operations by:

* [Prioritizing open alerts](../../../solutions/security/advanced-entity-analytics/asset-criticality.md#security-asset-criticality-prioritize-open-alerts)
* [Monitoring an entity’s risk](../../../solutions/security/advanced-entity-analytics/asset-criticality.md#security-asset-criticality-monitor-an-entitys-risk)


### Prioritize open alerts [security-asset-criticality-prioritize-open-alerts]

You can use asset criticality as a prioritization factor when triaging alerts and conducting investigations and response activities.

Once you assign a criticality level to an entity, all subsequent alerts related to that entity are enriched with its criticality level. This additional context allows you to  [prioritize alerts associated with business-critical entities](../../../solutions/security/advanced-entity-analytics/view-analyze-risk-score-data.md#security-analyze-risk-score-data-triage-alerts-associated-with-high-risk-or-business-critical-entities).


### Monitor an entity’s risk [security-asset-criticality-monitor-an-entitys-risk]

The risk scoring engine dynamically factors in an entity’s asset criticality, along with `Open` and `Acknowledged` detection alerts to [calculate the entity’s overall risk score](../../../solutions/security/advanced-entity-analytics/entity-risk-scoring.md#how-is-risk-score-calculated). This dynamic risk scoring allows you to monitor changes in the risk profiles of your most sensitive entities, and quickly escalate high-risk threats.

To view the impact of asset criticality on an entity’s risk score, follow these steps:

1. Open the [host details flyout](../../../solutions/security/explore/hosts-page.md#security-hosts-overview-host-details-flyout) or [user details flyout](../../../solutions/security/explore/users-page.md#security-users-page-user-details-flyout). The risk summary section shows asset criticality’s contribution to the overall risk score.
2. Click **View risk contributions** to open the flyout’s left panel.
3. In the **Risk contributions** section, verify the entity’s criticality level from the time the alert was generated.

:::{image} ../../../images/serverless--asset-criticality-impact.png
:alt: View asset criticality impact on host risk score
:class: screenshot
:::
