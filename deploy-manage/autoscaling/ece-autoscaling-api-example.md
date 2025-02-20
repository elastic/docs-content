---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-autoscaling-api-example.html
---

# Autoscaling through the API [ece-autoscaling-api-example]

This example demonstrates how to use the Elastic Cloud Enterprise RESTful API to create a deployment with autoscaling enabled.

The example deployment has a hot data and content tier, warm data tier, cold data tier, and a machine learning node, all of which will scale within the defined parameters. To learn about the autoscaling settings, check [Deployment autoscaling](../autoscaling.md) and [Autoscaling example](ece-autoscaling-example.md). For more information about using the Elastic Cloud Enterprise API in general, check [RESTful API](asciidocalypse://docs/cloud/docs/reference/cloud/cloud-enterprise/restful-api.md).


## Requirements [ece_requirements_3] 

Note the following requirements when you run this API request:

* On Elastic Cloud Enterprise, autoscaling is supported for custom deployment templates on version 2.12 and above. To learn more, refer to [Updating custom templates to support `node_roles` and autoscaling](../deploy/cloud-enterprise/ce-add-support-for-node-roles-autoscaling.md).
* All Elasticsearch components must be included in the request, even if they are not enabled (that is, if they have a zero size). All components are included in this example.
* The request requires a format that supports data tiers. Specifically, all Elasticsearch components must contain the following properties:

    * `id`
    * `node_attributes`
    * `node_roles`

* The `size`, `autoscaling_min`, and `autoscaling_max` properties must be specified according to the following rules. This is because:

    * On data tiers only upward scaling is currently supported.
    * On machine learning nodes both upward and downward scaling is supported.
    * On all other components autoscaling is not currently supported.


$$$ece-autoscaling-api-example-requirements-table$$$
+

|     |     |     |     |
| --- | --- | --- | --- |
|  | `size` | `autoscaling_min` | `autoscaling_max` |
| data tier | ✓ | ✕ | ✓ |
| machine learning node | ✕ | ✓ | ✓ |
| coordinating and master nodes | ✓ | ✕ | ✕ |
| Kibana | ✓ | ✕ | ✕ |
| APM | ✓ | ✕ | ✕ |

+

+ ✓ = Include the property.

+ ✕ = Do not include the property.

+ These rules match the behavior of the Elastic Cloud Enterprise user console.

+ * The `elasticsearch` object must contain the property `"autoscaling_enabled": true`.


## API request example [ece_api_request_example] 

Run this example API request to create a deployment with autoscaling:

```sh
curl -k -X POST -H "Authorization: ApiKey $ECE_API_KEY" https://$COORDINATOR_HOST:12443/api/v1/deployments -H 'content-type: application/json' -d '
{
 "name": "my-first-autoscaling-deployment",
 "resources": {
   "elasticsearch": [
     {
       "ref_id": "main-elasticsearch",
       "region": "ece-region",
       "plan": {
         "autoscaling_enabled": true,
         "cluster_topology": [
           {
             "id": "hot_content",
             "node_roles": [
               "master",
               "ingest",
               "remote_cluster_client",
               "data_hot",
               "transform",
               "data_content"
             ],
             "zone_count": 1,
             "elasticsearch": {
               "node_attributes": {
                 "data": "hot"
               },
               "enabled_built_in_plugins": []
             },
             "instance_configuration_id": "data.default",
             "size": {
               "value": 4096,
               "resource": "memory"
             },
             "autoscaling_max": {
               "value": 2097152,
               "resource": "memory"
             }
           },
           {
             "id": "warm",
             "node_roles": [
               "data_warm",
               "remote_cluster_client"
             ],
             "zone_count": 1,
             "elasticsearch": {
               "node_attributes": {
                 "data": "warm"
               },
               "enabled_built_in_plugins": []
             },
             "instance_configuration_id": "data.highstorage",
             "size": {
               "value": 0,
               "resource": "memory"
             },
             "autoscaling_max": {
               "value": 2097152,
               "resource": "memory"
             }
           },
           {
             "id": "cold",
             "node_roles": [
               "data_cold",
               "remote_cluster_client"
             ],
             "zone_count": 1,
             "elasticsearch": {
               "node_attributes": {
                 "data": "cold"
               },
               "enabled_built_in_plugins": []
             },
             "instance_configuration_id": "data.highstorage",
             "size": {
               "value": 0,
               "resource": "memory"
             },
             "autoscaling_max": {
               "value": 2097152,
               "resource": "memory"
             }
           },
           {
             "id": "coordinating",
             "node_roles": [
               "ingest",
               "remote_cluster_client"
             ],
             "zone_count": 1,
             "instance_configuration_id": "coordinating",
             "size": {
               "value": 0,
               "resource": "memory"
             },
             "elasticsearch": {
               "enabled_built_in_plugins": []
             }
           },
           {
             "id": "master",
             "node_roles": [
               "master"
             ],
             "zone_count": 1,
             "instance_configuration_id": "master",
             "size": {
               "value": 0,
               "resource": "memory"
             },
             "elasticsearch": {
               "enabled_built_in_plugins": []
             }
           },
           {
             "id": "ml",
             "node_roles": [
               "ml",
               "remote_cluster_client"
             ],
             "zone_count": 1,
             "instance_configuration_id": "ml",
             "autoscaling_min": {
               "value": 0,
               "resource": "memory"
             },
             "autoscaling_max": {
               "value": 2097152,
               "resource": "memory"
             },
             "elasticsearch": {
               "enabled_built_in_plugins": []
             }
           }
         ],
         "elasticsearch": {
           "version": "8.13.1"
         },
         "deployment_template": {
           "id": "default"
         }
       },
       "settings": {
         "dedicated_masters_threshold": 6
       }
     }
   ],
   "kibana": [
     {
       "ref_id": "main-kibana",
       "elasticsearch_cluster_ref_id": "main-elasticsearch",
       "region": "ece-region",
       "plan": {
         "zone_count": 1,
         "cluster_topology": [
           {
             "instance_configuration_id": "kibana",
             "size": {
               "value": 1024,
               "resource": "memory"
             },
             "zone_count": 1
           }
         ],
         "kibana": {
           "version": "8.13.1"
         }
       }
     }
   ],
   "apm": [
     {
       "ref_id": "main-apm",
       "elasticsearch_cluster_ref_id": "main-elasticsearch",
       "region": "ece-region",
       "plan": {
         "cluster_topology": [
           {
             "instance_configuration_id": "apm",
             "size": {
               "value": 512,
               "resource": "memory"
             },
             "zone_count": 1
           }
         ],
         "apm": {
           "version": "8.13.1"
         }
       }
     }
   ],
   "enterprise_search": []
 }
}
'
```


::::{note} 
Although autoscaling can scale some tiers by CPU, the primary measurement of tier size is memory. Limits on tier size are in terms of memory.
::::


