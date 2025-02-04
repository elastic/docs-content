---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-maintenance-mode.html
---

# Enable maintenance mode [ece-maintenance-mode]

Maintenance mode lets you perform actions on an allocator safely that might otherwise carry some risk. For example, if you want to remove the allocator role from a host, enabling maintenance mode prevents new Elasticsearch clusters and Kibana instances from being provisioned on the allocator whilst you are moving the existing nodes to another allocator or whilst you are removing the role.

To put an allocator into maintenance mode:

1. [Log into the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Allocators**.
3. Choose the allocator you want to work with and select **Enable Maintenance Mode**. Confirm the action.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.


After the allocator enters maintenance mode, no new Elasticsearch nodes or Kibana instances will be started on the allocator. Existing nodes will continue to work as expected. You can now safely perform actions like [moving nodes off the allocator](move-nodes-instances-from-allocators.md).

If you want to make the allocator fully active again, select **Disable Maintenance Mode**. Confirm the action.

::::{tip} 
If you need the existing instances to stop routing requests you can [stop routing requests](deployments-maintenance.md) to disable incoming requests to particular instances. You can also massively disable all allocator instances routing with the [allocator-toggle-routing-requests.sh](https://download.elastic.co/cloud/allocator-toggle-routing-requests.sh) script. The script runs with the following parameters in the form environment variables:

* `API_URL` Url of the administration API.
* `AUTH_HEADER` Curl format string representing the authentication header.
* `ALLOCATOR_ID` Action target allocator id.
* `ENABLE_TRAFFIC` Wether traffic to the selected allocator instances should be enabled (`true`) or disabled (`false`).

This is an example of script execution to disable routing on all instances running on a given allocator: In this example the script disables routing on all instances running on a given allocator:

```bash
AUTH_HEADER="Authorization: ApiKey $(cat ~/api.key)" API_URL="https://adminconsole:12443" ALLOCATOR_ID="192.168.44.10" ENABLE_TRAFFIC=false ./allocator-toggle-routing-requests.sh
```

The same script can be used to enable traffic again:

```bash
AUTH_HEADER="Authorization: ApiKey $(cat ~/api.key)" API_URL="https://adminconsole:12443" ALLOCATOR_ID="192.168.44.10" ENABLE_TRAFFIC=true ./allocator-toggle-routing-requests.sh
```

::::


