---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configuring-ece-tag-allocators.html
---

# Tag your allocators [ece-configuring-ece-tag-allocators]

You tag allocators to indicate what kind of hardware you have available. These tags matter, because they enable instance configurations to filter on allocators where components of the Elastic Stack should get deployed. Without tags, instance configurations will allow Elastic Stack components to get deployed wherever there is space on allocators. With tags, instance configurations can filter out those allocators that are best suited to deploy specific components of the Elastic Stack and make sure they get deployed there.

Allocator tags are a simple way of characterizing the hardware resources that you have in your ECE installation, such as:

* CPU (compute)
* Memory
* Storage
* I/O

You should tag your allocators under the following circumstances:

* After you upgrade to or install Elastic Cloud Enterprise 2.0 or later, to characterize what kind of hardware you have available in your installation.
* Before you create your own instance configurations and your own deployment templates, to indicate what hardware resources you can work with.
* After you add new allocators to your installation, to indicate what kind of hardware resources they provide.

::::{tip}
You can also delete tags, if you have no more use for them. Keep in mind that removing tags from allocators can in turn affect what allocators get matched. Removing a tag might prompt ECE to move instances of the Elastic Stack to other allocators.
::::



## Before You Begin [ece_before_you_begin]

Your tags should characterize what kind of hardware you have available. As you start developing your own tags, keep in mind that simpler is often better and that the tags you use will likely evolve over time. The main purpose of tagging is to go from  *this is an allocator*, which doesn’t tell you anything about the allocator’s hardware resources, to *this is an allocator with better CPU resources* or *this allocator provides a large amount of spindle-based storage*.

$$$allocator-sample-tags$$$Tags are simple key-value pairs. A small sampling of tags that you could use include:

`SSD: true`, `SSD: false`, `highstorage: true`
:   Indicates if you have fast SSD storage for incoming data (`SSD: true`) or spindle-based storage that can store larger volumes of less frequently queried data (`SSD: false` or `highstorage: true`).

`highCPU: true`
:   Indicates allocators that can run CPU-intensive workloads faster than others.

`instanceFamily: i3`, `instanceFamily: m5`
:   Indicates the host type, used extensively on {{ech}} to identify hosts with specific hardware characteristics. If you run your own hardware on-premise and have standardized on several specific host configurations, you could use similar tags. If you are deploying ECE on another cloud platform, you could use the instance type or machine type names from your provider.

Avoid tags that describe a particular use case or an Elastic Stack component you plan to run on these allocators. Examples of tags to avoid include `elasticsearch: false` or `kibana: true`. You should define the intended use at the level of instance configurations instead and tag your allocators only to describe hardware characteristics.

::::{tip}
If you have an allocator that meets several criteria, such as an allocator with multi-purpose hardware, consider assigning it a single tag that identifies its multipurpose view, such as the `instanceFamily: i3` example mentioned earlier. While it is not wrong to assign multiple tags to an allocator, filtering on the allocator when you create or edit instance configurations will be simpler with a single tag.
::::



## Tag allocators in the Cloud UI [ece_tag_allocators_in_the_cloud_ui]

1. [Log into the Cloud UI](log-into-cloud-ui.md).
2. From the **Platform** menu, select **Hosts**.
3. Select one of the hosts, and under the **Allocator** tab locate the **Allocator tags** section.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

4. Enter values into the **Key** and **Value** fields, and then select **Add tag**. For example: You could add `SSD: true` and `highCPU: true` tags from our [example tags](#allocator-sample-tags) if your allocator meets these criteria.

    :::{image} ../../../images/cloud-enterprise-ece-tagging-ui.png
    :alt: Adding key-value pairs as an allocator tags
    :::

5. Repeat the previous step until you have added all of the tags that you want to use to characterize the hardware of this allocator.
6. Repeat the previous steps for your other allocators until you have tagged all of them.


## Tag an allocator through the RESTful API [ece_tag_an_allocator_through_the_restful_api]

1. Get a list of the allocators in your ECE installation:

    ```sh
    curl -k -X GET -H "Authorization: ApiKey $ECE_API_KEY" https://COORDINATOR_HOST:12443/api/v1/platform/infrastructure/allocators
    ```

    ::::{note}
    The user must have sufficient privileges, such as the `admin` user.
    ::::

2. $$$check-allocator-tags$$$Check what tags have already been assigned to your allocators. In a new or newly upgraded ECE installation, this command returns `[]`, which means that you have not assigned any tags, yet.

    ```sh
    curl -k -X GET -H "Authorization: ApiKey $ECE_API_KEY" https://COORDINATOR_HOST:12443/api/v1/platform/infrastructure/allocators/ALLOCATOR_ID/metadata
    ```

    `ALLOCATOR_ID`
    :   The value of the `allocator_id` field for one of your allocators as returned by the `/api/v1/platform/infrastructure/allocators` API endpoint.

        ::::{tip}
        The examples in this section all use HTTPS over port 12443 and run against a host that holds the coordinator role. Using HTTPS requires that you have [a TLS certificate already installed](../../security/secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md). For testing purposes only, you can specify the `-k` option to turn off certificate verification, as shown in our examples, or use HTTP over port 12400 until you get your TLS certificate sorted out.
        ::::

3. Tag an allocator by assigning it the tags that you might need.

    * Example: To assign a single `highCPU: true` tag to an allocator:

        ```sh
        curl -k -X PUT -H "Authorization: ApiKey $ECE_API_KEY" https://COORDINATOR_HOST:12443/api/v1/platform/infrastructure/allocators/ALLOCATOR_ID/metadata/highCPU  -H 'content-type: application/json' -d '{ "value": "true" }'
        [{
          "key": "highCPU",
          "value": "true"
        }]
        ```

        After the API call completes successfully, ECE returns JSON output to show that the operation was successful.

    * Example: To assign multiple tags to an allocator with a single command:

        ```sh
        curl -k -X PUT -H "Authorization: ApiKey $ECE_API_KEY" https://COORDINATOR_HOST:12443/api/v1/platform/infrastructure/allocators/ALLOCATOR_ID/metadata -H 'content-type: application/json' -d '
        {
          "items": [
            {
              "key": "highCPU",
              "value": "true"
            },
            {
              "key": "SSD",
              "value": "true"
            }
          ]
        }'
        ```

        ::::{tip}
        When you assign multiple tags to an allocator as shown, any tags you assigned previously get replaced. That is, existing tags are not preserved and they do not get merged with new tags. If in doubt, <<[check-allocator-tag,check which tags have already been assigned>> and make sure you include those tags that you want to keep along with new tags.
        ::::

4. Repeat the previous step for your other allocators until you have tagged all of them.

