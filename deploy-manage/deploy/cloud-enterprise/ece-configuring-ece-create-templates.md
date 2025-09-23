---
navigation_title: Create templates
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configuring-ece-create-templates.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Create deployment templates [ece-configuring-ece-create-templates]

{{ece}} comes with some deployment templates already built in, but you can create new deployment templates to address particular use cases that you might have.

For example: You might decide to create a new deployment template, if you have a specific search use case that requires {{es}} data nodes in a specific configuration that also includes machine learning for anomaly detection. If you need to create these deployments fairly frequently, you can create a deployment template once and deploy it as many times as you like. Or, create a single template for both your test and production deployments to ensure they are exactly the same.


## Before you begin [ece_before_you_begin_3]

Before you start creating your own deployment templates, you should have: [tagged your allocators](ece-configuring-ece-tag-allocators.md) to tell ECE what kind of hardware you have available for {{stack}} deployments. If the default instance configurations don’t provide what you need, you might also need to [create your own instance configurations](ece-configuring-ece-instance-configurations-create.md) first.


## Create deployment templates in the UI [ece-configuring-ece-create-templates-ui]

1. [Log into the Cloud UI](log-into-cloud-ui.md).
2. From the **Platform** menu, select **Templates**.
3. Select **Create template**.
4. Give your template a name and include a description that reflects its intended use.
5. Select **Create template**. The **Configure instances** page opens.
6. Choose whether or not [autoscaling](/deploy-manage/autoscaling/autoscaling-in-ece-and-ech.md) is enabled by default for deployments created using the template. Autoscaling adjusts resources available to the deployment automatically as loads change over time.

    :::{image} /deploy-manage/images/cloud-enterprise-ece-create-template-autoscaling.png
    :alt: screencapture of the "Enable autoscaling by default" switch
    :::

