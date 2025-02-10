---
mapped_urls:
  - https://www.elastic.co/guide/en/cloud/current/ec-getting-started-node-js.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-getting-started-node-js.html
---

# Ingest data with Node.js

This guide tells you how to get started with:

* Securely connecting to your {{ech}} or {{ece}} deployment with Node.js
* Ingesting data into your deployment from your application
* Searching and modifying your data

If you are an Node.js application programmer who is new to the Elastic Stack, this content helps you get started more easily.

*Time required: 45 minutes*

## Create a deployment [ec_get_elasticsearch_service]

::::{tab-set}

:::{tab-item} Elastic Cloud Hosted
1. [Get a free trial](https://cloud.elastic.co/registration?page=docs&placement=docs-body).
2. Log into [Elastic Cloud](https://cloud.elastic.co?page=docs&placement=docs-body).
3. Select **Create deployment**.
4. Give your deployment a name. You can leave all other settings at their default values.
5. Select **Create deployment** and save your Elastic deployment credentials. You need these credentials later on.
6. When the deployment is ready, click **Continue** and a page of **Setup guides** is displayed. To continue to the deployment homepage click **I’d like to do something else**.

Prefer not to subscribe to yet another service? You can also get {{ech}} through [AWS, Azure, and GCP marketplaces](../../../deploy-manage/deploy/elastic-cloud/subscribe-from-marketplace.md).
:::

:::{tab-item} Elastic Cloud Enterprise
1. Log into the Elastic Cloud Enterprise admin console.
2. Select **Create deployment**.
3. Give your deployment a name. You can leave all other settings at their default values.
4. Select **Create deployment** and save your Elastic deployment credentials. You need these credentials later on.
5. When the deployment is ready, click **Continue** and a page of **Setup guides** is displayed. To continue to the deployment homepage click **I’d like to do something else**.
:::

::::

## Set up your application [ec_set_up_your_application]

These steps are applicable to your existing application. If you don’t have one, use the example included here to create one.


### Create the npm `package.json` file [ec_create_the_npm_package_json_file]

```sh
npm init
```


### Get the `elasticsearch` and `config` packages [ec_get_the_elasticsearch_and_config_packages]

```sh
npm install @elastic/elasticsearch
npm install config
```

::::{note}
The `config` package is not required if you have your own method to keep your configuration details private.
::::



### Create a configuration file [ec_create_a_configuration_file]

```sh
mkdir config
vi config/default.json
```

The example here shows what the `config` package expects. You need to update `config/default.json` with your deployment details in the following sections:

```json
{
  "elastic": {
    "cloudID": "DEPLOYMENT_NAME:CLOUD_ID_DETAILS", <1>
    "username": "elastic",
    "password": "LONGPASSWORD"
  }
}
```

1. Find your Cloud ID by going to the {{kib}} main menu and selecting Management > Integrations, and then selecting View deployment details.



## About connecting securely [ec_about_connecting_securely]

When connecting to {{ech}} or {{ece}}, use a Cloud ID to specify the connection details. You must pass the Cloud ID that is found in {{kib}} or the cloud console.

To connect to, stream data to, and issue queries, you need to think about authentication. Two authentication mechanisms are supported, *API key* and *basic authentication*. Here, to get you started quickly, we’ll show you how to use basic authentication, but you can also generate API keys as shown later on. API keys are safer and preferred for production environments.


### Basic authentication [ec_basic_authentication]

For basic authentication, use the same deployment credentials (`username` and `password` parameters) and Cloud ID you copied down earlier when you created your deployment. (If you did not save the password, you can [reset the password](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md) .)


## Create a sample application [ec_create_a_sample_application]

The sample application connects to {{es}}, creates an index, inserts some records, performs a search, and updates a record.

Read the configuration created earlier, and connect to {{es}}:

```javascript
const { Client } = require('@elastic/elasticsearch')
const config = require('config');
const elasticConfig = config.get('elastic');

const client = new Client({
  cloud: {
    id: elasticConfig.cloudID
  },
  auth: {
    username: elasticConfig.username,
    password: elasticConfig.password
  }
})
```

Now confirm that you are connected to the deployment by returning some information about the deployment:

```javascript
client.info()
  .then(response => console.log(response))
  .catch(error => console.error(error))
```


## Ingest data [ec_ingest_data]

After connecting to your deployment, you are ready to index and search data. Let’s create a new index, insert some quotes from our favorite characters, and refresh the index so that it is ready to be searched. A refresh makes all operations performed on an index since the last refresh available for search.

```javascript
async function run() {
  await client.index({
    index: 'game-of-thrones',
    body: {
      character: 'Ned Stark',
    quote: 'Winter is coming.'
    }
  })

  await client.index({
    index: 'game-of-thrones',
    body: {
      character: 'Daenerys Targaryen',
    quote: 'I am the blood of the dragon.'
    }
  })

  await client.index({
    index: 'game-of-thrones',
    body: {
      character: 'Tyrion Lannister',
    quote: 'A mind needs books like a sword needs whetstone.'
    }
  })

  await client.indices.refresh({index: 'game-of-thrones'})
}

run().catch(console.log)
```

When using the [client.index](https://www.elastic.co/guide/en/elasticsearch/client/javascript-api/current/api-reference.html#_index) API, the request automatically creates the `game-of-thrones` index if it doesn’t already exist, as well as document IDs for each indexed document if they are not explicitly specified.


## Search and modify data [ec_search_and_modify_data]

After creating a new index and ingesting some data, you are now ready to search. Let’s find what characters have said things about `winter`:

```javascript
async function read() {
  const { body } = await client.search({
    index: 'game-of-thrones',
    body: {
      query: {
        match: { quote: 'winter' }
      }
    }
  })
  console.log(body.hits.hits)
}

read().catch(console.log)
```

The search request returns content of documents containing `'winter'` in the `quote` field, including document IDs that were automatically generated. You can make updates to specific documents using document IDs. Let’s add a birthplace for our character:

```javascript
async function update() {
  await client.update({
    index: 'game-of-thrones',
    id: <ID>,
    body: {
      script: {
        source: "ctx._source.birthplace = 'Winterfell'"
      }
    }
  })
  const { body } = await client.get({
    index: 'game-of-thrones',
    id: <ID>
  })

  console.log(body)
}

update().catch(console.log)
```

This [more comprehensive list of API examples](https://www.elastic.co/guide/en/elasticsearch/client/javascript-api/current/examples.html) includes bulk operations, checking the existence of documents, updating by query, deleting, scrolling, and SQL queries. To learn more, check the complete [API reference](https://www.elastic.co/guide/en/elasticsearch/client/javascript-api/current/api-reference.html).


## Switch to API key authentication [ec_switch_to_api_key_authentication]

To get started, authentication to {{es}} used the `elastic` superuser and password, but an API key is much safer and a best practice for production.

In the example that follows, an API key is created with the cluster `monitor` privilege which gives read-only access for determining the cluster state. Some additional privileges also allow `create_index`, `write`, `read`, and `manage` operations for the specified index. The index `manage` privilege is added to enable index refreshes.

The `security.createApiKey` function returns an `id` and `api_key` value which can then be concatenated and encoded in `base64`:

```javascript
async function generateApiKeys (opts) {
  const { body } = await client.security.createApiKey({
    body: {
      name: 'nodejs_example',
      role_descriptors: {
        'nodejs_example_writer': {
          'cluster': ['monitor'],
          'index': [
            {
              'names': ['game-of-thrones'],
              'privileges': ['create_index', 'write', 'read', 'manage']
            }
          ]
        }
      }
    }
  })

  return Buffer.from(`${body.id}:${body.api_key}`).toString('base64')
}

generateApiKeys()
  .then(console.log)
  .catch(err => {
  console.error(err)
  process.exit(1)
})
```

The `base64` encoded output is as follows and is ready to be added to the configuration file:

```text
API_KEY_DETAILS
```

Edit the `config/default.json` configuration file you created earlier and add this API key:

```json
{
  "elastic-cloud": {
    "cloudID": "DEPLOYMENT_NAME:CLOUD_ID_DETAILS",
    "username": "elastic",
    "password": "LONGPASSWORD",
    "apiKey": "API_KEY_DETAILS"
  }
}
```

Now the API key can be used in place of the username and password. The client connection becomes:

```javascript
const elasticConfig = config.get('elastic-cloud');

const client = new Client({
  cloud: {
    id: elasticConfig.cloudID
  },
  auth: {
    apiKey: elasticConfig.apiKey
  }
})
```

Check [Create API key API](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-create-api-key.html) to learn more about API Keys and [Security privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md) to understand which privileges are needed. If you are not sure what the right combination of privileges for your custom application is, you can enable [audit logging](../../../deploy-manage/monitor/logging-configuration/enabling-elasticsearch-audit-logs.md) on {{es}} to find out what privileges are being used. To learn more about how logging works on {{ech}} or {{ece}}, check [Monitoring Elastic Cloud deployment logs and metrics](https://www.elastic.co/blog/monitoring-elastic-cloud-deployment-logs-and-metrics).


### Best practices [ec_best_practices]

Security
:   When connecting to {{ech}} or {{ece}}, the client automatically enables both request and response compression by default, since it yields significant throughput improvements. Moreover, the client also sets the SSL option `secureProtocol` to `TLSv1_2_method` unless specified otherwise. You can still override this option by configuring it.

    Do not enable sniffing when using {{ech}} or {{ece}}, since the nodes are behind a load balancer. {{ech}} and {{ece}} take care of everything for you. Take a look at [Elasticsearch sniffing best practices: What, when, why, how](https://www.elastic.co/blog/elasticsearch-sniffing-best-practices-what-when-why-how) if you want to know more.


Connections ({{ech}} only)
:   If your application connecting to {{ech}} runs under the Java security manager, you should at least disable the caching of positive hostname resolutions. To learn more, check the [Java API Client documentation](https://www.elastic.co/guide/en/elasticsearch/client/java-api-client/current/_others.html).

Schema
:   When the example code was run an index mapping was created automatically. The field types were selected by {{es}} based on the content seen when the first record was ingested, and updated as new fields appeared in the data. It would be more efficient to specify the fields and field types in advance to optimize performance. Refer to the Elastic Common Schema documentation and Field Type documentation when you are designing the schema for your production use cases.

Ingest
:   For more advanced scenarios, this [bulk ingestion](https://www.elastic.co/guide/en/elasticsearch/client/javascript-api/current/bulk_examples.html) reference gives an example of the `bulk` API that makes it possible to perform multiple operations in a single call. This bulk example also explicitly specifies document IDs. If you have a lot of documents to index, using bulk to batch document operations is significantly faster than submitting requests individually.

