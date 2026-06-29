---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-api-docs.html
description: Send Fleet API requests with the Kibana Console or cURL. Reference examples cover agent policies, integration policies, enrollment tokens, agent listing, KQL filters, and manual rollback.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Kibana Fleet APIs [fleet-api-docs]

This page provides cURL and {{kib}} Console examples for commonly used {{fleet}} APIs, including agent policies, integration policies, enrollment tokens, agent listing, KQL filtering, and agent rollback.

For full endpoint specifications, parameters, and response schemas, refer to the [Kibana API docs]({{kib-apis}}). For {{serverless-full}} projects, use the [Kibana Serverless API docs]({{kib-serverless-apis}}).


## Before you begin [fleet-api-before-you-begin]

You'll need:

* A running {{kib}} deployment or {{serverless-full}} project with {{fleet}} available
* The {{kib}} host URL for your deployment (for example, `https://my-kibana-host:9243`)
* Authentication credentials for {{kib}} API requests. API key authentication is recommended. For details, refer to [Authentication]({{kib-apis}}authentication).
* A {{kib}} user with the required {{fleet}} and {{integrations}} privileges. For details, refer to [Roles and privileges](/reference/fleet/fleet-roles-privileges.md).


## Using the Console [using-the-console]

You can run {{fleet}} API requests through the {{kib}} Console.

1. To open **Console**, find **Dev Tools** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In your request, prepend your {{fleet}} API endpoint with `kbn:`, for example:

    ```sh
    GET kbn:/api/fleet/agent_policies
    ```


For more details about using the {{kib}} Console, refer to [Run API requests](/explore-analyze/query-filter/tools/console.md).


## Create agent policy [create-agent-policy-api]

To create an agent policy in {{fleet}}, call `POST /api/fleet/agent_policies`.

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

1. Note the policy ID. You need it to add integration policies.



## Create integration policy [create-integration-policy-api]

To create an integration policy (also known as a package policy) and add it to an existing agent policy, call `POST /api/fleet/package_policies`.

::::{tip}
You can use the {{fleet}} API to [Create and customize an {{elastic-defend}} policy](/solutions/security/configure-elastic-defend/create-an-elastic-defend-policy-using-api.md).
::::


