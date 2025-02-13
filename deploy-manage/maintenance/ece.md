# ECE maintenance

Elastic Cloud Enterprise (ECE), being a self-managed Elastic Stack deployment platform, abstracts much of the complexity of running {{es}}, but still requires regular maintenance at both the platform and deployment levels. Maintenance activities range from managing individual deployments to performing infrastructure-level updates on ECE hosts.

## Deployment maintenance and host infrastructure maintenance [ece-deployment-host-infra-maintenance]

Deployment maintenance focuses on managing individual {{es}} and {{kib}} instances within ECE. This includes actions such as pausing instances, stopping request routing to nodes, and moving instances between allocators to optimize resource usage or prepare for maintenance. These tasks help maintain service availability and performance without affecting the underlying infrastructure.

ECE host infrastructure maintenance involves managing virtual machines that host ECE itself. This includes tasks like applying operating system patches, upgrading software, or decommissioning hosts. Infrastructure maintenance often requires more careful planning, as it can impact multiple deployments running on the affected hosts. Methods such as placing allocators into maintenance mode and redistributing workloads provide a smooth transition during maintenance operations.

This section provides guidance on best practices for both types of maintenance, helping you maintain a resilient ECE environment.

## Enabling Kibana [ece-manage-kibana]

{{kib}} is an open source analytics and visualization platform designed to work with {{es}}, that makes it easy to perform advanced data analysis and to visualize your data in a variety of charts, tables, and maps. Its simple, browser-based interface enables you to quickly create and share dynamic dashboards that display changes to {{es}} queries in real time.

Most deployment templates include a {{kib}} instance, but if it wasn’t part of the initial deployment you can go to the **{{kib}}** page and **Enable** {{kib}}.

The new {{kib}} instance takes a few moments to provision. After provisioning {{kib}} is complete, you can use the endpoint URL to access {{kib}}.

::::{tip}
You can log into Kibana as the `elastic` superuser. The password was provided when you created your deployment or can be [reset](users-roles/cluster-or-deployment-auth/built-in-users.md). On AWS and not able to access Kibana? [Check if you need to update your endpoint URL first](../troubleshoot/deployments/cloud-enterprise/common-issues.md#ece-aws-private-ip).
::::

From the deployment **{{kib}}** page you can also:

* Terminate your {{kib}} instance, which stops it. The information is stored in your {{es}} cluster, so stopping and restarting should not risk your {{kib}} information.
* Restart it after stopping.
* Upgrade your {{kib}} instance version if it is out of sync with your {{es}} cluster.
* Delete to fully remove the instance, wipe it from the disk, and stop charges.
