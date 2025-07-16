---
navigation_title: "Keyword search with Python"
description: An introduction to building an Elasticsearch query in Python. 
applies_to:
  serverless: all
products:
  - id: elasticsearch
---
# Build your first search query with Python

{{es}} provides a range of search techniques, starting with BM25, the industry standard for textual search.
It provides official clients for multiple programming languages, including Python, Rust, Java, JavaScript, and others. 
These clients offer full API support for indexing, searching, and cluster management.
They are optimized for performance and kept up to date with {{es}} releases, ensuring compatibility and security.

In this quickstart, you'll index a couple of documents and query them using Python.
By the end of this guide, you’ll have learned how to connect a backend application to {{es}} to answer your queries.

## Prerequisites

- If you're using [{{es-serverless}}](/solutions/search/serverless-elasticsearch-get-started.md), create a general purpose project. To add the sample data, you must have a `developer` or `admin` predefined role or an equivalent custom role.
<!--
If you're using [{{ech}}](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md) or [running {{es}} locally](/solutions/search/run-elasticsearch-locally.md), start {{es}} and {{kib}}. To add the sample data, log in with a user that has the `superuser` built-in role.
-->
  
To learn about role-based access control, check out [](/deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.md).

## Create an index

An index is a collection of documents uniquely identified by a name or an alias.
Go to **{{es}} > Home**, select keyword search, and follow the guided index workflow.
<!--
Click **Create a TBD index**.
- If you're using {{es-serverless}}...
- If you're using {{ech}} or running {{es}} locally, go to **{{es}} > Home** and click **Create API index**. Select the semantic search workflow.
-->

You've created your first index!
Next, create an API key so your application can talk to {{es}}.
<!--
TBD: Describe how to create the key
-->
:::{tip}
For an introduction to the concept of indices, check out [](/manage-data/data-store/index-basics.md).
:::

## Install an {{es}} client

Select your preferred language in the keyword search workflow. For this example, leverage Python.

![Client installation step in the index management workflow](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/bltbf810f73fd4082fb/67c21c06304ea9790b82ee4d/screenshot-my-index.png)

In your terminal, install the {{es}} client using `pip`:

```py
pip install elasticsearch
```

Copy your API key from the top right corner and add it to the client’s configuration alongside the project URL.

```py
from elasticsearch import Elasticsearch

client = Elasticsearch(
    "https://my-project-bff300.es.us-east-1.aws.elastic.cloud:443",
    api_key="YOUR-API-KEY"
)

index_name = "my-index"
```

## Create field mappings

At this stage, you can define the mappings for your index, including a single text field — named "text".

```py
mappings = {
    "properties": {
        "text": {
            "type": "text"
        }
    }
}

mapping_response = client.indices.put_mapping(index=index_name, body=mappings)
print(mapping_response)
```

## Add documents

Next, use a bulk request to index three documents in {{es}}.
Bulk requests are the preferred method for indexing large volumes of data, from hundreds to billions of documents.

```py
docs = [
    {
        "text": "Yellowstone National Park is one of the largest national parks in the United States. It ranges from the Wyoming to Montana and Idaho, and contains an area of 2,219,791 acress across three different states. Its most famous for hosting the geyser Old Faithful and is centered on the Yellowstone Caldera, the largest super volcano on the American continent. Yellowstone is host to hundreds of species of animal, many of which are endangered or threatened. Most notably, it contains free-ranging herds of bison and elk, alongside bears, cougars and wolves. The national park receives over 4.5 million visitors annually and is a UNESCO World Heritage Site."
    },
    {
        "text": "Yosemite National Park is a United States National Park, covering over 750,000 acres of land in California. A UNESCO World Heritage Site, the park is best known for its granite cliffs, waterfalls and giant sequoia trees. Yosemite hosts over four million visitors in most years, with a peak of five million visitors in 2016. The park is home to a diverse range of wildlife, including mule deer, black bears, and the endangered Sierra Nevada bighorn sheep. The park has 1,200 square miles of wilderness, and is a popular destination for rock climbers, with over 3,000 feet of vertical granite to climb. Its most famous and cliff is the El Capitan, a 3,000 feet monolith along its tallest face."
    },
    {
        "text": "Rocky Mountain National Park  is one of the most popular national parks in the United States. It receives over 4.5 million visitors annually, and is known for its mountainous terrain, including Longs Peak, which is the highest peak in the park. The park is home to a variety of wildlife, including elk, mule deer, moose, and bighorn sheep. The park is also home to a variety of ecosystems, including montane, subalpine, and alpine tundra. The park is a popular destination for hiking, camping, and wildlife viewing, and is a UNESCO World Heritage Site."
    }
]

bulk_response = helpers.bulk(client, docs, index=index_name)
print(bulk_response)
```

## Explore the data

You should be able to see the documents in {{es}}!

![Viewing data in the index management workflow](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt0ac36402cde2a645/67d0a443b8764e72b9e8e1f3/view_docs_in_elasticsearch.png)
<!--
To familiarize yourself with this data set, open [Discover](/explore-analyze/discover.md) from the navigation menu or the global search field.
-->

## Test keyword search

Create a new script (for instance `search.py`), which defines a query and runs the following search request:

```esql
FROM my-index
| WHERE MATCH(text, "yosemite")
| LIMIT 5
```

Add this query inside `client.esql.query`:

```py
from elasticsearch import Elasticsearch

client = Elasticsearch(
	"https://my-project-bff307.es.us-east-1.aws.elastic.cloud:443",
	api_key="YOUR-API-KEY"
)

# Run the search query
response = client.esql.query(
	query="""
    	FROM my-index
        	| WHERE MATCH(text, "yosemite")
        	| LIMIT 5
    	""",
	format="csv"
)

print(response)
```

## Analyze the results

Check your result:

```txt
"Yosemite National Park is a United States National Park, covering over 750,000 acres of land in California. A UNESCO World Heritage Site, the park is best known for its granite cliffs, waterfalls and giant sequoia trees. Yosemite hosts over four million visitors in most years, with a peak of five million visitors in 2016. The park is home to a diverse range of wildlife, including mule deer, black bears, and the endangered Sierra Nevada bighorn sheep. The park has 1,200 square miles of wilderness, and is a popular destination for rock climbers, with over 3,000 feet of vertical granite to climb. Its most famous and cliff is the El Capitan, a 3,000 feet monolith along its tallest face."
Now you are ready to use the client to query Elasticsearch from any Python backend like Flask, Django, etc. Check out the Elasticsearch Python Client documentation to explore further
```

<!--
When you finish your tests and no longer need the sample data set, delete the index:

```console
DELETE /semantic-index
```
-->

## Next steps

Thanks for taking the time to learn how to build an application on top of {{es}}.

For a deeper dive, check out the following resources:

- [Getting started with the Python client](elasticsearch-py://reference/getting-started.md)
- [Python notebooks](https://github.com/elastic/elasticsearch-labs/tree/main/notebooks/README.md)
- [](/manage-data/ingest/ingesting-data-from-applications/ingest-data-with-python-on-elasticsearch-service.md)