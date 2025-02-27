# Ingest data with Python on {{ech}} [ec-getting-started-python]

This guide tells you how to get started with:

* Securely connecting to {{ech}} with Python
* Ingesting data into your deployment from your application
* Searching and modifying your data on {{ech}}

If you are an Python application programmer who is new to the Elastic Stack, this content can help you get started more easily.

*Time required: 45 minutes*


## Prerequisites [ec_prerequisites]

These steps are applicable to your existing application. If you don’t have one, you can use the example included here to create one.


### Get the `elasticsearch` packages [ec_get_the_elasticsearch_packages]

```sh
python -m pip install elasticsearch
python -m pip install elasticsearch-async
```


### Create the `setup.py` file [ec_create_the_setup_py_file]

```sh
# Elasticsearch 7.x
elasticsearch>=7.0.0,<8.0.0
```


## Get {{ech}} [ec_get_elasticsearch_service_2]

1. [Get a free trial](https://cloud.elastic.co/registration?page=docs&placement=docs-body).
2. Log into [Elastic Cloud](https://cloud.elastic.co?page=docs&placement=docs-body).
3. Select **Create deployment**.
4. Give your deployment a name. You can leave all other settings at their default values.
5. Select **Create deployment** and save your Elastic deployment credentials. You need these credentials later on.
6. When the deployment is ready, click **Continue** and a page of **Setup guides** is displayed. To continue to the deployment homepage click **I’d like to do something else**.

Prefer not to subscribe to yet another service? You can also get {{ech}} through [AWS, Azure, and GCP marketplaces](../../../deploy-manage/deploy/elastic-cloud/subscribe-from-marketplace.md).


## Connect securely [ec_connect_securely]

When connecting to {{ech}} you need to use your Cloud ID to specify the connection details. Find your Cloud ID by going to the {{kib}} main menu and selecting Management > Integrations, and then selecting View deployment details.

To connect to, stream data to, and issue queries with {{ech}}, you need to think about authentication. Two authentication mechanisms are supported, *API key* and *basic authentication*. Here, to get you started quickly, we’ll show you how to use basic authentication, but you can also generate API keys as shown later on. API keys are safer and preferred for production environments.


### Basic authentication [ec_basic_authentication_2]

For basic authentication, use the same deployment credentials (`username` and `password` parameters) and Cloud ID you copied down earlier. Find your Cloud ID by going to the {{kib}} main menu and selecting Management > Integrations, and then selecting View deployment details. (If you did not save the password, you can [reset the password](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md) .)

You first need to create and edit an `example.ini` file with your deployment details:

```sh
[ELASTIC]
cloud_id = DEPLOYMENT_NAME:CLOUD_ID_DETAILS
user = elastic
password = LONGPASSWORD
```

The following examples are to be typed into the Python interpreter in interactive mode.  The prompts have been removed to make it easier for you to copy the samples, the output from the interpreter is shown unmodified.


### Import libraries and read in the configuration [ec_import_libraries_and_read_in_the_configuration]

```python
❯ python3
Python 3.9.6 (default, Jun 29 2021, 05:25:02)
[Clang 12.0.5 (clang-1205.0.22.9)] on darwin
Type "help", "copyright", "credits" or "license" for more information.

from elasticsearch import Elasticsearch, helpers
import configparser

config = configparser.ConfigParser()
config.read('example.ini')
```


#### Output [ec_output]

```python
['example.ini']
>>>
```


### Instantiate the {{es}} connection [ec_instantiate_the_es_connection]

```python
es = Elasticsearch(
    cloud_id=config['ELASTIC']['cloud_id'],
    http_auth=(config['ELASTIC']['user'], config['ELASTIC']['password'])
)
```

You can now confirm that you have connected to the deployment by returning some information about the deployment:

```python
es.info()
```


#### Output [ec_output_2]

```python
{'name': 'instance-0000000000',
  'cluster_name': '747ab208fb70403dbe3155af102aef56',
  'cluster_uuid': 'IpgjkPkVQ5efJY-M9ilG7g',
  'version': {'number': '7.15.0', 'build_flavor': 'default', 'build_type': 'docker', 'build_hash': '79d65f6e357953a5b3cbcc5e2c7c21073d89aa29', 'build_date': '2021-09-16T03:05:29.143308416Z', 'build_snapshot': False, 'lucene_version': '8.9.0', 'minimum_wire_compatibility_version': '6.8.0', 'minimum_index_compatibility_version': '6.0.0-beta1'},
  'tagline': 'You Know, for Search'}
```


## Ingest data [ec_ingest_data_2]

After connecting to your deployment, you are ready to index and search data. Let’s create a new index, insert some quotes from our favorite characters, and then refresh the index so that it is ready to be searched. A refresh makes all operations performed on an index since the last refresh available for search.


### Index a document [ec_index_a_document]

```python
es.index(
 index='lord-of-the-rings',
 document={
  'character': 'Aragon',
  'quote': 'It is not this day.'
 })
```


#### Output [ec_output_3]

```python
{'_index': 'lord-of-the-rings',
  '_type': '_doc',
  '_id': 'IanWEnwBg_mH2XweqDqg',
  '_version': 1,
  'result': 'created',
  '_shards': {'total': 2, 'successful': 1, 'failed': 0}, '_seq_no': 34, '_primary_term': 1}
```


### Index another record [ec_index_another_record]

```python
es.index(
 index='lord-of-the-rings',
 document={
  'character': 'Gandalf',
  'quote': 'A wizard is never late, nor is he early.'
 })
```


#### Output [ec_output_4]

```python
{'_index': 'lord-of-the-rings',
  '_type': '_doc',
  '_id': 'IqnWEnwBg_mH2Xwezjpj',
  '_version': 1,
  'result': 'created',
  '_shards': {'total': 2, 'successful': 1, 'failed': 0}, '_seq_no': 35, '_primary_term': 1}
```


### Index a third record [ec_index_a_third_record]

```python
es.index(
 index='lord-of-the-rings',
 document={
  'character': 'Frodo Baggins',
  'quote': 'You are late'
 })
```


#### Output [ec_output_5]

```python
{'_index': 'lord-of-the-rings',
  '_type': '_doc',
  '_id': 'I6nWEnwBg_mH2Xwe_Tre',
  '_version': 1,
  'result': 'created',
  '_shards': {'total': 2, 'successful': 1, 'failed': 0}, '_seq_no': 36, '_primary_term': 1}
```


### Refresh the index [ec_refresh_the_index]

```python
es.indices.refresh(index='lord-of-the-rings')
```


#### Output [ec_output_6]

```python
{'_shards': {'total': 2, 'successful': 1, 'failed': 0}}
```

When using the `es.index` API, the request automatically creates the `lord-of-the-rings` index, if it doesn’t exist already, as well as document IDs for each indexed document if they are not explicitly specified.


## Search and modify data [ec_search_and_modify_data_2]

After creating a new index and ingesting some data, you are now ready to search. Let’s find what different characters have said things about being `late`:

```python
result = es.search(
 index='lord-of-the-rings',
  query={
    'match': {'quote': 'late'}
  }
 )

result['hits']['hits']
```


### Output [ec_output_7]

```python
[{'_index': 'lord-of-the-rings',
  '_type': '_doc',
  '_id': '2EkAzngB_pyHD3p65UMt',
  '_score': 0.5820575,
  '_source': {'character': 'Frodo Baggins', 'quote': 'You are late'}},
 {'_index': 'lord-of-the-rings',
  '_type': '_doc',
  '_id': '10kAzngB_pyHD3p65EPR',
  '_score': 0.37883914,
  '_source': {'character': 'Gandalf',
   'quote': 'A wizard is never late, nor is he early.'}}]
```

The search request returns content of documents containing `late` in the quote field, including document IDs that were automatically generated.

You can make updates to specific documents using document IDs. Let’s add a birthplace for our character:

```python
es.update(
 index='lord-of-the-rings',
 id='2EkAzngB_pyHD3p65UMt', <1>
 doc={'birthplace': 'The Shire'}
 )
```

1. This update example uses the field `id` to identify the document to update. Copy the `id` from the document related to `Frodo Baggins` when you update and add the `birthplace`.



### Output [ec_output_8]

```python
es.get(index='lord-of-the-rings', id='2EkAzngB_pyHD3p65UMt')
{'_index': 'lord-of-the-rings',
 '_type': '_doc',
 '_id': '2EkAzngB_pyHD3p65UMt',
 '_version': 2,
 '_seq_no': 3,
 '_primary_term': 1,
 'found': True,
 '_source': {'character': 'Frodo Baggins',
  'quote': 'You are late',
  'birthplace': 'The Shire'}}
```

For frequently used API calls with the Python client, check [Examples](asciidocalypse://docs/elasticsearch-py/docs/reference/examples.md).


## Switch to API key authentication [ec_switch_to_api_key_authentication_2]

To get started, authentication to Elasticsearch used the `elastic` superuser and password, but an API key is much safer and a best practice for production.

In the example that follows, an API key is created with the cluster `monitor` privilege which gives read-only access for determining the cluster state. Some additional privileges also allow `create_index`, `write`, `read`, and `manage` operations for the specified index. The index `manage` privilege is added to enable index refreshes.

The easiest way to create this key is in the API console for your deployment. Select the deployment name and go to **☰** > **Management** > **Dev Tools**:

```json
POST /_security/api_key
{
  "name": "python_example",
  "role_descriptors": {
    "python_read_write": {
      "cluster": ["monitor"],
      "index": [
        {
          "names": ["test-index"],
          "privileges": ["create_index", "write", "read", "manage"]
        }
      ]
    }
  }
}
```


### The output is: [ec_the_output_is]

```json
{
  "id" : "API_KEY_ID",
  "name" : "python_example",
  "api_key" : "API_KEY_DETAILS"
}
```

Edit the `example.ini` file you created earlier and add the `id` and `api_key` you just created. You should also remove the lines for `user` and `password` you added earlier after you have tested the `api_key`, and consider changing the `elastic` password using the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).

```sh
[DEFAULT]
cloud_id = DEPLOYMENT_NAME:CLOUD_ID_DETAILS
apikey_id = API_KEY_ID
apikey_key = API_KEY_DETAILS
```

You can now use the API key in place of a username and password. The client connection becomes:

```python
es = Elasticsearch(
    cloud_id=config['DEFAULT']['cloud_id'],
    api_key=(config['DEFAULT']['apikey_id'], config['DEFAULT']['apikey_key']),
)
```

Check [Create API key API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key) to learn more about API Keys and [Security privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md) to understand which privileges are needed. If you are not sure what the right combination of privileges for your custom application is, you can enable [audit logging](../../../deploy-manage/monitor/logging-configuration/enabling-audit-logs.md) on {{es}} to find out what privileges are being used. To learn more about how logging works on {{ech}}, check [Monitoring Elastic Cloud deployment logs and metrics](https://www.elastic.co/blog/monitoring-elastic-cloud-deployment-logs-and-metrics).

For more information on refreshing an index, searching, updating, and deleting, check the [elasticsearch-py examples](asciidocalypse://docs/elasticsearch-py/docs/reference/examples.md).


### Best practices [ec_best_practices_2]

Security
:   When connecting to {{ech}}, the client automatically enables both request and response compression by default, since it yields significant throughput improvements. Moreover, the client also sets the SSL option `secureProtocol` to `TLSv1_2_method` unless specified otherwise. You can still override this option by configuring it.

    Do not enable sniffing when using {{ech}}, since the nodes are behind a load balancer. {{ech}} takes care of everything for you. Take a look at [Elasticsearch sniffing best practices: What, when, why, how](https://www.elastic.co/blog/elasticsearch-sniffing-best-practices-what-when-why-how) if you want to know more.


Schema
:   When the example code is run, an index mapping is created automatically. The field types are selected by {{es}} based on the content seen when the first record was ingested, and updated as new fields appeared in the data. It would be more efficient to specify the fields and field types in advance to optimize performance. Refer to the Elastic Common Schema documentation and Field Type documentation when you design the schema for your production use cases.

Ingest
:   For more advanced scenarios, [Bulk helpers](asciidocalypse://docs/elasticsearch-py/docs/reference/client-helpers.md#bulk-helpers) gives examples for the `bulk` API that makes it possible to perform multiple operations in a single call. If you have a lot of documents to index, using bulk to batch document operations is significantly faster than submitting requests individually.

