# Access Kibana [ech-access-kibana]

Kibana is an open source analytics and visualization platform designed to search, view, and interact with data stored in Elasticsearch indices. The use of Kibana is included with your subscription.

For new Elasticsearch clusters, we automatically create a Kibana instance for you.

To access Kibana:

1. Log in to the [Elasticsearch Add-On for Heroku console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Deployments** page, select your deployment.

    Narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. Under **Applications**, select the Kibana **Launch** link and wait for Kibana to open.

    ::::{note} 
    Both ports 443 and 9243 can be used to access Kibana. SSO only works with 9243 on older deployments, where you will see an option in the Cloud UI to migrate the default to port 443. In addition, any version upgrade will automatically migrate the default port to 443.
    ::::

4. Log into Kibana. Single sign-on (SSO) is enabled between your Cloud account and the Kibana instance. If you’re logged in already, then Kibana opens without requiring you to log in again. However, if your token has expired, choose from one of these methods to log in:

    * Select **Login with Cloud**. You’ll need to log in with your Cloud account credentials and then you’ll be redirected to Kibana.
    * Log in with the `elastic` superuser. The password was provided when you created your cluster or [can be reset](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md).
    * Log in with any users you created in Kibana already.


In production systems, you might need to control what Elasticsearch data users can access through Kibana, so you need create credentials that can be used to access the necessary Elasticsearch resources. This means granting read access to the necessary indexes, as well as access to update the `.kibana` index.

::::{tip} 
If your cluster didn’t include a Kibana instance initially, there might not be a Kibana endpoint URL shown, yet. To gain access, all you need to do is [enable Kibana first](../../../deploy-manage/deploy/elastic-cloud/access-kibana.md).
::::


