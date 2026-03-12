
- **Maximum of 20 linked projects:** Each origin project can have up to 20 linked projects. A linked project can be associated with any number of origin projects.
- **Chaining/transitivity not supported:** If Project A links to Project B, and Project B links to Project C, Project A cannot automatically search Project C. Each link is independent.
- **Links are unidirectional:** Searches that run from a linked project do **not** run against the origin project. If you need bidirectional search, link the projects twice, in both directions.
- **System indices are excluded:** System indices (such as `.security` and `.fleet-*`) are excluded from {{cps}}.
- **Unavailable APIs:** `_transform` and `_fleet_search` requests do not support {{cps-init}}.
- **Workplace AI projects:** Workplace AI projects are not compatible with {{cps}}.
- {applies_to}`serverless: preview` **New projects only:** During technical preview, only newly created projects can function as origin projects.
- {applies_to}`serverless: preview` **ML and transforms:** ML {{anomaly-jobs}} and transforms are not supported in the technical preview. They continue to run on origin project data only.
- {applies_to}`serverless: preview` **Failure store:** 🚧 TODO

% - {applies_to}`serverless: preview` **Project aliases:** During technical preview, you can't edit a project's alias on the **{{cps-cap}}** page.
