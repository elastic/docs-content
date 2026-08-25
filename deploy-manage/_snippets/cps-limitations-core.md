<!-- TODO (docs-content#8050): Confirm the linked project ceiling for CPS GA. The docs on this page say it's 20, but item #2 in https://github.com/elastic/docs-content/issues/8050 shows it's 100. Confirm the GA number with Platform PM (Tia Milosevic) and update it everywhere the ceiling is stated.

When updating CPS `applies_to` tags from preview to GA, revisit the "New projects only" item below (it is scoped to technical preview) and the `serverless: preview` lifecycle tags on the CPS pages.
-->


- **Maximum of 20 linked projects:** Each origin project can have up to 20 linked projects. A linked project can be associated with any number of origin projects.
- **System indices:** Indices such as `.security` and `.fleet-*` are excluded from {{cps}} results by design.
- **New projects only:** During technical preview, only newly created projects can function as origin projects.
- **{{anomaly-detect-cap}} and transforms:** {{anomaly-detect-cap}} job {{dfeeds}} and transforms can read linked-project data. Jobs, transforms, and their results live on the origin project.
- **{{dfanalytics-jobs-cap}}:** {{dfanalytics-jobs}} are not supported with {{cps-init}}. They continue to run on origin project data only.
- For {{esql}} limitations specific to {{cps-init}}, refer to [ES|QL with {{cps}}](elasticsearch://reference/query-languages/esql/esql-cross-serverless-projects.md#limitations).
