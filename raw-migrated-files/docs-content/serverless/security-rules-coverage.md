# MITRE ATT&CK® coverage [security-rules-coverage]

The **MITRE ATT&CK® coverage** page (**Rules** → **MITRE ATT&CK® Coverage**) shows which [MITRE ATT&CK®](https://attack.mitre.org) adversary tactics and techniques are covered by your installed and enabled detection rules. This includes both Elastic prebuilt rules and custom rules.

Mirroring the MITRE ATT&CK® framework, columns represent major tactics, and cells within each column represent a tactic’s related techniques. Cells are darker when a technique has more rules matching the current filters, as indicated in the **Legend** at the top.

::::{note}
This page only includes the detection rules you currently have installed, and only rules that are mapped to MITRE ATT&CK®. The coverage page maps detections to the following [MITRE ATT&CK® version](https://attack.mitre.org/resources/updates/updates-april-2024) used by {{elastic-sec}}: `v15.1`. Elastic prebuilt rules that aren’t installed and custom rules that are either unmapped or mapped to a deprecated tactic or technique will not appear on the coverage map.

You can map custom rules to tactics in **Advanced settings** when creating or editing a rule.

::::


:::{image} ../../../images/serverless--detections-rules-coverage.png
:alt: MITRE ATT&CK® coverage page
:class: screenshot
:::


## Filter rules [security-rules-coverage-filter-rules]

Use the drop-down filters at the top of the page to control which of your installed detection rules are included in calculating coverage.

* **Installed rule status**: Select to include **Enabled rules**, **Disabled rules**, or both.
* **Installed rule type**: Select to include **Elastic rules** (prebuilt rules), **Custom rules** (user-created rules), or both.

You can also search for a tactic or technique name, technique number, or rule name in the search bar. The search bar acts as a filter for the coverage grid: only rules matching the search term will be included.

::::{note}
Searches for tactics and techniques must match exactly, are case sensitive, and do *not* support wildcards.

::::



## Expand and collapse cells [security-rules-coverage-expand-and-collapse-cells]

Click **Collapse cells** or **Expand cells** to change how much information the cells display. Cells always include the technique’s name and the number of sub-techniques covered by enabled rules. Expand the cells to also display counts of disabled and enabled rules for each technique.

::::{note}
The counts inside cells are affected by how you filter the page. For example, if you filter the **Installed rule status** to only include **Enabled rules**, then all disabled rule counts will be 0 because disabled rules are filtered out.

::::



## Enable rules [security-rules-coverage-enable-rules]

You can quickly enable all the rules for a specific technique that you’ve installed, but not enabled. Click the technique’s cell, then click **Enable all disabled** in the popup that appears.


## Learn more about techniques and sub-techniques [security-rules-coverage-learn-more-about-techniques-and-sub-techniques]

For more information on a specific technique and its sub-techniques, click the technique’s cell, then click the title in the popup that appears. This opens a new browser tab with the technique’s MITRE ATT&CK® documentation.