This cURL example creates an integration policy for Nginx and adds it to the agent policy you created in [Create agent policy](#create-agent-policy-api):

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

## List all {{agents}} [list-agents-api]

Use the [Get agents API]({{kib-apis}}operation/operation-get-fleet-agents) to retrieve a list of enrolled {{agents}}:

```shell
curl -X GET 'http://<user>:<pass>@<kibana url>/api/fleet/agents'
```

By default, a maximum of 10,000 agents are returned, with 20 agents listed per page.

### List all {{agents}} with `perPage` setting [list-agents-api-perpage]

The following query returns the same list, showing 10,000 {{agents}} per page:

```shell
curl -X GET 'http://<user>:<pass>@<kibana url>/api/fleet/agents?perPage=10000'
```

### List the next set of 10,000 {{agents}} [list-agents-api-next-set]
```{applies_to}
stack: ga 9.1+
```

Beginning with {{stack}} version 9.1, the previous query response includes a `nextSearchAfter` parameter that you can pass in a subsequent call, to retrieve the next page of 10,000 enrolled agents:

```shell
curl -X GET 'http://<user>:<pass>@<kibana url>/api/fleet/agents?perPage=10000&searchAfter=<nextSearchAfter>'
```

### List all {{agents}} for a point in time [list-agents-api-point-in-time]
```{applies_to}
stack: ga 9.1+
```

Beginning with {{stack}} version 9.1, you can also capture a point-in-time ID (`pitId`) parameter from the `Get agents API` response, and use that together with the `nextSearchAfter` parameter to capture the next page of 10,000 enrolled agents for a specific point in time.

Include the `openPit` and `pitKeepAlive` parameters in your initial request:

```shell
curl -X GET 'http://<user>:<pass>@<kibana url>/api/fleet/agents?perPage=10000&openPit=true&pitKeepAlive=5m'
```

You can then use the returned values in a new request to retrieve the next set of 10,000 agents:

```shell
curl -X GET 'http://<user>:<pass>@<kibana url>/api/fleet/agents?perPage=10000&searchAfter=<nextSearchAfter>&pitId=<pit id>&pitKeepAlive=5m'
```


## Filter results with KQL [filter-results-with-kql]

The following {{fleet}} list endpoints accept a `kuery` query parameter that takes a [{{kib}} Query Language (KQL)](elasticsearch://reference/query-languages/kql.md) string to filter results: agents (`GET /api/fleet/agents`), agent policies (`GET /api/fleet/agent_policies`), package policies (`GET /api/fleet/package_policies`), and enrollment tokens (`GET /api/fleet/enrollment_api_keys`). To check whether another endpoint accepts `kuery`, refer to its parameters in the [Kibana API docs]({{kib-apis}}).

**Agents and enrollment tokens** are stored in {{es}} system indices. Reference fields directly, with no prefix. This cURL example returns only the online agents:

```shell
curl --request GET \
  --url 'https://my-kibana-host:9243/api/fleet/agents?kuery=status:online' \
  --header 'Authorization: ApiKey yourbase64encodedkey' \
  --header 'kbn-xsrf: xx'
```

**Agent policies and package policies** are stored as saved objects. When a field path contains a dot, prefix it with the saved object type so the query parser reads it as a field name and not as a type. This cURL example returns only the package policies for the `nginx` integration:

```shell
curl --request GET \
  --url 'https://my-kibana-host:9243/api/fleet/package_policies?kuery=ingest-package-policies.package.name:nginx' \
  --header 'Authorization: ApiKey yourbase64encodedkey' \
  --header 'kbn-xsrf: xx'
```

::::{tip}
The accepted saved object type prefix can differ across deployments and endpoints. If a query returns a `KQLSyntaxError` stating that a key does not exist in a saved object index pattern, use the index pattern named in the error as your prefix. For example, if the error names `ingest-agent-policies`, query `ingest-agent-policies.name`.
::::

For the full query syntax, including wildcards, ranges, and boolean operators, refer to [{{kib}} Query Language (KQL)](elasticsearch://reference/query-languages/kql.md).


## Manually roll back an {{agent}} upgrade [agent-rollback-api]
```{applies_to}
stack: ga 9.3+
```

The manual rollback feature for {{agent}} lets you roll back to the previously installed version if the install artifacts are still available on disk (typically seven days after the upgrade).

To roll back a single agent, call `POST /api/fleet/agents/{agentID}/rollback`.

To roll back multiple agents, call `POST /api/fleet/agents/bulk_rollback`.

### Limitations for manual rollback [rollback-limitations-api]

These limitations apply for the manual rollback feature:

* Rollback is limited to the version running _before_ the upgrade. Both the pre-upgrade and post-upgrade versions must be 9.3.0 or later for this functionality to be available.
* Data required for the rollback is stored on disk for seven days, which can impact available disk space.
* Rollback must be performed within seven days of the upgrade. Rollback data is automatically cleaned up after seven days and becomes unavailable.
* Manual rollback is not available for system-managed packages such as DEB and RPM.
* Some data might be re-ingested after rollback.

#### Possible errors [rollback-errors-api]

If no version is available on disk to rollback to, you get an error.
This situation can happen if:

- The version you upgraded from is earlier than 9.3.0, as the feature is not supported for earlier versions.

- The rollback window has ended (typically more than seven days). When the rollback window ends, the files from the previous version are removed to free up disk space.


## Next steps [fleet-api-next-steps]

After you create agent and integration policies with the API:

* [Enroll {{agents}}](/reference/fleet/fleet-enrollment-tokens.md) using enrollment tokens from your agent policy
* [Manage {{agents}} in {{fleet}}](/reference/fleet/manage-elastic-agents-in-fleet.md) to monitor status and policy assignments
* [Create an agent policy without using the UI](/reference/fleet/create-policy-no-ui.md) for automation use cases


## Related pages [fleet-api-related-pages]

* [Kibana API docs]({{kib-apis}})
* [Run API requests](/explore-analyze/query-filter/tools/console.md)
* [Roles and privileges](/reference/fleet/fleet-roles-privileges.md)
* [Grant standalone {{agents}} access to {{es}}](/reference/fleet/grant-access-to-elasticsearch.md)
* [{{kib}} Query Language (KQL)](elasticsearch://reference/query-languages/kql.md)
