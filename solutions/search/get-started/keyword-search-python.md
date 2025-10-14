---
navigation_title: "Keyword search with Python"
description: An introduction to building an Elasticsearch query in Python. 
applies_to:
  serverless:
    elasticsearch: ga
products:
  - id: elasticsearch
  - id: elasticsearch-client
---
# Build your first search query with Python

In this quickstart, you'll index a couple of documents and query them using [Python](https://www.python.org/).
These concepts and techniques will help you connect a backend application to {{es}} to answer your queries.

This quickstart also introduces you to the [official {{es}} clients](/reference/elasticsearch-clients/index.md), which are available for multiple programming languages.
These clients offer full API support for indexing, searching, and cluster management.
They are optimized for performance and kept up to date with {{es}} releases, ensuring compatibility and security.

This quickstart does not require previous knowledge of {{es}} but assumes a basic familiarity with Python development.
To follow the steps, you must have a recent version of a Python interpreter.

:::::{stepper}

::::{step} Create a project

:::{include} /deploy-manage/deploy/_snippets/create-serverless-project-intro.md
:::

Choose the {{es}} project type and provide a name.
You can optionally edit the project settings, such as the [region](/deploy-manage/deploy/elastic-cloud/regions.md).

To add the sample data in subsequent steps, you must have a `developer` or `admin` predefined role or an equivalent custom role.
To learn about role-based access control, go to [](/deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.md).
::::
::::{step} Create an index

An index is a collection of documents uniquely identified by a name or an alias.
To create an index:
1. Go to **Index Management** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Create index**, select **Keyword Search**, and follow the guided workflow.

To enable your client to talk to your project, you must also create an API key.
Select **Create an API Key** and use the default values, which are sufficient for this quickstart.

:::{tip}
For more information about indices and API keys, go to [](/manage-data/data-store/index-basics.md) and [](/deploy-manage/api-keys/serverless-project-api-keys.md).
:::
::::
::::{step} Install the Python client

Select your preferred language in the keyword search workflow.
For this quickstart, use Python.

![Client installation step in the keyword search workflow](/solutions/images/search-quickstart-install-python-client.png)

The {{es}} client library is a Python package that is installed with `pip`:

```py
python -m pip install elasticsearch
```

::::
::::{step} Connect to your project

To connect from your client to your {{es-serverless}} project, copy the following code example from the guided workflow into your Python interpreter in interactive mode:
For example, connect from your client to your {{es-serverless}} project:

```py
from elasticsearch import Elasticsearch, helpers

client = Elasticsearch(
    "YOUR-PROJECT-URL",
    api_key="YOUR-API-KEY"
)

index_name = "YOUR-INDEX"
```

You must replace the project URL, API key, and index name with the appropriate values.

::::
::::{step} Define field mappings

An index has mappings that define how data is stored and indexed.
Create mappings for your index, including a single text field named `text`:

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

A successful response will acknowledge the creation of the mappings:

```py
{'acknowledged': True}
```

::::
::::{step} Ingest documents

Next, use a bulk helper function to add three documents to your index.
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

For more details about bulker helpers, refer to [Client helpers](elasticsearch-py://reference/client-helpers.md).

::::
::::{step} Explore the data

You should now be able to see the documents in the guided workflow:

![Viewing data in the guided workflow](/solutions/images/search-quickstart-view-data-python-keywordsearch.png)

Optionally open [Discover](/explore-analyze/discover.md) from the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) to familiarize yourself with this data set.

::::
::::{step} Test keyword search

A keyword search, also known as lexical search or [full-text search](/solutions/search/full-text.md) finds relevant documents in your indices using exact matches, patterns, or similarity scoring.
The guided workflow provides an example that uses [Query DSL](/explore-analyze/query-filter/languages/querydsl.md).
Alternatively, try out [{{es}} Query Language](elasticsearch://reference/query-languages/esql.md) ({{esql}}) to find documents that match a specific keyword:

```py
response = client.esql.query(
	query="""
    	FROM *
        	| WHERE MATCH(text, "yosemite")
        	| LIMIT 5
    	""",
	format="csv"
)

print(response)
```

:::{tip}
Instead of using the `*` wildcard, you can narrow the query by using your index name.
For more details, refer to the [ES|QL reference](elasticsearch://reference/query-languages/esql.md)
:::

The results in this case contain the document that matches the query:

```txt
"Yosemite National Park is a United States National Park, covering over 750,000 acres of land in California. A UNESCO World Heritage Site, the park is best known for its granite cliffs, waterfalls and giant sequoia trees. Yosemite hosts over four million visitors in most years, with a peak of five million visitors in 2016. The park is home to a diverse range of wildlife, including mule deer, black bears, and the endangered Sierra Nevada bighorn sheep. The park has 1,200 square miles of wilderness, and is a popular destination for rock climbers, with over 3,000 feet of vertical granite to climb. Its most famous and cliff is the El Capitan, a 3,000 feet monolith along its tallest face."
Now you are ready to use the client to query Elasticsearch from any Python backend like Flask, Django, etc. Check out the Elasticsearch Python Client documentation to explore further
```

::::
:::::

## Next steps

Test some more keyword search queries or go to the **{{index-manage-app}}** page and follow the workflows for vector search or semantic search queries.

When you finish your tests and no longer need the sample data set, delete your index:

```py
client.indices.delete(index=index_name)
```

This quickstart covered the basics of working with {{es}}.
For a deeper dive, refer to the following resources:

- [Getting started with the Python client](elasticsearch-py://reference/getting-started.md)
- [](/manage-data/ingest/ingesting-data-from-applications/ingest-data-with-python-on-elasticsearch-service.md)
- [Python notebooks](https://github.com/elastic/elasticsearch-labs/tree/main/notebooks/README.md)
