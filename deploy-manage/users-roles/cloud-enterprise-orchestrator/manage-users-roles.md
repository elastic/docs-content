---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configure-rbac.html
---

# Manage users and roles [ece-configure-rbac]

:::{image} ../../../images/cloud-enterprise-ece-rbac-intro.png
:alt: User groups
:::

Role-based access control (RBAC) provides a way to add multiple users and restrict their access to specific platform resources. In addition to the system `admin` and `readonly` users, you can utilize pre-built roles to control access to platform operations, deployment assets, or API calls.

Implementing RBAC in your environment benefits you in several ways:

* Streamlines the process of assigning or updating privileges for users as a group, instead of painstakingly managing individual users.
* Limits access to just what’s needed for that user’s job function, isolating company assets.
* Assists with compliance to security and data standards or laws.
* Adds multiple users by:

    * Creating [native users](native-user-authentication.md) locally.
    * Integrating with third-party authentication providers like [ActiveDirectory](active-directory.md), [LDAP](ldap.md) or [SAML](saml.md).


::::{important}
With RBAC, interacting with API endpoints now requires a [bearer token](asciidocalypse://docs/cloud/docs/reference/cloud/cloud-enterprise/ece-api-command-line.md) or [API key](../../api-keys/elastic-cloud-enterprise-api-keys.md#ece-api-keys).
::::



## Before you begin [ece_before_you_begin_8]

To prepare for RBAC, you should review the Elastic Cloud Enterprise [limitations and known issues](asciidocalypse://docs/cloud/docs/release-notes/known-issues/cloud-enterprise.md).


## Available roles and permissions [ece-user-role-permissions]

Beyond the system users, there are several pre-built roles that you can apply to additional users:

Platform admin
:   Same access as the `admin` system user.

Platform viewer
:   Same access as the `readonly` system user, which includes being able to view secret and sensitive settings.

Deployment manager
:   Can create and manage non-system deployments, specify keystore security settings, and establish cross-cluster remote relationships. They can also reset the `elastic` password.

Deployment viewer
:   Can view non-system deployments, including their activity. Can prepare the diagnostic bundle, inspect the files, and download the bundle as a ZIP file.


## Configure security deployment [ece-configure-security-deployment]

The security deployment is a system deployment that manages all of the Elastic Cloud Enterprise authentication and permissions. It is created automatically during installation.

::::{important}
We strongly recommend using three availability zones with at least 1 GB Elasticsearch nodes. You can scale up if you expect a heavy authentication workload.
::::


1. [Log into the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. Go to **Deployments** a select the **security-cluster**.
3. Configure regular snapshots of the security deployment. This is critical if you plan to create any native users.
4. Optional: [Enable monitoring](../../monitor/stack-monitoring/ece-stack-monitoring.md) on the security deployment to a dedicated monitoring deployment.

If you have authentication issues, you check out the security deployment Elasticsearch logs.


## Change the order of provider profiles [ece-provider-order]

Elastic Cloud Enterprise performs authentication checks against the configured providers, in order. When a match is found, the user search stops. The roles specified by that first profile match dictate which permissions the user is granted—​regardless of what permissions might be available in another, lower-order profile.

To change the provider order:

1. [Log into the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. Go to **Users** and then **Authentication providers**.
3. Use the carets to update the provider order.

Changing the order is a configuration change and you can’t make changes to other providers until it is complete.


## Change the user settings [ece-rbac-user-settings]

Platform admins and users can access user settings. Full name, contact email, and updating the password can be changed by either. The username cannot be changed. The platform admin can also assign roles and disable users.

* For platform admins, the user settings are editable from the **Users** page.
* For users, they can edit their profile from the **Settings** page.





