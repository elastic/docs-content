---
navigation_title: "What is Kibana?"
---

# {{kib}}—your window into Elastic [introduction]


{{kib}} enables you to give shape to your data and navigate the Elastic Stack.  With {{kib}}, you can:

* **Search, observe, and protect your data.** From discovering documents to analyzing logs to finding security vulnerabilities, {{kib}} is your portal for accessing these capabilities and more.
* **Analyze your data.** Search for hidden insights, visualize what you’ve found in charts, gauges, maps, graphs, and more, and combine them in a dashboard.
* **Manage, monitor, and secure the Elastic Stack.** Manage your data, monitor the health of your Elastic Stack cluster, and control which users have access to which features.

:::{image} ../../../images/kibana-analytics-home-page.png
:alt: Analytics home page
:name: kibana-home-page
:class: screenshot
:::

**{{kib}} is for administrators, analysts, and business users.** As an admin, your role is to manage the Elastic Stack, from creating your deployment to getting {{es}} data into {{kib}}, and then managing the data.  As an analyst, you’re looking to discover insights in the data, visualize your data on dashboards, and share your findings.  As a business user, you want to view existing dashboards and drill down into details.

**{{kib}} works with all types of data.** Your data can be structured or unstructured text, numerical data, time series data, geospatial data, logs, metrics, security events, and more. No matter your data, {{kib}} can help you uncover patterns and relationships and visualize the results.


## Search, observe, and protect [extend-your-use-case]

Being able to search, observe, and protect your data is a requirement for any analyst. {{kib}} provides solutions for each of these use cases.

