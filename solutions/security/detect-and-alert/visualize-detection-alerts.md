---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/visualize-alerts.html
  - https://www.elastic.co/guide/en/serverless/current/security-visualize-alerts.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
description: Visualize and group detection alerts using Summary, Trend, Counts, and Treemap views on the Alerts page.
---

# Visualize detection alerts [security-visualize-alerts]

The Alerts page includes a visualization section that helps you spot patterns, identify high-volume rules, and prioritize investigation. Choose from four view types, each designed for different analysis tasks.

:::{image} /solutions/images/security-alert-page.png
:alt: Alerts page with visualizations section
:screenshot:
:::


## View types at a glance [view-types-overview]

| View | Best for | Supports secondary grouping |
|------|----------|----------------------------|
| [Summary](#security-visualize-alerts-summary) | Quick overview of severity, top rules, and affected hosts/users | No |
| [Trend](#security-visualize-alerts-trend) | Spotting alert spikes and patterns over time | No |
| [Counts](#security-visualize-alerts-counts) | Comparing alert volumes across rules, hosts, or other fields | Yes |
| [Treemap](#security-visualize-alerts-treemap) | Identifying the most frequent and critical alert combinations | Yes |


## Grouping alerts [grouping-alerts]

Use the dropdown menus above the visualization to group alerts by ECS fields:

| Menu | Purpose |
|------|---------|
| Group by (or Top alerts by) | Primary field for grouping alerts |
| Group by top | Secondary field for subdividing groups (available in Counts and Treemap views) |

**Example**: Group by `kibana.alert.rule.name`, then by `host.name` to see which rules fired and which hosts triggered each rule.

::::{note}
For groupings with many unique values, only the top 1,000 results are displayed.
::::


## Common actions [common-actions]

| Action | How to do it |
|--------|--------------|
| Reset grouping | Hover over the visualization, click {icon}`boxes_horizontal`, then select **Reset group by fields** |
| Inspect queries | Click {icon}`boxes_horizontal` and select **Inspect** |
| Add to case | Click {icon}`boxes_horizontal` and select **Add to case** (Trend and Counts views only) |
| Open in Lens | Click {icon}`boxes_horizontal` and select **Open in Lens** (Trend and Counts views only) |
| Collapse visualization | Click {icon}`arrow_down` to show a compact summary instead |

:::{image} /solutions/images/security-alert-page-viz-collapsed.png
:alt: Alerts page with visualizations section collapsed
:screenshot:
:::


## Summary [security-visualize-alerts-summary]

The default view. Shows alert distribution across three panels:

| Panel | What it shows |
|-------|---------------|
| Severity levels | Count of alerts by severity (`low`, `medium`, `high`, `critical`) |
| Alerts by name | Count of alerts by detection rule |
| Top alerts by | Percentage breakdown by `host.name`, `user.name`, `source.ip`, or `destination.ip` |

Click any element (severity level, rule name, or host) to filter the Alerts table to those values.

:::{image} /solutions/images/security-alerts-viz-summary.png
:alt: Summary visualization for alerts
:screenshot:
:::


## Trend [security-visualize-alerts-trend]

Shows alert volume over time as a stacked area chart. Use this to spot spikes, patterns, or changes in alert activity.

| Setting | Default |
|---------|---------|
| Group by | `kibana.alert.rule.name` |
| Secondary grouping | Not available |

:::{image} /solutions/images/security-alerts-viz-trend.png
:alt: Trend visualization for alerts
:screenshot:
:::


## Counts [security-visualize-alerts-counts]

Shows alert counts as a table, grouped by one or two fields. Use this to compare alert volumes across rules, hosts, users, or other dimensions.

| Setting | Default |
|---------|---------|
| Group by | `kibana.alert.rule.name` |
| Group by top | `host.name` |

:::{image} /solutions/images/security-alerts-viz-counts.png
:alt: Counts visualization for alerts
:screenshot:
:::


## Treemap [security-visualize-alerts-treemap]

Shows alert distribution as nested, proportionally-sized tiles. Larger tiles indicate more alerts; colors indicate risk score.

| Setting | Default |
|---------|---------|
| Group by | `kibana.alert.rule.name` |
| Group by top | `host.name` |

:::{image} /solutions/images/security-alerts-viz-treemap.png
:alt: Treemap visualization for alerts
:screenshot:
:::

### Treemap colors

| Color | Risk score range |
|-------|------------------|
| Green | Low (0–46) |
| Yellow | Medium (47–72) |
| Orange | High (73–98) |
| Red | Critical (99–100) |

### Interacting with the treemap

Click elements to filter the alerts table:
- Click a **group label** (above a section) to filter to that group
- Click an **individual tile** to filter to that specific combination

Filters appear below the KQL search bar, where you can edit or remove them.

:::{image} /solutions/images/security-treemap-click.gif
:alt: Animation of clicking the treemap
:screenshot:
:::

::::{tip}
Some tiles may be small depending on alert volume. Hover over tiles to see details in a tooltip.
::::
