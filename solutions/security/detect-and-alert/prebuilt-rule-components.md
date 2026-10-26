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

Each prebuilt rule includes several tags identifying the rule's purpose, detection method, associated resources, and other information to help categorize your rules. These tags are category-value pairs. For example, `OS: Windows` indicates rules designed for Windows endpoints. Use the **Tags** filter on the **{{siem-rules-ui}}** page to narrow the rule list to the rules that match your environment.

Elastic adds tag categories and values over time. To get the latest ones, update your prebuilt rules on the **Rule Updates** tab. If you added your own tags to a prebuilt rule, which requires an Enterprise subscription or a Security Analytics Complete project, first check [Preserve customizations during updates](/solutions/security/detect-and-alert/update-prebuilt-rules.md#preserve-customizations). An update can replace them.

Categories include:

| Tag category | Description | Example |
|--------------|-------------|---------|
| `Data Source` | The application, cloud provider, data shipper, or Elastic integration providing data for the rule. | `Data Source: Entra ID Sign-In Logs` |
| `Domain` | The attack surface the rule covers, such as cloud, endpoint, identity, network, email, or generative AI. | `Domain: Identity` |
| `Mitre Atlas` | [MITRE ATLAS](https://atlas.mitre.org) (Adversarial Threat Landscape for Artificial-Intelligence Systems) techniques, for rules that cover generative AI threats. | `Mitre Atlas: T0051` |
| `Noise` | The alert volume the rule typically produces. | `Noise: Low` |
| `OS` | The host operating system. | `OS: Windows` |
| `Performance` | The time the rule typically takes to run. | `Performance: Fast` |
| `Platform` | The technology ecosystem the rule targets, which isn't always the same as the data source. | `Platform: Entra ID` |
| `Profile` | Elastic's recommendation for how to prioritize the rule. | `Profile: Recommended` |
| `Promotion` | Identifies rules that turn alerts from an external system into {{elastic-sec}} alerts. | `Promotion: External Alerts` |
| `Resources` | Additional rule resources such as investigation guides. | `Resources: Investigation Guide` |
| `Rule Type` | The query engine the rule runs on, or the construction it uses. Values include `Custom Query (KQL)`, `Event Correlation (EQL)`, `ES\|QL`, `Threshold`, `New Terms`, `Indicator Match`, `Machine Learning`, `BBR`, and `Higher-Order`. | `Rule Type: Event Correlation (EQL)` |
| `Service` | A specific cloud service, SaaS application, or web server the rule targets. | `Service: Azure Key Vault` |
| `Tactic` | MITRE ATT&CK tactics that the rule addresses. | `Tactic: Initial Access` |
| `Threat` | A threat category the rule detects, or a named campaign or malware family. | `Threat: Ransomware` |
| `Use Case` | The type of activity the rule detects and its purpose. | `Use Case: Threat Detection` |
| `Vuln` | The Common Vulnerabilities and Exposures (CVE) identifier for the vulnerability that the rule detects exploitation of. | `Vuln: CVE-2021-44228` |

Both `Platform` and `OS` include `Windows`, `Linux`, and `macOS`. `OS` identifies the host operating system that endpoint data comes from. `Platform` identifies the ecosystem the rule targets, which can be an operating system, a cloud provider, or an identity provider.

Some prebuilt rules don't have all of these categories, because Elastic adds them in phases. Rules also keep their `Use Case` and `Promotion` tags from the earlier scheme, so your current filters continue to work.

### Operational profile tags [rule-operational-tags]

The `Noise`, `Performance`, and `Profile` tags describe how a rule behaves when you run it, rather than what it detects.

| Tag category | Values |
|--------------|--------|
| `Noise` | `Low`, `Medium`, `High`, `Unknown` |
| `Performance` | `Fast`, `Normal`, `Slow`, `Very Slow`, `Unknown` |

A `Noise` or `Performance` value of `Unknown` means Elastic doesn't yet have enough data to classify the rule. Usually the rule is new, or it runs in too few environments.

The `Profile` tag has three values:

* `Recommended`: A curated starting set. Elastic scores these rules on severity, alert volume, query cost, and coverage of a tracked threat, so you can enable them without significant tuning.
* `Aggressive`: Rules that produce high alert volume, or that score poorly on that same balance of detection value against cost. A rule can be aggressive because it's slow to run or doesn't map to a tracked threat, not only because it's noisy. These rules suit teams that can absorb the volume or plan to tune them.
* `Beta`: Rules that Elastic has designated as beta. Unlike the other two values, Elastic assigns this one manually.

Most rules have no `Profile` tag, which reflects where Elastic placed the rule rather than its quality.

::::{note}
Elastic derives the `Noise` and `Performance` tags, and the `Recommended` and `Aggressive` profiles, from telemetry across all deployments, then recalculates them periodically. A rule's tags can change between updates. These tags describe how the rule typically behaves, not how it behaves in your environment.
::::

To learn how to build your first set of rules, refer to [Choosing which rules to enable](/solutions/security/detect-and-alert/install-prebuilt-rules.md#choosing-rules-to-enable).

### Use case tags

The `Use Case` tag category has the following values:

| Use case | Description |
|----------|-------------|
| `Active Directory Monitoring` | Detects changes to Active Directory objects such as user accounts, groups, and group policies that could indicate privilege escalation or persistence. |
| `Asset Visibility` | Tracks changes to hosts, devices, and other assets to identify unauthorized modifications or new devices appearing on the network. |
| `Configuration Audit` | Identifies security-relevant configuration changes that could weaken defenses, such as disabled security controls or modified audit policies. |
| `Guided Onboarding` | Example rule used for {{elastic-sec}}'s guided onboarding tour. |
| `Identity and Access Audit` | Monitors identity and access management (IAM) activity such as permission changes, role assignments, and authentication policy modifications. |
| `Log Auditing` | Detects tampering with log configurations or storage, such as clearing event logs or disabling audit logging, which attackers use to cover their tracks. |
| `Network Security Monitoring` | Monitors network security configurations such as firewall rules, proxy settings, and DNS changes that could indicate compromise or policy violations. |
| `Threat Detection` | Identifies malicious behaviors, attack techniques, and indicators of compromise across endpoints, networks, and cloud environments. |
| `Vulnerability` | Detects active exploitation of known vulnerabilities (CVEs) in your environment. |


## Prebuilt rule data sources [rule-prerequisites]

Each prebuilt rule queries specific index patterns, which determine the data the rule searches at runtime. You can see a rule's index patterns on its details page under **Definition**.

To help you set up the right data sources, rule details pages include:

**Related integrations**
:   [{{product.integrations}}](https://docs.elastic.co/en/integrations) that can provide compatible data. You don't need to install all listed integrations—installing any integration that matches your environment is typically sufficient. If a rule requires multiple integrations, the setup guide specifies which ones. Some rules also work with data from legacy beats (such as {{filebeat}} or {{winlogbeat}}) without requiring a {{fleet}} integration. This field also displays each integration's installation status and includes links for installing and configuring the listed integrations.

**Required fields**
:   Data fields the rule expects to find. Most rules run even if fields are missing, but may not generate expected alerts. EQL rules have stricter validation and might fail if required fields are missing.

**Setup guide**
:   Step-by-step guidance for configuring the rule's data requirements.

### Check integration status from the Rules table

You can check rules' related integrations in the **Installed Rules** and **Rule Monitoring** tables. Select the **integrations** badge to display the related integrations in a popup. The badge shows how many of the rule's related integrations are currently installed and enabled—for example, `1/2` means one of two related integrations is installed and actively collecting data.

An integration is counted as enabled only if it has been added to an agent policy and that policy is deployed to at least one agent. Installing an integration package without adding it to a policy does not increment the enabled count.

:::{admonition} Requirements for viewing related integration status
To view related integration status in the Rules table, your role needs at least `Read` privileges for the following features under {{manage-app}}:

- {{integrations}}
- {{fleet}}
- {{saved-objects-app}}

Without these privileges, the integrations badge may not appear or may not reflect accurate installation status.
:::

::::{tip}
You can hide the **integrations** badge in the Rules tables by turning off the `securitySolution:showRelatedIntegrations` [advanced setting](kibana://reference/advanced-settings.md#kibana-siem-settings).
::::


## Prebuilt rule investigation guides [prebuilt-investigation-guides]

Many prebuilt rules include investigation guides—Markdown documents that help analysts triage, analyze, and respond to alerts. A good investigation guide reduces mean time to respond by giving analysts the context and queries they need without leaving the alert details flyout.

### Find a rule's investigation guide

1. Open an alert generated by the rule.
2. In the alert details flyout, go to the **Investigation** section on the **Overview** tab.
3. If the rule has an investigation guide, select **Show investigation guide** to open it in the details panel.

You can also view investigation guides from the rule's details page. Find **{{siem-rules-ui}}** in the navigation menu, then select the rule name.

### What investigation guides include

Prebuilt rule investigation guides typically contain:

- **Context**: Background on the threat or technique the rule detects.
- **Triage steps**: How to determine if the alert is a true positive.
- **Investigation queries**: Pre-built queries to gather additional context. Some guides include interactive Timeline buttons.
- **Response guidance**: Actions to take if the alert is confirmed as a true positive.

::::{note}
You cannot edit investigation guides for prebuilt rules. To customize a prebuilt rule's guide, [duplicate the rule](/solutions/security/detect-and-alert/customize-prebuilt-rules.md#duplicate-prebuilt-rules) first, then edit the duplicate's investigation guide.
::::

### Write investigation guides for custom rules

When you create custom rules, you can write your own investigation guides using Markdown with interactive elements like Timeline queries and Osquery buttons. Refer to [Write investigation guides](/solutions/security/detect-and-alert/write-investigation-guides.md) for syntax and best practices.


## Build custom rules [build-custom-rules]

Prebuilt rules cover common threats, but your environment has unique risks. When you need detection logic tailored to your infrastructure, applications, or threat model, refer to [Author rules](/solutions/security/detect-and-alert/author-rules.md) for guidance on selecting a rule type, writing queries, and configuring rule settings.
