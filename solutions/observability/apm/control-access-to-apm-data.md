---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-spaces.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
---

# Control access to APM data [apm-spaces]

Starting in version 8.2.0, the Applications UI is [Kibana space](/deploy-manage/manage-spaces.md) aware. This allows you to separate your data—and access to that data—by team, use case, service environment, or any other filter that you choose.

To take advantage of this feature, your APM data needs to be written to different data streams. One way to accomplish this is with different namespaces. For example, you can send production data to an APM integration with a namespace of `production`, while sending staging data to a different APM integration with a namespace of `staging`.

Multiple APM integration instances is not required though. The simplest way to take advantage of this feature is by creating filtered aliases. See the guide below for more information.

## Guide: Separate staging and production data [apm-spaces-example]

This guide will explain how to separate your staging and production data. This can be helpful to either remove noise when troubleshooting a production issue, or to create more granular access control for certain data.

This guide assumes that you:

* Are sending both staging and production APM data to an {{es}} cluster.
* Have configured the `environment` variable in your APM agent configurations. This variable sets the `service.environment` field in APM documents. You should have documents where `service.environment: production` and `service.environment: staging`. If this field is empty, see [service environment filter](/solutions/observability/apm/filter-data.md#apm-filter-your-data-service-environment-filter) to learn how to set this value.

### Step 1: Create filtered aliases [_step_1_create_filtered_aliases]

The Applications UI uses index patterns to query your APM data. An index pattern can match data streams, indices, and/or aliases. The default values are:

| Index setting | Default index pattern |
| --- | --- |
| Error | `logs-apm*` |
| Span/Transaction | `traces-apm*` |
| Metrics | `metrics-apm*` |

::::{note}
The default index settings also query the `apm-*` data view. This data view matches APM data shipped in earlier versions of APM (prior to v8.0).
::::

Instead of querying the default APM data views, we can create filtered aliases for the Applications UI to query. A filtered alias is a secondary name for a group of data streams that has a user-defined filter to limit the documents that the alias can access.

To separate `staging` and `production` APM data, we’d need to create six filtered aliases—three aliases for each service environment:

| Index setting | `production` env | `staging` env |
| --- | --- | --- |
| Error | `production-logs-apm` | `staging-logs-apm` |
| Span/Transaction | `production-traces-apm` | `staging-traces-apm` |
| Metrics | `production-metrics-apm` | `staging-metrics-apm` |

The `production-<event>-apm` aliases will contain a filter that only provides access to documents where the `service.environment` is `production`. Similarly, the `staging-<event>-apm` aliases will contain a filter that only provides access to documents where the `service.environment` is `staging`.

To create these six filtered aliases, use the {{es}} [Aliases API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-update-aliases). In {{kib}}, open **Dev Tools** and run the following POST requests.

::::{dropdown} traces-apm* production alias example
```console
POST /_aliases?pretty
{
  "actions": [
    {
      "add": {
        "index": "traces-apm*", <1>
        "alias": "production-traces-apm", <2>
        "filter": {
          "term": {
            "service.environment": {
              "value": "production" <3>
            }
          }
        }
      }
    }
  ]
}
```

1. This example matches the APM traces data stream
2. The alias must not match the default APM index (`traces-apm*,apm-*`)
3. Only match documents where `service.environment: production`

::::

::::{dropdown} logs-apm* production alias example
```console
POST /_aliases?pretty
{
  "actions": [
    {
      "add": {
        "index": "logs-apm*", <1>
        "alias": "production-logs-apm", <2>
        "filter": {
          "term": {
            "service.environment": {
              "value": "production" <3>
            }
          }
        }
      }
    }
  ]
}
```

1. This example matches the APM logs data stream
2. The alias must not match the default APM index (`logs-apm*,apm-*`)
3. Only match documents where `service.environment: production`

::::

::::{dropdown} metrics-apm* production alias example
```console
POST /_aliases?pretty
{
  "actions": [
    {
      "add": {
        "index": "metrics-apm*", <1>
        "alias": "production-metrics-apm", <2>
        "filter": {
          "term": {
            "service.environment": {
              "value": "production" <3>
            }
          }
        }
      }
    }
  ]
}
```

1. This example matches the APM metrics data stream
2. The alias must not match the default APM index (`metrics-apm*,apm-*`)
3. Only match documents where `service.environment: production`

::::

::::{dropdown} traces-apm* staging alias example
```console
POST /_aliases?pretty
{
  "actions": [
    {
      "add": {
        "index": "traces-apm*", <1>
        "alias": "staging-traces-apm", <2>
        "filter": {
          "term": {
            "service.environment": {
              "value": "staging" <3>
            }
          }
        }
      }
    }
  ]
}
```

1. This example matches the APM traces data stream
2. The alias must not match the default APM index (`traces-apm*,apm-*`)
3. Only match documents where `service.environment: staging`

::::

::::{dropdown} logs-apm* staging alias example
```console
POST /_aliases?pretty
{
  "actions": [
    {
      "add": {
        "index": "logs-apm*", <1>
        "alias": "staging-logs-apm", <2>
        "filter": {
          "term": {
            "service.environment": {
              "value": "staging" <3>
            }
          }
        }
      }
    }
  ]
}
```

1. This example matches the APM logs data stream
2. The alias must not match the default APM index (`logs-apm*,apm-*`)
3. Only match documents where `service.environment: staging`

::::

::::{dropdown} metrics-apm* staging alias example
```console
POST /_aliases?pretty
{
  "actions": [
    {
      "add": {
        "index": "metrics-apm*", <1>
        "alias": "staging-metrics-apm", <2>
        "filter": {
          "term": {
            "service.environment": {
              "value": "staging" <3>
            }
          }
        }
      }
    }
  ]
}
```

1. This example matches the APM metrics data stream
2. The alias must not match the default APM index (`metrics-apm*,apm-*`)
3. Only match documents where `service.environment: staging`

::::

### Step 2: Create {{kib}} spaces [_step_2_create_kib_spaces]

Next, you’ll need to create a {{kib}} space for each service environment. Open the **Spaces** management page from the navigation menu or using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). To create a new space, click **Create a space**. For this guide, we’ve created two Kibana spaces, one named `production` and one named `staging`.

