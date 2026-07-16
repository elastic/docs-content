- **Include empty rows**: Include buckets that contain no matching documents. Existing saved visualizations keep their configured setting.
  - {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` For new visualizations, this option is:
    - On by default for tables, line charts, and area charts
    - Off by default for bar charts, heat maps, pie charts, treemap charts, mosaic charts, waffle charts, metric charts, and tag clouds

    When you switch visualization or series type, Lens applies the default for the new type. If you switch back to the visualization type you saved, Lens restores the saved setting.
  - {applies_to}`stack: ga 9.0-9.4` This option is on by default for all visualization types.

- **Bind to global time picker**: Associate the selected field to the Lens or dashboard main time selector.

- **Minimum interval**: Define the time interval for aggregating the data. For example, `30s`, `20m`, `24h`, `2d`, `1w`, `1M`

- **Drop partial intervals**: Exclude incomplete intervals from the data. This option is off by default.
