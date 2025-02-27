---
applies_to:
  deployment:
    ece: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-change-roles.html
---

# Assign roles to hosts [ece-change-roles]

Assigning roles might be required after you [install Elastic Cloud Enterprise on hosts](install.md) to make sure the new hosts can be used for their intended purpose and to remove roles from the initial host to implement a recommended ECE installation. Similarly, if you need more processing capacity for Elasticsearch nodes in your deployment, change the role of a new runner to `allocator` to add its capacity to your installation.

These steps describe how to assign roles from the Cloud UI. For automation purposes, assigning roles with a [token you generate](generate-roles-tokens.md) is preferred.

Each Elastic Cloud Enterprise runner can take on several roles:

`allocator`
:   Allocates the available computing resources to Elasticsearch nodes or Kibana instances. In larger installations, a majority of the machines will be allocators.

`coordinator`
:   Serves as a distributed coordination system and resource scheduler.

`proxy`
:   Manages communication between a user and an Elasticsearch or Kibana instance.

`director`
:   Manages the ZooKeeper datastore. This role is typically shared with the coordinator role. In production deployments it can be separated from a coordinator.

::::{important} 
Once the `director` role is assigned to a runner, the Zookeeper service starts on that host. The Zookeeper service continues even after the  director role is removed from the runner. Therefore, if you remove the `director` role from any host that has ever had it, we highly recommend also [deleting the runner](../../maintenance/ece/delete-ece-hosts.md) and re-installing it.
::::


Each role is associated with a set of Docker containers that provide the specific functionality.

There are some additional roles shown in the Cloud UI, such as the [beats-runner](asciidocalypse://docs/docs-content/docs/reference/glossary/index.md#glossary-beats-runner) and [services-forwarder](asciidocalypse://docs/docs-content/docs/reference/glossary/index.md#glossary-services-forwarder) roles, that are required by Elastic Cloud Enterprise and that you cannot modify.

To assign roles to hosts:

1. [Log into the Cloud UI](log-into-cloud-ui.md).
2. From the **Platform** menu, select **Hosts**.

    The roles for each host are shown.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. To update the roles, select the host IP address and then choose **Manage roles** from the **Manage host** menu.
4. Select the role assignments for the host and choose **Update roles**.

Elastic Cloud Enterprise automatically starts managing the node in its new role and makes it available for use.

