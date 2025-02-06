---
applies:
  stack: all
  serverless: all
mapped_urls:
  - https://www.elastic.co/guide/en/kibana/current/xpack-spaces.html
  - https://www.elastic.co/guide/en/serverless/current/spaces.html
---

# Manage spaces [xpack-spaces]

% What needs to be done: Refine

% GitHub issue: https://github.com/elastic/docs-projects/issues/348

% Scope notes: Create a new landing page including the content that is relevant for both serverless and stateful Highlight the differences in subheadings for serverless and stateful Link to solution topics on spaces

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/kibana/kibana/xpack-spaces.md
% - [ ] ./raw-migrated-files/docs-content/serverless/spaces.md

% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):

$$$spaces-control-feature-visibility$$$

$$$spaces-control-user-access$$$

$$$spaces-managing$$$

**Spaces** let you organize your content and users according to your needs.

- Each space has its own saved objects. 
- Users can only access the spaces that they have been granted access to. This access is based on user roles, and a given role can have different permissions per space.
- Each space has its own navigation **[Non-serverless deployments only]**

{{kib}} creates a default space for you. When you create more spaces, users are asked to choose a space when they log in, and can change their current space at any time from the top menu.

:::{image} ../images/kibana-change-space.png
:alt: Change current space menu
:class: screenshot
:::

To go to **Spaces**, find **Stack Management** in the navigation menu or use the [global search bar](/get-started/the-stack.md#kibana-navigation-search).


## Required permissions [_required_privileges_3]

* **Serverless projects:** `Admin` or equivalent 
* **Non-serverless deployments:** `kibana_admin` or equivalent


## Create a space [spaces-managing]

The maximum number of spaces that you can have differs by deployment type: 

* **Serverless:** Maximum of 100 spaces.
* **Non-serverless deployments:** Controlled by the [`xpack.spaces.maxSpaces`](https://www.elastic.co/guide/en/kibana/current/spaces-settings-kb.html) setting. Default is 1000.

To create a space: 

::::{tab-set}
:group: stack-serverless

:::{tab-item} Serverless projects
:sync: serverless

1. Click **Create space** or select the space you want to edit.
2. Provide:

    * A meaningful name and description for the space.
    * A URL identifier. The URL identifier is a short text string that becomes part of the {{kib}} URL. {{kib}} suggests a URL identifier based on the name of your space, but you can customize the identifier to your liking. You cannot change the space identifier later.

3. Customize the avatar of the space to your liking.
4. Save the space.
:::

:::{tab-item} Non-serverless deployments
:sync: stack

1. Select **Create space** and provide a name, description, and URL identifier.
   The URL identifier is a short text string that becomes part of the {{kib}} URL when you are inside that space. {{kib}} suggests a URL identifier based on the name of your space, but you can customize the identifier to your liking. You cannot change the space identifier once you create the space.

2. Select a **Solution view**. This setting controls the navigation that all users of the space will get:
   * **Search**: A light navigation menu focused on analytics and Search use cases. Features specific to Observability and Security are hidden.
   * **Observability**: A light navigation menu focused on analytics and Observability use cases. Features specific to Search and Security are hidden.
   * **Security**: A light navigation menu focused on analytics and Security use cases. Features specific to Observability and Search are hidden.
   * **Classic**: All features from all solutions are visible by default using the classic, multilayered navigation menus. You can customize which features are visible individually.

3. If you selected the **Classic** solution view, you can customize the **Feature visibility** as you need it to be for that space.

   % This is hacking since proper admonition blocks are currently breaking my tabs
   > **Note:** Even when disabled in this menu, some Management features can remain visible to some users depending on their privileges. Additionally, controlling feature visibility is not a security feature. To secure access to specific features on a per-user basis, you must configure [{{kib}} Security](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md).

4. Customize the avatar of the space to your liking.
5. Save your new space by selecting **Create space**.
:::

::::

You can edit all of the space settings you just defined at any time, except for the URL identifier.

Elastic also allows you to manage spaces using APIs: 

* **Serverless projects:** [Spaces API](https://www.elastic.co/docs/api/doc/serverless/operation/operation-get-spaces-space)
* **Non-serverless deployments:** [Spaces API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-spaces-copy-saved-objects)


## Define access to a space [spaces-control-user-access]

**Serverless project types:** [![Elasticsearch](../images/serverless-es-badge.svg "")](/solutions/search.md) [![Security](../images/serverless-sec-badge.svg "")](/solutions/security/elastic-security-serverless.md)

Users can access spaces based on the roles that they have.

* Certain reserved roles can view and access all spaces by default. You can’t prevent those roles from accessing a space. Instead, you can grant different roles to your users.
* When creating or editing a role, you can define which existing spaces that role can access, and with which permissions. Role management differs between non-serverless deployments and serverless projects.
  - For non-Serverless deployments, check [Creating or editing a role](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md).
  - For Serverless projects, check [Custom roles](/deploy-manage/users-roles/cloud-organization/user-roles.md).


If you're managing a non-serverless deployment, then you can also assign roles and define permissions for a space from the **Permissions** tab of the space settings. 

When a role is assigned to *All Spaces*, you can’t remove its access from the space settings. You must instead edit the role to give it more granular access to individual spaces.



## Delete a space [_delete_a_space]

Deleting a space permanently removes the space and all of its contents. Find the space on the **Spaces** overview page and click the trash icon in the Actions column. You can’t delete the default space, but you can customize it to your liking.


## Move saved objects between spaces [spaces-moving-objects]

To move saved objects between spaces, you can [copy objects](/explore-analyze/find-and-organize/saved-objects.md#managing-saved-objects-copy-to-space), or [export and import objects](/explore-analyze/find-and-organize/saved-objects.md#managing-saved-objects-export-objects).


## Configure a space-level landing page [spaces-default-route]

You can create a custom experience for users by configuring the {{kib}} landing page on a per-space basis. The landing page can route users to a specific dashboard, application, or saved object as they enter each space.

To configure the landing page, use the default route setting in [Stack Management > {{kib}} > Advanced settings](https://www.elastic.co/guide/en/kibana/current/advanced-options.html#kibana-general-settings). For example, you might set the default route to `/app/dashboards`.

:::{image} ../images/kibana-spaces-configure-landing-page.png
:alt: Configure space-level landing page
:class: screenshot
:::