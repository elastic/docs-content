
When [{{cps}}](/explore-analyze/cross-project-search.md) is enabled and you have [linked projects](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md), rules query data across linked projects based on the **space-level {{cps}} scope**.

For how {{cps}} applies when you create or edit rules (space-level scope, the read-only scope selector, and query-level overrides) refer to [{{cps-cap}} availability by app](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md#cps-availability). 

For prerequisites such as linking projects and configuring default scope, refer to [{{cps-cap}}](/explore-analyze/cross-project-search.md) and [Configure {{cps}} access and scope](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md). 

<!-- TODO (docs-content#8050): The CPS GA issue says ML rule types alert on anomalies produced from linked-project data, which would change the note below. Kibana source at HEAD still pins anomaly result searches to `_alias:_origin`, and the rule type picker renders a "CPS support coming soon" badge for ML and transform health rule types. Confirm with Security PM (@chuddy-elastic) before changing the ML wording, and keep it in sync with /explore-analyze/cross-project-search/_snippets/cps-availability-security-apps.md and /deploy-manage/_snippets/cps-limitations-core.md. This snippet is shared by Security and Observability, so any change lands in both. -->

:::{note}
{{ml-cap}} rules don't support {{cps}}; they search data in the origin project only. Other features also have limited or no {{cps}} support. For details, refer to [{{cps-cap}} availability by app](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md#cps-availability).
:::
