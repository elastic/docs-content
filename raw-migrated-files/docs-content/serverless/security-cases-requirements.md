# Cases requirements [security-cases-requirements]

To access cases, you need either the appropriate [predefined Security user role](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles) or a [custom role](../../../deploy-manage/users-roles/cloud-organization/user-roles.md) with the right privileges.

You can create custom roles and define feature privileges at different levels to manage feature access in {{kib}}. {{kib}} privileges grant access to features within a specified {{kib}} space, and you can grant full or partial access. For more information, refer to [Custom roles](../../../deploy-manage/users-roles/cloud-organization/user-roles.md).

::::{note}
To send cases to external systems, you need the Security Analytics Complete [project feature](../../../deploy-manage/deploy/elastic-cloud/project-settings.md).

::::


::::{important}
Certain feature tiers and roles might be required to manage case attachments. For example, to add alerts to cases, you must have a role that allows [managing alerts](../../../solutions/security/detect-and-alert/detections-requirements.md#enable-detections-ui).

::::


To grant access to cases in a custom role, set the privileges for the **Cases** and **{{connectors-feature}}** features as follows:

| Action | {{kib}} Privileges |
| --- | --- |
| Give full access to manage cases and settings | * **All** for the **Cases*** feature under ***Security***<br>* ***All*** for the ***{{connectors-feature}}*** feature under ***Stack Management***<br><br>::::{note} <br>Roles without ***All*** privileges for the ***{{connectors-feature}}*** feature cannot create, add, delete, or modify case connectors.<br><br>By default, ***All** for the **Cases** feature allows you to delete cases, delete alerts and comments from cases, and edit case settings. You can customize the sub-feature privileges to limit feature access.<br><br>::::<br><br> |
| Give assignee access to cases | **All** for the **Cases** feature under **Security**<br><br>::::{note} <br>Before a user can be assigned to a case, they must log into {{kib}} at least once, which creates a user profile.<br><br>::::<br><br> |
| Give view-only access for cases | **Read** for the **Security*** feature and ***All** for the **Cases** feature<br><br>::::{note} <br>You can customize the sub-feature privileges to allow access to deleting cases, deleting alerts and comments from cases, viewing or editing case settings, adding case comments and attachments, and re-opening cases.<br><br>::::<br><br> |
| Revoke all access to cases | **None** for the **Cases** feature under **Security** |
