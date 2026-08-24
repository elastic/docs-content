<!-- TODO (docs-content#8050): Three items to confirm for CPS GA:

1. Linked project ceiling. This list says 20, the CPS GA issue says 100. Confirm the GA number with Platform PM (Tia Milosevic) and update it everywhere the ceiling is stated.

2. ML anomaly jobs and transforms. The GA issue says datafeeds and transforms can read linked-project data at GA. Kibana source shows datafeed and transform configs do accept `project_routing`, but anomaly results are still queried with `_alias:_origin` and the rule type picker renders a "CPS support coming soon" badge for ML and transform health rule types. Confirm the GA scope before relaxing this limitation, and keep it in sync with /solutions/_snippets/cps-sec-obs-rules.md.

3. Technical preview wording. The "New projects only" item below is scoped to technical preview. Revisit it, and the serverless: preview lifecycle tags on the CPS pages, when CPS goes GA.
-->

- **Maximum of 20 linked projects:** Each origin project can have up to 20 linked projects. A linked project can be associated with any number of origin projects.
- **System indices:** Indices such as `.security` and `.fleet-*` are excluded from {{cps}} results by design.
- **New projects only:** During technical preview, only newly created projects can function as origin projects.
- **{{anomaly-detect-cap}} and transforms:** During technical preview, ML {{anomaly-jobs}} and transforms are not supported with {{cps-init}}. They continue to run on origin project data only.
- **{{dfanalytics-jobs-cap}}:** {{dfanalytics-jobs}} are not supported with {{cps-init}}. They continue to run on origin project data only.
- For {{esql}} limitations specific to {{cps-init}}, refer to [ES|QL with {{cps}}](elasticsearch://reference/query-languages/esql/esql-cross-serverless-projects.md#limitations).