* [**Enterprise Search**](https://www.elastic.co/guide/en/enterprise-search/current/index.html) enables you to create a search experience for your app, workplace, and website.
* [**Elastic Observability**](../../../solutions/observability/get-started/what-is-elastic-observability.md) enables you to monitor and apply analytics in real time to events happening across all your environments. You can analyze log events, monitor the performance metrics for the host or container that it ran in, trace the transaction, and check the overall service availability.
* Designed for security analysts, [**Elastic Security**](../../../solutions/security.md) provides an overview of the events and alerts from your environment.  Elastic Security helps you defend your organization from threats before damage and loss occur.


## Analyze [visualize-and-analyze]

With {{kib}} [**Analytics**](../../../explore-analyze/overview/kibana-quickstart.md), you can quickly search through large amounts of data, explore fields and values, and then use the drag-and-drop interface to rapidly build charts, tables, metrics, and more.

:::{image} ../../../images/kibana-visualization-journey.png
:alt: User data analysis journey
:class: screenshot
:::

$$$get-data-into-kibana$$$

|     |     |
| --- | --- |
| **1** | **Add data.** The best way to add data to the Elastic Stack is to use one of our many [integrations](../../../manage-data/ingest.md).On the **Integrations** page, you can also find options to add sample data sets or to upload a file. |
| **2** | **Explore.** With [**Discover**](../../../explore-analyze/discover.md), you can search your data for hiddeninsights and relationships. Ask your questions, and then filter the results to just the data you want.You can limit your results to the most recent documents added to {{es}}. |
| **3** | **Visualize.** {{kib}} provides many options to create visualizations of your data, fromaggregation-based data to time series data to geo data.[**Dashboard**](../../../explore-analyze/dashboards.md) is your starting point to create visualizations,and then pulling them together to show your data from multiple perspectives.Use [**Canvas**](../../../explore-analyze/visualize/canvas.md),to give your datathe “wow” factor for display on a big screen. Use **Graph** to explore patterns and relationships. |
| **4** | **Model data behavior.**Use [**{{ml-cap}}**](../../../explore-analyze/machine-learning/machine-learning-in-kibana.md) to model the behavior of your data—forecast unusual behavior andperform outlier detection, regression, and classification analysis. |
| **5** | **Share.** Ready to [share](../../../explore-analyze/report-and-share.md) your findings with a larger audience? {{kib}} offers many options—embeda dashboard, share a link, export to PDF, and more. |


## Manage your data [_manage_your_data]

{{kib}} helps you perform your data management tasks from the convenience of a UI. You can:

* Refresh, flush, and clear the cache of your indices.
* Define the lifecycle of an index as it ages.
* Define a policy for taking snapshots of your cluster.
* Roll up data from one or more indices into a new, compact index.
* Replicate indices on a remote cluster and copy them to a local cluster.

For a full list of data management UIs, refer to [**Stack Management**](../../../deploy-manage/index.md).

:::{image} ../../../images/kibana-stack-management.png
:alt: Index Management view in Stack Management
:class: screenshot
:::


## Alert and take action [_alert_and_take_action]

Detecting and acting on significant shifts and signals in your data is a need that exists in almost every use case. Alerting allows you to detect conditions in different {{kib}} apps and trigger actions when those conditions are met. For example, you might trigger an alert when a shift occurs in your business critical KPIs or when memory, CPU, or disk space take a dip. When the alert triggers, you can send a notification to a system that is part of your daily workflow: email, Slack, PagerDuty, ServiceNow, and other third party integrations.

A dedicated view for creating, searching, and editing rules is in [**{{rules-ui}}**](../../../explore-analyze/alerts-cases/alerts/create-manage-rules.md).


## Organize content [organize-and-secure]

You might be managing tens, hundreds, or even thousands of dashboards, visualizations, and other {{kib}} assets. {{kib}} has several features for keeping your content organized.


### Collect related items in a space [organize-in-spaces]

{{kib}} provides [spaces](../../../deploy-manage/manage-spaces.md) for organizing your visualizations, dashboards, {{data-sources}}, and more. Think of a space as its own mini {{kib}} installation—it’s isolated from all other spaces, so you can tailor it to your specific needs without impacting others.

:::{image} ../../../images/kibana-select-your-space.png
:alt: Space selector view
:class: screenshot
:::


### Organize your content with tags [_organize_your_content_with_tags]

Tags are keywords or labels that you assign to saved objects, such as dashboards and visualizations, so you can classify them in a way that is meaningful to you. For example, if you tag objects with “design”, you can search and filter on the tag to see all related objects. Tags are also good for grouping content into categories within a space.

Don’t worry if you have hundreds of dashboards that need to be tagged. Use [**Tags**](../../../explore-analyze/find-and-organize/tags.md) in **Stack Management** to create your tags, then assign and delete them in bulk operations.


## Secure {{kib}} [intro-kibana-Security]

{{kib}} offers a range of security features for you to control who has access to what. [Security is enabled automatically](../../../deploy-manage/security/security-certificates-keys.md) when you enroll {{kib}} with a secured {{es}} cluster. For a description of all available configuration options, refer to [Security settings in {{kib}}](https://www.elastic.co/guide/en/kibana/current/security-settings-kb.html).


### Log in [_log_in]

{{kib}} supports several [authentication providers](../../../deploy-manage/users-roles/cluster-or-deployment-auth/user-authentication.md), allowing you to login using {{es}}’s built-in realms, or with your own single sign-on provider.

:::{image} ../../../images/kibana-kibana-login.png
:alt: Login page
:class: screenshot
:::


### Secure access [_secure_access]

{{kib}} provides roles and privileges for controlling which users can view and manage {{kib}} features. Privileges grant permission to view an application or perform a specific action and are assigned to roles. Roles allow you to describe a “template” of capabilities that you can grant to many users, without having to redefine what each user should be able to do.

When you create a role, you can scope the assigned {{kib}} privileges to specific spaces. This makes it possible to grant users different access levels in different spaces, or even give users their very own private space. For example, power users might have privileges to create and edit visualizations and dashboards, while analysts or executives might have **Dashboard** and **Canvas** with read-only privileges.

The {{kib}} role management interface allows you to describe these various access levels, or you can automate role creation by using [role APIs](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-roles).

:::{image} ../../../images/kibana-spaces-roles.png
:alt: {kib privileges}
:class: screenshot
:::


### Audit access [_audit_access]

Once you have your users and roles configured, you might want to maintain a record of who did what, when. The {{kib}} audit log will record this information for you, which can then be correlated with {{es}} audit logs to gain more insights into your users’ behavior. For more information, see [{{kib}} audit logging](../../../deploy-manage/monitor/logging-configuration/enabling-kibana-audit-logs.md).


## Find apps and objects [kibana-navigation-search]

To quickly find apps and the objects you create, use the search field in the global header. Search suggestions include deep links into applications, allowing you to directly navigate to the views you need most.

:::{image} ../../../images/kibana-app-navigation-search.png
:alt: Example of searching for apps
:class: screenshot
:::

You can search for objects by type, name, and tag. To get the most from the search feature, follow these tips:

* Use the keyboard shortcut—Ctrl+/ on Windows and Linux, Command+/ on MacOS—to focus on the input at any time.
* Use the provided syntax keywords.

    |     |     |
    | --- | --- |
    | Search by type | `type:dashboard`<br>Available types: `application`, `canvas-workpad`, `dashboard`, `data-view`, `lens`, `maps`, `query`, `search`, `visualization` |
    | Search by tag | `tag:mytagname`<br>`tag:"tag name with spaces"` |
    | Search by type and name | `type:dashboard my_dashboard_title` |
    | Advanced searches | `tag:(tagname1 or tagname2) my_dashboard_title`<br>`type:lens tag:(tagname1 or tagname2)`<br>`type:(dashboard or canvas-workpad) logs`<br> |


This example searches for visualizations with the tag `design` .

:::{image} ../../../images/kibana-tags-search.png
:alt: Example of searching for tags
:class: screenshot
:::


## View all {{kib}} has to offer [_view_all_kib_has_to_offer]

To view the full list of apps and features, go to [{{kib}} features](https://www.elastic.co/kibana/features).


## Get help [try-kibana]

Click ![Help icon in navigation bar](../../../images/kibana-intro-help-icon.png "") for help with questions or to provide feedback.

To keep up with what’s new and changed in Elastic, click the celebration icon in the global header.
