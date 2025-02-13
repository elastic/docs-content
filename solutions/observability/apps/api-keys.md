---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-api-key.html
---

# API keys [apm-api-key]

::::{important}
API keys are sent as plain-text, so they only provide security when used in combination with [TLS](apm-agent-tls-communication.md).
::::


When enabled, API keys are used to authorize requests to the APM Server. API keys are not applicable for APM agents running on clients, like the RUM agent, as there is no way to prevent them from being publicly exposed.

You can assign one or more unique privileges to each API key:

* **Agent configuration** (`config_agent:read`): Required for agents to read [Agent configuration remotely](apm-agent-central-configuration.md).
* **Ingest** (`event:write`): Required for ingesting agent events.

To secure the communication between APM Agents and the APM Server with API keys, make sure [TLS](apm-agent-tls-communication.md) is enabled, then complete these steps:

1. [Enable API keys](#apm-enable-api-key)
2. [Create an API key user](#apm-create-api-key-user)
3. [Create an API key in {{kib}}](#apm-create-an-api-key)
4. [Set the API key in your APM agents](#apm-agent-api-key)


## Enable API keys [apm-enable-api-key]

:::::::{tab-set}

::::::{tab-item} Fleet-managed
Enable API key authorization in the [API key authentication options](apm-agent-authorization.md#apm-api-key-auth-settings). You should also set a limit on the number of unique API keys that APM Server allows per minute; this value should be the number of unique API keys configured in your monitored services.
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


All other configuration options are described in [API keys]().
::::::

:::::::

## Create an API key user in {{kib}} [apm-create-api-key-user]

API keys can only have the same or lower access rights than the user that creates them. Instead of using a superuser account to create API keys, you can create a role with the minimum required privileges.

The user creating an {{apm-agent}} API key must have at least the `manage_own_api_key` cluster privilege and the APM application-level privileges that it wishes to grant. In addition, when creating an API key from the Applications UI, you’ll need the appropriate {{kib}} Space and Feature privileges.

The example below uses the {{kib}} [role management API](https://www.elastic.co/guide/en/kibana/current/role-management-api.html) to create a role named `apm_agent_key_role`.

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


## Create an API key in the Applications UI [apm-create-an-api-key]

The Applications UI has a built-in workflow that you can use to easily create and view {{apm-agent}} API keys. Only API keys created in the Applications UI will show up here.

Using a superuser account, or a user with the role created in the previous step, In {{kib}}, find **Applications** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Go to **Settings** → **Agent keys**. Enter a name for your API key and select at least one privilege.

For example, to create an API key that can be used to ingest APM events and read agent central configuration, select `config_agent:read` and `event:write`.

Click **Create APM Agent key** and copy the Base64 encoded API key. You will need this for the next step, and you will not be able to view it again.

:::{image} ../../../images/observability-apm-ui-api-key.png
:alt: Applications UI API key
:class: screenshot
:::


## Set the API key in your APM agents [apm-agent-api-key]

You can now apply your newly created API keys in the configuration of each of your APM agents. See the relevant agent documentation for additional information:

* **Android**: [`apiKey`](https://www.elastic.co/guide/en/apm/agent/android/current/configuration.html)
* **Go agent**: [`ELASTIC_APM_API_KEY`](https://www.elastic.co/guide/en/apm/agent/go/current/configuration.html#config-api-key)
* **.NET agent**: [`ApiKey`](https://www.elastic.co/guide/en/apm/agent/dotnet/current/config-reporter.html#config-api-key)
* **iOS**: [`withApiKey`](https://www.elastic.co/guide/en/apm/agent/swift/current/configuration.html#withApiKey)
* **Java agent**: [`api_key`](https://www.elastic.co/guide/en/apm/agent/java/current/config-reporter.html#config-api-key)
* **Node.js agent**: [`apiKey`](https://www.elastic.co/guide/en/apm/agent/nodejs/current/configuration.html#api-key)
* **PHP agent**: [`api_key`](https://www.elastic.co/guide/en/apm/agent/php/{{apm-php-branch}}/configuration-reference.html#config-api-key)
* **Python agent**: [`api_key`](https://www.elastic.co/guide/en/apm/agent/python/current/configuration.html#config-api-key)
* **Ruby agent**: [`api_key`](https://www.elastic.co/guide/en/apm/agent/ruby/current/configuration.html#config-api-key)


## Alternate API key creation methods [apm-configure-api-key-alternative]

API keys can also be created and validated outside of {{kib}}:

* [APM Server API key workflow](#apm-create-api-key-workflow-apm-server)
* [{{es}} API key workflow](#apm-create-api-key-workflow-es)


### APM Server API key workflow [apm-create-api-key-workflow-apm-server]

This API creation method only works with the APM Server binary.

::::{admonition} Deprecated in 8.6.0.
:class: warning

Users should create API Keys through {{kib}} or the {{es}} REST API
::::


APM Server provides a command line interface for creating, retrieving, invalidating, and verifying API keys. Keys created using this method can only be used for communication with APM Server.


#### `apikey` subcommands [apm-create-api-key-subcommands]

**`create`**
:   Create an API Key with the specified privilege(s). No required flags.

    The user requesting to create an API Key needs to have APM privileges used by the APM Server. A superuser, by default, has these privileges.

    ::::{dropdown} **Expand for more information on assigning these privileges to other users**
    To create an APM Server user with the required privileges for creating and managing API keys:

    1. Create an **API key role**, called something like `apm_api_key`, that has the following `cluster` level privileges:

        | Privilege | Purpose |
        | --- | --- |
        | `manage_own_api_key` | Allow APM Server to create, retrieve, and invalidate API keys |

    2. Depending on what the **API key role** will be used for, also assign the appropriate `apm` application-level privileges:

        * To **receive Agent configuration**, assign `config_agent:read`.
        * To **ingest agent data**, assign `event:write`.
        * To **upload source maps**, assign `sourcemap:write`.


    ::::


**`info`**
:   Query API Key(s). `--id` or `--name` required.

**`invalidate`**
:   Invalidate API Key(s). `--id` or `--name` required.

**`verify`**
:   Check if a credentials string has the given privilege(s). `--credentials` required.


#### Privileges [apm-create-api-key-privileges]

If privileges are not specified at creation time, the created key will have all privileges.

* `--agent-config` grants the `config_agent:read` privilege
* `--ingest` grants the `event:write` privilege
* `--sourcemap` grants the `sourcemap:write` privilege


#### Create an API key [apm-create-api-key-workflow]

Create an API key with the `create` subcommand.

The following example creates an API key with a `name` of `java-001`, and gives the "agent configuration" and "ingest" privileges.

```sh
apm-server apikey create --ingest --agent-config --name java-001
```

The response will look similar to this:

```console-result
Name ........... java-001
Expiration ..... never
Id ............. qT4tz28B1g59zC3uAXfW
API Key ........ rH55zKd5QT6wvs3UbbkxOA (won't be shown again)
Credentials .... cVQ0dHoyOEIxZzU5ekMzdUFYZlc6ckg1NXpLZDVRVDZ3dnMzVWJia3hPQQ== (won't be shown again)
```

You should always verify the privileges of an API key after creating it. Verification can be done using the `verify` subcommand.

The following example verifies that the `java-001` API key has the "agent configuration" and "ingest" privileges.

```sh
apm-server apikey verify --agent-config --ingest --credentials cVQ0dHoyOEIxZzU5ekMzdUFYZlc6ckg1NXpLZDVRVDZ3dnMzVWJia3hPQQ==
```

If the API key has the requested privileges, the response will look similar to this:

```console-result
Authorized for privilege "event:write"...:          Yes
Authorized for privilege "config_agent:read"...:    Yes
```

To invalidate an API key, use the `invalidate` subcommand. Due to {{es}} caching, there may be a delay between when this subcommand is executed and when it takes effect.

The following example invalidates the `java-001` API key.

```sh
apm-server apikey invalidate --name java-001
```

The response will look similar to this:

```console-result
Invalidated keys ... qT4tz28B1g59zC3uAXfW
Error count ........ 0
```

A full list of `apikey` subcommands and flags is available in the [API key command reference](apm-server-command-reference.md#apm-apikey-command).


### {{es}} API key workflow [apm-create-api-key-workflow-es]

It is also possible to create API keys using the {{es}} [create API key API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key).

This example creates an API key named `java-002`:

```kibana
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
