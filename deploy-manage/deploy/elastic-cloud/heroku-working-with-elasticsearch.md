---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-working-with-elasticsearch.html
applies_to:
  deployment:
    ess:
products:
  - id: cloud-hosted
---

# Work with {{es}} [ech-working-with-elasticsearch]

You can interact with {{es}} from the command line, or programmatically by sending requests to your {{es}} endpoint.

::::{tip}
If you are looking for a user interface for {{es}} and your data, go to {{kib}}(/deploy-manage/deploy/elastic-cloud/access-kibana.md).
::::

## Find your {{es}} endpoint [echbefore_you_begin_2]

To find out what the ELASTICSEARCH_URL is for your {{es}} cluster, grep on the output of the `heroku config` command for your app:

```bash
heroku config --app MY_APP | grep ELASTICSEARCH_URL
ELASTICSEARCH_URL: <example-es-url>.aws.found.io
```

When you know your {{es}} URL, you can interact with the {{es}} endpoint using tools like curl.

## Example [echindexing]

To index a document into {{es}}, `POST` your document:

```bash
curl -u USER:PASSWORD https://<ELASTICSEARCH_URL>/my_index/_doc -XPOST -H 'Content-Type: application/json' -d '{
    "title": "One", "tags": ["ruby"]
}'
```

To show that the operation worked, {{es}} returns a JSON response that looks like `{"_index":"my_index","_type":"_doc","_id":"0KNPhW4BnhCSymaq_3SI","_version":1,"result":"created","_shards":{"total":2,"successful":2,"failed":0},"_seq_no":0,"_primary_term":1}`.

In this example, the index `my_index` is created dynamically when the first document is inserted into it. All documents in {{es}} have a `type` and an `id`, which is echoed as `"_type":"_doc"` and `_id":"0KNPhW4BnhCSymaq_3SI` in the JSON response. If no ID is specified during indexing, a random `id` is generated.

:::{tip}
These examples use the `elastic` user. If you didn’t copy down the password for the `elastic` user, you can [reset the password](/deploy-manage/users-roles/cluster-or-deployment-auth/manage-elastic-user-cloud.md).
:::

For more examples, refer to the [document APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-document). You can also use [clients](/reference/elasticsearch-clients/index.md) to interact with these APIs.

To learn more about working with data in {{es}}, refer to [](/manage-data/index.md).