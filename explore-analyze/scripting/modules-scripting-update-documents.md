---
navigation_title: Update documents using scripts
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Update documents using scripts [scripts-update-scripts]

You can use the [update API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-update) to update documents with a specified script. The script can update, delete, or skip modifying the document. The update API also supports passing a partial document, which is merged into the existing document.

First, let’s index a simple document:

```console
PUT my-index-000001/_doc/1
{
  "counter" : 1,
  "tags" : ["red"]
}
```

To increment the counter, you can submit an update request with the following script:

```console
POST my-index-000001/_update/1
{
  "script" : {
    "source": "ctx._source.counter += params.count",
    "lang": "painless",
    "params" : {
      "count" : 4
    }
  }
}
```

Similarly, you can use an update script to add a tag to the list of tags. Because this is just a list, the tag is added even it exists:

```console
POST my-index-000001/_update/1
{
  "script": {
    "source": "ctx._source.tags.add(params['tag'])",
    "lang": "painless",
    "params": {
      "tag": "blue"
    }
  }
}
```

You can also remove a tag from the list of tags. The `remove` method of a Java `List` is available in Painless. It takes the index of the element you want to remove. To avoid a possible runtime error, you first need to make sure the tag exists. If the list contains duplicates of the tag, this script just removes one occurrence.

```console
POST my-index-000001/_update/1
{
  "script": {
    "source": "if (ctx._source.tags.contains(params['tag'])) { ctx._source.tags.remove(ctx._source.tags.indexOf(params['tag'])) }",
    "lang": "painless",
    "params": {
      "tag": "blue"
    }
  }
}
```

You can also add and remove fields from a document. For example, this script adds the field `new_field`:

```console
POST my-index-000001/_update/1
{
  "script" : "ctx._source.new_field = 'value_of_new_field'"
}
```

Conversely, this script removes the field `new_field`:

```console
POST my-index-000001/_update/1
{
  "script" : "ctx._source.remove('new_field')"
}
```

Instead of updating the document, you can also change the operation that is executed from within the script. For example, this request deletes the document if the `tags` field contains `green`. Otherwise it does nothing (`noop`):

```console
POST my-index-000001/_update/1
{
  "script": {
    "source": "if (ctx._source.tags.contains(params['tag'])) { ctx.op = 'delete' } else { ctx.op = 'none' }",
    "lang": "painless",
    "params": {
      "tag": "green"
    }
  }
}
```
