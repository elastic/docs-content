The Cloud Native Vulnerability Management (CNVM) dashboard gives you an overview of vulnerabilities detected in your cloud infrastructure.

:::{image} /solutions/images/security-vuln-management-dashboard.png
:alt: The CNVM dashboard
:::

::::{admonition} Requirements
* To collect this data, install the [Cloud Native Vulnerability Management](/solutions/security/cloud/get-started-with-cnvm.md) integration.
* The CNVM dashboard is available to all Elastic Cloud users. For on-premises deployments, it requires an [appropriate subscription](https://www.elastic.co/pricing) level.

::::


::::{warning}
This functionality is in beta and is subject to change. The design and code is less mature than official GA features and is being provided as-is with no warranties. Beta features are not subject to the support SLA of official GA features.
::::



## CNVM dashboard UI [CNVM-dashboard-UI-dash]

The summary cards at the top of the dashboard display the number of monitored cloud accounts, scanned virtual machines (VMs), and vulnerabilities (grouped by severity).

The **Trend by severity** bar graph complements the summary cards by displaying the number of vulnerabilities found on your infrastructure over time, sorted by severity. It has a maximum time scale of 30 days.

::::{admonition} Graph tips
* Click the severity levels legend on its right to hide/show each severity level.
* To display data from specific cloud accounts, select the account names from the **Accounts** drop-down menu.

::::


The page also includes three tables:

* **Top 10 vulnerable resources** shows your VMs with the highest number of vulnerabilities.
* **Top 10 patchable vulnerabilities** shows the most common vulnerabilities in your environment that can be fixed by a software update.
* **Top 10 vulnerabilities** shows the most common vulnerabilities in your environment, with additional details.

Click **View all vulnerabilities** at the bottom of a table to open the [Vulnerabilities Findings](/solutions/security/cloud/findings-page-3.md) page, where you can view additional details.

