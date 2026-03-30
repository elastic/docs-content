---
navigation_title: SIEM Readiness
description: Use SIEM Readiness to assess your deployment across four dimensions—coverage, quality, continuity, and retention—and take guided actions to close gaps.
applies_to:
  stack: preview 9.4
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# Assess your SIEM data posture with SIEM Readiness [siem-readiness]

SIEM Readiness gives you a centralized view of your security data health across four dimensions: coverage, quality, continuity, and retention. Rather than checking multiple dashboards individually, you can use SIEM Readiness to quickly identify gaps in your SIEM configuration and take guided actions to close them.

You can find SIEM Readiness in the **Launchpad** section of the {{security-app}} navigation menu, alongside **Get started** and **Value report**.

[Screenshot suggestion: Full SIEM Readiness page showing the four pillar summary cards at the top, with the Coverage tab active. Capture the summary bar that shows each pillar's status (Healthy or Actions required).]

## Requirements [siem-readiness-requirements]

[TODO: Confirm RBAC requirements with PM. Likely needs specific Kibana privileges. Update this section with exact role/privilege requirements once confirmed.]

## The four pillars [siem-readiness-pillars]

SIEM Readiness organizes your data health assessment into four pillars. Each one appears as a summary card at the top of the page showing its current status: **Healthy** or **Actions required**. Select any pillar's tab to view its details.

### Coverage [siem-readiness-coverage]

The Coverage pillar answers: *Are the data sources your detection rules need actually present?* It has two components: data rule coverage and data coverage.

#### Data rule coverage [siem-readiness-data-rule-coverage]

Data rule coverage shows how many of your active detection rules have the required integrations installed. Rules that are active but missing their required data source can't run properly.

You can switch between two views:

- **All enabled rules**: A summary showing total enabled rules, how many have installed integrations, and how many are missing integrations. You can click **View installed integrations** or **View missing integrations** to see the specific integrations involved. Clicking an integration name takes you directly to its installation page.
- **MITRE ATT&CK enabled rules**: A grid showing which MITRE ATT&CK tactics have enabled rules mapped to them and whether any of those rules are missing required integrations. Click a tactic to see the list of required integrations for that tactic's rules.

[Screenshot suggestion: Coverage tab showing the Data rule coverage section with the "All enabled rules" view selected, displaying the donut chart of total enabled rules and the integration status breakdown table.]

[Screenshot suggestion: Coverage tab showing the MITRE ATT&CK view with the tactic grid, color-coded to show which tactics have missing integrations.]

#### Data coverage [siem-readiness-data-coverage]

Data coverage shows which log categories are sending data to {{elastic-sec}} and which aren't. Log categories include:

- Endpoint
- Identity
- Network
- Cloud
- Application / SaaS

Each category displays a coverage status (**Has data** or **Missing data**) and links to view the installed integrations contributing to that category. If a category has missing data, you can click **View integrations** to see which integrations you can install to close the gap.

[Screenshot suggestion: Data coverage table showing log categories with their coverage status and action links.]

### Quality [siem-readiness-quality]

The Quality pillar answers: *Are your logs ECS-compatible?* Schema errors can prevent rules, dashboards, and correlations from working correctly.

Quality checks your data sources for [Elastic Common Schema (ECS)](/manage-data/data-store/map-custom-data-to-ecs.md) compatibility issues and missing fields. Results are grouped by log category (such as Endpoint, Identity, Network, Cloud, and Application / SaaS), and each category shows:

- **Status**: **Healthy** or **Actions required**
- **Incompatible fields**: The number of fields with mapping issues
- **Affected integrations**: How many integrations in the category have issues

Expand a category to see individual data sources with their incompatible field count, the time since the last check, and their status. Click **View Data quality** to open the Data Quality dashboard for a more detailed investigation.

[Screenshot suggestion: Quality tab with an expanded category showing the data source table with incompatible fields, last checked time, and status columns.]

### Continuity [siem-readiness-continuity]

The Continuity pillar answers: *Are your ingest pipelines healthy, or are failures creating blind spots?*

Continuity tracks ingest pipeline failure rates across your log categories. Each category shows:

- **Status**: **Healthy** or **Actions required**
- **Pipelines**: The number of ingest pipelines in the category
- **Docs ingested**: Total documents processed
- **Failure rate**: The percentage of failed documents

Expand a category to see individual pipelines with their ingestion counts, failed document counts, failure rates, and status. Click **View failures** to investigate failing pipelines in Stack Management, or click the pipeline name to view its details.

[Screenshot suggestion: Continuity tab with an expanded category showing the pipeline table with docs ingested, failed docs, failure rate, and status columns.]

### Retention [siem-readiness-retention]

The Retention pillar answers: *Do your index lifecycle policies meet recommended retention periods?*

Retention checks whether your indices comply with recommended baselines. In 9.4, these baselines are based on FedRAMP requirements. Each log category shows:

- **Status**: **Healthy** or **Actions required**
- **Indices**: The number of indices in the category

Expand a category to see individual indices with their current retention period, the recommended baseline retention, and compliance status. Click **Adjust ILM policy** to open the relevant index lifecycle management policy and update the retention period.

[Screenshot suggestion: Retention tab with an expanded category showing the index table with current retention, baseline retention (FedRAMP), status, and action columns.]

## Take action on SIEM Readiness findings [siem-readiness-actions]

SIEM Readiness provides two types of guided actions that you can take directly from the page:

Create cases
: Each section of the SIEM Readiness page includes a **Create new case** button. Cases are pre-filled with context specific to the current finding, such as a list of missing integrations or non-compliant indices with links to relevant resources. You can use these cases to track remediation work or share findings with your team. For more information about cases, refer to [Cases](/solutions/security/investigate/security-cases.md).

Navigate to source tools
: Guided action links throughout the page take you directly to the relevant tool for resolving a finding. For example, clicking **View missing integrations** in the Coverage pillar takes you to the integrations page with filters already applied, and clicking **Adjust ILM policy** in the Retention pillar opens the relevant lifecycle policy.

You can also click **View all related cases** at the top of the page to see all cases that were created from SIEM Readiness.

## Configure SIEM Readiness [siem-readiness-configure]

If certain log categories aren't relevant to your environment, you can exclude them from all SIEM Readiness views. Click **Configuration** at the top of the page to open the configuration panel, then remove any categories you don't want to monitor.

Excluded categories won't affect your pillar status calculations, so your health scores reflect only the data sources that matter to your environment.

## Export a report [siem-readiness-export]

Click **Export report** at the top of the page to generate a downloadable report of your current SIEM Readiness status. You can share this report with stakeholders to communicate your security data posture.

## How SIEM Readiness relates to other tools [siem-readiness-related-tools]

SIEM Readiness complements the existing Data Quality dashboard and Detection Rule Monitoring dashboard — it doesn't replace them. Think of SIEM Readiness as your starting point for understanding overall SIEM health, while the other tools provide the deep-dive capabilities for resolving specific issues.

The following table summarizes how these tools work together:

| Tool | Purpose | When to use it |
|------|---------|----------------|
| SIEM Readiness | Assess overall SIEM data health across coverage, quality, continuity, and retention | Start here to identify which areas need attention |
| Data Quality dashboard | Deep ECS field-level analysis per data stream | Investigate specific data quality issues flagged by SIEM Readiness |
| Detection Rule Monitoring | Rule execution health, failures, and gaps | Review specific rules that are missing data sources |

In practice, you might open SIEM Readiness and see that the Quality pillar flags ECS compatibility issues for a log category. You can then click through to the Data Quality dashboard to identify and fix the specific field mapping problems.

## Related pages [siem-readiness-related-pages]

- [Detection rules](/solutions/security/detect-and-alert/manage-detection-rules.md)
- [Integrations](/solutions/security/get-started/ingest-data-to-elastic-security.md)
- [Index lifecycle management](/manage-data/lifecycle/index-lifecycle-management.md)
- [MITRE ATT&CK coverage](/solutions/security/detect-and-alert/mitre-attack-coverage.md)
- [Cases](/solutions/security/investigate/security-cases.md)
