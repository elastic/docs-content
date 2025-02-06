---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/tutorial-secure-access-to-kibana.html
---

# Quickstart [tutorial-secure-access-to-kibana]

{{kib}} is home to an ever-growing suite of powerful features, which help you get the most out of your data. Your data is important, and should be protected. {{kib}} allows you to secure access to your data and control how users are able to interact with your data.

For example, some users might only need to view your stunning dashboards, while others might need to manage your fleet of Elastic agents and run machine learning jobs to detect anomalous behavior in your network.

This guide introduces you to three of {{kib}}'s security features: spaces, roles, and users. By the end of this tutorial, you will learn how to manage these entities, and how you can leverage them to secure access to both {{kib}} and your data.


## Spaces [_spaces]

Do you have multiple teams using {{kib}}? Do you want a “playground” to experiment with new visualizations or rules? If so, then [{{kib}} Spaces](../../manage-spaces.md) can help.

Think of a space as another instance of {{kib}}. A space allows you to organize your [dashboards](../../../explore-analyze/dashboards.md), [rules](../../../explore-analyze/alerts-cases/alerts.md), [machine learning jobs](../../../explore-analyze/machine-learning/machine-learning-in-kibana.md), and much more into their own categories. For example, you might have a Marketing space for your marketeers to track the results of their campaigns, and an Engineering space for your developers to [monitor application performance](https://www.elastic.co/guide/en/apm/guide/current/apm-overview.html).

The assets you create in one space are isolated from other spaces, so when you enter a space, you only see the assets that belong to that space.

Refer to the [Spaces documentation](../../manage-spaces.md) for more information.


## Roles [_roles]

Once your spaces are setup, the next step to securing access is to provision your roles. Roles are a collection of privileges that allow you to perform actions in {{kib}} and Elasticsearch. Roles are assigned to users, and to [system accounts](built-in-users.md) that power the Elastic Stack.

You can create your own roles, or use any of the [built-in roles](built-in-roles.md). Some built-in roles are intended for Elastic Stack components and should not be assigned to end users directly.

One of the more useful built-in roles is `kibana_admin`. Assigning this role to your users will grant access to all of {{kib}}'s features. This includes the ability to manage Spaces.

The built-in roles are great for getting started with the Elastic Stack, and for system administrators who do not need more restrictive access. With so many features, it’s not possible to ship more granular roles to accommodate everyone’s needs. This is where custom roles come in.

As an administrator, you have the ability to create your own roles to describe exactly the kind of access your users should have. For example, you might create a `marketing_user` role, which you then assign to all users in your marketing department. This role would grant access to all of the necessary data and features for this team to be successful, without granting them access they don’t require.


## Users [_users]

Once your roles are setup, the next step to securing access is to create your users, and assign them one or more roles. {{kib}}'s user management allows you to provision accounts for each of your users.

::::{tip}
Want Single Sign-on? {{kib}} supports a wide range of SSO implementations, including SAML, OIDC, LDAP/AD, and Kerberos. [Learn more about {{kib}}'s SSO features](user-authentication.md).
::::



## Example: Create a user with access only to dashboards [tutorial-secure-kibana-dashboards-only]

Let’s work through an example together. Consider a marketing analyst who wants to monitor the effectiveness of their campaigns. They should be able to see their team’s dashboards, but not be allowed to view or manage anything else in {{kib}}. All of the team’s dashboards are located in the Marketing space.


### Create a space [_create_a_space]

Create a Marketing space for your marketing analysts to use.

1. Go to the **Spaces** management page using the navigation menu or the [global search field](../../../get-started/the-stack.md#kibana-navigation-search).
2. Click **Create a space**.
3. Give this space a unique name. For example: `Marketing`.
4. Click **Create space**.

    If you’ve followed the example above, you should end up with a space that looks like this:

    :::{image} ../../../images/kibana-tutorial-secure-access-example-1-space.png
    :alt: Create space UI
    :class: screenshot
    :::



### Create a role [_create_a_role]

To effectively use dashboards, create a role that describes the privileges you want to grant. In this example, a marketing analyst will need:

* Access to **read** the data that powers the dashboards
* Access to **read** the dashboards within the `Marketing` space

To create the role:

1. Go to the **Roles** management page using the navigation menu or the [global search field](../../../get-started/the-stack.md#kibana-navigation-search).
2. Click **Create role**.
3. Give this role a unique name. For example: `marketing_dashboards_role`.
4. For this example, you want to store all marketing data in the `acme-marketing-*` set of indices. To grant this access, locate the **Index privileges** section and enter:

    1. `acme-marketing-*` in the **Indices** field.
    2. `read` and `view_index_metadata` in the **Privileges** field.

        ::::{tip}
        You can add multiple patterns of indices, and grant different access levels to each. Click **Add index privilege** to grant additional access.
        ::::

5. To grant access to dashboards in the `Marketing` space, locate the {{kib}} section, and click **Add {{kib}} privilege**:

    1. From the **Spaces** dropdown, select the `Marketing` space.
    2. Expand the **Analytics*** section, and select the ***Read*** privilege for ***Dashboard**.
    3. Click **Add Kibana privilege**.

6. Click **Create role**.

    If you’ve followed the example above, you should end up with a role that looks like this:

    :::{image} ../../../images/kibana-tutorial-secure-access-example-1-role.png
    :alt: Create role UI
    :class: screenshot
    :::



### Create a user [_create_a_user]

Now that you created a role, create a user account.

1. Navigate to **Stack Management**, and under **Security**, select **Users**.
2. Click **Create user**.
3. Give this user a descriptive username, and choose a secure password.
4. Assign the **marketing_dashboards_role** that you previously created to this new user.
5. Click **Create user**.

:::{image} ../../../images/kibana-tutorial-secure-access-example-1-user.png
:alt: Create user UI
:class: screenshot
:::


### Verify [_verify]

Verify that the user and role are working correctly.

1. Logout of {{kib}} if you are already logged in.
2. In the login screen, enter the username and password for the account you created.

    You’re taken into the `Marketing` space, and the main navigation shows only the **Dashboard** application.

    :::{image} ../../../images/kibana-tutorial-secure-access-example-1-test.png
    :alt: Verifying access to dashboards
    :class: screenshot
    :::



## What’s next? [_whats_next_2]

This guide is an introduction to {{kib}}'s security features. Check out these additional resources to learn more about authenticating and authorizing your users.

* View the [authentication guide](user-authentication.md) to learn more about single-sign on and other login features.
* View the [authorization guide](defining-roles.md) to learn more about authorizing access to {{kib}}'s features.

Still have questions? Ask  on our [Kibana discuss forum](https://discuss.elastic.co/c/kibana) and a fellow community member or Elastic engineer will help out.
