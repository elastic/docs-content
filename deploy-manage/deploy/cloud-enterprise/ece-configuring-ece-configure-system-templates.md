---
navigation_title: Configure default templates
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configuring-ece-configure-system-templates.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Configure default system deployment templates [ece-configuring-ece-configure-system-templates]

While you can create new deployment templates for some use cases, if the default system templates meet your needs but require minor adjustments, you may choose to configure or modify them.

For example, you want to use [Autoscaling](/deploy-manage/autoscaling/autoscaling-in-ece-and-ech.md) with the system templates, but want to modify some of the default values for autoscaling in those templates. You might want to enable autoscaling by default for new deployments, or adjust the default value of the autoscaling maximum for the hot tier.

::::{note}
You cannot edit system templates through the UI; they can only be configured through the API.
::::

## Configure system deployment templates through the RESTful API [ece_configure_system_deployment_templates_through_the_restful_api] 

::::{note} 
The API user must have the `Platform admin` role in order to configure system templates.
::::

1. Obtain the existing system deployment template you wish to modify. Note the `id` of the system deployment template as you will include this value in the API call to edit the template.

    ```sh
    curl -k -X GET -H "Authorization: ApiKey $ECE_API_KEY" https://$COORDINATOR_HOST:12443/api/v1/deployments/templates?region=ece-region
    ```

