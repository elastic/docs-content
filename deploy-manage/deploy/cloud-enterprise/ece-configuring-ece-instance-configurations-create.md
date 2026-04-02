---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configuring-ece-instance-configurations-create.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Create instance configurations [ece-configuring-ece-instance-configurations-create]

If you plan to [create your own templates](ece-configuring-ece-create-templates.md) and the [default instance configurations](./ece-configuring-ece-instance-configurations-default.md) that ship with ECE don’t quite suit your purpose, it’s generally easier and safer to create your own custom instance configurations first. Instance configurations match components of the {{stack}} to allocators and tailor how memory and storage resources get sized relative to each other, and what sizes are available.


## Before you begin [ece_before_you_begin_2] 

Before you start creating your own instance configurations, you should have [tagged your allocators](ece-configuring-ece-tag-allocators.md) to tell ECE what kind of hardware you have available for {{stack}} deployments. If you do not tag your allocators, templates that use these instance configurations will deploy wherever there is space rather than on specific allocators.


## Create an instance configuration in the UI [ece_create_an_instance_configuration_in_the_ui] 

1. [Log into the Cloud UI](log-into-cloud-ui.md).
2. From the **Platform** menu, select **Templates**.
3. Open the **Instance configurations** tab and select **Create instance configuration**.
4. In the **Input** section, construct a query that filters on specific allocator tags.

    ::::{tip} 
    An *outer clause* ANDs or ORs your main filtering criteria. You use outer clauses to find the allocators that you tagged earlier. An *inner clause* modifies an outer clause and let’s you refine your filtering criteria further. If you are unsure how the process works, try searching on some of the allocator tags that you added and check how the query results change.
    ::::


    1. Select **And** or **Or** to add a first outer clause.
    2. Enter a key-value pair in the **Key** and **Value** fields that you previously [tagged your allocators](ece-configuring-ece-tag-allocators.md) with.

        For example: If you tagged your allocators with this tag, enter `SSD` and `true` or enter whatever tag you are using for a similar purpose.

    3. Check the list of allocators that get matched by your query:

        * If you are satisfied that your query matches all the allocators where the component(s) of the {{stack}} can be deployed, move on to the next step.
        * If you need to refine your query further, continue to adjust your outer or inner clauses. If you are unsure what to do, we recommend keeping your initial query simple. You can always refine the query later on by re-editing the instance configuration.

5. Select **Instance types**.
6. Pick the products and features of the {{stack}} that can get deployed on the allocators you identified in the previous step. For products such as {{es}}, you can also select some additional options, such as the specific node types that can be deployed.

    Note that not all combinations of {{es}} node types are available. You can create either a general purpose {{es}} node that includes all three of data, master, and coordinating, or a dedicated node that includes any one of these types. Machine learning is also available as a separate instance type.

7. Select **Sizes**.
8. Adjust how memory and storage resources get sized relative to each other and set the available sizes, including the default size. Size your instance configuration so that it will use the available memory and storage on your allocators efficiently, without leaving hardware resources unused. Keep in mind that very small sizes might not provide adequate performance for some use cases.

    The size of an instance configuration also determines performance, as CPU resources get sized in lockstep. For example: A 32 GB instance configuration receives double the CPU resources of a 16 GB one.

9. Select **Name**.
10. Give your instance configuration a name and include a description that reflects its intended use.
11. Select **Save and create configuration**.


## Create an instance configuration through the RESTful API [ece_create_an_instance_configuration_through_the_restful_api] 

1. Obtain the existing instance configurations to get some examples of what the required JSON looks like. You can take the JSON for one of the existing configurations and modify it to create a new instance configuration, similar to what gets shown in the next step.

    ```sh
    curl -k -X GET -H "Authorization: ApiKey $ECE_API_KEY" https://$COORDINATOR_HOST:12443/api/v1/platform/configuration/instances
    ```

2. Post the JSON for your new instance configuration.

    The following examples creates an instance configuration for machine learning with size increments that start at the recommended minimum of 16 GB of memory. To make sure that machine learning nodes get deployed only on the right allocators, this instance configuration also filters for [allocator tags from our earlier example](ece-configuring-ece-tag-allocators.md) to match only allocators with high CPU resources and SSD storage.

    ```sh
    curl -k -X POST -H "Authorization: ApiKey $ECE_API_KEY" https://$COORDINATOR_HOST:12443/api/v1/platform/configuration/instances -H 'content-type: application/json' -d '{
     "name": "Machine Learning Only",
      "description": "Custom machine learning instance configuration",
      "storage_multiplier": 32.0,
      "discrete_sizes": {
        "sizes": [16384, 32768, 65536],
        "default_size": 16384,
        "resource": "memory"
      },
      "allocator_filter": {
        "bool": {
          "must": [{
            "bool": {
              "must": [{
                "nested": {
                  "query": {
                    "bool": {
                      "must": [{
                        "term": {
                          "metadata.key": {
                            "value": "SSD"
                          }
                        }
                      }, {
                        "term": {
                          "metadata.value.keyword": {
                            "value": "true"
                          }
                        }
                      }]
                    }
                  },
                  "path": "metadata"
                }
              }]
            }
          }, {
            "bool": {
              "must": [{
                "nested": {
                  "query": {
                    "bool": {
                      "must": [{
                        "term": {
                          "metadata.key": {
                            "value": "highCPU"
                          }
                        }
                      }, {
                        "term": {
                          "metadata.value.keyword": {
                            "value": "true"
                          }
                        }
                      }]
                    }
                  },
                  "path": "metadata"
                }
              }]
            }
          }]
        }
      },
      "node_types": ["ml"], <1>
      "instance_type": "elasticsearch"
    }'
    ```

    1. Note, that not all combinations of {{es}} node types are allowed here. You can create either a general purpose {{es}} node that includes all three of `data`, `master`, and `ingest`, or a dedicated node, that includes any one of these types or `ml`.


    After you have created your new instance configuration, you can use it when you [create new deployment templates](ece-configuring-ece-create-templates.md) or when you edit existing ones.


