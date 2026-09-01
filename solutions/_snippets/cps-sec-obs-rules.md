When [{{cps}}](/explore-analyze/cross-project-search.md) is enabled and you have [linked projects](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md), rules query data across linked projects based on the **space-level {{cps}} scope**.

When you create or edit a rule, the [{{cps-init}} scope selector](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md#cps-in-kibana) in the header shows the current {{cps}} scope but is read-only. To change which projects most rules query, update the [{{cps}} scope configured for the space](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope).

You can't select a {{cps}} scope for an individual rule in the header. These rule types can still control which projects they query:

- **{{esql}} rules:** Add [`SET project_routing`](/explore-analyze/cross-project-search/cross-project-search-project-routing.md) at the start of the rule query to override the space-level scope.
- **Rules that use index patterns:** Use [qualified index expressions](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions) in the index pattern to target specific projects.
- **{{ml-cap}} rules:** These rules alert on {{anomaly-detect}} results stored on the origin project. {{anomaly-jobs-cap}} can read linked-project data; jobs and results stay on the origin.

<!-- TODO: After https://github.com/elastic/docs-content/pull/7814 merges, restore the link on "can read linked-project data" to /explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md#ml-ad-cps-scope. -->

For prerequisites such as linking projects and configuring default scope, refer to [](/explore-analyze/cross-project-search.md) and [](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md).