2. Edit the JSON of the system deployment template you wish to modify.
3. Make the API call to modify the deployment template. Note that the last path segment in the URL is the `id` of the system template you wish to modify. Check [set deployment template API](https://www.elastic.co/docs/api/doc/cloud-enterprise/operation/operation-set-deployment-template-v2) for more detail.

    The following example modifies the Default system deployment template (that, is the system template with `id` value of `default`), setting the default value of `autoscaling_enabled` to `true` and the default autoscaling maximum size of the hot tier to 4,194,304MB (64GB * 64 nodes).

    ```sh
    curl -k -X PUT -H "Authorization: ApiKey $ECE_API_KEY" https://$COORDINATOR_HOST:12443/api/v1/deployments/templates/default?region=ece-region -H 'content-type: application/json' -d '{
      {
      "name" : "Default",
      "description" : "Default deployment template for clusters",
      "deployment_template" : {
        "resources" : {
          "elasticsearch" : [
            {
              "ref_id" : "es-ref-id",
              "region" : "ece-region",
              "plan" : {
                "cluster_topology" : [
                  {
                    "id" : "hot_content",
                    "node_type" : {
                      "master" : true,
                      "data" : true,
                      "ingest" : true
                    },
                    "node_roles" : [
                      "master",
                      "ingest",
                      "remote_cluster_client",
                      "data_hot",
                      "transform",
                      "data_content"
                    ],
                    "zone_count" : 1,
                    "elasticsearch" : {
                      "node_attributes" : {
                        "data" : "hot"
                      }
                    },
                    "instance_configuration_id" : "data.default",
                    "size" : {
                      "value" : 4096,
                      "resource" : "memory"
                    },
                    "autoscaling_max" : {
                      "value" : 4194304,
                      "resource" : "memory"
                    },
                    "topology_element_control" : {
                      "min" : {
                        "value" : 1024,
                        "resource" : "memory"
                      }
                    }
                  },
                  {
                    "id" : "warm",
                    "node_type" : {
                      "master" : false,
                      "data" : true,
                      "ingest" : false
                    },
                    "node_roles" : [
                      "data_warm",
                      "remote_cluster_client"
                    ],
                    "zone_count" : 1,
                    "elasticsearch" : {
                      "node_attributes" : {
                        "data" : "warm"
                      }
                    },
                    "instance_configuration_id" : "data.highstorage",
                    "size" : {
                      "value" : 0,
                      "resource" : "memory"
                    },
                    "autoscaling_max" : {
                      "value" : 2097152,
                      "resource" : "memory"
                    },
                    "topology_element_control" : {
                      "min" : {
                        "value" : 0,
                        "resource" : "memory"
                      }
                    }
                  },
                  {
                    "id" : "cold",
                    "node_type" : {
                      "master" : false,
                      "data" : true,
                      "ingest" : false
                    },
                    "node_roles" : [
                      "data_cold",
                      "remote_cluster_client"
                    ],
                    "zone_count" : 1,
                    "elasticsearch" : {
                      "node_attributes" : {
                        "data" : "cold"
                      }
                    },
                    "instance_configuration_id" : "data.highstorage",
                    "size" : {
                      "value" : 0,
                      "resource" : "memory"
                    },
                    "autoscaling_max" : {
                      "value" : 2097152,
                      "resource" : "memory"
                    },
                    "topology_element_control" : {
                      "min" : {
                        "value" : 0,
                        "resource" : "memory"
                      }
                    }
                  },
                  {
                    "id" : "coordinating",
                    "node_type" : {
                      "master" : false,
                      "data" : false,
                      "ingest" : true
                    },
                    "node_roles" : [
                      "ingest",
                      "remote_cluster_client"
                    ],
                    "zone_count" : 1,
                    "instance_configuration_id" : "coordinating",
                    "size" : {
                      "value" : 0,
                      "resource" : "memory"
                    },
                    "topology_element_control" : {
                      "min" : {
                        "value" : 0,
                        "resource" : "memory"
                      }
                    }
                  },
                  {
                    "id" : "master",
                    "node_type" : {
                      "master" : true,
                      "data" : false,
                      "ingest" : false
                    },
                    "node_roles" : [
                      "master",
                      "remote_cluster_client"
                    ],
                    "zone_count" : 1,
                    "instance_configuration_id" : "master",
                    "size" : {
                      "value" : 0,
                      "resource" : "memory"
                    },
                    "topology_element_control" : {
                      "min" : {
                        "value" : 0,
                        "resource" : "memory"
                      }
                    }
                  },
                  {
                    "id" : "ml",
                    "node_type" : {
                      "master" : false,
                      "data" : false,
                      "ingest" : false,
                      "ml" : true
                    },
                    "node_roles" : [
                      "ml",
                      "remote_cluster_client"
                    ],
                    "zone_count" : 1,
                    "instance_configuration_id" : "ml",
                    "size" : {
                      "value" : 0,
                      "resource" : "memory"
                    },
                    "autoscaling_min" : {
                      "value" : 0,
                      "resource" : "memory"
                    },
                    "autoscaling_max" : {
                      "value" : 2097152,
                      "resource" : "memory"
                    },
                    "topology_element_control" : {
                      "min" : {
                        "value" : 0,
                        "resource" : "memory"
                      }
                    }
                  }
                ],
                "elasticsearch" : {

                },
                "autoscaling_enabled" : true
              },
              "settings" : {
                "dedicated_masters_threshold" : 6
              }
            }
          ],
          "kibana" : [
            {
              "ref_id" : "kibana-ref-id",
              "elasticsearch_cluster_ref_id" : "es-ref-id",
              "region" : "ece-region",
              "plan" : {
                "zone_count" : 1,
                "cluster_topology" : [
                  {
                    "instance_configuration_id" : "kibana",
                    "size" : {
                      "value" : 1024,
                      "resource" : "memory"
                    }
                  }
                ],
                "kibana" : {

                }
              }
            }
          ],
          "apm" : [
            {
              "ref_id" : "apm-ref-id",
              "elasticsearch_cluster_ref_id" : "es-ref-id",
              "region" : "ece-region",
              "plan" : {
                "cluster_topology" : [
                  {
                    "instance_configuration_id" : "apm",
                    "size" : {
                      "value" : 0,
                      "resource" : "memory"
                    },
                    "zone_count" : 1
                  }
                ],
                "apm" : {

                }
              }
            }
          ],
          "enterprise_search" : [
            {
              "ref_id" : "enterprise_search-ref-id",
              "elasticsearch_cluster_ref_id" : "es-ref-id",
              "region" : "ece-region",
              "plan" : {
                "cluster_topology" : [
                  {
                    "node_type" : {
                      "appserver" : true,
                      "worker" : true,
                      "connector" : true
                    },
                    "instance_configuration_id" : "enterprise.search",
                    "size" : {
                      "value" : 0,
                      "resource" : "memory"
                    },
                    "zone_count" : 2
                  }
                ],
                "enterprise_search" : {

                }
              }
            }
          ]
        }
      },
      "system_owned" : true,
      "metadata" : [
        {
          "key" : "parent_solution",
          "value" : "stack"
        }
      ],
      "order" : 0,
      "template_category_id" : "default"
    }'
    ```


After you have edited the template, you can start [creating new deployments](create-deployment.md) with it.

