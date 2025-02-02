---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-installing-additional.html
---

# Install ECE on additional hosts [ece-installing-additional]

You can install Elastic Cloud Enterprise on additional hosts if you want:

* More processing capacity for Elasticsearch nodes in your deployment. You can add a host by installing Elastic Cloud Enterprise on it and then [assign the allocator role](assign-roles-to-hosts.md) in the Cloud UI.
* To [create a deployment](create-deployment.md) that is fault-tolerant, with enough resources available to support multiple availability zones.

To install Elastic Cloud Enterprise on additional hosts:

1. Download and run the installation script on each additional host. Include the `--coordinator-host HOST_IP` and `--roles-token 'TOKEN'` parameters provided to you when you installed on the first host, otherwise the new host will be rejected. As well, `VERSION_NAME` must match your current ECE installation version for the process to succeed.

    ```
    bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install
      --coordinator-host HOST_IP
      --roles-token 'TOKEN'
      --cloud-enterprise-version VERSION_NAME
    ```
    If you are creating a larger Elastic Cloud Enterprise installation:

    * Make your installation [fault tolerant or highly available](ece-ha.md) by determining the failure domain for each host and using the `--availability-zone ZONE_NAME` parameter to specify the name of an [availability zone](ece-ha.md). For production systems, hosts should go into three different availability zones. For example, including the parameter `--availability-zone ece-zone-1c` when you install on additional hosts will assign each host to availability zone `ece-zone-1c`.
    * To simplify the steps for assigning roles so that you do not have to change the roles in the Cloud UI later on, include the `--roles` parameter. For example, to bring up additional allocators to scale out your installation, specify the `--roles "allocator"` parameter. You do need to [generate a roles token](generate-roles-tokens.md) that has the right permissions for this to work; the token generated during the installation on the first host will not suffice.


After installation completes, additional hosts come online with some roles assigned to them already. If you did not specify additional roles with the `--roles` parameter, you can [assign new roles to nodes](assign-roles-to-hosts.md) in the Cloud UI later.

For automation purposes, you can set up a DNS hostname for the coordinator host. Setting up a round robin CNAME should be enough to ensure that the value does not need to change in automation scripts. Any one coordinator can be used, including the initial coordinator (the first host you installed Elastic Cloud Enterprise on).

