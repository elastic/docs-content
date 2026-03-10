---
navigation_title: Prebuilt rule components
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Understand prebuilt rule tags, data sources, investigation guides, and how to transition to custom rules.
---

# Prebuilt rule components [prebuilt-rule-components]

Elastic prebuilt rules are designed to detect common threats across your environment. This page explains how prebuilt rules are organized, what data they need, and how to use the investigation guides that accompany them.


## Prebuilt rule tags [prebuilt-rule-tags]

Each prebuilt rule includes several tags identifying the rule's purpose, detection method, associated resources, and other information to help categorize your rules. These tags are category-value pairs; for example, `OS: Windows` indicates rules designed for Windows endpoints. Categories include:

| Tag category | Description |
|--------------|-------------|
| `Data Source` | The application, cloud provider, data shipper, or Elastic integration providing data for the rule. |
| `Domain` | A general category of data source types (such as cloud, endpoint, or network). |
| `OS` | The host operating system. |
| `Resources` | Additional rule resources such as investigation guides. |
| `Rule Type` | Identifies if the rule depends on specialized resources (such as {{ml}} jobs or threat intelligence indicators), or if it's a higher-order rule built from other rules' alerts. |
| `Tactic` | MITRE ATT&CK tactics that the rule addresses. |
| `Threat` | Specific threats the rule detects (such as Cobalt Strike or BPFDoor). |
| `Use Case` | The type of activity the rule detects and its purpose. |

### Use case tags

The `Use Case` tag category has the following values:

| Use case | Description |
|----------|-------------|
| `Active Directory Monitoring` | Detects changes related to Active Directory. |
| `Asset Visibility` | Detects changes to specified asset types. |
| `Configuration Audit` | Detects undesirable configuration changes. |
| `Guided Onboarding` | Example rule, used for {{elastic-sec}}'s guided onboarding tour. |
| `Identity and Access Audit` | Detects activity related to identity and access management (IAM). |
| `Log Auditing` | Detects activity on log configurations or storage. |
| `Network Security Monitoring` | Detects network security configuration activity. |
| `Threat Detection` | Detects threats. |
| `Vulnerability` | Detects exploitation of specific vulnerabilities. |


## Prebuilt rule data sources [rule-prerequisites]

Each prebuilt rule queries specific index patterns or a {{data-source}}, which determines the data the rule searches at runtime. You can see a rule's index patterns on its details page under **Definition**.

To help you set up the right data sources, rule details pages include:

**Related integrations**
:   [{{product.integrations}}](https://docs.elastic.co/en/integrations) that can provide compatible data. You don't need to install all listed integrations—installing any integration that matches your environment is typically sufficient. Some rules also work with data from legacy beats (such as {{filebeat}} or {{winlogbeat}}) without requiring a {{fleet}} integration. This field also displays each integration's installation status and includes links for installing and configuring the listed integrations.

**Required fields**
:   Data fields the rule expects to find. This is informational; rules run even if fields are missing, but may not generate expected alerts.

**Setup guide**
:   Step-by-step guidance for configuring the rule's data requirements.

:::{image} /solutions/images/security-rule-details-prerequisites.png
:alt: Rule details page with Related integrations
:screenshot:
:::

### Check integration status from the {{rules-ui}} table

You can check rules' related integrations in the **Installed Rules** and **Rule Monitoring** tables. Select the **integrations** badge to display the related integrations in a popup. The badge shows how many of the rule's related integrations are currently installed and enabled—for example, `1/2` means one of two related integrations is installed and actively collecting data.

An integration is counted as enabled only if it has been added to an agent policy and that policy is deployed to at least one agent. Installing an integration package without adding it to a policy does not increment the enabled count.

:::{admonition} Requirements for viewing related integration status
To view related integration status in the {{rules-ui}} table, your role needs at least `Read` privileges for the following features under {{manage-app}}:

- {{integrations}}
- {{fleet}}
- {{saved-objects-app}}

Without these privileges, the integrations badge may not appear or may not reflect accurate installation status.
:::

:::{image} /solutions/images/security-rules-table-related-integrations.png
:alt: {{rules-ui}} table with related integrations popup
:screenshot:
:::

::::{tip}
You can hide the **integrations** badge in the {{rules-ui}} tables by turning off the `securitySolution:showRelatedIntegrations` [advanced setting](/solutions/security/get-started/configure-advanced-settings.md#show-related-integrations).
::::


## Prebuilt rule investigation guides [prebuilt-investigation-guides]

Many prebuilt rules include investigation guides—Markdown documents that help analysts triage, analyze, and respond to alerts. A good investigation guide reduces mean time to respond by giving analysts the context and queries they need without leaving the alert details flyout.

### Find a rule's investigation guide

1. Open an alert generated by the rule.
2. In the alert details flyout, go to the **Investigation** section on the **Overview** tab.
3. If the rule has an investigation guide, select **Show investigation guide** to open it in the details panel.

You can also view investigation guides from the rule's details page (find **Detection rules (SIEM)** in the navigation menu, then select the rule name).

### What investigation guides include

Prebuilt rule investigation guides typically contain:

- **Context**: Background on the threat or technique the rule detects
- **Triage steps**: How to determine if the alert is a true positive
- **Investigation queries**: Pre-built queries to gather additional context (some guides include interactive Timeline buttons)
- **Response guidance**: Actions to take if the alert is confirmed

::::{note}
You cannot edit investigation guides for prebuilt rules. To customize a prebuilt rule's guide, [duplicate the rule](/solutions/security/detect-and-alert/customize-prebuilt-rules.md#duplicate-prebuilt-rules) first, then edit the duplicate's investigation guide.
::::

### Write investigation guides for custom rules

When you create custom rules, you can write your own investigation guides using Markdown with interactive elements like Timeline queries and Osquery buttons. Refer to [Write investigation guides](/solutions/security/detect-and-alert/write-investigation-guides.md) for syntax and best practices.


## Build custom rules [build-custom-rules]

Prebuilt rules cover common threats, but your environment has unique risks. When you need detection logic tailored to your infrastructure, applications, or threat model, refer to [Author rules](/solutions/security/detect-and-alert/author-rules.md) for guidance on selecting a rule type, writing queries, and configuring rule settings.
