---
applies_to:
  deployment:
    ece: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-access-kibana.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-manage-kibana.html
---

# Access Kibana [ece-access-kibana]

Kibana is an open source analytics and visualization platform designed to search, view, and interact with data stored in Elasticsearch indices.

::::{tip} 
Most deployment templates include a Kibana instance, but if it wasn’t part of the initial deployment you can [customize your deployment components](./customize-deployment.md) to add {{kib}}.
::::

To access Kibana:

1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. Under **Applications**, select the Kibana **Open** link and wait for Kibana to open.

    ::::{note} 
    Both ports 443 and 9243 can be used to access Kibana. SSO only works with 9243 on older deployments, where you will see an option in the Cloud UI to migrate the default to port 443. In addition, any version upgrade will automatically migrate the default port to 443.
    ::::

4. Log into Kibana. Single sign-on (SSO) is enabled between your {{ece}} account and the Kibana instance. If you’re logged in already, then Kibana opens without requiring you to log in again. However, if your token has expired, choose from one of these methods to log in:

    * Select **Login with Cloud**. You’ll need to log in with an [ECE account](/deploy-manage/users-roles/cloud-enterprise-orchestrator/manage-users-roles.md) credentials and then you’ll be redirected to Kibana.
    * Log in with the `elastic` superuser. The password was provided when you created your cluster and [can be reset](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md).
    * Log in with [any users you created in Kibana already](/deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.md).

    ::::{tip}
    On AWS and not able to access Kibana? [Check if you need to update your endpoint URL first](../../../troubleshoot/deployments/cloud-enterprise/common-issues.md#ece-aws-private-ip).
    ::::

In production systems, you might need to control what Elasticsearch data users can access through Kibana, so you need create credentials that can be used to access the necessary Elasticsearch resources. This means granting read access to the necessary indexes, as well as access to update the `.kibana` index. Refer to [](/deploy-manage/users-roles/cluster-or-deployment-auth.md) for more information.

