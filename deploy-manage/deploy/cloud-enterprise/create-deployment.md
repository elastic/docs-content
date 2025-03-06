---
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-create-deployment.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-access-kibana.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-manage-kibana.html
---

# Create a deployment

An ECE deployment is a fully managed Elastic Stack environment running on {{ece}}. It includes {{es}}, {{kib}}, and optional features like Machine Learning, or an Integrations (Fleet & APM) Server.

Each deployment is based on a [deployment template](./deployment-templates.md), which defines its resources, default topology, scaling policies, and available features. Deployments can be customized based on workload requirements, including autoscaling, snapshot settings, and security configurations.

In this section, you'll learn how to:

* [Create a deployment](#ece-create-deployment)
* [Access Kibana](#ece-access-kibana)

## Create a deployment [ece-create-deployment]

To create a deployment in ECE:

1. From the Cloud UI, select **Create deployment**.

    :::{image} ../../../images/cloud-enterprise-ece-create-deployment.png
    :alt: Create a deployment
    :::

    On the **Create deployment** page, you can edit the basic settings or adjust advanced configurations. **Advanced settings** allow you to modify deployment parameters defined by the selected template, such as autoscaling, storage, memory, data tiers, and additional {{stack}} components.

2. Set a name for your deployment.

3. Select a deployment template.

::::{tip}
* Refer to [](./deployment-templates.md) for more information about deployment templates, including descriptions of the default system templates.
* If the system templates do not meet your requirements, you can [modify them](./ece-configuring-ece-configure-system-templates.md) or [create your own custom templates](../../../deploy-manage/deploy/cloud-enterprise/ece-configuring-ece-create-templates.md).
::::

4. Choose your {{stack}} version. To manage available versions, refer to [](./manage-elastic-stack-versions.md).

5. Optionally, [use snapshots](../../tools/snapshot-and-restore/cloud-enterprise.md) to back up your data or [restore data from another deployment](../../tools/snapshot-and-restore/ece-restore-across-clusters.md).

::::{tip}
    Restoring a snapshot can help with major version upgrades by creating a separate, non-production deployment where you can test, for example. Or, make life easier for your developers by providing them with a development environment that is populated with real data.
::::

6. Select **Advanced settings**, to configure your deployment for [autoscaling](../../autoscaling/ece-autoscaling.md), storage, memory, and data tiers. Check [Customize your deployment](../../../deploy-manage/deploy/cloud-enterprise/customize-deployment.md) for more details.

7. Select **Create deployment**. It takes a few minutes before your deployment gets created.

   While waiting, you are prompted to save the admin credentials for your deployment which provides you with superuser access to Elasticsearch. Write down the password for the `elastic` user and keep it somewhere safe. These credentials also help you [add data using Kibana](../../../manage-data/ingest.md). If you need to refresh these credentials, you can [reset the password](../../../deploy-manage/users-roles/cluster-or-deployment-auth/manage-elastic-user-cloud.md).

8. Once the deployment is ready, select **Continue** to open the deployment’s main page.

After a deployment is spun up, you can scale the size and add other features; however, the instance configuration and computing ratios cannot be changed. If you need to change an existing deployment to another template, we recommend [migrating your data](../../../manage-data/migrate.md).

## Access Kibana [ece-access-kibana]

Kibana is an open source analytics and visualization platform designed to search, view, and interact with data stored in Elasticsearch indices.

::::{tip} 
Most deployment templates include a Kibana instance, but if it wasn’t part of the initial deployment you can [](./customize-deployment.md) and add {{kib}}.
::::

To access Kibana:

1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. Under **Applications**, select the Kibana **Launch** link and wait for Kibana to open.

    ::::{note} 
    Both ports 443 and 9243 can be used to access Kibana. SSO only works with 9243 on older deployments, where you will see an option in the Cloud UI to migrate the default to port 443. In addition, any version upgrade will automatically migrate the default port to 443.
    ::::

4. Log into Kibana. Single sign-on (SSO) is enabled between your Cloud account and the Kibana instance. If you’re logged in already, then Kibana opens without requiring you to log in again. However, if your token has expired, choose from one of these methods to log in:

    * Select **Login with Cloud**. You’ll need to log in with your Cloud account credentials and then you’ll be redirected to Kibana.
    * Log in with the `elastic` superuser. The password was provided when you created your cluster or [can be reset](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md).
    * Log in with any users you created in Kibana already.

    ::::{tip} 
    On AWS and not able to access Kibana? [Check if you need to update your endpoint URL first](../../../troubleshoot/deployments/cloud-enterprise/common-issues.md#ece-aws-private-ip).
    ::::

In production systems, you might need to control what Elasticsearch data users can access through Kibana, so you need create credentials that can be used to access the necessary Elasticsearch resources. This means granting read access to the necessary indexes, as well as access to update the `.kibana` index.

## Next steps

 Once you have created your deployment, consider the following activities:

* Connect your applications to your {{es}} cluster to start sending data.
* [Add data](../../../manage-data/ingest.md)
* Configure [users and roles](../../users-roles.md)
* TBD
From "here", you can start ingesting data or simply [try a sample data](../../../explore-analyze/index.md#gs-get-data-into-kibana) set to get started.

Check all other actions from [](./working-with-deployments.md).
