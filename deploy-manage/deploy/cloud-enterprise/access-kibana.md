---
navigation_title: Access {{kib}}
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-access-kibana.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-manage-kibana.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Access {{kib}} on {{ece}} [ece-access-kibana]

{{kib}} is an open source analytics and visualization platform designed to search, view, and interact with data stored in {{es}} indices.

::::{tip} 
Most deployment templates include a {{kib}} instance, but if it wasn’t part of the initial deployment you can [customize your deployment components](./customize-deployment.md) to add {{kib}}.
::::

To access {{kib}}:

1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. Under **Applications**, select the {{kib}} **Open** link and wait for {{kib}} to open.

    ::::{note} 
    The URL provided to access {{kib}} is based on the [endpoint URL](/deploy-manage/deploy/cloud-enterprise/change-endpoint-urls.md) configured in the ECE **Settings** UI. This URL should resolve to your [external load balancer](/deploy-manage/deploy/cloud-enterprise/ece-load-balancers.md), which forwards the traffic to ECE proxies on port `9243`.

    If your load balancer is configured to accept traffic on both ports `9243` and `443`, you can use either port when connecting to {{kib}}. However, [built-in SSO](/deploy-manage/users-roles/cloud-enterprise-orchestrator/configure-sso-for-deployments.md) will only work with the URL configured in ECE **Settings** UI.
    ::::

4. Log into {{kib}}. Single sign-on (SSO) is enabled between your {{ece}} account and the {{kib}} instance. If you’re logged in already, then {{kib}} opens without requiring you to log in again. However, if your token has expired, choose from one of these methods to log in:

    * Select **Login with Cloud**. You’ll need to log in with an [ECE account](/deploy-manage/users-roles/cloud-enterprise-orchestrator/manage-users-roles.md) credentials and then you’ll be redirected to {{kib}}.
    * Log in with the `elastic` superuser. The password was provided when you created your cluster and [can be reset](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md).
    * Log in with [any users you created in {{kib}} already](/deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.md).

    ::::{tip}
    On AWS and not able to access {{kib}}? [Check if you need to update your endpoint URL first](../../../troubleshoot/deployments/cloud-enterprise/common-issues.md#ece-aws-private-ip).
    ::::

In production systems, you might need to control what {{es}} data users can access through {{kib}}, so you need create credentials that can be used to access the necessary {{es}} resources. This means granting read access to the necessary indexes, as well as access to update the `.kibana` index. Refer to [](/deploy-manage/users-roles/cluster-or-deployment-auth.md) for more information.

