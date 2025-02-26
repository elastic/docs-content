---
navigation_title: "Use feature roles"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-feature-roles.html
---



# Create and assign feature roles to APM Server users [apm-feature-roles]


::::{note}
Kibana custom roles are *not* compatible with [{{serverless-full}}](https://docs.elastic.co/serverless).

::::


Manage access on a feature-by-feature basis by creating several custom feature-related *roles* and assigning one or more of these roles to each *user or group* based on which features they need to access.

::::{tip}
A *role* identifies a set of permissions that translates to privileges on resources. You can associate a *user or group* with an arbitrary number of roles. The total set of permissions that a user has is defined by the union of the permissions in all its roles.

In general, there are three types of privileges you’ll work with when creating roles:

* **{{es}} cluster privileges**: Manage the actions a user can perform against your cluster.
* **{{es}} index privileges**: Control access to the data in specific indices of your cluster.
* **{{kib}} space privileges**: Grant users write or read access to features and apps within {{kib}}.

::::


The following are common roles that APM Server users might need:

* [**Writer role**](#apm-privileges-to-publish-events): Allows a user to publish events collected by APM Server, which is **required** to write to {{es}}.
* [**Central configuration management role**](#apm-privileges-agent-central-config): Allows a user to view APM Agent central configurations, which is **required** when [central configuration management](apm-agent-central-configuration.md) is enabled (it is enabled by default).
* [**Monitoring role**](#apm-privileges-to-publish-monitoring): Allows a user to publish monitoring data, view monitoring data, or both.
* [**RUM source mapping role**](#apm-privileges-rum-source-mapping): Allows a user to read RUM source maps.

::::{admonition} Example: Assigning multiple roles to an APM Server user
If you want to create an APM Server user who can use the Elastic APM Real User Monitoring (RUM) JavaScript Agent to ingest data from a frontend application and you use central configuration to manage APM agents, you would need to assign these three roles to the user:

* [Writer role](#apm-privileges-to-publish-events)
* [Central configuration management role](#apm-privileges-agent-central-config)
* [RUM source mapping role](#apm-privileges-rum-source-mapping)

::::



## Create a *writer* role [apm-privileges-to-publish-events]

APM users that publish events to {{es}} *must* have privileges to write to APM data streams.

::::{note}
This is not needed when APM Server doesn’t write to {{es}} directly. For example, in some cases you may configure APM Server to write to another output like Logstash, Kafka, or any other output supported by libbeat. In these cases, different authentication credentials will need to be passed to [`apm-server.agent.config.elasticsearch`](configure-apm-agent-central-configuration.md#apm-agent-config-elasticsearch).

::::


To grant an APM Server user the required privileges for writing events to {{es}}:

1. Create a **general writer role**, called something like `apm_writer`, that has the following privileges:

    | Type | Privilege | Purpose |
    | --- | --- | --- |
    | Index | `auto_configure` on `traces-apm*`, `logs-apm*`, and `metrics-apm*` indices | Permits auto-creation of indices and data streams |
    | Index | `create_doc` on `traces-apm*`, `logs-apm*`, and `metrics-apm*` indices | Write events into {{es}} |
    | Cluster | `monitor` | Allows cluster UUID checks, which are performed as part of APM server startup preconditionsif [Elasticsearch security](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/security-settings.md) is enabled (it is enabled by default), and allows a license check, which is required if [tail-based sampling](transaction-sampling.md#apm-tail-based-sampling) is enabled. |


::::{note}
If you have explicitly disabled Elastic security *and* you are *not* using tail-based sampling, the `monitor` privilege may not be necessary.
::::


1. Assign the **general writer role** to APM Server users who need to publish APM data.

::::{note}
Assign additional APM feature roles to users as needed including the *Central configuration management role*, which is [required in most cases](#apm-central-config-role-note).

::::



## Create a *central configuration management* role [apm-privileges-agent-central-config]

::::{important}
:name: apm-central-config-role-note

The privileges included in this role are **required** for all users when [central configuration management](apm-agent-central-configuration.md) is enabled (it is enabled by default). You need this role unless central configuration management has been explicitly disabled in the Applications UI.

::::


$$$apm-privileges-agent-central-config-server$$$
APM Server acts as a proxy between your APM agents and the Applications UI. The Applications UI communicates any changed settings to APM Server so that your agents only need to poll the Server to determine which central configuration settings have changed.

To create a role with the required privileges for managing central configuration in {{es}} without {{kib}}, you must use the [Roles API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-role) (the required privileges can’t be assigned to a role in Kibana):

```console
POST /_security/role/apm_agentcfg
{
 "description": "Allow APM Server to manage central configurations in Elasticsearch.",
 "indices": [
   {
     "names": [".apm-agent-configuration"],
     "privileges": ["read"],
     "allow_restricted_indices": true
   }
 ]
}
```

The previous privileges should be sufficient for APM agent central configuration to work properly as long as APM Server communicates with {{es}} successfully. If it fails, it may fallback to read agent central configuration through {{kib}} if configured, which requires the following privileges:

| Type | Privilege | Purpose |
| --- | --- | --- |
| Spaces | `Read` on Applications UI | Allow APM Server to manage central configurations via the Applications UI |

::::{note}
Assign additional APM feature roles to users as needed including the *Writer role*, which is [required in most cases](#apm-privileges-to-publish-events).

::::


::::{tip}
Looking for privileges and roles needed to use central configuration from the Applications UI or APM UI API? See [Applications UI central configuration user](applications-ui-central-config-user.md).
::::



## Create a *monitoring* role [apm-privileges-to-publish-monitoring]

{{es-security-features}} provides built-in users and roles for publishing and viewing monitoring data. The privileges and roles needed to publish monitoring data depend on the method used to collect that data.

* [Publish monitoring data](#apm-privileges-to-publish-monitoring-write)

    * [Internal collection](#apm-privileges-to-publish-monitoring-internal)
    * [{{metricbeat}} collection](#apm-privileges-to-publish-monitoring-metricbeat)

* [View monitoring data](#apm-privileges-to-publish-monitoring-view)


### Publish monitoring data [apm-privileges-to-publish-monitoring-write]

::::{important}
**{{ecloud}} users:** This section does not apply to [{{ech}}](https://www.elastic.co/cloud/elasticsearch-service). Monitoring on {{ecloud}} is enabled by clicking the **Enable** button in the **Monitoring** panel.

::::



#### Internal collection [apm-privileges-to-publish-monitoring-internal]

If you’re using [internal collection](use-internal-collection-to-send-monitoring-data.md) to collect metrics about APM Server, either:

* Use the built-in `apm_system` user or role
* Create a custom role

**Use a built-in user or role**

{{es-security-features}} provides the `apm_system` [built-in user](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md) and `apm_system` [built-in role](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md) to send monitoring information. You can use the built-in user, if it’s available in your environment, create a user who has the built-in role assigned, or create a user and manually assign the privileges needed to send monitoring information.

If you use the built-in `apm_system` user, make sure you set the password before using it.

**Create a custom role**

If you don’t use the `apm_system` user, you can create a custom role:

1. Create a **monitoring role**, called something like `apm_monitoring_writer`, that has the following privileges:

    | Type | Privilege | Purpose |
    | --- | --- | --- |
    | Index | `create_index` on `.monitoring-beats-*` indices | Create monitoring indices in {{es}} |
    | Index | `create_doc` on `.monitoring-beats-*` indices | Write monitoring events into {{es}} |

2. Assign the **monitoring role** to APM Server users who need to write monitoring data to {{es}}.

::::{note}
Assign additional APM feature roles to users as needed including the [*Writer role*](#apm-privileges-to-publish-events) and [*Central configuration management role*](#apm-central-config-role-note), both of which are required in most cases.

::::



#### {{metricbeat}} collection [apm-privileges-to-publish-monitoring-metricbeat]

::::{note}
When using {{metricbeat}} to collect metrics, no roles or users need to be created with APM Server. See [Use {{metricbeat}} collection](use-metricbeat-to-send-monitoring-data.md) for complete details on setting up {{metricbeat}} collection.
::::


If you’re [using {{metricbeat}}](use-metricbeat-to-send-monitoring-data.md) to collect metrics about APM Server, you can either:

* Use the built-in `remote_monitoring_user` user or role
* Create a custom user

**Use a built-in user or role**

{{es-security-features}} provides the `remote_monitoring_user` [built-in user](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md), and the `remote_monitoring_collector` and `remote_monitoring_agent` [built-in roles](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md) for collecting and sending monitoring information. You can use the built-in user, if it’s available in your environment, or create a user who has the privileges needed to collect and send monitoring information.

If you use the built-in `remote_monitoring_user` user, make sure you set the password before using it.

**Create a custom user**

If you don’t use the `remote_monitoring_user` user, you can create a custom user:

1. Create a **monitoring user** on the production cluster who will collect and send monitoring information. Assign the following roles to the **monitoring user**:

    | Role | Purpose |
    | --- | --- |
    | `remote_monitoring_collector` | Collect monitoring metrics from APM Server |
    | `remote_monitoring_agent` | Send monitoring data to the monitoring cluster |


::::{note}
Assign additional APM feature roles to users as needed including the [*Writer role*](#apm-privileges-to-publish-events) and [*Central configuration management role*](#apm-central-config-role-note), both of which are required in most cases.

::::



### View monitoring data [apm-privileges-to-publish-monitoring-view]

To grant users the required privileges for viewing monitoring data:

1. Create a **monitoring role**, called something like `apm_monitoring_viewer`, that has the following privileges:

    | Type | Privilege | Purpose |
    | --- | --- | --- |
    | Spaces | `Read` on Stack monitoring | Read-only access to the {{stack-monitor-app}} feature in {{kib}}. |
    | Spaces | `Read` on Dashboards | Read-only access to the Dashboards feature in {{kib}}. |

2. Assign the **monitoring role**, along with the following built-in roles, to users who need to view monitoring data for APM Server:

    | Role | Purpose |
    | --- | --- |
    | `monitoring_user` | Grants access to monitoring indices for APM Server |


::::{note}
Assign additional APM feature roles to users as needed including the [*Writer role*](#apm-privileges-to-publish-events) and [*Central configuration management role*](#apm-central-config-role-note), both of which are required in most cases.

::::



## Create a *source map* role [apm-privileges-rum-source-map]

$$$apm-privileges-rum-source-mapping$$$
If [real user monitoring](configure-real-user-monitoring-rum.md) is enabled, additional privileges are required to read source maps.

To grant an APM Server user with the required privileges for reading RUM source maps from {{es}} directly without {{kib}}, assign the user the following privileges:

| Type | Privilege | Purpose |
| --- | --- | --- |
| Index | `read` on `.apm-source-map` index | Allow APM Server to read RUM source maps from {{es}} |

::::{note}
Assign additional APM feature roles to users as needed including the [*Writer role*](#apm-privileges-to-publish-events) and [*Central configuration management role*](#apm-central-config-role-note), both of which are required in most cases.

::::


The previous privileges should be sufficient for RUM source mapping to work properly as long as APM Server communicates with {{es}} successfully. If it fails, it may fallback to read source maps through {{kib}} if configured, which requires additional {{kib}} privileges. For more details, refer to the [{{stack}}](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-apm-sourcemaps) or [{{serverless-short}}](https://www.elastic.co/docs/api/doc/serverless/group/endpoint-apm-sourcemaps) API documentation.