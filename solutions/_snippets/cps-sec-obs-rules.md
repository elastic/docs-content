
When [{{cps}}](/explore-analyze/cross-project-search.md) is enabled and you have [linked projects](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md), rules query data across linked projects based on the **space-level {{cps}} scope**. You can't set a {{cps}} scope on individual rules.

When you create or edit a rule, the [{{cps-init}} scope selector](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md#cps-in-kibana) in the header shows the current {{cps}} scope but is read-only. To change which projects rules query, update the [{{cps}} scope configured for the space](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#cps-default-search-scope).

For {{esql}} rules, you can use [`SET project_routing`](/explore-analyze/cross-project-search/cross-project-search-project-routing.md) in the rule query to target specific linked projects, overriding the space-level scope. For non-{{esql}} rules that use index patterns, you can use [qualified index expressions](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions) to scope the rule to specific projects.

For prerequisites such as linking projects and configuring default scope, refer to [{{cps-cap}}](/explore-analyze/cross-project-search.md) and [Configure {{cps}} access and scope](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md).

:::{note}
<!-- TODO: After https://github.com/elastic/docs-content/pull/7814 merges, restore the link on "can read linked-project data" to /explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md#ml-ad-cps-scope. -->
{{ml-cap}} rules alert on {{anomaly-detect}} results stored on the origin project. {{anomaly-jobs-cap}} can read linked-project data; jobs and results stay on the origin. Other features also have limited or no {{cps}} support. For details, refer to [{{cps-cap}} availability by app](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md).
:::
