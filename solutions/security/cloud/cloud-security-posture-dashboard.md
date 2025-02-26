---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/cspm-posture-dashboard.html
  - https://www.elastic.co/guide/en/serverless/current/security-cloud-posture-dashboard-dash-cspm.html
---

# Cloud Security Posture dashboard

% What needs to be done: Align serverless/stateful

% Scope notes: Duplicate of Cloud Security Posture dashboard page in Dashboards section. Consider removing this page and keeping the one in Dashboards.

% Use migrated content from existing pages that map to this page:

% - [x] ./raw-migrated-files/security-docs/security/cspm-posture-dashboard.md
% - [ ] ./raw-migrated-files/docs-content/serverless/security-cloud-posture-dashboard-dash-cspm.md

The Cloud Security Posture dashboard summarizes your cloud infrastructure’s overall performance against [security guidelines](/solutions/security/cloud/benchmarks-2.md) defined by the Center for Internet Security (CIS). To get started monitoring your security posture, refer to [Get started with Cloud Security Posture Management](/solutions/security/cloud/get-started-with-cspm-for-aws.md) or [Get started with Kubernetes Security Posture Management](/solutions/security/cloud/get-started-with-kspm.md).

:::{image} ../../../images/security-cloud-sec-dashboard.png
:alt: The cloud Security dashboard
:class: screenshot
:::

The Cloud Security Posture dashboard shows:

* Configuration risk metrics for all monitored cloud accounts and Kubernetes clusters
* Configuration risk metrics grouped by the applicable benchmark, for example CIS GCP, CIS Azure, CIS Kubernetes, or CIS EKS
* Configuration risks grouped by CIS section (security guideline category)

::::{admonition} Requirements
* The Cloud Security Posture dashboard is available to all Elastic Cloud users. For on-prem deployments, it requires an [Enterprise subscription](https://www.elastic.co/pricing).

::::



## Cloud Security Posture dashboard UI [cspm-posture-dashboard-UI]

At the top of the dashboard, you can switch between the cloud accounts and Kubernetes cluster views.

The top section of either view summarizes your overall cloud security posture (CSP) by aggregating data from all monitored resources. The summary cards on the left show the number of cloud accounts or clusters evaluated, and the number of resources evaluated. You can click **Enroll more accounts** or **Enroll more clusters** to deploy to additional cloud assets. Click **View all resources** to open the [Findings page](/solutions/security/cloud/findings-page-2.md).

The remaining summary cards show your overall compliance score, and your compliance score for each CIS section. Click **View all failed findings** to view all failed findings, or click a CIS section name to view failed findings from only that section on the Findings page.

Below the summary section, each row shows the CSP for a benchmark that applies to your monitored cloud resources. For example, if you are monitoring GCP and Azure cloud accounts, a row appears for CIS GCP and another appears for CIS Azure. Each row shows the CIS benchmark, the number of cloud accounts it applies to, its overall compliance score, and its compliance score grouped by CIS section.

:::{image} ../../../images/security-cloud-sec-dashboard-individual-row.png
:alt: A row representing a single cluster in the Cloud Security Posture dashboard
:class: screenshot
:::


## FAQ (Frequently Asked Questions) [cspm-posture-dashboard-faq]

::::{dropdown} When do newly-enrolled assets appear on the dashboard?
It can take up to 10 minutes for deployment, resource fetching, evaluation, and data processing before a newly-enrolled AWS account or Kubernetes cluster appears on the dashboard.

::::


::::{dropdown} When do unenrolled accounts disappear from the dashboard?
An account will disappear as soon as your integration fetches data while that account is not enrolled. The fetch process repeats every four hours, which means a newly unenrolled account can take a maximum of four hours to disappear from the dashboard.

::::


