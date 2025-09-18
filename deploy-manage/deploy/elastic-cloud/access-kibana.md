---
navigation_title: Access {{kib}}
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-access-kibana.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-access-kibana.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-enable-kibana2.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Access {{kib}} on {{ech}} [ec-access-kibana]

% What needs to be done: Lift-and-shift

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/cloud/cloud/ec-access-kibana.md
% - [ ] ./raw-migrated-files/cloud/cloud-heroku/ech-access-kibana.md
% - [ ] ./raw-migrated-files/cloud/cloud-heroku/ech-enable-kibana2.md

% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):


$$$ec-enable-kibana2$$$


{{kib}} is an open source analytics and visualization platform designed to search, view, and interact with data stored in {{es}} indices. The use of {{kib}} is included with your subscription.

For new {{es}} clusters, we automatically create a {{kib}} instance for you.

To access {{kib}}:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Hosted deployments** page, select your deployment.

    On the **Hosted deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. Under **Applications**, select the {{kib}} **Launch** link and wait for {{kib}} to open.

    ::::{note}
    Both ports 443 and 9243 can be used to access {{kib}}. SSO only works with 9243 on older deployments, where you will see an option in the Cloud UI to migrate the default to port 443. In addition, any version upgrade will automatically migrate the default port to 443.
    ::::

4. Log into {{kib}}. Single sign-on (SSO) is enabled between your Cloud account and the {{kib}} instance. If you’re logged in already, then {{kib}} opens without requiring you to log in again. However, if your token has expired, choose from one of these methods to log in:

    * Select **Login with Cloud**. You’ll need to log in with your Cloud account credentials and then you’ll be redirected to {{kib}}.
    * Log in with the `elastic` superuser. The password was provided when you created your cluster or [can be reset](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md).
    * Log in with any users you created in {{kib}} already.


In production systems, you might need to control what {{es}} data users can access through {{kib}}, so you need create credentials that can be used to access the necessary {{es}} resources. This means granting read access to the necessary indexes, as well as access to update the `.kibana` index.