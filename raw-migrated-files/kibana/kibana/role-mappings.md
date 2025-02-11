# Role mappings [role-mappings]

Role mappings are part of single sign-on (SSO), a [subscription feature](https://www.elastic.co/subscriptions). This feature allows you to describe which roles to assign to your users using a set of rules.

Role mappings are required when authenticating via an external identity provider, such as Active Directory, Kerberos, PKI, OIDC, or SAML. Role mappings have no effect for users inside the `native` or `file` realms.

You can find the **Role mappings** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

With **Role mappings**, you can:

* View your configured role mappings
* Create/Edit/Delete role mappings

![Role mappings](../../../images/kibana-role-mappings-grid.png "")


### Required permissions [_required_permissions_8]

The `manage_security` cluster privilege is required to manage Role Mappings.


## Create a role mapping [_create_a_role_mapping]

1. Go to the **Role mappings** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Create role mapping**.
3. Give your role mapping a unique name, and choose which roles you wish to assign to your users.

    If you need more flexibility, you can use [role templates](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-put-role-mapping.html#_role_templates) instead.

4. Define the rules describing which users should receive the roles you defined. Rules can optionally grouped and nested, allowing for sophisticated logic to suite complex requirements.
5. View the [role mapping resources for an overview of the allowed rule types](../../../deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md).


## Example [_example_2]

Let’s create a `sales-users` role mapping, which assigns a `sales` role to users whose username starts with `sls_`, **or** belongs to the `executive` group.

First, we give the role mapping a name, and assign the `sales` role:

![Create role mapping, step 1](../../../images/kibana-role-mappings-create-step-1.png "")

Next, we define the two rules, making sure to set the group to **Any are true**:

![Create role mapping, step 2](../../../images/kibana-role-mappings-create-step-2.gif "")

Click **Save role mapping** once you’re finished.

