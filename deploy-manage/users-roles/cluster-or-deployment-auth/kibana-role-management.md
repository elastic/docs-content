---
navigation_title: Using Kibana
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/kibana-role-management.html
applies_to:
  stack: all
products:
  - id: kibana
---

# Role management using {{kib}} [kibana-role-management]

Roles are a collection of privileges that allow you to perform actions in {{kib}} and {{es}}. Users are not directly granted privileges, but are instead assigned one or more roles that describe the desired level of access. When you assign a user multiple roles, the user receives a union of the roles’ privileges. This means that you cannot reduce the privileges of a user by assigning them an additional role. You must instead remove or edit one of their existing roles.

To create a role:

1. Go to the **Roles** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). 
2. Click **Create role**.

## Required permissions [_required_permissions_7]

The `manage_security` [cluster privilege](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster) is required to access role management.

## Cluster privileges [adding_cluster_privileges]

Cluster privileges grant access to monitoring and management features in {{es}}. They also enable [Stack Management](/deploy-manage/index.md) capabilities in {{kib}}.

Refer to [cluster privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster) for a complete description of available options.

## Index privileges [adding_index_privileges]

Each role can grant access to multiple data indices, and each index can have a different set of privileges. We recommend granting the `read` and `view_index_metadata` privileges to each index that you expect your users to work with in {{kib}}.

Refer to [index privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) for a complete description of available options.

Document-level and field-level security affords you even more granularity when it comes to granting access to your data. With document-level security (DLS), you can write an {{es}} query to describe which documents this role grants access to. With field-level security (FLS), you can instruct {{es}} to grant or deny access to specific fields within each document.

### Example: Grant access to indices that match the `filebeat-*` pattern [index_privilege_example_1]

1. Go to the **Roles** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). 
2. Click **Create role**.
3. In **Index privileges**, enter:

    1. `filebeat-*` in the **Index** field.
    2. `read` and `view_index_metadata` in the **Privileges** field.

<br>
:::{image} /deploy-manage/images/kibana-create-role-index-example.png
:alt: Create role with index privileges
:screenshot:
:::

### Example: Grant read access to specific documents in indices that match the `filebeat-*` pattern [index_privilege_dls_example]

[Document-level security](/deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md) is a [subscription feature](https://www.elastic.co/subscriptions).

1. Go to the **Roles** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). 
2. Click **Create role**.
3. In **Index privileges**, enter:

    1. `filebeat-*` in the **Indices** field.
    2. `read` and `view_index_metadata` in the **Privileges** field.

4. Select **Grant read privileges to specific documents**.
5. Enter an {{es}} query that matches the documents your users should access. This example writes a query that allows access to documents that have a `category` field equal to `click`:

    ```sh
    {
      "match": {
        "category": "click"
      }
    }
    ```

    ::::{note}
    {{kib}} automatically surrounds your DLS query with a `query` block, so you don’t have to provide your own.
    ::::

<br>
:::{image} /deploy-manage/images/kibana-create-role-dls-example.png
:alt: Create role with DLS index privileges
:screenshot:
:::



## Remote index privileges [adding_remote_index_privileges]

If you have at least a platinum license, you can manage access to indices in remote clusters.

You can assign the same privileges, document-level, and field-level as for [local index privileges](#adding_index_privileges).

### Example: Grant access to indices in remote clusters [remote_index_privilege_example_1]

1. Go to the **Roles** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). 
2. Click **Create role**.
3. In **Remote index privileges**, enter:

    1. The name of your remote cluster in the **Remote clusters** field.
    2. The name of the index in your remote cluster in the **Remote indices** field.
    3. The allowed actions in the **Privileges** field. (e.g. `read` and `view_index_metadata`)

<br>
:::{image} /deploy-manage/images/kibana-create-role-remote-index-example.png
:alt: Create role with remote index privileges
:screenshot:
:::

## {{kib}} privileges [adding_kibana_privileges]

To assign {{kib}} privileges to the role, click **Add {{kib}} privilege** in the {{kib}} section.

<br>
:::{image} /deploy-manage/images/kibana-spaces-roles.png
:alt: Add {{kib}} privileges
:screenshot:
:width: 650px
:::

