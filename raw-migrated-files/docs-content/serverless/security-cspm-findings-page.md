# Findings page [security-cspm-findings-page]

The **Misconfigurations** tab on the **Findings** page displays the configuration risks identified by the [CSPM](../../../solutions/security/cloud/cloud-security-posture-management.md) and [KSPM](../../../solutions/security/cloud/kubernetes-security-posture-management.md) integrations, as well as data from [third-party integrations](../../../solutions/security/cloud/ingest-third-party-cloud-security-data.md).

:::{image} ../../../images/serverless--cloud-native-security-findings-page.png
:alt: Findings page
:class: screenshot
:::


## What are CSPM and KSPM findings? [cspm-findings-page-what-are-findings]

CSPM and KSPM findings indicate whether a given resource passed or failed evaluation against a specific security guideline. Each finding includes metadata about the resource evaluated and the security guideline used to evaluate it. Each finding’s result (`pass` or `fail`) indicates whether a particular part of your infrastructure meets a security guideline.


## Group and filter findings [cspm-findings-page-group-filter]

By default, the Findings page lists all findings, without grouping or filtering.


### Group findings [security-cspm-findings-page-group-findings]

Click **Group findings by** to group your data by a field. Select one of the suggested fields or **Custom field** to choose your own. You can select up to three group fields at once.

* When grouping is turned on, click a group to expand it and examine all sub-groups or findings within that group.
* To turn off grouping, click **Group findings by** and select **None**.

::::{note}
Multiple groupings apply to your data in the order you selected them. For example, if you first select **Cloud account**, then select **Resource***, the top-level grouping will be based on ***Cloud account**, and its subordinate grouping will be based on **Resource**.

::::



### Filter findings [cspm-findings-page-filter-findings]

You can filter findings data in two ways:

* **KQL search bar**: For example, search for `result.evaluation : failed` to view all failed findings.
* **In-table value filters**: Hover over a finding to display available inline actions. Use the **Filter In** (plus) and **Filter Out** (minus) buttons.


## Customize the Findings table [security-cspm-findings-page-customize-the-findings-table]

You can use the toolbar buttons in the upper-left of the Findings table to select which columns appear:

* **Columns**: Select the left-to-right order in which columns appear.
* **Sort fields**: Sort the table by one or more columns, or turn sorting off.
* **Fields**: Select which fields to display for each finding. Selected fields appear in the table and the **Columns** menu.

::::{tip}
You can also click a column’s name to open a menu that allows you to perform multiple actions on the column.

::::



## Remediate failed findings [cspm-findings-page-remediate-findings]

To remediate failed findings and reduce your attack surface:

1. First, [filter for failed findings](../../../solutions/security/cloud/findings-page.md#cspm-findings-page-filter-findings).
2. Click the arrow to the left of a failed finding to open the findings flyout.
3. Follow the steps under **Remediation**.

    ::::{note}
    Remediation steps typically include commands for you to execute. These sometimes contain placeholder values that you must replace before execution.

    ::::



## Generate alerts for failed Findings [cspm-create-rule-from-finding]

You can create detection rules that detect specific failed findings directly from the Findings page.

1. Click the arrow to the left of a Finding to open the findings flyout.
2. Click **Take action**, then **Create a detection rule**. This automatically creates a detection rule that creates alerts when the associated benchmark rule generates a failed finding.
3. To review or customize the new rule, click **View rule**.
