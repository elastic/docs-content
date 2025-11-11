---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-api-key.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
navigation_title: API keys
---

# API keys for Elastic APM [apm-api-key]

:::{include} _snippets/apm-server-vs-mis.md
:::

::::{important}
API keys are sent as plain-text, so they only provide security when used in combination with [TLS](/solutions/observability/apm/apm-agent-tls-communication.md).
::::

When enabled, API keys are used to authorize requests to {{apm-server-or-mis}}. API keys are not applicable for APM agents running on clients, like the RUM agent, as there is no way to prevent them from being publicly exposed.

You can assign one or more unique privileges to each API key:

* **Agent configuration** (`config_agent:read`): Required for agents to read [Agent configuration remotely](/solutions/observability/apm/apm-server/apm-agent-central-configuration.md).
* **Ingest** (`event:write`): Required for ingesting agent events.

To secure the communication between APM Agents and either {{apm-server-or-mis}} with API keys, make sure [TLS](/solutions/observability/apm/apm-agent-tls-communication.md) is enabled, then complete these steps:

1. [Enable API keys](#apm-enable-api-key)
2. [Create an API key user](#apm-create-api-key-user)
3. [Create an API key in {{kib}}](#apm-create-an-api-key)
4. [Set the API key in your APM agents](#apm-agent-api-key)

## Enable API keys [apm-enable-api-key]

:::::::{tab-set}

::::::{tab-item} Fleet-managed
Enable API key authorization in the [API key authentication options](/solutions/observability/apm/apm-server/apm-agent-authorization.md#apm-api-key-auth-settings). You should also set a limit on the number of unique API keys that APM Server allows per minute; this value should be the number of unique API keys configured in your monitored services.
::::::

::::::{tab-item} APM Server binary
API keys are disabled by default. Enable and configure this feature in the `apm-server.auth.api_key` section of the `apm-server.yml` configuration file.

At a minimum, you must enable API keys, and should set a limit on the number of unique API keys that APM Server allows per minute. Here’s an example `apm-server.auth.api_key` config using 50 unique API keys:

```yaml
apm-server.auth.api_key.enabled: true <1>
apm-server.auth.api_key.limit: 50 <2>
```

1. Enables API keys
2. Restricts the number of unique API keys that {{es}} allows each minute. This value should be the number of unique API keys configured in your monitored services.

::::::

::::::{tab-item} {{serverless-full}}
API keys are enabled by default.
::::::

:::::::

## Create an API key user in {{kib}} [apm-create-api-key-user]

API keys can only have the same or lower access rights than the user that creates them.

:::::::{tab-set}

::::::{tab-item} Fleet-managed or APM Server binary
Instead of using a superuser account to create API keys, you can create a role with the minimum required privileges.

The user creating an {{apm-agent}} API key must have at least the `manage_own_api_key` cluster privilege and the APM application-level privileges that it wishes to grant. In addition, when creating an API key from the Applications UI, you’ll need the appropriate {{kib}} Space and Feature privileges.

The example below uses the {{kib}} [role management API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-roles) to create a role named `apm_agent_key_role`.

```js
POST /_security/role/apm_agent_key_role
{
   "cluster": [ "manage_own_api_key" ],
   "applications": [
      {
         "application":"apm",
         "privileges":[
            "event:write",
            "config_agent:read"
         ],
         "resources":[ "*" ]
      },
      {
         "application":"kibana-.kibana",
         "privileges":[ "feature_apm.all" ],
         "resources":[ "space:default" ] <1>
      }
   ]
}
```

1. This example assigns privileges for the default space.

Assign the newly created `apm_agent_key_role` role to any user that wishes to create {{apm-agent}} API keys.
::::::

::::::{tab-item} {{serverless-full}}
**For Observability Serverless projects**, the Editor role or higher is required to create and manage API keys. To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).
::::::

:::::::

## Create an API key in the Applications UI [apm-create-an-api-key]

The Applications UI has a built-in workflow that you can use to easily create and view {{apm-agent}} API keys. Only API keys created in the Applications UI will show up here.

:::::::{tab-set}

::::::{tab-item} Fleet-managed or APM Server binary

Using a superuser account, or a user with the role created in the previous step, In {{kib}}, find **Applications** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Go to **Settings** → **Agent keys**. Enter a name for your API key and select at least one privilege.

For example, to create an API key that can be used to ingest APM events and read agent central configuration, select `config_agent:read` and `event:write`.

Click **Create APM Agent key** and copy the Base64 encoded API key. You will need this for the next step, and you will not be able to view it again.

:::{image} /solutions/images/observability-apm-ui-api-key.png
:alt: Applications UI API key
:screenshot:
:::

::::::

::::::{tab-item} {{serverless-full}}
To create a new API key:

1. In your Elastic Observability Serverless project, go to any Applications page.
1. Click **Settings**.
1. Select the **Agent keys** tab.
1. Click **Create APM agent key**.
1. Name the key and assign privileges to it.
1. Click **Create APM agent key**.
1. Copy the key now. You will not be able to see it again. API keys do not expire.

To view all API keys for your project:

1. Expand **Project settings**.
1. Select **Management**.
1. Select **API keys**.
::::::

:::::::

## Set the API key in your APM agents [apm-agent-api-key]

You can now apply your newly created API keys in the configuration of each of your APM agents. See the relevant agent documentation for additional information:

* **Android**: [`apiKey`](apm-agent-android://reference/edot-android/configuration.md)
* **Go agent**: [`ELASTIC_APM_API_KEY`](apm-agent-go://reference/configuration.md#config-api-key)
* **.NET agent**: [`ApiKey`](apm-agent-dotnet://reference/config-reporter.md#config-api-key)
* **iOS**: [`withApiKey`](apm-agent-ios://reference/edot-ios/configuration.md#withapikey)
* **Java agent**: [`api_key`](apm-agent-java://reference/config-reporter.md#config-api-key)
* **Node.js agent**: [`apiKey`](apm-agent-nodejs://reference/configuration.md#api-key)
* **PHP agent**: [`api_key`](apm-agent-php://reference/configuration-reference.md#config-api-key)
* **Python agent**: [`api_key`](apm-agent-python://reference/configuration.md#config-api-key)
* **Ruby agent**: [`api_key`](apm-agent-ruby://reference/configuration.md#config-api-key)

## Alternate API key creation method [apm-configure-api-key-alternative]

```{applies_to}
stack: ga
serverless: unavailable
```

It is also possible to create API keys using the {{es}} [create API key API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key).

This example creates an API key named `java-002`:

```bash
POST /_security/api_key
{
  "name": "java-002", <1>
  "expiration": "1d", <2>
  "role_descriptors": {
    "apm": {
      "applications": [
        {
          "application": "apm",
          "privileges": ["sourcemap:write", "event:write", "config_agent:read"], <3>
          "resources": ["*"]
        }
      ]
    }
  }
}
```

1. The name of the API key
2. The expiration time of the API key
3. Any assigned privileges

The response will look similar to this:

```console-result
{
  "id" : "GnrUT3QB7yZbSNxKET6d",
  "name" : "java-002",
  "expiration" : 1599153532262,
  "api_key" : "RhHKisTmQ1aPCHC_TPwOvw"
}
```

The `credential` string, which is what agents use to communicate with APM Server, is a base64 encoded representation of the API key’s `id:api_key`. It can be created like this:

```console-result
echo -n GnrUT3QB7yZbSNxKET6d:RhHKisTmQ1aPCHC_TPwOvw | base64
```

You can verify your API key has been base64-encoded correctly with the [Authenticate API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-authenticate):

```sh
curl -H "Authorization: ApiKey R0gzRWIzUUI3eVpiU054S3pYSy06bXQyQWl4TlZUeEcyUjd4cUZDS0NlUQ==" localhost:9200/_security/_authenticate
```

If the API key has been encoded correctly, you’ll see a response similar to the following:

```console-result
{
   "username":"1325298603",
   "roles":[],
   "full_name":null,
   "email":null,
   "metadata":{
      "saml_nameid_format":"urn:oasis:names:tc:SAML:2.0:nameid-format:transient",
      "saml(http://saml.elastic-cloud.com/attributes/principal)":[
         "1325298603"
      ],
      "saml_roles":[
         "superuser"
      ],
      "saml_principal":[
         "1325298603"
      ],
      "saml_nameid":"_7b0ab93bbdbc21d825edf7dca9879bd8d44c0be2",
      "saml(http://saml.elastic-cloud.com/attributes/roles)":[
         "superuser"
      ]
   },
   "enabled":true,
   "authentication_realm":{
      "name":"_es_api_key",
      "type":"_es_api_key"
   },
   "lookup_realm":{
      "name":"_es_api_key",
      "type":"_es_api_key"
   }
}
```

You can then use the APM Server CLI to verify that the API key has the requested privileges:

```sh
apm-server apikey verify --credentials R25yVVQzUUI3eVpiU054S0VUNmQ6UmhIS2lzVG1RMWFQQ0hDX1RQd092dw==
```

If the API key has the requested privileges, the response will look similar to this:

```console-result
Authorized for privilege "config_agent:read"...:  Yes
Authorized for privilege "event:write"...:        Yes
Authorized for privilege "sourcemap:write"...:    Yes
```
