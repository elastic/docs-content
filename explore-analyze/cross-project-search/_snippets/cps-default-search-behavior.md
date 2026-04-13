Projects are intended to act as logical namespaces for data, not hard boundaries for querying it. You can split data into projects to organize ownership, use cases, or environments, while still expecting to search and analyze that data from a single place.

After you link projects, searches from the origin project run across the origin and all linked projects by default.
This default behavior provides a consistent experience for querying, analysis, and insights across linked projects.
Restricting search scope is always possible, by explicitly scoping the search request using [qualified expressions](/explore-analyze/cross-project-search/cross-project-search-search.md#search-expressions) or [project routing parameters](/explore-analyze/cross-project-search/cross-project-search-project-routing.md).
