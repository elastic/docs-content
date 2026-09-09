* **From within {{kib}}:** Searches you run from the origin project use your [{{ecloud}} user role assignments](/deploy-manage/users-roles/cloud-organization/user-roles.md) on each project that participates in the search. Each role assignment must include [Cloud Console, {{es}}, and {{kib}} access](/deploy-manage/users-roles/cloud-organization/user-roles.md#access) to those projects to return project data.

* **Programmatically:** Requests authenticated with an [{{ecloud}} API key](/deploy-manage/api-keys/elastic-cloud-api-keys.md) use that key’s role assignments on each project. Each role assignment must include [Cloud, {{es}}, and {{kib}} API access](/deploy-manage/api-keys/elastic-cloud-api-keys.md#project-access) to those projects to return project data.

Alternatively, a user or key can be granted organization-level roles that grant access to all projects in the organization.

Permissions are always evaluated per project. It does not matter whether you query that project from its own endpoint or from an origin project linked through {{cps-init}}: the same role assignments apply.

{{cps-cap}} features in {{kib}}, such as the [{{cps-init}} scope selector](/explore-analyze/cross-project-search/cross-project-search-manage-scope.md#cps-in-kibana), require the [`read_project_routing` cluster privilege](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster). When you create [custom roles](/deploy-manage/users-roles/serverless-custom-roles.md) for users who search across projects, grant the `read_project_routing` cluster privilege alongside the `read` index privilege.

::::{admonition} Use {{ecloud}} API keys for {{cps-init}}
For {{cps}}, you must use [{{ecloud}} API keys](/deploy-manage/api-keys/elastic-cloud-api-keys.md), which can authenticate across project boundaries. 

{{cps-cap}} is not available when performing programmatic searches using [{{es}} API keys](/deploy-manage/api-keys/serverless-project-api-keys.md), because they're scoped to a single project. These keys return results from the origin project only.
::::