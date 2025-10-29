---
applies_to:
  stack: ga 9.2
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Endpoint Detection and Response dashboard

The Endpoint Detection and Response (EDR) dashboard provides visualizations that help you monitor and analyze detection and prevention activity on endpoints running {{elastic-defend}}. It shows total counts of detection, prevention, and ransomware alerts, as well as open alerts by severity, MITRE technique, and operating system. It also highlights the top 10 most infected endpoints and the top 10 most impacted users per endpoint.

With these insights, security analysts and administrators can quickly identify high-risk endpoints or potentially compromised users, evaluate detection rule performance, understand environment coverage, and pivot directly into the relevant alert details to begin investigations.

To access the dashboard:
1. Find **Dashboards** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the **Custom Dashboards** section, search for "Endpoint Detection and Response".

:::{image} /solutions/images/security-endpoint-detection-response-dashboard.png
:alt: Endpoint Detection and Response dashboard
:::

::::{admonition} Requirements
To access this dashboard and its data, you must have at least `Read` [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) for both the **Analytics > Dashboard** and **Security > Security** {{kib}} features.
::::

## Visualization data and types 

The dashboard presents various information about detections, preventions, and alerts from endpoints protected by {{elastic-defend}}. Visualizations display and calculate data within the time range and filters selected at the top of the dashboard.

The following visualizations are included:

* **Total detection, prevention, and ransomware alerts**
* **Open alerts over time**
* **Open alerts by severity**
* **Open alerts by top 10 MITRE technique**
* **Open alerts by OS**
* **Top 10 infected endpoints**
* **Top 10 impacted users per endpoint**

## Visualization panel actions 

Hover over a visualization panel to take the following actions:

* **Query**: View the panel's KQL query.
* **Show visualization configuration**: View the visualization's configuration.
* **Explore in Discover**: Open Discover with preloaded filters to display the panel’s data.
* **Inspect**: Examine the panel’s underlying data.
* **Maximize**: Expand the panel.
* **Settings**: Open the settings flyout.
* **Download CSV**: Download the panel’s data as a CSV file.
* **Copy to dashboard**: Copy the panel to an existing or new dashboard.
* **Add to case**: Add the panel to an existing case.

## Duplicate and edit the dashboard 

This dashboard is managed by Elastic, so any changes you make to it will not persist. To make persistent changes, you can duplicate the dashboard and edit the copy. Your copy will not get updated when Elastic updates the managed dashboard.

1. Click **Duplicate** in the toolbar.
2. In the **Duplicate dashboard** window, enter a title and optional description and tags.
3. Click **Save**. You will be redirected to the duplicated dashboard.

