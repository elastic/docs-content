---
applies_to:
  stack: all
  serverless:
    security: all
---

# View entity details

You can lean more about an entity (host, user, or service) from the entity details flyout, which is available throughout the {{elastic-sec}} app. To access this flyout, click on an entity name in places such as:

* The Alerts table
* The Entity Analytics overview
* The **Users** and user details pages
* The **Hosts** and host details pages

## Entity details flyout

The entity details flyout includes the following sections:

* [Entity risk summary](#entity-risk-summary), which displays entity risk data and inputs.
* [Asset Criticality](#asset-criticality), which allows you to view and assign asset criticality.
* [Insights](#insights), which displays vulnerabilities or misconfiguration findings for the entity.
* [Observed data](#observed-data), which displays entity details.

:::{image} /solutions/images/security-host-details-flyout.png
:alt: Host details flyout
:screenshot:
:::

### Entity risk summary

::::{admonition} Requirements
The entity risk summary section is only available if the [risk scoring engine is turned on](/solutions/security/advanced-entity-analytics/turn-on-risk-scoring-engine.md).
::::

The entity risk summary section contains a risk summary visualization and table.

The risk summary visualization shows the entity risk score and risk level. Hover over the visualization to display the **Options** menu. Use this menu to inspect the visualization's queries, add it to a new or existing case, save it to your Visualize Library, or open it in Lens for customization.

The risk summary table shows the category, score, and number of risk inputs that determine the entity risk score. Hover over the table to display the **Inspect** button, which allows you to inspect the table's queries.

To expand the entity risk summary section, click **View risk contributions**. The left panel displays additional details about the entity's risk inputs:

* The asset criticality level and contribution score from the latest risk scoring calculation.
* The top 10 alerts that contributed to the latest risk scoring calculation, and each alert's contribution score.

If more than 10 alerts contributed to the risk scoring calculation, the remaining alerts' aggregate contribution score is displayed below the **Alerts** table.

:::{image} /solutions/images/security-host-risk-inputs.png
:alt: Host risk inputs
:screenshot:
:::

### Asset Criticality

The **Asset Criticality** section displays the selected entity's [asset criticality level](/solutions/security/advanced-entity-analytics/asset-criticality.md). Asset criticality contributes to the overall [entity risk score](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md). The criticality level defines how impactful the entity is when calculating the risk score.

:::{image} /solutions/images/security-host-asset-criticality.png
:alt: Asset criticality
:screenshot:
:::

Click **Assign** to assign a criticality level to the selected entity, or **Change** to change the currently assigned criticality level.

### Insights

The **Insights** section displays [Vulnerabilities Findings](/solutions/security/cloud/findings-page-3.md) for the host or [Misconfiguration Findings](/solutions/security/cloud/findings-page.md) for the user. Click **Vulnerabilities** or **Misconfigurations** to expand the flyout and view this data.

:::{image} /solutions/images/security--host-details-insights-expanded.png
:alt: Host details flyout with the Vulnerabilities section expanded
:::

### Observed data

This section displays details such as the entity ID, when the entity was first and last seen, and the associated IP addresses and operating system.
:::{image} /solutions/images/security-host-observed-data.png
:alt: Host observed data
:screenshot:
:::