7. Configure the initial settings for all of the data tiers and components that will be available in the template. A default is provided for every setting and you can adjust these as needed. For each data tier and component, you can:

    * Select which [instance configuration](ece-configuring-ece-instance-configurations-create.md) to assign to the template. This allows you to optimize the performance of your deployments by matching a machine type to a use case. A hot data and content tier, for example, is best suited to be allocated with an instance configuration having fast SSD storage, while warm and cold data tiers should be allocated with an instance configuration with larger storage but likely less performant, lower cost hardware.

        :::{image} /deploy-manage/images/cloud-enterprise-ece-create-template-instance-configuration.png
        :alt: screencapture of the "Initial size per zone" dropdown box
        :::

    * Adjust the default, initial amount of memory and storage. Increasing memory and storage also improves performance by increasing the CPU resources that get assigned relative to the size of the instance, meaning that a 32 GB instance gets twice as much CPU resource as a 16 GB one. These resources are just template defaults that can be adjusted further before you create actual deployments.

        :::{image} /deploy-manage/images/cloud-enterprise-ece-create-template-initial-size.png
        :alt: screencapture of the "Initial size per zone" dropdown box
        :::

    * Configure autoscaling settings for the deployment.

        :::{image} /deploy-manage/images/cloud-enterprise-ece-create-template-max-autoscaling.png
        :alt: screencapture of the "Maximum autoscaling size per zone" dropdown box
        :::

        * For data nodes, autoscaling up is supported based on the amount of available storage. You can set the default initial size of the node and the default maximum size that the node can be autoscaled up to.
        * For machine learning nodes, autoscaling is supported based on the expected memory requirements for machine learning jobs. You can set the default minimum size that the node can be scaled down to and the default maximum size that the node can be scaled up to. If autoscaling is not enabled for the deployment, the "minimum" value will instead be the default initial size of the machine learning node.

        The default values provided by the deployment template can be adjusted at any time. Check our [Autoscaling example](../../autoscaling/autoscaling-in-ece-and-ech.md#ec-autoscaling-example) for details about these settings. Nodes and components that currently support autoscaling are indicated by a `supports autoscaling` badge on the **Configure instances** page.

    * Add [fault tolerance](ece-ha.md) (high availability) by using more than one availability zone.

        :::{image} /deploy-manage/images/cloud-enterprise-ece-create-template-availability-zones.png
        :alt: screencapture of the "Availability zones" radio buttons
        :::

    * Add user settings to configure how {{es}} and other components run. Check [Editing your user settings](edit-stack-settings.md) for details about what settings are available.

        :::{image} /deploy-manage/images/cloud-enterprise-ece-create-template-user-settings.png
        :alt: screencapture of the "User settings" expandable section
        :::


    If a data tier or component is not required for your particular use case, you can simply set its initial size per zone to `0`. You can enable a tier or component anytime you need it just by scaling up the size. If autoscaling is enabled, data tiers and machine learning nodes are sized up automatically when they’re needed. For example, when you configure your first machine learning job, ML nodes are enabled by the autoscaling process. Similarly, if you choose to create a cold data phase as part of your deployment’s index lifecycle management (ILM) policy, a cold data node is enabled automatically without your needing to configure it.

8. Select **Manage indices**.
   
   On this page, you can [configure index management](ece-configure-templates-index-management.md) by assigning attributes to each of the data nodes in the deployment template. In {{kib}}, you can configure an index lifecycle management (ILM) policy, based on the node attributes, to control how data moves across the nodes in your deployment.
10. Select **Stack features**. On this page, you can manage the following options:
    
    * You can select a [snapshot repository](../../tools/snapshot-and-restore/cloud-enterprise.md) to be used by default for deployment backups.
    
    * You can choose to [enable logging and monitoring](../../monitor/stack-monitoring/ece-ech-stack-monitoring.md) by default, so that deployment logs and metrics are send to a dedicated monitoring deployment, and so that additional log types, retention options, and {{kib}} visualizations are available on all deployments created using this template.
11. Select **Extensions**.
    
    Select any {{es}} extensions that you would like to be available automatically to all deployments created using the template.
12. Select **Save and create template**.


## Create deployment templates through the RESTful API [ece_create_deployment_templates_through_the_restful_api]

1. Obtain the existing deployment templates to get some examples of what the required JSON looks like. You can take the JSON for one of the existing templates and modify it to create a new template, similar to what gets shown in the next step.

    ```sh
    curl -k -X GET -H "Authorization: ApiKey $ECE_API_KEY" https://$COORDINATOR_HOST:12443/api/v1/deployments/templates?region=ece-region
    ```

2. Post the JSON for your new deployment template.

    The following example creates a deployment template that defaults to a highly available {{es}} cluster with 4 GB per hot node, a 16 GB machine learning node, 3 dedicated master nodes of 1 GB each, a 1 GB {{kib}} instance, and a 1 GB dedicated coordinating node that is tasked with handling and coordinating all incoming requests for the cluster. {{es}} and {{kib}} use the default instance configurations, but the machine learning node is based on the custom instance configuration in our previous example.

    ```sh
    curl -k -X POST -H "Authorization: ApiKey $ECE_API_KEY" https://$COORDINATOR_HOST:12443/api/v1/deployments/templates?region=ece-region -H 'content-type: application/json' -d '{
        "name" : "Default",
        "description" : "Default deployment template for clusters",
        "deployment_template": {
          "resources": {
            "elasticsearch": [
              {
                "ref_id": "es-ref-id",
                "region": "ece-region",
                "plan": {
                  "cluster_topology": [
                    {
                      "node_type": {
                        "master": true,
                        "data": true,
                        "ingest": true
                      },
                      "zone_count": 1,
                      "instance_configuration_id": "data.default",
                      "size": {
                        "value": 4096,
                        "resource": "memory"
                      },
                      "node_roles": [
                        "master",
                        "ingest",
                        "data_hot",
                        "data_content",
                        "remote_cluster_client",
                        "transform"
                      ],
                      "id": "hot_content",
                      "elasticsearch": {
                        "node_attributes": {
                          "data": "hot"
                        }
                      },
                      "topology_element_control": {
                        "min": {
                          "value": 1024,
                          "resource": "memory"
                        }
                      },
                      "autoscaling_max": {
                        "value": 2097152,
                        "resource": "memory"
                      }
                    },
                    {
                      "node_type": {
                        "data": true,
                        "ingest": false,
                        "master": false
                      },
                      "instance_configuration_id": "data.highstorage",
                      "zone_count": 1,
                      "size": {
                        "resource": "memory",
                        "value": 0
                      },
                      "node_roles": [
                        "data_warm",
                        "remote_cluster_client"
                      ],
                      "id": "warm",
                      "elasticsearch": {
                        "node_attributes": {
                          "data": "warm"
                        }
                      },
                      "topology_element_control": {
                        "min": {
                          "value": 0,
                          "resource": "memory"
                        }
                      },
                      "autoscaling_max": {
                        "value": 2097152,
                        "resource": "memory"
                      }
                    },
                    {
                      "node_type": {
                        "data": true,
                        "ingest": false,
                        "master": false
                      },
                      "instance_configuration_id": "data.highstorage",
                      "zone_count": 1,
                      "size": {
                        "resource": "memory",
                        "value": 0
                      },
                      "node_roles": [
                        "data_cold",
                        "remote_cluster_client"
                      ],
                      "id": "cold",
                      "elasticsearch": {
                        "node_attributes": {
                          "data": "cold"
                        }
                      },
                      "topology_element_control": {
                        "min": {
                          "value": 0,
                          "resource": "memory"
                        }
                      },
                      "autoscaling_max": {
                        "value": 2097152,
                        "resource": "memory"
                      }
                    },
                    {
                      "node_type": {
                        "data": true,
                        "ingest": false,
                        "master": false
                      },
                      "instance_configuration_id": "data.frozen",
                      "zone_count": 1,
                      "size": {
                        "resource": "memory",
                        "value": 0
                      },
                      "node_roles": [
                        "data_frozen"
                      ],
                      "id": "frozen",
                      "elasticsearch": {
                        "node_attributes": {
                          "data": "frozen"
                        }
                      },
                      "topology_element_control": {
                        "min": {
                          "value": 0,
                          "resource": "memory"
                        }
                      },
                      "autoscaling_max": {
                        "value": 2097152,
                        "resource": "memory"
                      }
                    },
                    {
                      "node_type": {
                        "master": false,
                        "data": false,
                        "ingest": true
                      },
                      "zone_count": 1,
                      "instance_configuration_id": "coordinating",
                      "size": {
                        "value": 1024,
                        "resource": "memory"
                      },
                      "node_roles": [
                        "ingest",
                        "remote_cluster_client"
                      ],
                      "id": "coordinating",
                      "topology_element_control": {
                        "min": {
                          "value": 0,
                          "resource": "memory"
                        }
                      }
                    },
                    {
                      "node_type": {
                        "master": true,
                        "data": false,
                        "ingest": false
                      },
                      "zone_count": 3,
                      "instance_configuration_id": "master",
                      "size": {
                        "value": 1024,
                        "resource": "memory"
                      },
                      "node_roles": [
                        "master",
                        "remote_cluster_client"
                      ],
                      "id": "master",
                      "topology_element_control": {
                        "min": {
                          "value": 0,
                          "resource": "memory"
                        }
                      }
                    },
                    {
                      "node_type": {
                        "master": false,
                        "data": false,
                        "ingest": false,
                        "ml": true
                      },
                      "zone_count": 1,
                      "instance_configuration_id": "ml",
                      "size": {
                        "value": 0,
                        "resource": "memory"
                      },
                      "node_roles": [
                        "ml",
                        "remote_cluster_client"
                      ],
                      "id": "ml",
                      "topology_element_control": {
                        "min": {
                          "value": 16384,
                          "resource": "memory"
                        }
                      },
                      "autoscaling_min": {
                        "resource": "memory",
                        "value": 16384
                      },
                      "autoscaling_max": {
                        "value": 2097152,
                        "resource": "memory"
                      }
                    }
                  ],
                  "elasticsearch": {},
                  "autoscaling_enabled": false
                },
                "settings": {
                  "dedicated_masters_threshold": 3
                }
              }
            ],
            "kibana": [
              {
                "ref_id": "kibana-ref-id",
                "elasticsearch_cluster_ref_id": "es-ref-id",
                "region": "ece-region",
                "plan": {
                  "zone_count": 1,
                  "cluster_topology": [
                    {
                      "instance_configuration_id": "kibana",
                      "size": {
                        "value": 1024,
                        "resource": "memory"
                      }
                    }
                  ],
                  "kibana": {}
                }
              }
            ],
            "apm": [
              {
                "ref_id": "apm-ref-id",
                "elasticsearch_cluster_ref_id": "es-ref-id",
                "region": "ece-region",
                "plan": {
                  "cluster_topology": [
                    {
                      "instance_configuration_id": "apm",
                      "size": {
                        "value": 0,
                        "resource": "memory"
                      },
                      "zone_count": 1
                    }
                  ],
                  "apm": {}
                }
              }
            ],
            "enterprise_search": [
              {
                "ref_id": "enterprise_search-ref-id",
                "elasticsearch_cluster_ref_id": "es-ref-id",
                "region": "ece-region",
                "plan": {
                  "cluster_topology": [
                    {
                      "node_type": {
                        "appserver": true,
                        "connector": true,
                        "worker": true
                      },
                      "instance_configuration_id": "enterprise.search",
                      "size": {
                        "value": 0,
                        "resource": "memory"
                      },
                      "zone_count": 2
                    }
                  ],
                  "enterprise_search": {}
                }
              }
            ]
          }
        }
    }'
    ```


::::{note}
When specifying `node_roles` in the {{es}} plan of the deployment template, the template must contain all resource types and all {{es}} tiers. The deployment template must contain exactly one entry for each resource type. It must have one {{es}}, one {{kib}}, and one APM. On top of that, it must also include all supported {{es}} tiers in the {{es}} plan. The supported tiers are identified by the IDs `hot_content`, `warm`, `cold`, `frozen`, `master`, `coordinating` and `ml`.
::::

::::{note}
Deployment templates without `node_roles` or `id` should only contain hot and warm data tiers, with different `instance_configuration_id`s. Node roles are highly recommended when using the cold tier and are mandatory for the frozen tier.
::::

::::{note}
To support deployment templates that are versioned due to a constraint on architecture that is only supported by newer versions of ECE, for example ARM instances, you must add additional configuration:

* The `template_category_id` for both template versions must be identical.
* The `min_version` attribute must be set.

These attributes are set at the same level as `name` and `description`. The UI selects the template with the highest matching `min_version` that is returned by the API.

::::


## Next steps

After you have saved your new template, you can start [creating new deployments](create-deployment.md) with it.


