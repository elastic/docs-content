---
navigation_title: Data tiers and autoscaling support
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ce-add-support-for-node-roles-and-autoscaling.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Updating custom templates to support node_roles and autoscaling [ce-add-support-for-node-roles-and-autoscaling]

Templates created in older versions of ECE should be updated in order to take advantage of new {{ece}} features, such as [Data tiers](../../../manage-data/lifecycle/data-tiers.md), and [Deployment autoscaling](../../autoscaling.md). By updating these templates we also ensure forward compatibility with future {{ece}} versions that will require certain fields such as `node_roles` and `id` to be present in the deployment configuration.

::::{note}
System owned deployment templates are automatically updated during the ECE upgrade process to support both data tiers with `node_roles` and autoscaling. However, custom templates that you created must be manually updated by following the steps in this guide.
::::

## Adding support for node_roles [ece_adding_support_for_node_roles]

The `node_roles` field defines the roles that an {{es}} topology element can have, which is used in place of `node_type` when a new feature such as autoscaling is enabled, or when a new data tier is added. This field is supported on [{{stack}} versions 7.10 and above](cloud://reference/cloud-enterprise/changes-to-index-allocation-api.md).

There are a number of fields that need to be added to each {{es}} node in order to support `node_roles`:

* **id**: Unique identifier of the topology element. This field, along with the `node_roles`, identifies an {{es}} topology element.
* **node_roles**: The list of node roles. Allowable roles are: `master`, `ingest`, `ml`, `data_hot`, `data_content`, `data_warm`, `data_cold`, `data_frozen`, `remote_cluster_client`, and `transform`. For details, check [Node roles](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md#node-roles).
* **topology_element_control**: Controls for the topology element.

    * **min**: The absolute minimum size limit for a topology element. If the value is `0`, that means the topology element can be disabled.


The following example is based on the `default` system owned deployment template that already supports `node_roles`. This template will be used as a reference for the next sections:

::::{dropdown} Reference example with support for node_roles
:name: ece-node-roles-support-example

```json
{
  ...
  "deployment_template": {
    "resources": {
      "elasticsearch": [
        {
          "plan": {
            "cluster_topology": [
              {
                "id": "hot_content",
                "instance_configuration_id": "data.default",
                "zone_count": 1,
                "node_roles": [
                  "master",
                  "ingest",
                  "data_hot",
                  "data_content",
                  "remote_cluster_client",
                  "transform"
                ],
                "node_type": {
                  "master": true,
                  "data": true,
                  "ingest": true
                },
                "elasticsearch": {
                  "node_attributes": {
                  "data": "hot"
                  }
                },
                "size": {
                  "value": 4096,
                  "resource": "memory"
                },
                "topology_element_control": {
                  "min": {
                  "value": 1024,
                  "resource": "memory"
                  }
                }
              },
              {
                "id": "warm",
                "instance_configuration_id": "data.highstorage",
                "zone_count": 1,
                "node_roles": [
                  "data_warm",
                  "remote_cluster_client"
                ],
                "node_type": {
                  "data": true,
                  "ingest": false,
                  "master": false
                },
                "elasticsearch": {
                  "node_attributes": {
                  "data": "warm"
                  }
                },
                "size": {
                  "resource": "memory",
                  "value": 0
                },
                "topology_element_control": {
                  "min": {
                  "value": 0,
                  "resource": "memory"
                  }
                }
              },
              {
                "id": "cold",
                "instance_configuration_id": "data.highstorage",
                "zone_count": 1,
                "node_roles": [
                  "data_cold",
                  "remote_cluster_client"
                ],
                "node_type": {
                  "data": true,
                  "ingest": false,
                  "master": false
                },
                "elasticsearch": {
                  "node_attributes": {
                  "data": "cold"
                  }
                },
                "size": {
                  "resource": "memory",
                  "value": 0
                },
                "topology_element_control": {
                  "min": {
                  "value": 0,
                  "resource": "memory"
                  }
                }
              },
              {
                "id": "frozen",
                "instance_configuration_id": "data.frozen",
                "zone_count": 1,
                "node_roles": [
                  "data_frozen"
                ],
                "node_type": {
                  "data": true,
                  "ingest": false,
                  "master": false
                },
                "elasticsearch": {
                  "node_attributes": {
                  "data": "frozen"
                  }
                },
                "size": {
                  "resource": "memory",
                  "value": 0
                },
                "topology_element_control": {
                  "min": {
                  "value": 0,
                  "resource": "memory"
                  }
                }
              },
              {
                "id": "coordinating",
                "zone_count": 1,
                "instance_configuration_id": "coordinating",
                "node_roles": [
                  "ingest",
                  "remote_cluster_client"
                ],
                "node_type": {
                  "master": false,
                  "data": false,
                  "ingest": true
                },
                "size": {
                  "value": 0,
                  "resource": "memory"
                },
                "topology_element_control": {
                  "min": {
                  "value": 0,
                  "resource": "memory"
                  }
                }
              },
              {
                "id": "master",
                "zone_count": 1,
                "instance_configuration_id": "master",
                "node_roles": [
                  "master",
                  "remote_cluster_client"
                ],
                "node_type": {
                  "master": true,
                  "data": false,
                  "ingest": false
                },
                "size": {
                  "value": 0,
                  "resource": "memory"
                },
                "topology_element_control": {
                  "min": {
                  "value": 0,
                  "resource": "memory"
                  }
                }
              },
              {
                "id": "ml",
                "zone_count": 1,
                "instance_configuration_id": "ml",
                "node_roles": [
                  "ml",
                  "remote_cluster_client"
                ],
                "node_type": {
                  "master": false,
                  "data": false,
                  "ingest": false,
                  "ml": true
                },
                "size": {
                  "value": 0,
                  "resource": "memory"
                },
                "topology_element_control": {
                  "min": {
                  "value": 0,
                  "resource": "memory"
                  }
                }
              }
            ],
            "elasticsearch": {}
          },
          ...
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
}
```

::::


In the reference example there are seven different *{{es}} topology elements*: `hot_content`, `warm`, `cold`, `frozen`, `coordinating`, `master`, and `ml`. These names map to the `id` field of each topology element. In addition, this template contains four different *resources*: `elasticsearch`, `kibana`, `apm`, and `enterprise_search`.


### Requirements [ece_requirements]

To add support for `node_roles`, the deployment template has to meet the following requirements:

* Contains all four `resources`: `elasticsearch`, `kibana`, `apm`, and `enterprise_search`.
* The `elasticsearch` resource contains all seven topology elements: `hot_content`, `warm`, `cold`, `frozen`, `coordinating`, `master`, and `ml`.

    ::::{note}
    :name: ece-ce-valid-topology-element-ids

    The IDs `hot_content`, `warm`, `cold`, `frozen`, `coordinating`, `master`, and `ml` are the **only** ones supported in an {{es}} topology element. In addition, there may not be topology elements with duplicate IDs inside the `elasticsearch` resource.
    ::::

* Each topology element contains the `id`, `node_roles`, and `topology_element_control` fields.

It is also recommended that all {{es}} topology elements have the `node_attributes` field. This field can be useful in ILM policies, when creating a deployment using a version below 7.10, that does not support `node_roles`.

Except for the `id` and `node_roles`, all fields can be configured by the user. Also, the topology elements must contain the exact same `id` and `node_roles` that are present in the reference example.

::::{note}
Although it is required for the template to contain all resources and topology elements, it is possible to disable certain components by setting their `size.value` (and `topology_element_control.size` in the case of the {{es}} topology elements) to `0`.
::::



### Updating an ECE custom template to support `node_roles` [ece_updating_an_ece_custom_template_to_support_node_roles]

To update a custom deployment template:

1. Add the `id`, `node_roles`, `node_attributes`, and `topology_element_control` fields to the existing {{es}} topology elements. Keep in mind that these fields must match the {{es}} topology element in question:

    * If the `id` of the topology elements in the existing templates already match any of the seven mentioned in the requirements, then simply add the `node_roles` and `topology_element_control` to those elements, based on the reference example.
    * Otherwise, map each of the existing topology elements to one of the seven {{es}} topology elements, based on their `node_type`, and add the fields accordingly.

2. Add the `elasticsearch` topology elements that are missing.
3. Add the `resources` that are missing.

::::{note}
It is recommended to add the `id` field to each {{es}} topology element in the deployment plan, before updating the template. This can be performed either through a deployment update API request or using the deployment **Advanced edit** page. Refer to the [note above](#ece-ce-valid-topology-element-ids) to understand which values are available for the `id` field.
::::



### Example [ece-ce-add-support-to-node-roles-example]

The existing template contains three {{es}} topology elements and two resources (`elasticsearch` and `kibana`).

::::{dropdown} Custom example without support for node_roles
```json
{
  ...
  "deployment_template": {
    "resources": {
      "elasticsearch": [
        {
          "plan": {
            "cluster_topology": [
              {
                "instance_configuration_id": "custom.data",
                "zone_count": 2,
                "node_type": {
                  "master": true,
                  "data": true,
                  "ingest": true
                },
                "size": {
                  "value": 8192,
                  "resource": "memory"
                },
                "topology_element_control": {
                  "min": {
                    "value": 1024,
                    "resource": "memory"
                  }
                }
              },
              {
                "zone_count": 1,
                "instance_configuration_id": "custom.master",
                "node_type": {
                  "master": true,
                  "data": false,
                  "ingest": false
                },
                "size": {
                  "value": 0,
                  "resource": "memory"
                },
                "topology_element_control": {
                  "min": {
                    "value": 0,
                    "resource": "memory"
                  }
                }
              },
              {
                "zone_count": 1,
                "instance_configuration_id": "custom.ml",
                "node_type": {
                  "master": false,
                  "data": false,
                  "ingest": false,
                  "ml": true
                },
                "size": {
                  "value": 0,
                  "resource": "memory"
                },
                "topology_element_control": {
                  "min": {
                    "value": 0,
                    "resource": "memory"
                  }
                }
              }
            ],
            "elasticsearch": {}
          },
          ...
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
      ]
    }
  }
}
```

::::


In this case we can match the three existing {{es}} topology elements to `hot_content`, `master`, and `ml`, respectively, based on their `node_type` field. Therefore, we can simply add the `id`, `node_roles`, `topology_element_control`, and `node_attributes` that are already associated with these topology elements in the reference example.

Then, it is only necessary to add the four {{es}} topology elements (`warm`, `cold`, `frozen`, and `coordinating`) and two resources (`apm` and `enterprise_search`) that are missing. These fields can also be added based on the reference example.

After adding support for `node_roles`, the resulting deployment template should look similar to the following:

::::{dropdown} Custom example with support for node_roles
:name: example-with-support-for-node-roles

```json
{
  ...
  "deployment_template": {
    "resources": {
      "elasticsearch": [
        {
          "plan": {
            "cluster_topology": [
              {
                "id": "hot_content",
                "instance_configuration_id": "custom.data",
                "zone_count": 2,
                "node_roles": [
                  "master",
                  "ingest",
                  "data_hot",
                  "data_content",
                  "remote_cluster_client",
                  "transform"
                ],
                "node_type": {
                  "master": true,
                  "data": true,
                  "ingest": true
                },
                "elasticsearch": {
                  "node_attributes": {
                    "data": "hot"
                  }
                },
                "size": {
                  "value": 8192,
                  "resource": "memory"
                },
                "topology_element_control": {
                  "min": {
                    "value": 1024,
                    "resource": "memory"
                  }
                }
              },
              {
                "id": "warm",
                "instance_configuration_id": "data.highstorage",
                "zone_count": 1,
                "node_roles": [
                  "data_warm",
                  "remote_cluster_client"
                ],
                "node_type": {
                  "data": true,
                  "ingest": false,
                  "master": false
                },
                "elasticsearch": {
                  "node_attributes": {
                    "data": "warm"
                  }
                },
                "size": {
                  "resource": "memory",
                  "value": 0
                },
                "topology_element_control": {
                  "min": {
                    "value": 0,
                    "resource": "memory"
                  }
                }
              },
              {
                "id": "cold",
                "instance_configuration_id": "data.highstorage",
                "zone_count": 1,
                "node_roles": [
                  "data_cold",
                  "remote_cluster_client"
                ],
                "node_type": {
                  "data": true,
                  "ingest": false,
                  "master": false
                },
                "elasticsearch": {
                  "node_attributes": {
                    "data": "cold"
                  }
                },
                "size": {
                  "resource": "memory",
                  "value": 0
                },
                "topology_element_control": {
                  "min": {
                    "value": 0,
                    "resource": "memory"
                  }
                }
              },
              {
                "id": "frozen",
                "instance_configuration_id": "data.frozen",
                "zone_count": 1,
                "node_roles": [
                  "data_frozen"
                ],
                "node_type": {
                  "data": true,
                  "ingest": false,
                  "master": false
                },
                "elasticsearch": {
                  "node_attributes": {
                    "data": "frozen"
                  }
                },
                "size": {
                  "resource": "memory",
                  "value": 0
                },
                "topology_element_control": {
                  "min": {
                    "value": 0,
                    "resource": "memory"
                  }
                }
              },
              {
                "id": "coordinating",
                "zone_count": 1,
                "instance_configuration_id": "coordinating",
                "node_roles": [
                  "ingest",
                  "remote_cluster_client"
                ],
                "node_type": {
                  "master": false,
                  "data": false,
                  "ingest": true
                },
                "size": {
                  "value": 0,
                  "resource": "memory"
                },
                "topology_element_control": {
                  "min": {
                    "value": 0,
                    "resource": "memory"
                  }
                }
              },
              {
                "id": "master",
                "zone_count": 1,
                "instance_configuration_id": "custom.master",
                "node_roles": [
                  "master",
                  "remote_cluster_client"
                ],
                "node_type": {
                  "master": true,
                  "data": false,
                  "ingest": false
                },
                "size": {
                  "value": 0,
                  "resource": "memory"
                },
                "topology_element_control": {
                  "min": {
                    "value": 0,
                    "resource": "memory"
                  }
                }
              },
              {
                "id": "ml",
                "zone_count": 1,
                "instance_configuration_id": "custom.ml",
                "node_roles": [
                  "ml",
                  "remote_cluster_client"
                ],
                "node_type": {
                  "master": false,
                  "data": false,
                  "ingest": false,
                  "ml": true
                },
                "size": {
                  "value": 0,
                  "resource": "memory"
                },
                "topology_element_control": {
                  "min": {
                    "value": 0,
                    "resource": "memory"
                  }
                }
              }
            ],
            "elasticsearch": {}
          },
          ...
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
}
```

::::



## Adding support for autoscaling [ece_adding_support_for_autoscaling]

After adding support for `node_roles` we can then update the template to support autoscaling. Autoscaling is used to automatically adjust the available resources in the deployments. Currently, this feature is available for {{es}} data tiers and machine learning node in [{{stack}} versions 7.11 and above](../../autoscaling.md).

There are a number of autoscaling fields that need to be added in order to support autoscaling:

* **autoscaling_min**: The default minimum size of an {{es}} topology element when autoscaling is enabled. This setting is currently available only for machine learning nodes, since these are the only nodes that support scaling down.
* **autoscaling_max**: The default maximum size of an {{es}} topology element when autoscaling is enabled. This setting is currently available only for data tiers and machine learning nodes, since these are the only nodes that support scaling up.
* **autoscaling_enabled**: When set to `true`, autoscaling is enabled by default on an {{es}} cluster.

::::{note}
These fields represent the default settings for the deployment. However, autoscaling can be enabled/disabled and the maximum and minimum autoscaling sizes can be adjusted in the deployment settings.
::::


Similar to the `node_roles` example, the following one is also based on the `default` deployment template that already supports `node_roles` and autoscaling. This template will be used as a reference for the next sections:

::::{dropdown} Reference example with support for node_roles and autoscaling
```json
{
  ...
  "deployment_template": {
    "resources": {
      "elasticsearch": [
        {
          "plan": {
            "cluster_topology": [
              {
                "id": "hot_content",
                "instance_configuration_id": "data.default",
                "zone_count": 1,
                "node_roles": [
                  "master",
                  "ingest",
                  "data_hot",
                  "data_content",
                  "remote_cluster_client",
                  "transform"
                ],
                "node_type": {
                  "master": true,
                  "data": true,
                  "ingest": true
                },
                "elasticsearch": {
                  "node_attributes": {
                    "data": "hot"
                  }
                },
                "size": {
                  "value": 4096,
                  "resource": "memory"
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
                "id": "warm",
                "instance_configuration_id": "data.highstorage",
                "zone_count": 1,
                "node_roles": [
                  "data_warm",
                  "remote_cluster_client"
                ],
                "node_type": {
                  "data": true,
                  "ingest": false,
                  "master": false
                },
                "elasticsearch": {
                  "node_attributes": {
                    "data": "warm"
                  }
                },
                "size": {
                  "resource": "memory",
                  "value": 0
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
                "id": "cold",
                "instance_configuration_id": "data.highstorage",
                "zone_count": 1,
                "node_roles": [
                  "data_cold",
                  "remote_cluster_client"
                ],
                "node_type": {
                  "data": true,
                  "ingest": false,
                  "master": false
                },
                "elasticsearch": {
                  "node_attributes": {
                    "data": "cold"
                  }
                },
                "size": {
                  "resource": "memory",
                  "value": 0
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
                "id": "frozen",
                "instance_configuration_id": "data.frozen",
                "zone_count": 1,
                "node_roles": [
                  "data_frozen"
                ],
                "node_type": {
                  "data": true,
                  "ingest": false,
                  "master": false
                },
                "elasticsearch": {
                  "node_attributes": {
                    "data": "frozen"
                  }
                },
                "size": {
                  "resource": "memory",
                  "value": 0
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
                "id": "coordinating",
                "zone_count": 1,
                "instance_configuration_id": "coordinating",
                "node_roles": [
                  "ingest",
                  "remote_cluster_client"
                ],
                "node_type": {
                  "master": false,
                  "data": false,
                  "ingest": true
                },
                "size": {
                  "value": 0,
                  "resource": "memory"
                },
                "topology_element_control": {
                  "min": {
                    "value": 0,
                    "resource": "memory"
                  }
                }
              },
              {
                "id": "master",
                "zone_count": 1,
                "instance_configuration_id": "master",
                "node_roles": [
                  "master",
                  "remote_cluster_client"
                ],
                "node_type": {
                  "master": true,
                  "data": false,
                  "ingest": false
                },
                "size": {
                  "value": 0,
                  "resource": "memory"
                },
                "topology_element_control": {
                  "min": {
                    "value": 0,
                    "resource": "memory"
                  }
                }
              },
              {
                "id": "ml",
                "zone_count": 1,
                "instance_configuration_id": "ml",
                "node_roles": [
                  "ml",
                  "remote_cluster_client"
                ],
                "node_type": {
                  "master": false,
                  "data": false,
                  "ingest": false,
                  "ml": true
                },
                "size": {
                  "value": 0,
                  "resource": "memory"
                },
                "topology_element_control": {
                  "min": {
                    "value": 0,
                    "resource": "memory"
                  }
                },
                "autoscaling_min": {
                  "resource": "memory",
                  "value": 0
                },
                "autoscaling_max": {
                  "value": 2097152,
                  "resource": "memory"
                }
              }
            ],
            "elasticsearch": {},
            "autoscaling_enabled": true
          },
          ...
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
}
```

::::



### Requirements [ece_requirements_2]

To add support for autoscaling, the deployment template has to meet the following requirements:

1. Already has support for `node_roles`.
2. Contains the `size`, `autoscaling_min`, and `autoscaling_max` fields, according to the rules specified in the [autoscaling requirements table](../../autoscaling/autoscaling-in-ece-and-ech.md#ece-autoscaling-api-example-requirements-table).
3. Contains the `autoscaling_enabled` fields on the `elasticsearch` resource.

If necessary, the values chosen for each field can be based on the reference example.


### Updating an ECE custom template to support autoscaling [ece_updating_an_ece_custom_template_to_support_autoscaling]

To update a custom deployment template:

1. Add the `autoscaling_min` and `autoscaling_max` fields to the {{es}} topology elements (check [Autoscaling through the API](../../autoscaling/autoscaling-in-ece-and-ech.md#ec-autoscaling-api-example)).
2. Add the `autoscaling_enabled` fields to the `elasticsearch` resource. Set this field to `true` in case you want autoscaling enabled by default, and to `false` otherwise.


### Example [ece_example]

After adding support for autoscaling to the [example](#ece-node-roles-support-example) presented in the previous section, the resulting deployment template should look similar to the following:

::::{dropdown} Custom example with support for node_roles and autoscaling
```json
{
  ...
  "deployment_template": {
    "resources": {
      "elasticsearch": [
        {
          "plan": {
            "cluster_topology": [
              {
                "id": "hot_content",
                "instance_configuration_id": "custom.data",
                "zone_count": 2,
                "node_roles": [
                  "master",
                  "ingest",
                  "data_hot",
                  "data_content",
                  "remote_cluster_client",
                  "transform"
                ],
                "node_type": {
                  "master": true,
                  "data": true,
                  "ingest": true
                },
                "elasticsearch": {
                  "node_attributes": {
                    "data": "hot"
                  }
                },
                "size": {
                  "value": 8192,
                  "resource": "memory"
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
                "id": "warm",
                "instance_configuration_id": "data.highstorage",
                "zone_count": 1,
                "node_roles": [
                  "data_warm",
                  "remote_cluster_client"
                ],
                "node_type": {
                  "data": true,
                  "ingest": false,
                  "master": false
                },
                "elasticsearch": {
                  "node_attributes": {
                    "data": "warm"
                  }
                },
                "size": {
                  "resource": "memory",
                  "value": 0
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
                "id": "cold",
                "instance_configuration_id": "data.highstorage",
                "zone_count": 1,
                "node_roles": [
                  "data_cold",
                  "remote_cluster_client"
                ],
                "node_type": {
                  "data": true,
                  "ingest": false,
                  "master": false
                },
                "elasticsearch": {
                  "node_attributes": {
                    "data": "cold"
                  }
                },
                "size": {
                  "resource": "memory",
                  "value": 0
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
                "id": "frozen",
                "instance_configuration_id": "data.frozen",
                "zone_count": 1,
                "node_roles": [
                  "data_frozen"
                ],
                "node_type": {
                  "data": true,
                  "ingest": false,
                  "master": false
                },
                "elasticsearch": {
                  "node_attributes": {
                    "data": "frozen"
                  }
                },
                "size": {
                  "resource": "memory",
                  "value": 0
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
                "id": "coordinating",
                "zone_count": 1,
                "instance_configuration_id": "coordinating",
                "node_roles": [
                  "ingest",
                  "remote_cluster_client"
                ],
                "node_type": {
                  "master": false,
                  "data": false,
                  "ingest": true
                },
                "size": {
                  "value": 0,
                  "resource": "memory"
                },
                "topology_element_control": {
                  "min": {
                    "value": 0,
                    "resource": "memory"
                  }
                }
              },
              {
                "id": "master",
                "zone_count": 1,
                "instance_configuration_id": "custom.master",
                "node_roles": [
                  "master",
                  "remote_cluster_client"
                ],
                "node_type": {
                  "master": true,
                  "data": false,
                  "ingest": false
                },
                "size": {
                  "value": 0,
                  "resource": "memory"
                },
                "topology_element_control": {
                  "min": {
                    "value": 0,
                    "resource": "memory"
                  }
                }
              },
              {
                "id": "ml",
                "zone_count": 1,
                "instance_configuration_id": "custom.ml",
                "node_roles": [
                  "ml",
                  "remote_cluster_client"
                ],
                "node_type": {
                  "master": false,
                  "data": false,
                  "ingest": false,
                  "ml": true
                },
                "size": {
                  "value": 0,
                  "resource": "memory"
                },
                "topology_element_control": {
                  "min": {
                    "value": 0,
                    "resource": "memory"
                  }
                },
                "autoscaling_min": {
                  "resource": "memory",
                  "value": 0
                },
                "autoscaling_max": {
                  "value": 2097152,
                  "resource": "memory"
                }
              }
            ],
            "elasticsearch": {},
            "autoscaling_enabled": true
          },
          ...
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
}
```

::::



## Updating a custom template through the RESTful API [ece_updating_a_custom_template_through_the_restful_api]

Having added support for `node_roles` and autoscaling to your custom template, it is possible to perform the update through the RESTful API, by following these steps:

1. Obtain the existing deployment templates by sending the following `GET` request, and take note of the `id` of the template you wish to update.

    ```sh
    curl -k -X GET -H "Authorization: ApiKey $ECE_API_KEY" https://$COORDINATOR_HOST:12443/api/v1/deployments/templates?region=ece-region
    ```

2. Send a `PUT` request with the updated template on the payload, in order to effectively replace the outdated template with the new one. Note that the following request is just an example, you have to replace `{{template_id}}` with the `id` you collected on step 1. and set the payload to the updated template JSON. Check [set deployment template API](https://www.elastic.co/docs/api/doc/cloud-enterprise/operation/operation-set-deployment-template-v2) for more details.

    ::::{dropdown} Update template API request example
    ```sh
    curl -k -X PUT -H "Authorization: ApiKey $ECE_API_KEY" https://$COORDINATOR_HOST:12443/api/v1/deployments/templates/{template_id}?region=ece-region -H 'content-type: application/json' -d '
    {
      "name": "ECE Custom Template",
      "description": "ECE custom template with support for node_roles and autoscaling",
      "deployment_template": {
        "resources": {
          "elasticsearch": [
            {
              "ref_id": "es-ref-id",
              "region": "ece-region",
              "plan": {
                "cluster_topology": [
                  {
                    "id": "hot_content",
                    "instance_configuration_id": "custom.data",
                    "zone_count": 2,
                    "node_roles": [
                      "master",
                      "ingest",
                      "data_hot",
                      "data_content",
                      "remote_cluster_client",
                      "transform"
                    ],
                    "node_type": {
                      "master": true,
                      "data": true,
                      "ingest": true
                    },
                    "elasticsearch": {
                      "node_attributes": {
                        "data": "hot"
                      }
                    },
                    "size": {
                      "value": 8192,
                      "resource": "memory"
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
                    "id": "warm",
                    "instance_configuration_id": "data.highstorage",
                    "zone_count": 1,
                    "node_roles": [
                      "data_warm",
                      "remote_cluster_client"
                    ],
                    "node_type": {
                      "data": true,
                      "ingest": false,
                      "master": false
                    },
                    "elasticsearch": {
                      "node_attributes": {
                        "data": "warm"
                      }
                    },
                    "size": {
                      "resource": "memory",
                      "value": 0
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
                    "id": "cold",
                    "instance_configuration_id": "data.highstorage",
                    "zone_count": 1,
                    "node_roles": [
                      "data_cold",
                      "remote_cluster_client"
                    ],
                    "node_type": {
                      "data": true,
                      "ingest": false,
                      "master": false
                    },
                    "elasticsearch": {
                      "node_attributes": {
                        "data": "cold"
                      }
                    },
                    "size": {
                      "resource": "memory",
                      "value": 0
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
                    "id": "frozen",
                    "instance_configuration_id": "data.frozen",
                    "zone_count": 1,
                    "node_roles": [
                      "data_frozen"
                    ],
                    "node_type": {
                      "data": true,
                      "ingest": false,
                      "master": false
                    },
                    "elasticsearch": {
                      "node_attributes": {
                        "data": "frozen"
                      }
                    },
                    "size": {
                      "resource": "memory",
                      "value": 0
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
                    "id": "coordinating",
                    "zone_count": 1,
                    "instance_configuration_id": "coordinating",
                    "node_roles": [
                      "ingest",
                      "remote_cluster_client"
                    ],
                    "node_type": {
                      "master": false,
                      "data": false,
                      "ingest": true
                    },
                    "size": {
                      "value": 0,
                      "resource": "memory"
                    },
                    "topology_element_control": {
                      "min": {
                        "value": 0,
                        "resource": "memory"
                      }
                    }
                  },
                  {
                    "id": "master",
                    "zone_count": 1,
                    "instance_configuration_id": "custom.master",
                    "node_roles": [
                      "master",
                      "remote_cluster_client"
                    ],
                    "node_type": {
                      "master": true,
                      "data": false,
                      "ingest": false
                    },
                    "size": {
                      "value": 0,
                      "resource": "memory"
                    },
                    "topology_element_control": {
                      "min": {
                        "value": 0,
                        "resource": "memory"
                      }
                    }
                  },
                  {
                    "id": "ml",
                    "zone_count": 1,
                    "instance_configuration_id": "custom.ml",
                    "node_roles": [
                      "ml",
                      "remote_cluster_client"
                    ],
                    "node_type": {
                      "master": false,
                      "data": false,
                      "ingest": false,
                      "ml": true
                    },
                    "size": {
                      "value": 0,
                      "resource": "memory"
                    },
                    "topology_element_control": {
                      "min": {
                        "value": 0,
                        "resource": "memory"
                      }
                    },
                    "autoscaling_min": {
                      "resource": "memory",
                      "value": 0
                    },
                    "autoscaling_max": {
                      "value": 2097152,
                      "resource": "memory"
                    }
                  }
                ],
                "elasticsearch": {},
                "autoscaling_enabled": true
              },
              "settings": {
                "dedicated_masters_threshold": 6
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
                      "worker": true,
                      "connector": true
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
      },
      "system_owned": false
    }'
    ```

    ::::


After the template is updated, you can start [creating new deployments](create-deployment.md) or [migrating existing ones to `node_roles`](#ece-migrating-a-deployment-to-node-roles).

Although `node_roles` and autoscaling are only available in more recent {{stack}} versions, an updated template can still be used with deployments that have versions below 7.10. In these cases, the data tiers and autoscaling features will only take effect once the deployment is upgraded to versions 7.10 and 7.11, respectively.


## Migrating a deployment to `node_roles` [ece-migrating-a-deployment-to-node-roles]

Once a custom template is updated with `node_roles`, the existing deployments associated with this template can be migrated to `node_roles`. This migration can be done automatically by performing one of the following actions through the UI:

* Enable a warm, cold, or frozen tier.
* Upgrade the deployment.
* Enable autoscaling (only possible if the custom template has support for autoscaling).

If you do not intend to perform any of these actions, the migration can only be done by manually updating the necessary fields in the deployment plan. This can be performed either through the API or using the deployment **Advanced edit** page.

**Using the API:**

1. Go to the deployment **Edit** page.
2. Get the deployment update payload by clicking **Equivalent API request** at the bottom of the page.
3. Update the payload by replacing `node_type` with `node_roles` in each {{es}} topology element. To know which `node_roles` to add to each topology element, refer to the [custom template example](#ece-ce-add-support-to-node-roles-example) where support for `node_roles` is added.
4. Send a `PUT` request with the updated deployment payload to conclude the migration. Check the [Update Deployment](https://www.elastic.co/docs/api/doc/cloud-enterprise/operation/operation-update-deployment) API documentation for more details.

**Using the Advanced edit:**

::::{note}
To follow this approach you need to have administrator privileges.
::::


1. Go to the deployment **Edit** page.
2. Click **Advanced edit** at the bottom of the page.
3. Update the **Deployment configuration** by replacing `node_type` with `node_roles` in each {{es}} topology element. To know which `node_roles` to add to each topology element, refer to the [custom template example](#ece-ce-add-support-to-node-roles-example) where support for `node_roles` is added.
4. Click **Save** to conclude the migration.

::::{warning}
Once a deployment is migrated to node roles, it is not possible to roll back.
::::


After the migration plan has finished, we recommend following the [Migrate index allocation filters to node roles](../../../manage-data/lifecycle/index-lifecycle-management/migrate-index-allocation-filters-to-node-roles.md) guide. Step 1 of this guide was already accomplished by adding support for `node_roles`. However, performing steps 2, 3, and 4, which involves updating index settings, index templates, and ILM policies, can prevent shard allocation issues caused by conflicting ILM policies.


### Example [ece_example_2]

The following is an example of a deployment plan that does not contain `node_roles`:

::::{dropdown} Example deployment plan with node_type
```json
{
  "name": "Example deployment",
  "prune_orphans": true,
  "metadata": {
    "system_owned": false,
    "hidden": false
  },
  "resources": {
    "elasticsearch": [
      {
        "ref_id": "es-ref-id",
        "region": "ece-region",
        "plan": {
          "tiebreaker_topology": {
            "memory_per_node": 1024
          },
          "cluster_topology": [
            {
              "id": "hot_content",
              "instance_configuration_id": "custom.data",
              "zone_count": 2,
              "node_type": {
                "master": true,
                "data": true,
                "ingest": true
              },
              "elasticsearch": {
                "node_attributes": {
                  "data": "hot"
                }
              },
              "size": {
                "value": 8192,
                "resource": "memory"
              }
            },
            {
              "id": "warm",
              "instance_configuration_id": "data.highstorage",
              "zone_count": 1,
              "node_type": {
                "data": true,
                "ingest": false,
                "master": false
              },
              "elasticsearch": {
                "node_attributes": {
                  "data": "warm"
                }
              },
              "size": {
                "resource": "memory",
                "value": 0
              }
            },
            {
              "id": "coordinating",
              "zone_count": 1,
              "instance_configuration_id": "coordinating",
              "node_type": {
                "master": false,
                "data": false,
                "ingest": true
              },
              "size": {
                "value": 0,
                "resource": "memory"
              }
            },
            {
              "id": "master",
              "zone_count": 1,
              "instance_configuration_id": "custom.master",
              "node_type": {
                "master": true,
                "data": false,
                "ingest": false
              },
              "size": {
                "value": 0,
                "resource": "memory"
              }
            },
            {
              "id": "ml",
              "zone_count": 1,
              "instance_configuration_id": "custom.ml",
              "node_type": {
                "master": false,
                "data": false,
                "ingest": false,
                "ml": true
              },
              "size": {
                "value": 0,
                "resource": "memory"
              }
            }
          ],
          "elasticsearch": {
            "version": "7.17.0"
          },
          "deployment_template": {
            "id": "custom-template"
          }
        }
      }
    ],
    "kibana": [
      {
        "region": "ece-region",
        "ref_id": "kibana-ref-id",
        "elasticsearch_cluster_ref_id": "es-ref-id",
        "plan": {
          "cluster_topology": [
            {
              "instance_configuration_id": "kibana",
              "size": {
                "value": 1024,
                "resource": "memory"
              },
              "zone_count": 1,
              "kibana": {}
            }
          ],
          "kibana": {
            "version": "7.17.0"
          }
        }
      }
    ],
    "apm": [],
    "enterprise_search": []
  }
}
```

::::


After adding support for `node_roles` to the example deployment plan, the resulting plan should look similar to the following:

::::{dropdown} Example deployment plan with node_roles
```json
{
  "name": "Example deployment",
  "prune_orphans": true,
  "metadata": {
    "system_owned": false,
    "hidden": false
  },
  "resources": {
    "elasticsearch": [
      {
        "ref_id": "es-ref-id",
        "region": "ece-region",
        "plan": {
          "tiebreaker_topology": {
            "memory_per_node": 1024
          },
          "cluster_topology": [
            {
              "id": "hot_content",
              "instance_configuration_id": "custom.data",
              "zone_count": 2,
              "node_roles": [
                "master",
                "ingest",
                "data_hot",
                "data_content",
                "remote_cluster_client",
                "transform"
              ],
              "elasticsearch": {
                "node_attributes": {
                  "data": "hot"
                }
              },
              "size": {
                "value": 8192,
                "resource": "memory"
              }
            },
            {
              "id": "warm",
              "instance_configuration_id": "data.highstorage",
              "zone_count": 1,
              "node_roles": [
                "data_warm",
                "remote_cluster_client"
              ],
              "elasticsearch": {
                "node_attributes": {
                  "data": "warm"
                }
              },
              "size": {
                "resource": "memory",
                "value": 0
              }
            },
            {
              "id": "coordinating",
              "zone_count": 1,
              "instance_configuration_id": "coordinating",
              "node_roles": [
                "ingest",
                "remote_cluster_client"
              ],
              "size": {
                "value": 0,
                "resource": "memory"
              }
            },
            {
              "id": "master",
              "zone_count": 1,
              "instance_configuration_id": "custom.master",
              "node_roles": [
                "master",
                "remote_cluster_client"
              ],
              "size": {
                "value": 0,
                "resource": "memory"
              }
            },
            {
              "id": "ml",
              "zone_count": 1,
              "instance_configuration_id": "custom.ml",
              "node_roles": [
                "ml",
                "remote_cluster_client"
              ],
              "size": {
                "value": 0,
                "resource": "memory"
              }
            }
          ],
          "elasticsearch": {
            "version": "7.17.0"
          },
          "deployment_template": {
            "id": "custom-template"
          }
        }
      }
    ],
    "kibana": [
      {
        "region": "ece-region",
        "ref_id": "kibana-ref-id",
        "elasticsearch_cluster_ref_id": "es-ref-id",
        "plan": {
          "cluster_topology": [
            {
              "instance_configuration_id": "kibana",
              "size": {
                "value": 1024,
                "resource": "memory"
              },
              "zone_count": 1,
              "kibana": {}
            }
          ],
          "kibana": {
            "version": "7.17.0"
          }
        }
      }
    ],
    "apm": [],
    "enterprise_search": []
  }
}
```

::::
