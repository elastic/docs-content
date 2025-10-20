---
navigation_title: CNVM Findings
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/vuln-management-findings.html
  - https://www.elastic.co/guide/en/serverless/current/security-vuln-management-findings.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# View and manage CNVM vulnerabilities in Findings [security-vuln-management-findings]

The **Vulnerabilities** tab on the **Findings** page displays the vulnerabilities detected by the [CNVM integration](cloud-native-vulnerability-management.md), as well as those detected by [third-party integrations](integrations/ingest-third-party-cloud-security-data.md).

:::{image} /solutions/images/serverless--cloud-native-security-cnvm-findings-page.png
:alt: The Vulnerabilities tab of the Findings page
:screenshot:
:::


## What are CNVM findings? [security-vuln-management-findings-what-are-cnvm-findings]

CNVM findings represent security vulnerabilities detected in your cloud. They include metadata such as the CVE identifier, CVSS score, severity, affected package, and fix version if available, as well as information about impacted systems.

Clicking on a finding provides a detailed description of the vulnerability, and any available remediation information.


## Group and filter findings [vuln-findings-grouping]

To help you prioritize remediation efforts, you can organize findings in various ways.


### Group findings [security-vuln-management-findings-group-findings]

Click **Group vulnerabilities by** to group your data by a field. Select one of the suggested fields or **Custom field** to choose your own. You can select up to three group fields at once.

* When grouping is turned on, click a group to expand it and examine all sub-groups or findings within that group.
* To turn off grouping, click **Group vulnerabilities by:** and select **None**.

::::{note}
Multiple groupings apply to your data in the order you selected them. For example, if you first select **Cloud account**, then select **Resource**, the top-level grouping will be based on **Cloud account**, and its subordinate grouping will be based on **Resource**, as demonstrated in the following screenshot.

::::


:::{image} /solutions/images/serverless--cloud-native-security-cnvm-findings-grouped.png
:alt: The Vulnerabilities tab of the Findings page
:screenshot:
:::


### Filter findings [security-vuln-management-findings-filter-findings]

You can filter the data in two ways:

* **KQL search bar**: For example, search for `vulnerability.severity : "HIGH"` to view high severity vulnerabilities.
* **In-table value filters**: Hover over a finding to display available inline actions. Use the **Filter In** (plus) and **Filter Out** (minus) buttons.


### Customize the Findings table [security-vuln-management-findings-customize-the-findings-table]

When grouping is turned off, you can use the toolbar buttons in the upper-left of the Findings table to select which columns appear:

* **Columns**: Select the left-to-right order in which columns appear.
* **Sort fields**: Sort the table by one or more columns, or turn sorting off.
* **Fields**: Select which fields to display for each finding. Selected fields appear in the table and the **Columns** menu.

::::{tip}
You can also click a column’s name to open a menu that allows you to perform multiple actions on the column.

::::



## Learn more about a vulnerability [security-vuln-management-findings-learn-more-about-a-vulnerability]

Click a vulnerability to open the vulnerability details flyout. This flyout includes a link to the related vulnerability database, the vulnerability’s publication date, CVSS vector strings, fix versions (if available), and more.

When you open the vulnerability details flyout, it defaults to the **Overview** tab, which highlights key information. To view every field present in the vulnerability document, select the **Table** or **JSON** tabs.


## Remediate vulnerabilities [vuln-findings-remediate]

To remediate a vulnerability and reduce your attack surface, update the affected package if a fix is available.


## Generate alerts for failed Findings [cnvm-create-rule-from-finding]

You can create detection rules that detect specific vulnerabilities directly from the Findings page:

1. Click a vulnerability to open the vulnerability details flyout flyout.
2. Click **Take action**, then **Create a detection rule**. This automatically creates a detection rule that creates alerts when the associated vulnerability is found.
3. To review or customize the new rule, click **View rule**.