See [Kibana spaces](/deploy-manage/manage-spaces.md) for more information on creating a space.

### Step 3: Update APM index settings in each space [_step_3_update_apm_index_settings_in_each_space]

Now we can change the default data views that the Applications UI queries in each space.

Open the Applications UI and navigate to **Settings** → **Indices**. Use the table below to update your settings for each space. The values in each column match the names of the filtered aliases we created in step one.

| Index setting | `production` space | `staging` space |
| --- | --- | --- |
| Error indices | `production-logs-apm` | `staging-logs-apm` |
| Span indices | `production-traces-apm` | `staging-traces-apm` |
| Transaction indices | `production-traces-apm` | `staging-traces-apm` |
| Metrics indices | `production-metrics-apm` | `staging-metrics-apm` |

### Step 4: Create {{kib}} access roles [_step_4_create_kib_access_roles]

Open the **Roles** management page from the navigation menu or using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Click **Create role**.

You’ll need to create two roles: one for `staging` users (we’ll call this role `staging_apm_viewer`) and one for `production` users (we’ll call this role `production_apm_viewer`).

Using the table below, assign each role the following privileges:

| Privileges | `production_apm_viewer` | `staging_apm_viewer` |
| --- | --- | --- |
| Index privileges | index: `production-*-apm`, privilege: `read` | index: `staging-*-apm`, privilege: `read` |
| Kibana privileges | space: `production`, feature privileges: `APM and User Experience: read` | space: `staging`, feature privileges: `APM and User Experience: read` |

:::{image} /solutions/images/observability-apm-roles-config.png
:alt: APM role config example
:screenshot:
:::

Alternatively, you can use the {{es}} [Create or update roles API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-role):

::::{dropdown} Create a production_apm_viewer role
This request creates a `production_apm_viewer` role:

```console
POST /_security/role/production_apm_viewer
{
  "cluster": [ ],
  "indices": [
    {
      "names": ["production-*-apm"], <1>
      "privileges": ["read"]
    }
  ],
  "applications": [
    {
      "application" : "kibana-.kibana",
      "privileges" : [
        "feature_apm.read" <2>
      ],
      "resources" : [
        "space:production" <3>
      ]
    }
  ]
}
```

1. This data view matches all of the production aliases created in step one.
2. Assigns `read` privileges for the Applications and User Experience UIs.
3. Provides access to the space named `production`.

::::

::::{dropdown} Create a staging_apm_viewer role
This request creates a `staging_apm_viewer` role:

```console
POST /_security/role/staging_apm_viewer
{
  "cluster": [ ],
  "indices": [
    {
      "names": ["staging-*-apm"], <1>
      "privileges": ["read"]
    }
  ],
  "applications": [
    {
      "application" : "kibana-.kibana",
      "privileges" : [
        "feature_apm.read" <2>
      ],
      "resources" : [
        "space:staging" <3>
      ]
    }
  ]
}
```

1. This data view matches all of the staging aliases created in step one.
2. Assigns `read` privileges for the Applications and User Experience UIs.
3. Provides access to the space named `staging`.

::::

### Step 5: Assign users to roles [_step_5_assign_users_to_roles]

The last thing to do is assign users to the newly created roles above. Users will only have access to the data within the spaces that they are granted.

For information on how to create users and assign them roles with the {{kib}} UI, see [](/deploy-manage/users-roles/cluster-or-deployment-auth/quickstart.md).

Alternatively, you can use the {{es}} [Create or update users API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-user).

This example creates a new user and assigns them the `production_apm_viewer` role created in the previous step. This user will only have access to the production space and data with a `service.environment` of `production`. Remember to change the `password`, `full_name`, and `email` fields.

```console
POST /_security/user/production-apm-user
{
  "password" : "l0ng-r4nd0m-p@ssw0rd",
  "roles" : [ "production_apm_viewer" ], <1>
  "full_name" : "Jane Production Smith",
  "email" : "janesmith@example.com"
}
```

1. Assigns the previously created `production_apm_viewer` role.

This example creates a new user and assigns them the `staging_apm_viewer` role created in the previous step. This user will only have access to the staging space and data with a `service.environment` of `staging`. Remember to change the `password`, `full_name`, and `email` fields.

```console
POST /_security/user/staging-apm-user
{
  "password" : "l0ng-r4nd0m-p@ssw0rd",
  "roles" : [ "staging_apm_viewer" ], <1>
  "full_name" : "John Staging Doe",
  "email" : "johndoe@example.com"
}
```

1. Assigns the previously created `staging_apm_viewer` role.

### Step 6: Marvel [_step_6_marvel]

That’s it! Head back to the Applications UI and marvel at your space-specific data.
