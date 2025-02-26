---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/rules-coverage.html
  - https://www.elastic.co/guide/en/serverless/current/security-rules-coverage.html
---

# MITRE ATT&CK® coverage

% What needs to be done: Lift-and-shift

% Use migrated content from existing pages that map to this page:

% - [x] ./raw-migrated-files/security-docs/security/rules-coverage.md
% - [ ] ./raw-migrated-files/docs-content/serverless/security-rules-coverage.md

The **MITRE ATT&CK® coverage** page shows which [MITRE ATT&CK®](https://attack.mitre.org) adversary tactics and techniques are covered by your installed and enabled detection rules. This includes both Elastic prebuilt rules and custom rules.

Mirroring the MITRE ATT&CK® framework, columns represent major tactics, and cells within each column represent a tactic’s related techniques. Cells are darker when a technique has more rules matching the current filters, as indicated in the **Legend** at the top.

To access the **MITRE ATT&CK® coverage** page, find **Detection rules (SIEM)** in the navigation menu or look for “Detection rules (SIEM)” using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to **MITRE ATT&CK® coverage**.

::::{note}
This page only includes the detection rules you currently have installed, and only rules that are mapped to MITRE ATT&CK®. The coverage page maps detections to the following [MITRE ATT&CK® version](https://attack.mitre.org/resources/updates/updates-april-2024) used by {{elastic-sec}}: `v15.1`. Elastic prebuilt rules that aren’t installed and custom rules that are either unmapped or mapped to a deprecated tactic or technique will not appear on the coverage map.

You can map custom rules to tactics in **Advanced settings** when creating or editing a rule.

::::


:::{image} ../../../images/security-rules-coverage.png
:alt: MITRE ATT&CK® coverage page
:class: screenshot
:::


## Filter rules [_filter_rules]

Use the drop-down filters at the top of the page to control which of your installed detection rules are included in calculating coverage.

* **Installed rule status**: Select to include **Enabled rules**, **Disabled rules**, or both.
* **Installed rule type**: Select to include **Elastic rules** (prebuilt rules), **Custom rules** (user-created rules), or both.

You can also search for a tactic or technique name, technique number, or rule name in the search bar. The search bar acts as a filter for the coverage grid: only rules matching the search term will be included.

::::{note}
Searches for tactics and techniques must match exactly, are case sensitive, and do *not* support wildcards.
::::



## Expand and collapse cells [_expand_and_collapse_cells]

Click **Collapse cells** or **Expand cells** to change how much information the cells display. Cells always include the technique’s name and the number of sub-techniques covered by enabled rules. Expand the cells to also display counts of disabled and enabled rules for each technique.

::::{note}
The counts inside cells are affected by how you filter the page. For example, if you filter the **Installed rule status** to only include **Enabled rules**, then all disabled rule counts will be 0 because disabled rules are filtered out.
::::



## Enable rules [_enable_rules]

You can quickly enable all the rules for a specific technique that you’ve installed, but not enabled. Click the technique’s cell, then click **Enable all disabled** in the popup that appears.


## Learn more about techniques and sub-techniques [_learn_more_about_techniques_and_sub_techniques]

For more information on a specific technique and its sub-techniques, click the technique’s cell, then click the title in the popup that appears. This opens a new browser tab with the technique’s MITRE ATT&CK® documentation.
