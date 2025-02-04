# Manage your Kibana instance [ece-manage-kibana]

Kibana is an open source analytics and visualization platform designed to work with Elasticsearch, that makes it easy to perform advanced data analysis and to visualize your data in a variety of charts, tables, and maps. Its simple, browser-based interface enables you to quickly create and share dynamic dashboards that display changes to Elasticsearch queries in real time.

Most deployment templates include a Kibana instance, but if it wasn’t part of the initial deployment you can go to the **Kibana** page and **Enable** Kibana.

The new Kibana instance takes a few moments to provision. After provisioning Kibana is complete, you can use the endpoint URL to access Kibana.

::::{tip} 
You can log into Kibana as the `elastic` superuser. The password was provided when you created your deployment or can be [reset](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md). On AWS and not able to access Kibana? [Check if you need to update your endpoint URL first](../../../troubleshoot/deployments/cloud-enterprise/common-issues.md#ece-aws-private-ip).
::::


From the deployment **Kibana** page you can also:

* Terminate your Kibana instance, which stops it. The information is stored in your Elasticsearch cluster, so stopping and restarting should not risk your Kibana information.
* Restart it after stopping.
* Upgrade your Kibana instance version if it is out of sync with your Elasticsearch cluster.
* Delete to fully remove the instance, wipe it from the disk, and stop charges.

