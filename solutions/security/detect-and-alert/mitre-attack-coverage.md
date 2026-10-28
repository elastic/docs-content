---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/rules-coverage.html
  - https://www.elastic.co/guide/en/serverless/current/security-rules-coverage.html
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: View which MITRE ATT&CK and MITRE ATLAS tactics and techniques your installed detection rules cover, and enable rules to close coverage gaps.
---

# MITRE coverage [security-rules-coverage]

The MITRE coverage page shows which adversary tactics and techniques your installed detection rules cover, both Elastic prebuilt and custom. It maps rules to these frameworks:

* [MITRE ATT&CK®](https://attack.mitre.org): Attacks on enterprise IT systems.
* {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` [MITRE ATLAS™](https://atlas.mitre.org): Attacks on AI and machine learning systems, such as prompt injection.

How you use this page depends on your goal:

- **Identifying coverage gaps**: Filter to view only enabled rules, then look for light or empty cells to find tactics and techniques where your detection coverage is thin. Use this to prioritize which [prebuilt rules](/solutions/security/detect-and-alert/install-prebuilt-rules.md) to install or which [custom rules](/solutions/security/detect-and-alert/using-the-rule-ui.md) to build next.
- **Activating coverage quickly**: Find techniques you care about and [enable installed rules](#security-rules-coverage-enable-rules) directly from the coverage grid, without leaving the page.

## Access the page [access-mitre-page]

Find the page in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Its name depends on your version:

* {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` **MITRE coverage**
* {applies_to}`stack: ga 9.0-9.5` **MITRE ATT&CK coverage**

To view the page, you need at least read access to detection rules. To enable rules from the coverage grid, you also need privileges to enable and disable rules. For details, refer to [Detections privileges](/solutions/security/detect-and-alert/detections-privileges.md#detections-privileges-manage-rules).

:::{image} /solutions/images/security-rules-coverage.png
:alt: MITRE ATT&CK coverage page
:screenshot:
:::

## Read the coverage grid [read-coverage-grid]

Columns represent the major tactics of the framework you're viewing, and cells within each column represent a tactic's related techniques. Cells are darker when a technique has more rules matching the current filters, as indicated in the **Legend** at the top.

::::{note}
The coverage grid only includes detection rules you currently have installed, and only rules that are mapped to the framework you're viewing. Prebuilt rules that are not installed, and custom rules that are unmapped or mapped to a deprecated tactic or technique, do not appear. You can map custom rules to tactics in **Advanced settings** when creating or editing a rule.
::::

## View MITRE ATLAS coverage [view-mitre-atlas-coverage]
```{applies_to}
stack: ga 9.6+
serverless: ga
```

The page opens on the **MITRE ATT&CK** tab. To view coverage of MITRE ATLAS [v2026.08](https://github.com/mitre-atlas/atlas-data/releases/tag/v2026.08), select the **MITRE ATLAS** tab. Each tab counts only its own framework's mappings, so a rule mapped to both frameworks appears on both tabs.

Some Elastic prebuilt rules for generative AI threats include MITRE ATLAS mappings. To map a custom rule, add MITRE ATLAS in the rule's [**Threat mappings**](/solutions/security/detect-and-alert/common-rule-settings.md#rule-ui-advanced-params) setting.

## Supported MITRE ATT&CK versions [supported-versions]

The coverage page maps detections to [MITRE ATT&CK versions](https://attack.mitre.org/resources/updates/) used by {{elastic-sec}}.

| {{elastic-sec}} version | MITRE ATT\&CK version |
| :---- | :---- |
| 9.0.0 | [v15.1](https://attack.mitre.org/resources/updates/updates-april-2024/) |
| 9.0.1-9.0.6 | [v16.1](https://attack.mitre.org/resources/updates/updates-october-2024/) |
| 9.0.7-9.0.8 | [v17.1](https://attack.mitre.org/resources/updates/updates-april-2025/) |
| 9.1.0-9.1.3 | [v16.1](https://attack.mitre.org/resources/updates/updates-october-2024/) |
| 9.1.4-9.1.9 | [v17.1](https://attack.mitre.org/resources/updates/updates-april-2025/) |
| 9.1.10 | [v18.1](https://attack.mitre.org/resources/updates/updates-october-2025/) |
| 9.2.0-9.2.3 | [v17.1](https://attack.mitre.org/resources/updates/updates-april-2025/) |
| 9.2.4-9.4.3 | [v18.1](https://attack.mitre.org/resources/updates/updates-october-2025/) |
| 9.5.x | [v19.1](https://attack.mitre.org/resources/updates/updates-april-2026/) |
| 9.6.0+ | [v19.2](https://attack.mitre.org/resources/updates/updates-august-2026/) |
| {{serverless-short}} | [v19.2](https://attack.mitre.org/resources/updates/updates-august-2026/) |

::::{note}
:applies_to: {stack: ga 9.5, serverless: ga}
MITRE ATT\&CK v19 retires the Defense Evasion tactic and replaces it with Stealth and Defense Impairment. If you have custom rules mapped to MITRE ATT\&CK, check [](/solutions/security/detect-and-alert/remap-mitre-attack.md) to find and update mappings that changed in v19.
::::


## Filter rules [security-rules-coverage-filter-rules]

Use the drop-down filters at the top of the page to control which of your installed detection rules are included in calculating coverage.

* **Installed rule status**: Select to include **Enabled rules**, **Disabled rules**, or both.
* **Installed rule type**: Select to include **Elastic rules** (prebuilt rules), **Custom rules** (user-created rules), or both.

You can also search for a tactic or technique name, technique number, or rule name in the search bar. The search bar acts as a filter for the coverage grid: only rules matching the search term are included.

::::{note}
Searches for tactics and techniques must match exactly, are case sensitive, and do *not* support wildcards.
::::


## Expand and collapse cells [security-rules-coverage-expand-and-collapse-cells]

Select **Collapse cells** or **Expand cells** to change how much information the cells display. Cells always include the technique's name and the number of sub-techniques covered by enabled rules. Expand the cells to also display counts of disabled and enabled rules for each technique.

::::{note}
The counts inside cells are affected by how you filter the page. For example, if you filter the **Installed rule status** to only include **Enabled rules**, then all disabled rule counts are 0 because those rules are filtered out.
::::



## Enable rules [security-rules-coverage-enable-rules]

You can quickly enable all the rules for a specific technique that you've installed but not yet enabled. Select the technique's cell, then select **Enable all disabled** in the popup that appears.


## Learn more about techniques and sub-techniques [security-rules-coverage-learn-more-about-techniques-and-sub-techniques]

For more information on a specific technique and its sub-techniques, select the technique's cell, then click the title in the popup that appears. This opens a new browser tab with the technique's documentation on the MITRE ATT&CK or MITRE ATLAS website.