Open the **Spaces** selection control to specify whether to grant the role access to all spaces **All Spaces** or one or more individual spaces. If you select **All Spaces**, you can’t select individual spaces until you clear your selection.

Use the **Privilege** menu to grant access to features. The default is **Custom**, which you can use to grant access to individual features. Otherwise, you can grant read and write access to all current and future features by selecting **All**, or grant read access to all current and future features by selecting **Read**.

When using the **Customize by feature** option, you can choose either **All**, **Read** or **None** for access to each feature. As new features are added to {{kib}}, roles that use the custom option do not automatically get access to the new features. You must manually update the roles.

::::{note}
**{{stack-monitor-app}}** relies on built-in roles to grant access. When a user is assigned the appropriate roles, the **{{stack-monitor-app}}** application is available; otherwise, it is not visible.
::::


To apply your changes, click **Add {{kib}} privilege**. The privilege shows up under the {{kib}} privileges section of the role.

<br>
:::{image} /deploy-manage/images/kibana-create-space-privilege.png
:alt: Add {{kib}} privilege
:screenshot:
:::


## Feature availability [_feature_availability]

Features are available to users when their roles grant access to the features, **and** those features are visible in their current space. The following matrix explains when features are available to users when controlling access via [spaces](/deploy-manage/manage-spaces.md#spaces-managing) and role-based access control:

| **Spaces config** | **Role config** | **Result** |
| --- | --- | --- |
| Feature hidden | Feature disabled | Feature not available |
| Feature hidden | Feature enabled | Feature not available |
| Feature visible | Feature disabled | Feature not available |
| Feature visible | Feature enabled | **Feature available** |


## Assigning different privileges to different spaces [_assigning_different_privileges_to_different_spaces]

Using the same role, it’s possible to assign different privileges to different spaces. After you’ve added privileges, click **Add {{kib}} privilege**. If you’ve already added privileges for either **All Spaces** or an individual space, you will not be able to select these in the **Spaces** selection control.

Additionally, if you’ve already assigned privileges at **All Spaces**, you are only able to assign additional privileges to individual spaces. Similar to the behavior of multiple roles granting the union of all privileges, {{kib}} privileges are also a union. If you’ve already granted the user the **All** privilege at **All Spaces**, you’re not able to restrict the role to only the **Read** privilege at an individual space.


## Privilege summary [_privilege_summary]

To view a summary of the privileges granted, click **View privilege summary**.

## Example 1: Grant all access to Dashboard at an individual space [_example_1_grant_all_access_to_dashboard_at_an_individual_space]

1. Click **Add {{kib}} privilege**.
2. For **Spaces**, select an individual space.
3. For **Privilege**, leave the default selection of **Custom**.
4. For the Dashboard feature, select **All**
5. Click **Add {{kib}} privilege**.

<br>
:::{image} /deploy-manage/images/kibana-privilege-example-1.png
:alt: Privilege example 1
:screenshot:
:width: 650px
:::


## Example 2: Grant all access to one space and read access to another [_example_2_grant_all_access_to_one_space_and_read_access_to_another]

1. Click **Add {{kib}} privilege**.
2. For **Spaces**, select the first space.
3. For **Privilege**, select **All**.
4. Click **Add {{kib}} privilege**.
5. For **Spaces**, select the second space.
6. For **Privilege**, select **Read**.
7. Click **Add {{kib}} privilege**.

<br>
:::{image} /deploy-manage/images/kibana-privilege-example-2.png
:alt: Privilege example 2
:screenshot:
:::


## Example 3: Grant read access to all spaces and write access to an individual space [_example_3_grant_read_access_to_all_spaces_and_write_access_to_an_individual_space]

1. Click **Add {{kib}} privilege**.
2. For **Spaces**, select **All Spaces**.
3. For **Privilege**, select **Read**.
4. Click **Add {{kib}} privilege**.
5. For **Spaces**, select the individual space.
6. For **Privilege**, select **All**.
7. Click **Add {{kib}} privilege**.

<br>
:::{image} /deploy-manage/images/kibana-privilege-example-3.png
:alt: Privilege example 3
:screenshot:
:::
