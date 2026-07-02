The following organization-level roles are required to manage network security policies through the {{ecloud}} Console. For more information about roles and scoping, refer to [User roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md).

::::{applies-switch}
:::{applies-item} ess:

| Action | Required role |
| --- | --- |
| View network security policies | Any organization member |
| Create a network security policy | Organization owner<br><br>Admin or Editor on at least one Hosted deployment |
| Edit or delete a network security policy | Organization owner<br><br>Admin or Editor on at least one Hosted deployment |
| Mark a network security policy to apply to new deployments by default | Organization owner<br><br>Admin or Editor scoped to all Hosted deployments |
| Associate or disassociate a network security policy with a specific deployment | Admin or Editor on that deployment |

:::
:::{applies-item} serverless:

| Action | Required role |
| --- | --- |
| View network security policies | Any organization member |
| Create a network security policy | Organization owner<br><br>Admin or Editor on at least one project |
| Edit or delete a network security policy | Organization owner<br><br>Admin or Editor on at least one project |
| Mark a network security policy to apply to new projects by default | Organization owner<br><br>Admin or Editor scoped to all {{es}}, Observability, and Security projects |
| Associate or disassociate a network security policy with a specific project | Admin or Editor on that project |

:::
::::
