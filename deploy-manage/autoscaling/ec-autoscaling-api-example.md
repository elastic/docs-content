---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-autoscaling-api-example.html
---

# Autoscaling through the API [ec-autoscaling-api-example]

This example demonstrates how to use the {{ecloud}} RESTful API to create a deployment with autoscaling enabled.

The example deployment has a hot data and content tier, warm data tier, cold data tier, and a machine learning node, all of which will scale within the defined parameters. To learn about the autoscaling settings, check [Deployment autoscaling](../autoscaling.md) and [Autoscaling example](ec-autoscaling-example.md). For more information about using the {{ecloud}} API in general, check [RESTful API](asciidocalypse://docs/cloud/docs/reference/cloud-hosted/ec-api-restful.md).


## Requirements [ec_requirements] 

Note the following requirements when you run this API request:

* All Elasticsearch components must be included in the request, even if they are not enabled (that is, if they have a zero size). All components are included in this example.
* The request requires a format that supports data tiers. Specifically, all Elasticsearch components must contain the following properties:

    * `id`
    * `node_attributes`
    * `node_roles`

* The `size`, `autoscaling_min`, and `autoscaling_max` properties must be specified according to the following rules. This is because:

    * On data tiers only upward scaling is currently supported.
    * On machine learning nodes both upward and downward scaling is supported.
    * On all other components autoscaling is not currently supported.


$$$ec-autoscaling-api-example-requirements-table$$$
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

+ These rules match the behavior of the {{ecloud}} Console.

+ * The `elasticsearch` object must contain the property `"autoscaling_enabled": true`.


## API request example [ec_api_request_example] 

Run this example API request to create a deployment with autoscaling:


```sh
curl -XPOST \
-H 'Content-Type: application/json' \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/deployments" \
-d '
{
 "name": "my-first-autoscaling-deployment",
 "resources": {
   "elasticsearch": [
     {
       "ref_id": "main-elasticsearch",
       "region": "us-east-1",
       "plan": {
         "autoscaling_enabled": true,
         "cluster_topology": [
           {
             "id": "hot_content",
             "node_roles": [
               "remote_cluster_client",
               "data_hot",
               "transform",
               "data_content",
               "master",
               "ingest"
             ],
             "zone_count": 2,
             "elasticsearch": {
               "node_attributes": {
                 "data": "hot"
               },
               "enabled_built_in_plugins": []
             },
             "instance_configuration_id": "aws.data.highio.i3",
             "size": {
               "resource": "memory",
               "value": 8192
             },
             "autoscaling_max": {
               "value": 118784,
               "resource": "memory"
             }
           },
           {
             "id": "warm",
             "node_roles": [
               "data_warm",
               "remote_cluster_client"
             ],
             "zone_count": 2,
             "elasticsearch": {
               "node_attributes": {
                 "data": "warm"
               },
               "enabled_built_in_plugins": []
             },
             "instance_configuration_id": "aws.data.highstorage.d3",
             "size": {
               "value": 0,
               "resource": "memory"
             },
             "autoscaling_max": {
               "value": 118784,
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
             "instance_configuration_id": "aws.data.highstorage.d3",
             "size": {
               "value": 0,
               "resource": "memory"
             },
             "autoscaling_max": {
               "value": 59392,
               "resource": "memory"
             }
           },
           {
             "id": "coordinating",
             "zone_count": 2,
             "node_roles": [
               "ingest",
               "remote_cluster_client"
             ],
             "instance_configuration_id": "aws.coordinating.m5d",
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
             "zone_count": 3,
             "instance_configuration_id": "aws.master.r5d",
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
             "instance_configuration_id": "aws.ml.m5d",
             "autoscaling_min": {
               "value": 0,
               "resource": "memory"
             },
             "autoscaling_max": {
               "value": 61440,
               "resource": "memory"
             },
             "elasticsearch": {
               "enabled_built_in_plugins": []
             }
           }
         ],
         "elasticsearch": {
           "version": "7.11.0"
         },
         "deployment_template": {
           "id": "aws-io-optimized-v2"
         }
       },
       "settings": {
         "dedicated_masters_threshold": 6
       }
     }
   ],
   "kibana": [
     {
       "elasticsearch_cluster_ref_id": "main-elasticsearch",
       "region": "us-east-1",
       "plan": {
         "cluster_topology": [
           {
             "instance_configuration_id": "aws.kibana.r5d",
             "zone_count": 1,
             "size": {
               "resource": "memory",
               "value": 1024
             }
           }
         ],
         "kibana": {
           "version": "7.11.0"
         }
       },
       "ref_id": "main-kibana"
     }
   ],
   "apm": [
     {
       "elasticsearch_cluster_ref_id": "main-elasticsearch",
       "region": "us-east-1",
       "plan": {
         "cluster_topology": [
           {
             "instance_configuration_id": "aws.apm.r5d",
             "zone_count": 1,
             "size": {
               "resource": "memory",
               "value": 512
             }
           }
         ],
         "apm": {
           "version": "7.11.0"
         }
       },
       "ref_id": "main-apm"
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


