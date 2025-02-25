---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-api-docs.html
---

# Kibana Fleet APIs [fleet-api-docs]

You can find details for all available {{fleet}} API endpoints in our generated [Kibana API docs](https://www.elastic.co/docs/api/doc/kibana).

In this section, we provide examples of some commonly used {{fleet}} APIs.


## Using the Console [using-the-console]

You can run {{fleet}} API requests through the {{kib}} Console.

1. Open the {{kib}} menu and go to **Management → Dev Tools**.
2. In your request, prepend your {{fleet}} API endpoint with `kbn:`, for example:

    ```sh
    GET kbn:/api/fleet/agent_policies
    ```


For more detail about using the {{kib}} Console refer to [Run API requests](/explore-analyze/query-filter/tools/console.md).


## Authentication [authentication]

Authentication is required to send {{fleet}} API requests. For more information, refer to [Authentication](https://www.elastic.co/docs/api/doc/kibana/authentication).


## Create agent policy [create-agent-policy-api]

To create a new agent policy in {{fleet}}, call `POST /api/fleet/agent_policies`.

This cURL example creates an agent policy called `Agent policy 1` in the default namespace.

```shell
curl --request POST \
  --url 'https://my-kibana-host:9243/api/fleet/agent_policies?sys_monitoring=true' \
  --header 'Accept: */*' \
  --header 'Authorization: ApiKey yourbase64encodedkey' \
  --header 'Cache-Control: no-cache' \
  --header 'Connection: keep-alive' \
  --header 'Content-Type: application/json' \
  --header 'kbn-xsrf: xxx' \
  --data '{
  "name": "Agent policy 1",
  "description": "",
  "namespace": "default",
  "monitoring_enabled": [
    "logs",
    "metrics"
  ]
}'
```

::::{admonition}
To save time, you can use {{kib}} to generate the API request, then run it from the Dev Tools console.

1. Go to **{{fleet}} → Agent policies**.
2. Click **Create agent policy** and give the policy a name.
3. Click **Preview API request**.
4. Click **Open in Console** and run the request.

::::


Example response:

```shell
{
  "item": {
    "id": "2b820230-4b54-11ed-b107-4bfe66d759e4", <1>
    "name": "Agent policy 1",
    "description": "",
    "namespace": "default",
    "monitoring_enabled": [
      "logs",
      "metrics"
    ],
    "status": "active",
    "is_managed": false,
    "revision": 1,
    "updated_at": "2022-10-14T00:07:19.763Z",
    "updated_by": "1282607447",
    "schema_version": "1.0.0"
  }
}
```

1. Make a note of the policy ID. You’ll need the policy ID to add integration policies.



## Create integration policy [create-integration-policy-api]

To create an integration policy (also known as a package policy) and add it to an existing agent policy, call `POST /api/fleet/package_policies`.

::::{tip}
You can use the {{fleet}} API to [Create and customize an {{elastic-defend}} policy](/reference/security/elastic-defend/create-defend-policy-api.md).
::::


This cURL example creates an integration policy for Nginx and adds it to the agent policy created in the previous example:

```shell
curl --request POST \
  --url 'https://my-kibana-host:9243/api/fleet/package_policies' \
  --header 'Authorization: ApiKey yourbase64encodedkey' \
  --header 'Content-Type: application/json' \
  --header 'kbn-xsrf: xx' \
  --data '{
  "name": "nginx-demo-123",
  "policy_id": "2b820230-4b54-11ed-b107-4bfe66d759e4",
  "package": {
    "name": "nginx",
    "version": "1.5.0"
  },
  "inputs": {
    "nginx-logfile": {
      "streams": {
        "nginx.access": {
          "vars": {
            "tags": [
              "test"
            ]
          }
        },
        "nginx.error": {
          "vars": {
            "tags": [
              "test"
            ]
          }
        }
      }
    }
  }
}'
```

::::{admonition}
* To save time, you can use {{kib}} to generate the API call, then run it from the Dev Tools console.

    1. Go to **Integrations**, select an {{agent}} integration, and click **Add <Integration>**.
    2. Configure the integration settings and select which agent policy to use.
    3. Click **Preview API request**.

        If you’re creating the integration policy for a new agent policy, the preview shows two requests: one to create the agent policy, and another to create the integration policy.

    4. Click **Open in Console** and run the request (or requests).

* To find out which inputs, streams, and variables are available for an integration, go to **Integrations**, select an {{agent}} integration, and click **API reference**.

::::


Example response (truncated for readability):

```shell
{
   "item" : {
      "created_at" : "2022-10-15T00:41:28.594Z",
      "created_by" : "1282607447",
      "enabled" : true,
      "id" : "92f33e57-3165-4dcd-a1d5-f01c8ffdcbcd",
      "inputs" : [
         {
            "enabled" : true,
            "policy_template" : "nginx",
            "streams" : [
               {
                  "compiled_stream" : {
                     "exclude_files" : [
                        ".gz$"
                     ],
                     "ignore_older" : "72h",
                     "paths" : [
                        "/var/log/nginx/access.log*"
                     ],
                     "processors" : [
                        {
                           "add_locale" : null
                        }
                     ],
                     "tags" : [
                        "test"
                     ]
                  },
                  "data_stream" : {
                     "dataset" : "nginx.access",
                     "type" : "logs"
                  },
                  "enabled" : true,
                  "id" : "logfile-nginx.access-92f33e57-3165-4dcd-a1d5-f01c8ffdcbcd",
                  "release" : "ga",
                  "vars" : {
                     "ignore_older" : {
                        "type" : "text",
                        "value" : "72h"
                     },
                     "paths" : {
                        "type" : "text",
                        "value" : [
                           "/var/log/nginx/access.log*"
                        ]
                     },
                     "preserve_original_event" : {
                        "type" : "bool",
                        "value" : false
                     },
                     "processors" : {
                        "type" : "yaml"
                     },
                     "tags" : {
                        "type" : "text",
                        "value" : [
                           "test"
                        ]
                     }
                  }
               },
               {
                  "compiled_stream" : {
                     "exclude_files" : [
                        ".gz$"
                     ],
                     "ignore_older" : "72h",
                     "multiline" : {
                        "match" : "after",
                        "negate" : true,
                        "pattern" : "^\\d{4}\\/\\d{2}\\/\\d{2} "
                     },
                     "paths" : [
                        "/var/log/nginx/error.log*"
                     ],
                     "processors" : [
                        {
                           "add_locale" : null
                        }
                     ],
                     "tags" : [
                        "test"
                     ]
                  },
                  "data_stream" : {
                     "dataset" : "nginx.error",
                     "type" : "logs"
                  },
                  "enabled" : true,
                  "id" : "logfile-nginx.error-92f33e57-3165-4dcd-a1d5-f01c8ffdcbcd",
                  "release" : "ga",
                  "vars" : {
                     "ignore_older" : {
                        "type" : "text",
                        "value" : "72h"
                     },
                     "paths" : {
                        "type" : "text",
                        "value" : [
                           "/var/log/nginx/error.log*"
                        ]
                     },
                     "preserve_original_event" : {
                        "type" : "bool",
                        "value" : false
                     },
                     "processors" : {
                        "type" : "yaml"
                     },
                     "tags" : {
                        "type" : "text",
                        "value" : [
                           "test"
                        ]
                     }
                  }
               }
            ],
            "type" : "logfile"
         },
         ...
         {
            "enabled" : true,
            "policy_template" : "nginx",
            "streams" : [
               {
                  "compiled_stream" : {
                     "hosts" : [
                        "http://127.0.0.1:80"
                     ],
                     "metricsets" : [
                        "stubstatus"
                     ],
                     "period" : "10s",
                     "server_status_path" : "/nginx_status"
                  },
                  "data_stream" : {
                     "dataset" : "nginx.stubstatus",
                     "type" : "metrics"
                  },
                  "enabled" : true,
                  "id" : "nginx/metrics-nginx.stubstatus-92f33e57-3165-4dcd-a1d5-f01c8ffdcbcd",
                  "release" : "ga",
                  "vars" : {
                     "period" : {
                        "type" : "text",
                        "value" : "10s"
                     },
                     "server_status_path" : {
                        "type" : "text",
                        "value" : "/nginx_status"
                     }
                  }
               }
            ],
            "type" : "nginx/metrics",
            "vars" : {
               "hosts" : {
                  "type" : "text",
                  "value" : [
                     "http://127.0.0.1:80"
                  ]
               }
            }
         }
      ],
      "name" : "nginx-demo-123",
      "namespace" : "default",
      "package" : {
         "name" : "nginx",
         "title" : "Nginx",
         "version" : "1.5.0"
      },
      "policy_id" : "d625b2e0-4c21-11ed-9426-31f0877749b7",
      "revision" : 1,
      "updated_at" : "2022-10-15T00:41:28.594Z",
      "updated_by" : "1282607447",
      "version" : "WzI5OTAsMV0="
   }
}
```


## Get enrollment tokens [get-enrollment-token-api]

To get a list of valid enrollment tokens from {{fleet}}, call `GET /api/fleet/enrollment_api_keys`.

This cURL example returns a list of enrollment tokens.

```shell
curl --request GET \
  --url 'https://my-kibana-host:9243/api/fleet/enrollment_api_keys' \
  --header 'Authorization: ApiKey N2VLRDA0TUJIQ05MaGYydUZrN1Y6d2diMUdwSkRTWGFlSm1rSVZlc2JGQQ==' \
  --header 'Content-Type: application/json' \
  --header 'kbn-xsrf: xx'
```

Example response (formatted for readability):

```shell
{
   "items" : [
      {
         "active" : true,
         "api_key" : "QlN2UaA0TUJlMGFGbF8IVkhJaHM6eGJjdGtyejJUUFM0a0dGSwlVSzdpdw==",
         "api_key_id" : "BSvR04MBe0aFl_HVHIhs",
         "created_at" : "2022-10-14T00:07:21.420Z",
         "id" : "39703af4-5945-4232-90ae-3161214512fa",
         "name" : "Default (39703af4-5945-4232-90ae-3161214512fa)",
         "policy_id" : "2b820230-4b54-11ed-b107-4bfe66d759e4"
      },
      {
         "active" : true,
         "api_key" : "Yi1MSTA2TUJIQ05MaGYydV9kZXQ5U2dNWFkyX19sWEdSemFQOUfzSDRLZw==",
         "api_key_id" : "b-LI04MBHCNLhf2u_det",
         "created_at" : "2022-10-13T23:58:29.266Z",
         "id" : "e4768bf2-55a6-433f-a540-51d4ca2d34be",
         "name" : "Default (e4768bf2-55a6-433f-a540-51d4ca2d34be)",
         "policy_id" : "ee37a8e0-4b52-11ed-b107-4bfe66d759e4"
      },
      {
         "active" : true,
         "api_key" : "b3VLbjA0TUJIQ04MaGYydUk1Z3Q6VzhMTTBITFRTmnktRU9IWDaXWnpMUQ==",
         "api_key_id" : "luKn04MBHCNLhf2uI5d4",
         "created_at" : "2022-10-13T23:21:30.707Z",
         "id" : "d18d2918-bb10-44f2-9f98-df5543e21724",
         "name" : "Default (d18d2918-bb10-44f2-9f98-df5543e21724)",
         "policy_id" : "c3e31e80-4b4d-11ed-b107-4bfe66d759e4"
      },
      {
         "active" : true,
         "api_key" : "V3VLRTa0TUJIQ05MaGYydVMx4S06WjU5dsZ3YzVRSmFUc5xjSThImi1ydw==",
         "api_key_id" : "WuKE04MBHCNLhf2uS1E-",
         "created_at" : "2022-10-13T22:43:27.139Z",
         "id" : "aad31121-df89-4f57-af84-7c43f72640ee",
         "name" : "Default (aad31121-df89-4f57-af84-7c43f72640ee)",
         "policy_id" : "72fcc4d0-4b48-11ed-b107-4bfe66d759e4"
      },
   ],
   "page" : 1,
   "perPage" : 20,
   "total" : 4
}
```
