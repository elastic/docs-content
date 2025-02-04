# Granting access to {{kib}} [xpack-security-authorization]

The Elastic Stack comes with the `kibana_admin` [built-in role](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md), which you can use to grant access to all {{kib}} features in all spaces. To grant users access to a subset of spaces or features, you can create a custom role that grants the desired {{kib}} privileges.

When you assign a user multiple roles, the user receives a union of the roles’ privileges. Therefore, assigning the `kibana_admin` role in addition to a custom role that grants {{kib}} privileges is ineffective because `kibana_admin` has access to all the features in all spaces.

