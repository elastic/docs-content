---
navigation_title: "Quickstart: Vector and full-text search"
description: Step-by-step tutorial for connecting a client to Elasticsearch, indexing data, and running keyword, semantic, and hybrid search.
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/quickstart.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Quickstart: Vector and full-text search [hybrid-search-quickstart]

{{es}} is a search and vector engine that supports full-text, semantic, and hybrid search over your data. In this quickstart, you index five books, compare these search approaches, and use {{esql}} to count the books by publication decade.

If you're new to using {{es}} for search, you can complete this quickstart in less than 10 minutes after setting up a deployment.

:::{tip}
If you're working with an AI coding agent, point it to the [Elasticsearch onboarding skill](https://github.com/elastic/agent-skills/tree/main/skills/elasticsearch/elasticsearch-onboarding). To complete the quickstart yourself, continue with the steps below.
:::

## Set up {{es}} [vector-full-text-search-create-project]

You can use this quickstart with any type of deployment, although for most search use cases we recommend creating a free [{{es}} {{vectordb}} project](https://cloud.elastic.co/serverless-registration?onboarding_token=vector).

The project takes about a minute to start. When it is ready, open the project. The **Getting started** page displays the **{{es}} endpoint** and a generated API key. Copy both values. If you need a new API key, refer to [Create an API key](/solutions/search/set-up/api-key-and-endpoints.md#get-your-api-key).

:::{important}
If you use an existing deployment, ensure that it has an inference endpoint available for the `semantic_text` field. The [default inference endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints) depends on your deployment type and version.

The example output in this quickstart assumes the `.jina-embeddings-v5-text-small` inference endpoint, which is the default for `semantic_text` on {{ech}} and {{serverless-short}}. If your deployment uses a different endpoint, such as ELSER, your scores and the order of the results might differ.
:::

## Choose how to run the examples [vector-full-text-search-install-sdk]

Use an {{es}} client, curl, or {{kib}} Console to run the examples.

- **Console:** No client installation or connection configuration is needed. Continue to [Create an index and add data](#vector-full-text-search-add-data).
- **curl:** [Set the environment variables](#vector-full-text-search-connect), then continue to [Create an index and add data](#vector-full-text-search-add-data).
- **Language client:** Install and initialize the client for your language, [set the environment variables](#vector-full-text-search-connect), then continue to [Create an index and add data](#vector-full-text-search-add-data).

To install your client:

:::::{tab-set}
:group: languages

::::{tab-item} Python
:sync: python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install elasticsearch
```

For supported Python versions and other requirements, refer to the [Python client documentation](elasticsearch-py://reference/getting-started.md#_requirements).

::::

::::{tab-item} TypeScript
:sync: typescript

```bash
npm install @elastic/elasticsearch
npm install --save-dev typescript tsx @types/node
npm pkg set type=module
```

For supported Node.js versions and other requirements, refer to the [JavaScript client documentation](elasticsearch-js://reference/index.md).

::::

::::{tab-item} PHP
:sync: php

```bash
composer require elasticsearch/elasticsearch
```

For supported PHP versions and other requirements, refer to the [PHP client documentation](elasticsearch-php://reference/index.md).

::::

::::{tab-item} Ruby
:sync: ruby

```bash
bundle init
bundle add elasticsearch
```

For supported Ruby versions and other requirements, refer to the [Ruby client installation documentation](elasticsearch-ruby://reference/installation.md).

::::

::::{tab-item} C# (.NET)
:sync: csharp

```bash
dotnet new console
dotnet add package Elastic.Clients.Elasticsearch
```

For supported .NET versions and other requirements, refer to the [.NET client documentation](elasticsearch-net://reference/index.md).

::::

::::{tab-item} Java
:sync: java

Create a Gradle project:

```bash
gradle init --type java-application --dsl groovy --test-framework junit-jupiter \
  --package quickstart --project-name quickstart --use-defaults
```

The generated `app/build.gradle` already sets `mainClass` to `quickstart.App`. In its `dependencies` block, add the client dependency:

```groovy
dependencies {
    implementation "co.elastic.clients:elasticsearch-java:VERSION"
}
```

Replace `VERSION` with the version from the [latest Java client release](https://github.com/elastic/elasticsearch-java/releases). For supported Java versions and other requirements, refer to the [Java client documentation](elasticsearch-java://reference/index.md).

::::

::::{tab-item} Go
:sync: go

```bash
go mod init quickstart
go get github.com/elastic/go-elasticsearch/v9
```

For supported Go versions and other requirements, refer to the [Go client installation documentation](https://www.elastic.co/docs/reference/elasticsearch/clients/go/installation).

::::

:::::

$$$vector-full-text-search-init-client$$$
After installation, initialize the client:

:::::{tab-set}
:group: languages

::::{tab-item} Python
:sync: python

```python
import os
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch(
    os.environ["ES_URL"],
    api_key=os.environ["ES_API_KEY"],
)
```

::::

::::{tab-item} TypeScript
:sync: typescript

```typescript
import { Client } from "@elastic/elasticsearch";

const es = new Client({
  node: process.env.ES_URL,
  auth: { apiKey: process.env.ES_API_KEY! },
});
```

::::

::::{tab-item} PHP
:sync: php

```php
<?php

require __DIR__ . "/vendor/autoload.php";

use Elastic\Elasticsearch\ClientBuilder;

$es = ClientBuilder::create()
    ->setHosts([getenv("ES_URL")])
    ->setApiKey(getenv("ES_API_KEY"))
    ->build();
```

::::

::::{tab-item} Ruby
:sync: ruby

```ruby
require "elasticsearch"

es = Elasticsearch::Client.new(
  url: ENV.fetch("ES_URL"),
  api_key: ENV.fetch("ES_API_KEY")
)
```

::::

::::{tab-item} C# (.NET)
:sync: csharp

```csharp
using System.Text.Json;
using System.Text.Json.Serialization;
using Elastic.Clients.Elasticsearch;
using Elastic.Clients.Elasticsearch.Core.Bulk;
using Elastic.Clients.Elasticsearch.Esql;
using Elastic.Transport;

var url = Environment.GetEnvironmentVariable("ES_URL")
    ?? throw new InvalidOperationException("ES_URL is not set.");
var apiKey = Environment.GetEnvironmentVariable("ES_API_KEY")
    ?? throw new InvalidOperationException("ES_API_KEY is not set.");

var settings = new ElasticsearchClientSettings(new Uri(url))
    .Authentication(new ApiKey(apiKey));
var es = new ElasticsearchClient(settings);
```

::::

::::{tab-item} Java
:sync: java

```java
package quickstart;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.StringReader;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.elasticsearch._types.Refresh;
import co.elastic.clients.elasticsearch.core.BulkRequest;
import co.elastic.clients.elasticsearch.core.BulkResponse;
import co.elastic.clients.elasticsearch.core.SearchResponse;
import co.elastic.clients.elasticsearch.core.search.Hit;
import co.elastic.clients.elasticsearch.esql.EsqlFormat;
import co.elastic.clients.transport.endpoints.BinaryResponse;

public class App {
    public static void main(String[] args) throws Exception {
        String serverUrl = System.getenv("ES_URL");
        String apiKey = System.getenv("ES_API_KEY");

        try (ElasticsearchClient es = ElasticsearchClient.of(b -> b
            .host(serverUrl)
            .apiKey(apiKey)
        )) {
            // Add the code from the following steps here.
        }
    }
}
```

The `try` block closes the client when the program ends. Without it, the {{es}} client keeps the program running after `main` returns. Add the example code from the following steps inside the `try` block.

::::

::::{tab-item} Go
:sync: go

```go
package main

import (
	"log"
	"os"

	"github.com/elastic/go-elasticsearch/v9"
)

func main() {
	es, err := elasticsearch.New(
		elasticsearch.WithAddresses(os.Getenv("ES_URL")),
		elasticsearch.WithAPIKey(os.Getenv("ES_API_KEY")),
	)
	if err != nil {
		log.Fatal(err)
	}
}
```

::::

:::::

## Connect to your deployment or project [vector-full-text-search-connect]

Set the endpoint and API key of your deployment or project as environment variables:

:::::{tab-set}
:group: operating-systems

::::{tab-item} macOS and Linux
:sync: macos-linux

```bash
export ES_URL="<YOUR_ELASTICSEARCH_URL>" <1>
export ES_API_KEY="YOUR_API_KEY"
```

1. For example, `https://my-project.es.us-east-1.aws.elastic.cloud:443`.

::::

::::{tab-item} Windows PowerShell
:sync: windows-powershell

```powershell
$Env:ES_URL = "<YOUR_ELASTICSEARCH_URL>" <1>
$Env:ES_API_KEY = "YOUR_API_KEY"
```

1. For example, `https://my-project.es.us-east-1.aws.elastic.cloud:443`.

::::

:::::

## Create an index and add data [vector-full-text-search-add-data]

Create the `books` index and add the sample data. The sample data contains five books, each with a `title`, an `author`, a `release_year`, and a `description`.

:::{note}
The following examples show one step at a time rather than a complete program. Language-client examples use the Elasticsearch client that you initialized earlier and leave out setup code such as imports and class definitions. To run the entire quickstart, use the [complete script](#vector-full-text-search-complete-script).
:::

### Create an index

You define the `description` field as `semantic_text` and add a `text` subfield, `description.text`, so that you can also run full-text queries on the same description. {{es}} automatically chooses a data type for each of the other fields:

:::::{tab-set}
:group: languages

::::{tab-item} Python
:sync: python

```python
es.indices.create(
    index="books",
    mappings={
        "properties": { <1>
            "description": {
                "type": "semantic_text", <2>
                "fields": {"text": {"type": "text"}},
            }
        }
    },
)
```

1. With [dynamic mapping](/manage-data/data-store/mapping/dynamic-mapping.md), {{es}} automatically chooses a data type for every new field based on its value. This happens whenever a field first appears, even if it is in a later document. In this quickstart, you only define `description` yourself. Setting it to `semantic_text` tells {{es}} to prepare the text for meaning-based search. To learn more, refer to [](/manage-data/data-store/mapping.md).
2. You define `description` as a [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field. When you index this field, {{es}} sends the text to an {{infer}} endpoint. There, an embedding model converts it into an [embedding](/solutions/search/vector.md#vector-embedding), a numerical representation of its meaning. {{es}} uses these embeddings to find text with similar meaning. This example uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints), but you can [configure another endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints) to use a custom model.



::::

::::{tab-item} TypeScript
:sync: typescript

```typescript
await es.indices.create({
  index: "books",
  mappings: {
    properties: { <1>
      description: {
        type: "semantic_text", <2>
        fields: { text: { type: "text" } },
      },
    },
  },
});
```

1. With [dynamic mapping](/manage-data/data-store/mapping/dynamic-mapping.md), {{es}} automatically chooses a data type for every new field based on its value. This happens whenever a field first appears, even if it is in a later document. In this quickstart, you only define `description` yourself. Setting it to `semantic_text` tells {{es}} to prepare the text for meaning-based search. To learn more, refer to [](/manage-data/data-store/mapping.md).
2. You define `description` as a [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field. When you index this field, {{es}} sends the text to an {{infer}} endpoint. There, an embedding model converts it into an [embedding](/solutions/search/vector.md#vector-embedding), a numerical representation of its meaning. {{es}} uses these embeddings to find text with similar meaning. This example uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints), but you can [configure another endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints) to use a custom model.

::::

::::{tab-item} PHP
:sync: php

```php
$es->indices()->create([
    "index" => "books",
    "body" => [
        "mappings" => [
            "properties" => [ <1>
                "description" => [
                    "type" => "semantic_text", <2>
                    "fields" => ["text" => ["type" => "text"]],
                ],
            ],
        ],
    ],
]);
```

1. With [dynamic mapping](/manage-data/data-store/mapping/dynamic-mapping.md), {{es}} automatically chooses a data type for every new field based on its value. This happens whenever a field first appears, even if it is in a later document. In this quickstart, you only define `description` yourself. Setting it to `semantic_text` tells {{es}} to prepare the text for meaning-based search. To learn more, refer to [](/manage-data/data-store/mapping.md).
2. You define `description` as a [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field. When you index this field, {{es}} sends the text to an {{infer}} endpoint. There, an embedding model converts it into an [embedding](/solutions/search/vector.md#vector-embedding), a numerical representation of its meaning. {{es}} uses these embeddings to find text with similar meaning. This example uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints), but you can [configure another endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints) to use a custom model.

::::

::::{tab-item} Ruby
:sync: ruby

```ruby
es.indices.create(
  index: "books",
  body: {
    mappings: {
      properties: { <1>
        description: {
          type: "semantic_text", <2>
          fields: { text: { type: "text" } }
        }
      }
    }
  }
)
```

1. With [dynamic mapping](/manage-data/data-store/mapping/dynamic-mapping.md), {{es}} automatically chooses a data type for every new field based on its value. This happens whenever a field first appears, even if it is in a later document. In this quickstart, you only define `description` yourself. Setting it to `semantic_text` tells {{es}} to prepare the text for meaning-based search. To learn more, refer to [](/manage-data/data-store/mapping.md).
2. You define `description` as a [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field. When you index this field, {{es}} sends the text to an {{infer}} endpoint. There, an embedding model converts it into an [embedding](/solutions/search/vector.md#vector-embedding), a numerical representation of its meaning. {{es}} uses these embeddings to find text with similar meaning. This example uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints), but you can [configure another endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints) to use a custom model.

::::

::::{tab-item} C# (.NET)
:sync: csharp

```csharp
await es.Indices.CreateAsync<Book>("books", c => c
    .Mappings(m => m
        .Properties(p => p <1>
            .SemanticText(b => b.Description, st => st <2>
                .Fields(f => f.Text("text"))
            )
        )
    )
);
```

1. With [dynamic mapping](/manage-data/data-store/mapping/dynamic-mapping.md), {{es}} automatically chooses a data type for every new field based on its value. This happens whenever a field first appears, even if it is in a later document. In this quickstart, you only define `description` yourself. Setting it to `semantic_text` tells {{es}} to prepare the text for meaning-based search. To learn more, refer to [](/manage-data/data-store/mapping.md).
2. You define `description` as a [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field. When you index this field, {{es}} sends the text to an {{infer}} endpoint. There, an embedding model converts it into an [embedding](/solutions/search/vector.md#vector-embedding), a numerical representation of its meaning. {{es}} uses these embeddings to find text with similar meaning. This example uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints), but you can [configure another endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints) to use a custom model.

::::

::::{tab-item} Java
:sync: java

```java
es.indices().create(c -> c
    .index("books")
    .withJson(new StringReader("""
        {
          "mappings": {
            "properties": { <1>
              "description": {
                "type": "semantic_text", <2>
                "fields": {"text": {"type": "text"}}
              }
            }
          }
        }
        """))
);
```

1. With [dynamic mapping](/manage-data/data-store/mapping/dynamic-mapping.md), {{es}} automatically chooses a data type for every new field based on its value. This happens whenever a field first appears, even if it is in a later document. In this quickstart, you only define `description` yourself. Setting it to `semantic_text` tells {{es}} to prepare the text for meaning-based search. To learn more, refer to [](/manage-data/data-store/mapping.md).
2. You define `description` as a [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field. When you index this field, {{es}} sends the text to an {{infer}} endpoint. There, an embedding model converts it into an [embedding](/solutions/search/vector.md#vector-embedding), a numerical representation of its meaning. {{es}} uses these embeddings to find text with similar meaning. This example uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints), but you can [configure another endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints) to use a custom model.

::::

::::{tab-item} Go
:sync: go

```go
createResponse, err := es.Indices.Create(
	"books",
	es.Indices.Create.WithBody(strings.NewReader(`{
	  "mappings": {
	    "properties": { <1>
	      "description": {
	        "type": "semantic_text", <2>
	        "fields": {"text": {"type": "text"}}
	      }
	    }
	  }
	}`)),
)
if err != nil {
	panic(err)
}
if createResponse.IsError() {
	log.Fatal(createResponse)
}
createResponse.Body.Close()
```

1. With [dynamic mapping](/manage-data/data-store/mapping/dynamic-mapping.md), {{es}} automatically chooses a data type for every new field based on its value. This happens whenever a field first appears, even if it is in a later document. In this quickstart, you only define `description` yourself. Setting it to `semantic_text` tells {{es}} to prepare the text for meaning-based search. To learn more, refer to [](/manage-data/data-store/mapping.md).
2. You define `description` as a [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field. When you index this field, {{es}} sends the text to an {{infer}} endpoint. There, an embedding model converts it into an [embedding](/solutions/search/vector.md#vector-embedding), a numerical representation of its meaning. {{es}} uses these embeddings to find text with similar meaning. This example uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints), but you can [configure another endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints) to use a custom model.

::::

::::{tab-item} Console
:sync: console

```console
PUT books
{
  "mappings": {
    "properties": { <1>
      "description": {
        "type": "semantic_text", <2>
        "fields": {"text": {"type": "text"}}
      }
    }
  }
}
```

1. With [dynamic mapping](/manage-data/data-store/mapping/dynamic-mapping.md), {{es}} automatically chooses a data type for every new field based on its value. This happens whenever a field first appears, even if it is in a later document. In this quickstart, you only define `description` yourself. Setting it to `semantic_text` tells {{es}} to prepare the text for meaning-based search. To learn more, refer to [](/manage-data/data-store/mapping.md).
2. You define `description` as a [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field. When you index this field, {{es}} sends the text to an {{infer}} endpoint. There, an embedding model converts it into an [embedding](/solutions/search/vector.md#vector-embedding), a numerical representation of its meaning. {{es}} uses these embeddings to find text with similar meaning. This example uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints), but you can [configure another endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints) to use a custom model.

::::

::::{tab-item} curl
:sync: curl

```bash
curl -X PUT "$ES_URL/books" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "mappings": {
      "properties": { <1>
        "description": {
          "type": "semantic_text", <2>
          "fields": {"text": {"type": "text"}}
        }
      }
    }
  }'
```

1. With [dynamic mapping](/manage-data/data-store/mapping/dynamic-mapping.md), {{es}} automatically chooses a data type for every new field based on its value. This happens whenever a field first appears, even if it is in a later document. In this quickstart, you only define `description` yourself. Setting it to `semantic_text` tells {{es}} to prepare the text for meaning-based search. To learn more, refer to [](/manage-data/data-store/mapping.md).
2. You define `description` as a [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) field. When you index this field, {{es}} sends the text to an {{infer}} endpoint. There, an embedding model converts it into an [embedding](/solutions/search/vector.md#vector-embedding), a numerical representation of its meaning. {{es}} uses these embeddings to find text with similar meaning. This example uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints), but you can [configure another endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints) to use a custom model.

::::

:::::

### Index the sample data

Next, index five books in one bulk request:

:::::{tab-set}
:group: languages

::::{tab-item} Python
:sync: python

```python
books = [
    {"title": "The Left Hand of Darkness", "author": "Ursula K. Le Guin", "release_year": 1969,
     "description": "An envoy visits an icy planet whose people have no fixed gender, feeling out politics and friendship across a deep cultural gap."},
    {"title": "Project Hail Mary", "author": "Andy Weir", "release_year": 2021,
     "description": "A lone astronaut wakes with amnesia on a spaceship and has to stop a disaster that threatens all life on Earth."},
    {"title": "The Name of the Wind", "author": "Patrick Rothfuss", "release_year": 2007,
     "description": "A gifted young musician and magician tells the story of his rise from orphan to legend."},
    {"title": "Klara and the Sun", "author": "Kazuo Ishiguro", "release_year": 2021,
     "description": "An artificial friend watches human love and loneliness while hoping a child will pick her."},
    {"title": "Dune", "author": "Frank Herbert", "release_year": 1965,
     "description": "On a desert planet prized for a rare spice, a young heir is pulled into a war over ecology, religion, and power."},
]

success_count, errors = helpers.bulk(
    es,
    ({"_index": "books", "_source": b} for b in books),
    refresh="wait_for",
    raise_on_error=False,
)
```

:::{dropdown} Check that all books were indexed
A bulk request can return a successful HTTP response even when an individual operation fails. Check the bulk result before continuing:

```python
if errors:
    raise RuntimeError(f"{len(errors)} book(s) failed to index")
print(f"Indexed {success_count} books")
```
:::

::::

::::{tab-item} TypeScript
:sync: typescript

```typescript
const books = [
  {
    title: "The Left Hand of Darkness",
    author: "Ursula K. Le Guin",
    release_year: 1969,
    description: "An envoy visits an icy planet whose people have no fixed gender, feeling out politics and friendship across a deep cultural gap.",
  },
  {
    title: "Project Hail Mary",
    author: "Andy Weir",
    release_year: 2021,
    description: "A lone astronaut wakes with amnesia on a spaceship and has to stop a disaster that threatens all life on Earth.",
  },
  {
    title: "The Name of the Wind",
    author: "Patrick Rothfuss",
    release_year: 2007,
    description: "A gifted young musician and magician tells the story of his rise from orphan to legend.",
  },
  {
    title: "Klara and the Sun",
    author: "Kazuo Ishiguro",
    release_year: 2021,
    description: "An artificial friend watches human love and loneliness while hoping a child will pick her.",
  },
  {
    title: "Dune",
    author: "Frank Herbert",
    release_year: 1965,
    description: "On a desert planet prized for a rare spice, a young heir is pulled into a war over ecology, religion, and power.",
  },
];

const bulkResponse = await es.bulk({
  refresh: "wait_for",
  operations: books.flatMap((book) => [
    { index: { _index: "books" } },
    book,
  ]),
});
```

:::{dropdown} Check that all books were indexed
A bulk request can return a successful HTTP response even when an individual operation fails. Check the bulk result before continuing:

```typescript
if (bulkResponse.errors) {
  throw new Error("One or more books failed to index");
}
console.log(`Indexed ${bulkResponse.items.length} books`);
```
:::

::::

::::{tab-item} PHP
:sync: php

```php
$books = [
    [
        "title" => "The Left Hand of Darkness",
        "author" => "Ursula K. Le Guin",
        "release_year" => 1969,
        "description" => "An envoy visits an icy planet whose people have no fixed gender, feeling out politics and friendship across a deep cultural gap.",
    ],
    [
        "title" => "Project Hail Mary",
        "author" => "Andy Weir",
        "release_year" => 2021,
        "description" => "A lone astronaut wakes with amnesia on a spaceship and has to stop a disaster that threatens all life on Earth.",
    ],
    [
        "title" => "The Name of the Wind",
        "author" => "Patrick Rothfuss",
        "release_year" => 2007,
        "description" => "A gifted young musician and magician tells the story of his rise from orphan to legend.",
    ],
    [
        "title" => "Klara and the Sun",
        "author" => "Kazuo Ishiguro",
        "release_year" => 2021,
        "description" => "An artificial friend watches human love and loneliness while hoping a child will pick her.",
    ],
    [
        "title" => "Dune",
        "author" => "Frank Herbert",
        "release_year" => 1965,
        "description" => "On a desert planet prized for a rare spice, a young heir is pulled into a war over ecology, religion, and power.",
    ],
];

$operations = [];
foreach ($books as $book) {
    $operations[] = [
        "index" => [
            "_index" => "books",
        ],
    ];
    $operations[] = $book;
}

$bulkResponse = $es->bulk([
    "refresh" => "wait_for",
    "body" => $operations,
]);
```

:::{dropdown} Check that all books were indexed
A bulk request can return a successful HTTP response even when an individual operation fails. Check the bulk result before continuing:

```php
if ($bulkResponse["errors"]) {
    throw new RuntimeException("One or more books failed to index");
}
echo "Indexed " . count($bulkResponse["items"]) . " books\n";
```
:::

::::

::::{tab-item} Ruby
:sync: ruby

```ruby
books = [
  {
    title: "The Left Hand of Darkness",
    author: "Ursula K. Le Guin",
    release_year: 1969,
    description: "An envoy visits an icy planet whose people have no fixed gender, feeling out politics and friendship across a deep cultural gap."
  },
  {
    title: "Project Hail Mary",
    author: "Andy Weir",
    release_year: 2021,
    description: "A lone astronaut wakes with amnesia on a spaceship and has to stop a disaster that threatens all life on Earth."
  },
  {
    title: "The Name of the Wind",
    author: "Patrick Rothfuss",
    release_year: 2007,
    description: "A gifted young musician and magician tells the story of his rise from orphan to legend."
  },
  {
    title: "Klara and the Sun",
    author: "Kazuo Ishiguro",
    release_year: 2021,
    description: "An artificial friend watches human love and loneliness while hoping a child will pick her."
  },
  {
    title: "Dune",
    author: "Frank Herbert",
    release_year: 1965,
    description: "On a desert planet prized for a rare spice, a young heir is pulled into a war over ecology, religion, and power."
  }
]

operations = books.flat_map do |book|
  [
    { index: { _index: "books" } },
    book
  ]
end

bulk_response = es.bulk(
  body: operations,
  refresh: "wait_for"
)
```

:::{dropdown} Check that all books were indexed
A bulk request can return a successful HTTP response even when an individual operation fails. Check the bulk result before continuing:

```ruby
raise "One or more books failed to index" if bulk_response["errors"]
puts "Indexed #{bulk_response['items'].length} books"
```
:::

::::

::::{tab-item} C# (.NET)
:sync: csharp

In `Program.cs`, keep all `record` declarations at the end of the file, after all other code.

```csharp
var books = new[]
{
    new Book(
        "The Left Hand of Darkness",
        "Ursula K. Le Guin",
        1969,
        "An envoy visits an icy planet whose people have no fixed gender, feeling out politics and friendship across a deep cultural gap."
    ),
    new Book(
        "Project Hail Mary",
        "Andy Weir",
        2021,
        "A lone astronaut wakes with amnesia on a spaceship and has to stop a disaster that threatens all life on Earth."
    ),
    new Book(
        "The Name of the Wind",
        "Patrick Rothfuss",
        2007,
        "A gifted young musician and magician tells the story of his rise from orphan to legend."
    ),
    new Book(
        "Klara and the Sun",
        "Kazuo Ishiguro",
        2021,
        "An artificial friend watches human love and loneliness while hoping a child will pick her."
    ),
    new Book(
        "Dune",
        "Frank Herbert",
        1965,
        "On a desert planet prized for a rare spice, a young heir is pulled into a war over ecology, religion, and power."
    )
};

var operations = new BulkOperationsCollection();
foreach (var book in books)
{
    operations.Add(new BulkIndexOperation<Book>(book)
    {
        Index = "books"
    });
}

var bulkResponse = await es.BulkAsync(new BulkRequest
{
    Refresh = Refresh.WaitFor,
    Operations = operations
});

public record Book(
    string Title,
    string Author,
    [property: JsonPropertyName("release_year")] int ReleaseYear,
    string Description
);
```

:::{dropdown} Check that all books were indexed
A bulk request can return a successful HTTP response even when an individual operation fails. Add this code after the `BulkAsync` call and before the `Book` record declaration:

```csharp
if (!bulkResponse.IsValidResponse || bulkResponse.Errors)
{
    throw new Exception("One or more books failed to index");
}
Console.WriteLine($"Indexed {bulkResponse.Items.Count} books");
```
:::

::::

::::{tab-item} Java
:sync: java

```java
record Book(
    String title,
    String author,
    int release_year,
    String description
) {}

Book[] books = {
    new Book(
        "The Left Hand of Darkness",
        "Ursula K. Le Guin",
        1969,
        "An envoy visits an icy planet whose people have no fixed gender, feeling out politics and friendship across a deep cultural gap."
    ),
    new Book(
        "Project Hail Mary",
        "Andy Weir",
        2021,
        "A lone astronaut wakes with amnesia on a spaceship and has to stop a disaster that threatens all life on Earth."
    ),
    new Book(
        "The Name of the Wind",
        "Patrick Rothfuss",
        2007,
        "A gifted young musician and magician tells the story of his rise from orphan to legend."
    ),
    new Book(
        "Klara and the Sun",
        "Kazuo Ishiguro",
        2021,
        "An artificial friend watches human love and loneliness while hoping a child will pick her."
    ),
    new Book(
        "Dune",
        "Frank Herbert",
        1965,
        "On a desert planet prized for a rare spice, a young heir is pulled into a war over ecology, religion, and power."
    )
};

BulkRequest.Builder bulk = new BulkRequest.Builder()
    .refresh(Refresh.WaitFor);

for (Book book : books) {
    bulk.operations(op -> op
        .index(idx -> idx
            .index("books")
            .document(book)
        )
    );
}

BulkResponse bulkResponse = es.bulk(bulk.build());
```

:::{dropdown} Check that all books were indexed
A bulk request can return a successful HTTP response even when an individual operation fails. Check the bulk result before continuing:

```java
if (bulkResponse.errors()) {
    throw new RuntimeException("One or more books failed to index");
}
System.out.println("Indexed " + bulkResponse.items().size() + " books");
```
:::

::::

::::{tab-item} Go
:sync: go

```go
type Book struct {
	Title       string `json:"title"`
	Author      string `json:"author"`
	ReleaseYear int    `json:"release_year"`
	Description string `json:"description"`
}

books := []Book{
	{
		Title:       "The Left Hand of Darkness",
		Author:      "Ursula K. Le Guin",
		ReleaseYear: 1969,
		Description: "An envoy visits an icy planet whose people have no fixed gender, feeling out politics and friendship across a deep cultural gap.",
	},
	{
		Title:       "Project Hail Mary",
		Author:      "Andy Weir",
		ReleaseYear: 2021,
		Description: "A lone astronaut wakes with amnesia on a spaceship and has to stop a disaster that threatens all life on Earth.",
	},
	{
		Title:       "The Name of the Wind",
		Author:      "Patrick Rothfuss",
		ReleaseYear: 2007,
		Description: "A gifted young musician and magician tells the story of his rise from orphan to legend.",
	},
	{
		Title:       "Klara and the Sun",
		Author:      "Kazuo Ishiguro",
		ReleaseYear: 2021,
		Description: "An artificial friend watches human love and loneliness while hoping a child will pick her.",
	},
	{
		Title:       "Dune",
		Author:      "Frank Herbert",
		ReleaseYear: 1965,
		Description: "On a desert planet prized for a rare spice, a young heir is pulled into a war over ecology, religion, and power.",
	},
}

indexer, err := esutil.NewBulkIndexer(esutil.BulkIndexerConfig{
	Client:  es,
	Index:   "books",
	Refresh: "wait_for",
})
if err != nil {
	panic(err)
}

ctx := context.Background()
for _, book := range books {
	data, err := json.Marshal(book)
	if err != nil {
		panic(err)
	}

	err = indexer.Add(ctx, esutil.BulkIndexerItem{
		Action: "index",
		Body:   bytes.NewReader(data),
	})
	if err != nil {
		panic(err)
	}
}

if err := indexer.Close(ctx); err != nil {
	panic(err)
}
```

:::{dropdown} Check that all books were indexed
A bulk request can return a successful HTTP response even when an individual operation fails. Check the bulk result before continuing:

```go
stats := indexer.Stats()
if stats.NumFailed > 0 {
	panic("One or more books failed to index")
}
fmt.Printf("Indexed %d books\n", stats.NumIndexed)
```
:::

::::

::::{tab-item} Console
:sync: console

```console
POST books/_bulk?refresh=wait_for
{ "index": {} }
{ "title": "The Left Hand of Darkness", "author": "Ursula K. Le Guin", "release_year": 1969, "description": "An envoy visits an icy planet whose people have no fixed gender, feeling out politics and friendship across a deep cultural gap." }
{ "index": {} }
{ "title": "Project Hail Mary", "author": "Andy Weir", "release_year": 2021, "description": "A lone astronaut wakes with amnesia on a spaceship and has to stop a disaster that threatens all life on Earth." }
{ "index": {} }
{ "title": "The Name of the Wind", "author": "Patrick Rothfuss", "release_year": 2007, "description": "A gifted young musician and magician tells the story of his rise from orphan to legend." }
{ "index": {} }
{ "title": "Klara and the Sun", "author": "Kazuo Ishiguro", "release_year": 2021, "description": "An artificial friend watches human love and loneliness while hoping a child will pick her." }
{ "index": {} }
{ "title": "Dune", "author": "Frank Herbert", "release_year": 1965, "description": "On a desert planet prized for a rare spice, a young heir is pulled into a war over ecology, religion, and power." }
```

:::{dropdown} Check that all books were indexed
A bulk request can return a successful HTTP response even when an individual operation fails. Confirm that the response contains `"errors": false`, then run:

```console
GET books/_count
```

The response should contain `"count": 5`.
:::

::::

::::{tab-item} curl
:sync: curl

```bash
curl -X POST "$ES_URL/books/_bulk?refresh=wait_for" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/x-ndjson" \
  --data-binary @- <<'EOF'
{ "index": {} }
{ "title": "The Left Hand of Darkness", "author": "Ursula K. Le Guin", "release_year": 1969, "description": "An envoy visits an icy planet whose people have no fixed gender, feeling out politics and friendship across a deep cultural gap." }
{ "index": {} }
{ "title": "Project Hail Mary", "author": "Andy Weir", "release_year": 2021, "description": "A lone astronaut wakes with amnesia on a spaceship and has to stop a disaster that threatens all life on Earth." }
{ "index": {} }
{ "title": "The Name of the Wind", "author": "Patrick Rothfuss", "release_year": 2007, "description": "A gifted young musician and magician tells the story of his rise from orphan to legend." }
{ "index": {} }
{ "title": "Klara and the Sun", "author": "Kazuo Ishiguro", "release_year": 2021, "description": "An artificial friend watches human love and loneliness while hoping a child will pick her." }
{ "index": {} }
{ "title": "Dune", "author": "Frank Herbert", "release_year": 1965, "description": "On a desert planet prized for a rare spice, a young heir is pulled into a war over ecology, religion, and power." }
EOF
```

:::{dropdown} Check that all books were indexed
A bulk request can return a successful HTTP response even when an individual operation fails. Confirm that the response contains `"errors": false`, then run:

```bash
curl -X GET "$ES_URL/books/_count" \
  -H "Authorization: ApiKey $ES_API_KEY"
```

The response should contain `"count": 5`.
:::

::::

:::::

## Run searches [vector-full-text-search-search]

In this section, you run three searches on the same books dataset. [Full-text search](/solutions/search/full-text.md) matches [analyzed query terms](/manage-data/data-store/text-analysis.md), [semantic search](/solutions/search/vector.md#semantic-search-vs-vector-search) finds text with related meaning, and [hybrid search](/solutions/search/hybrid-search.md) combines both approaches.

:::{note}
The example outputs show rounded scores. Your exact scores might be different, especially for full-text and hybrid search, because relevance scores depend on how {{es}} stores your documents. With the Jina endpoint assumed in this quickstart, the order of the results should stay the same.
:::

### Full-text search [vector-full-text-search-keyword]

Run a full-text search for `wind` in the `title` field:

:::::{tab-set}
:group: languages

::::{tab-item} Python
:sync: python

```python
resp = es.search(
    index="books",
    query={
        "match": {
            "title": "wind",
        }
    },
)

for hit in resp["hits"]["hits"]:
    print(hit["_score"], hit["_source"]["title"])
```

::::

::::{tab-item} TypeScript
:sync: typescript

```typescript
interface Book {
  title: string;
}

const resp = await es.search<Book>({
  index: "books",
  query: {
    match: {
      title: "wind",
    },
  },
});

for (const hit of resp.hits.hits) {
  console.log(hit._score, hit._source?.title);
}
```

::::

::::{tab-item} PHP
:sync: php

```php
$response = $es->search([
    "index" => "books",
    "body" => [
        "query" => [
            "match" => [
                "title" => "wind",
            ],
        ],
    ],
]);

foreach ($response["hits"]["hits"] as $hit) {
    echo $hit["_score"] . " " . $hit["_source"]["title"] . "\n";
}
```

::::

::::{tab-item} Ruby
:sync: ruby

```ruby
response = es.search(
  index: "books",
  body: {
    query: {
      match: {
        title: "wind"
      }
    }
  }
)

response["hits"]["hits"].each do |hit|
  puts "#{hit["_score"]} #{hit["_source"]["title"]}"
end
```

::::

::::{tab-item} C# (.NET)
:sync: csharp

```csharp
var response = await es.SearchAsync<SearchBook>(s => s
    .Indices("books")
    .Query(q => q
        .Match(match => match
            .Field(book => book.Title)
            .Query("wind")
        )
    )
);

foreach (var hit in response.Hits)
{
    Console.WriteLine($"{hit.Score} {hit.Source?.Title}");
}

public record SearchBook(
    [property: JsonPropertyName("title")] string Title
);
```

::::

::::{tab-item} Java
:sync: java

```java
String query = """
    {
      "query": {
        "match": {
          "title": "wind"
        }
      }
    }
    """;

SearchResponse<Book> response = es.search(s -> s
        .index("books")
        .withJson(new StringReader(query)),
    Book.class
);

for (Hit<Book> hit : response.hits().hits()) {
    System.out.println(hit.score() + " " + hit.source().title());
}
```

::::

::::{tab-item} Go
:sync: go

```go
query := strings.NewReader(`{
	  "query": {
	    "match": {
	      "title": "wind"
	    }
	  }
	}`)

	res, err := es.Search(
		es.Search.WithContext(context.Background()),
		es.Search.WithIndex("books"),
		es.Search.WithBody(query),
	)
	if err != nil {
		log.Fatal(err)
	}
	defer res.Body.Close()
	if res.IsError() {
		log.Fatal(res)
	}

	var response struct {
		Hits struct {
			Hits []struct {
				Score  float64 `json:"_score"`
				Source struct {
					Title string `json:"title"`
				} `json:"_source"`
			} `json:"hits"`
		} `json:"hits"`
	}
	if err := json.NewDecoder(res.Body).Decode(&response); err != nil {
		log.Fatal(err)
	}

for _, hit := range response.Hits.Hits {
	fmt.Println(hit.Score, hit.Source.Title)
}
```

::::

::::{tab-item} Console
:sync: console

```console
GET books/_search
{
  "query": {
    "match": {
      "title": "wind"
    }
  }
}
```

::::

::::{tab-item} curl
:sync: curl

```bash
curl -X GET "$ES_URL/books/_search" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "match": {
        "title": "wind"
      }
    }
  }'
```

::::

:::::

:::{dropdown} Example output
The first result is:

```text
0.29 The Name of the Wind
```

**The Name of the Wind** ranks first because the title contains the word "wind".
:::

### Semantic search [vector-full-text-search-semantic]

Run a semantic search against the `description` field:

:::::{tab-set}
:group: languages

::::{tab-item} Python
:sync: python

```python
resp = es.search(
    index="books",
    query={
        "semantic": {
            "field": "description",
            "query": "surviving alone in space",
        }
    },
)

for hit in resp["hits"]["hits"]:
    print(hit["_score"], hit["_source"]["title"])
```

::::

::::{tab-item} TypeScript
:sync: typescript

```typescript
interface Book {
  title: string;
}

const resp = await es.search<Book>({
  index: "books",
  query: {
    semantic: {
      field: "description",
      query: "surviving alone in space",
    },
  },
});

for (const hit of resp.hits.hits) {
  console.log(hit._score, hit._source?.title);
}
```

::::

::::{tab-item} PHP
:sync: php

```php
$response = $es->search([
    "index" => "books",
    "body" => [
        "query" => [
            "semantic" => [
                "field" => "description",
                "query" => "surviving alone in space",
            ],
        ],
    ],
]);

foreach ($response["hits"]["hits"] as $hit) {
    echo $hit["_score"] . " " . $hit["_source"]["title"] . "\n";
}
```

::::

::::{tab-item} Ruby
:sync: ruby

```ruby
response = es.search(
  index: "books",
  body: {
    query: {
      semantic: {
        field: "description",
        query: "surviving alone in space"
      }
    }
  }
)

response["hits"]["hits"].each do |hit|
  puts "#{hit["_score"]} #{hit["_source"]["title"]}"
end
```

::::

::::{tab-item} C# (.NET)
:sync: csharp

```csharp
var response = await es.SearchAsync<SearchBook>(s => s
    .Indices("books")
    .Query(q => q
        .Semantic(semantic => semantic
            .Field("description")
            .Query("surviving alone in space")
        )
    )
);

foreach (var hit in response.Hits)
{
    Console.WriteLine($"{hit.Score} {hit.Source?.Title}");
}

public record SearchBook(
    [property: JsonPropertyName("title")] string Title
);
```

::::

::::{tab-item} Java
:sync: java

```java
String query = """
    {
      "query": {
        "semantic": {
          "field": "description",
          "query": "surviving alone in space"
        }
      }
    }
    """;

SearchResponse<Book> response = es.search(s -> s
        .index("books")
        .withJson(new StringReader(query)),
    Book.class
);

for (Hit<Book> hit : response.hits().hits()) {
    System.out.println(hit.score() + " " + hit.source().title());
}
```

::::

::::{tab-item} Go
:sync: go

```go
query := strings.NewReader(`{
	  "query": {
	    "semantic": {
	      "field": "description",
	      "query": "surviving alone in space"
	    }
	  }
	}`)

	res, err := es.Search(
		es.Search.WithContext(context.Background()),
		es.Search.WithIndex("books"),
		es.Search.WithBody(query),
	)
	if err != nil {
		log.Fatal(err)
	}
	defer res.Body.Close()
	if res.IsError() {
		log.Fatal(res)
	}

	var response struct {
		Hits struct {
			Hits []struct {
				Score  float64 `json:"_score"`
				Source struct {
					Title string `json:"title"`
				} `json:"_source"`
			} `json:"hits"`
		} `json:"hits"`
	}
	if err := json.NewDecoder(res.Body).Decode(&response); err != nil {
		log.Fatal(err)
	}

for _, hit := range response.Hits.Hits {
	fmt.Println(hit.Score, hit.Source.Title)
}
```

::::

::::{tab-item} Console
:sync: console

```console
GET books/_search
{
  "query": {
    "semantic": {
      "field": "description",
      "query": "surviving alone in space"
    }
  }
}
```

::::

::::{tab-item} curl
:sync: curl

```bash
curl -X GET "$ES_URL/books/_search" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "semantic": {
        "field": "description",
        "query": "surviving alone in space"
      }
    }
  }'
```

::::

:::::

:::{dropdown} Example output
The first result is:

```text
0.78 Project Hail Mary
```

**Project Hail Mary** ranks first because its description includes "A lone astronaut," which is semantically similar to "surviving alone in space" even though the wording differs.
:::

### Hybrid search [vector-full-text-search-hybrid]

Hybrid search combines semantic search with full-text search. This example searches for `friendship` in two ways. A full-text `match` query on `description.text` finds the exact word, and a `semantic` query on `description` finds text with a similar meaning:

:::::{tab-set}
:group: languages

::::{tab-item} Python
:sync: python

```python
resp = es.search(
    index="books",
    query={
        "bool": {
            "should": [
                {
                    "match": { <1>
                        "description.text": "friendship"
                    }
                },
                {
                    "semantic": { <2>
                        "field": "description",
                        "query": "friendship",
                    }
                },
            ]
        }
    },
)

for hit in resp["hits"]["hits"]:
    print(hit["_score"], hit["_source"]["title"])
```

1. The `match` clause performs full-text search on the `description.text` subfield and scores how well the analyzed text matches `friendship`.
2. The `semantic` clause searches `description` by meaning, so it can also match books that never use the word `friendship`.

::::

::::{tab-item} TypeScript
:sync: typescript

```typescript
interface Book {
  title: string;
}

const resp = await es.search<Book>({
  index: "books",
  query: {
    bool: {
      should: [
        {
          match: { <1>
            "description.text": "friendship",
          },
        },
        {
          semantic: { <2>
            field: "description",
            query: "friendship",
          },
        },
      ],
    },
  },
});

for (const hit of resp.hits.hits) {
  console.log(hit._score, hit._source?.title);
}
```

1. The `match` clause performs full-text search on the `description.text` subfield and scores how well the analyzed text matches `friendship`.
2. The `semantic` clause searches `description` by meaning, so it can also match books that never use the word `friendship`.

::::

::::{tab-item} PHP
:sync: php

```php
$response = $es->search([
    "index" => "books",
    "body" => [
        "query" => [
            "bool" => [
                "should" => [
                    [
                        "match" => [ <1>
                            "description.text" => "friendship",
                        ],
                    ],
                    [
                        "semantic" => [ <2>
                            "field" => "description",
                            "query" => "friendship",
                        ],
                    ],
                ],
            ],
        ],
    ],
]);

foreach ($response["hits"]["hits"] as $hit) {
    echo $hit["_score"] . " " . $hit["_source"]["title"] . "\n";
}
```

1. The `match` clause performs full-text search on the `description.text` subfield and scores how well the analyzed text matches `friendship`.
2. The `semantic` clause searches `description` by meaning, so it can also match books that never use the word `friendship`.

::::

::::{tab-item} Ruby
:sync: ruby

```ruby
response = es.search(
  index: "books",
  body: {
    query: {
      bool: {
        should: [
          {
            match: { <1>
              "description.text": "friendship"
            }
          },
          {
            semantic: { <2>
              field: "description",
              query: "friendship"
            }
          }
        ]
      }
    }
  }
)

response["hits"]["hits"].each do |hit|
  puts "#{hit["_score"]} #{hit["_source"]["title"]}"
end
```

1. The `match` clause performs full-text search on the `description.text` subfield and scores how well the analyzed text matches `friendship`.
2. The `semantic` clause searches `description` by meaning, so it can also match books that never use the word `friendship`.

::::

::::{tab-item} C# (.NET)
:sync: csharp

```csharp
var response = await es.SearchAsync<SearchBook>(s => s
    .Indices("books")
    .Query(q => q
        .Bool(b => b
            .Should(
                should => should
                    .Match(match => match <1>
                        .Field("description.text")
                        .Query("friendship")
                    ),
                should => should
                    .Semantic(semantic => semantic <2>
                        .Field("description")
                        .Query("friendship")
                    )
            )
        )
    )
);

foreach (var hit in response.Hits)
{
    Console.WriteLine($"{hit.Score} {hit.Source?.Title}");
}

public record SearchBook(
    [property: JsonPropertyName("title")] string Title
);
```

1. The `match` clause performs full-text search on the `description.text` subfield and scores how well the analyzed text matches `friendship`.
2. The `semantic` clause searches `description` by meaning, so it can also match books that never use the word `friendship`.

::::

::::{tab-item} Java
:sync: java

```java
String query = """
    {
      "query": {
        "bool": {
          "should": [
            {
              "match": { <1>
                "description.text": "friendship"
              }
            },
            {
              "semantic": { <2>
                "field": "description",
                "query": "friendship"
              }
            }
          ]
        }
      }
    }
    """;

SearchResponse<Book> response = es.search(s -> s
        .index("books")
        .withJson(new StringReader(query)),
    Book.class
);

for (Hit<Book> hit : response.hits().hits()) {
    System.out.println(hit.score() + " " + hit.source().title());
}
```

1. The `match` clause performs full-text search on the `description.text` subfield and scores how well the analyzed text matches `friendship`.
2. The `semantic` clause searches `description` by meaning, so it can also match books that never use the word `friendship`.

::::

::::{tab-item} Go
:sync: go

```go
query := strings.NewReader(`{
	  "query": {
	    "bool": {
	      "should": [
	        {
	          "match": { <1>
	            "description.text": "friendship"
	          }
	        },
	        {
	          "semantic": { <2>
	            "field": "description",
	            "query": "friendship"
	          }
	        }
	      ]
	    }
	  }
	}`)

	res, err := es.Search(
		es.Search.WithContext(context.Background()),
		es.Search.WithIndex("books"),
		es.Search.WithBody(query),
	)
	if err != nil {
		log.Fatal(err)
	}
	defer res.Body.Close()
	if res.IsError() {
		log.Fatal(res)
	}

	var response struct {
		Hits struct {
			Hits []struct {
				Score  float64 `json:"_score"`
				Source struct {
					Title string `json:"title"`
				} `json:"_source"`
			} `json:"hits"`
		} `json:"hits"`
	}
	if err := json.NewDecoder(res.Body).Decode(&response); err != nil {
		log.Fatal(err)
	}

for _, hit := range response.Hits.Hits {
	fmt.Println(hit.Score, hit.Source.Title)
}
```

1. The `match` clause performs full-text search on the `description.text` subfield and scores how well the analyzed text matches `friendship`.
2. The `semantic` clause searches `description` by meaning, so it can also match books that never use the word `friendship`.

::::

::::{tab-item} Console
:sync: console

```console
GET books/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "match": { <1>
            "description.text": "friendship"
          }
        },
        {
          "semantic": { <2>
            "field": "description",
            "query": "friendship"
          }
        }
      ]
    }
  }
}
```

1. The `match` clause performs full-text search on the `description.text` subfield and scores how well the analyzed text matches `friendship`.
2. The `semantic` clause searches `description` by meaning, so it can also match books that never use the word `friendship`.

::::

::::{tab-item} curl
:sync: curl

```bash
curl -X GET "$ES_URL/books/_search" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "bool": {
        "should": [
          {
            "match": { <1>
              "description.text": "friendship"
            }
          },
          {
            "semantic": { <2>
              "field": "description",
              "query": "friendship"
            }
          }
        ]
      }
    }
  }'
```

1. The `match` clause performs full-text search on the `description.text` subfield and scores how well the analyzed text matches `friendship`.
2. The `semantic` clause searches `description` by meaning, so it can also match books that never use the word `friendship`.

::::

:::::

:::{dropdown} Example output
The first two results are:

```text
0.91 The Left Hand of Darkness
0.67 Klara and the Sun
```

They match the query for different reasons:

- **The Left Hand of Darkness** matches both clauses. Its description contains the word "friendship", and its meaning is also similar to the query.
- **Klara and the Sun** matches only the semantic clause. Its description doesn't contain "friendship", but "an artificial friend" is close in meaning. Semantic search alone ranks it first.

The exact word match moves **The Left Hand of Darkness** to the top. Hybrid search ranks it above the book that is closest in meaning, so you get both kinds of relevance in one ranking. In this small dataset, the semantic clause already returns all five books, so the full-text clause doesn't add results. It changes their order.
:::

## Aggregate the data with {{esql}} [vector-full-text-search-esql]

Use [{{esql}}](elasticsearch://reference/query-languages/esql.md) to summarize, analyze, and calculate metrics on your data. This query counts the books released in each decade:

:::::{tab-set}
:group: languages

::::{tab-item} Python
:sync: python

```python
resp = es.esql.query(query="""
    FROM books
    | STATS books = COUNT(*) BY decade = release_year - (release_year % 10)
    | SORT decade ASC
    | LIMIT 10
""")

cols = {c["name"]: i for i, c in enumerate(resp["columns"])}
for row in resp["values"]:
    print(f"{row[cols['decade']]}s: {row[cols['books']]}")
```

::::

::::{tab-item} TypeScript
:sync: typescript

```typescript
const resp = await es.esql.query({
  query: `
    FROM books
    | STATS books = COUNT(*) BY decade = release_year - (release_year % 10)
    | KEEP decade, books
    | SORT decade ASC
  `,
});

for (const [decade, count] of resp.values ?? []) {
  console.log(`${decade}s: ${count}`);
}
```

::::

::::{tab-item} PHP
:sync: php

```php
$response = $es->esql()->query([
    "body" => [
        "query" => <<<'ESQL'
            FROM books
            | STATS books = COUNT(*) BY decade = release_year - (release_year % 10)
            | KEEP decade, books
            | SORT decade ASC
            ESQL,
    ],
]);

foreach ($response["values"] as [$decade, $count]) {
    echo $decade . "s: " . $count . "\n";
}
```

::::

::::{tab-item} Ruby
:sync: ruby

```ruby
response = es.esql.query(
  body: {
    query: <<~ESQL
      FROM books
      | STATS books = COUNT(*) BY decade = release_year - (release_year % 10)
      | KEEP decade, books
      | SORT decade ASC
    ESQL
  }
)

response["values"].each do |decade, count|
  puts "#{decade}s: #{count}"
end
```

::::

::::{tab-item} C# (.NET)
:sync: csharp

```csharp
var response = await es.Esql.QueryAsync(r => r
    .Query("""
        FROM books
        | STATS books = COUNT(*) BY decade = release_year - (release_year % 10)
        | KEEP decade, books
        | SORT decade ASC
        """)
    .Format(EsqlFormat.Json)
);

using var result = JsonDocument.Parse(response.Body);
foreach (
    var row in result.RootElement.GetProperty("values").EnumerateArray()
)
{
    Console.WriteLine($"{row[0]}s: {row[1]}");
}
```

::::

::::{tab-item} Java
:sync: java

```java
String query = """
    FROM books
    | STATS books = COUNT(*) BY decade = release_year - (release_year % 10)
    | KEEP decade, books
    | SORT decade ASC
    """;

BinaryResponse response = es.esql().query(q -> q
    .query(query)
    .format(EsqlFormat.Csv)
);

try (BufferedReader reader = new BufferedReader(
    new InputStreamReader(response.content())
)) {
    reader.lines().skip(1).forEach(line -> {
        String[] values = line.split(",", -1);
        System.out.println(values[0] + "s: " + values[1]);
    });
}
```

::::

::::{tab-item} Go
:sync: go

```go
typed, err := elasticsearch.NewTyped(
	elasticsearch.WithAddresses(os.Getenv("ES_URL")),
	elasticsearch.WithAPIKey(os.Getenv("ES_API_KEY")),
)
if err != nil {
	log.Fatal(err)
}

query := `FROM books
		| STATS books = COUNT(*) BY decade = release_year - (release_year % 10)
		| KEEP decade, books
		| SORT decade ASC`

response, err := typed.Esql.Query().
		Query(query).
		Format(esqlformat.Csv).
		Do(context.Background())
	if err != nil {
		log.Fatal(err)
	}

	rows, err := csv.NewReader(bytes.NewReader(response)).ReadAll()
	if err != nil {
		log.Fatal(err)
	}

for _, row := range rows[1:] {
	fmt.Printf("%ss: %s\n", row[0], row[1])
}
```

::::

::::{tab-item} Console
:sync: console

```console
POST _query
{
  "query": """
    FROM books
    | STATS books = COUNT(*) BY decade = release_year - (release_year % 10)
    | KEEP decade, books
    | SORT decade ASC
  """
}
```

::::

::::{tab-item} curl
:sync: curl

```bash
curl -X POST "$ES_URL/_query" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "FROM books | STATS books = COUNT(*) BY decade = release_year - (release_year % 10) | KEEP decade, books | SORT decade ASC"
  }'
```

::::

:::::

:::{dropdown} Example output
The output contains one row per decade:

```text
1960s: 2
2000s: 1
2020s: 2
```
:::

You can also use {{esql}} inference capabilities to build search workflows:

- [`TEXT_EMBEDDING`](elasticsearch://reference/query-languages/esql/functions-operators/dense-vector-functions/text_embedding.md) generates embeddings from text. For example, turn a reader's description of their ideal book into a query vector for similarity search.
- [`EMBEDDING`](elasticsearch://reference/query-languages/esql/functions-operators/dense-vector-functions/embedding.md) generates embeddings from multimodal input. For example, use an image as the starting point for a search.
- [`COMPLETION`](elasticsearch://reference/query-languages/esql/commands/completion.md) sends prompts to an LLM. For example, summarize retrieved books or explain why they match a reader's interests.
- [`RERANK`](elasticsearch://reference/query-languages/esql/commands/rerank.md) re-scores search results with an inference model. For example, reorder books to better match a detailed reading request.

Availability and lifecycle status vary by version and deployment type. Refer to each linked page for details.

To explore these and other capabilities, refer to [{{esql}} for search](/solutions/search/esql-for-search.md).

## Run the steps in one script [vector-full-text-search-complete-script]

The examples above show each step on its own. This script runs them together: it creates an index, adds the sample books, runs a keyword search, a semantic search, and a hybrid search, and counts the books by decade.

1. [Set up {{es}}](#vector-full-text-search-create-project).
2. [Choose how to run the examples](#vector-full-text-search-install-sdk). If you use a language client, install and initialize it.
3. [Connect to your deployment or project](#vector-full-text-search-connect). If you use Console, skip this step.
4. Select the corresponding tab and expand the complete script. For a language client, save and run it using the file name and command shown.

:::{tip}
To rerun the examples, use a new index name consistently throughout the requests. The step-by-step examples use `books`, while the complete scripts use `books-complete`.
:::

:::::{tab-set}
:group: languages

::::{tab-item} Python
:sync: python

Save the script as `quickstart.py` in the project directory, then run it from the activated virtual environment:

```bash
python3 quickstart.py
```

:::{dropdown} Complete runnable script

```python
import os
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch(os.environ["ES_URL"], api_key=os.environ["ES_API_KEY"])

# Declare the semantically searchable field. Other fields are inferred on ingest.
es.indices.create(
    index="books-complete",
    mappings={"properties": {"description": {"type": "semantic_text", "fields": {"text": {"type": "text"}}}}},
)

# Index the sample data.
books = [
    {"title": "The Left Hand of Darkness", "author": "Ursula K. Le Guin", "release_year": 1969,
     "description": "An envoy visits an icy planet whose people have no fixed gender, feeling out politics and friendship across a deep cultural gap."},
    {"title": "Project Hail Mary", "author": "Andy Weir", "release_year": 2021,
     "description": "A lone astronaut wakes with amnesia on a spaceship and has to stop a disaster that threatens all life on Earth."},
    {"title": "The Name of the Wind", "author": "Patrick Rothfuss", "release_year": 2007,
     "description": "A gifted young musician and magician tells the story of his rise from orphan to legend."},
    {"title": "Klara and the Sun", "author": "Kazuo Ishiguro", "release_year": 2021,
     "description": "An artificial friend watches human love and loneliness while hoping a child will pick her."},
    {"title": "Dune", "author": "Frank Herbert", "release_year": 1965,
     "description": "On a desert planet prized for a rare spice, a young heir is pulled into a war over ecology, religion, and power."},
]
success_count, errors = helpers.bulk(
    es,
    ({"_index": "books-complete", "_source": b} for b in books),
    refresh="wait_for",
    raise_on_error=False,
)
if errors:
    raise RuntimeError(f"{len(errors)} book(s) failed to index")

# Keyword search.
resp = es.search(
    index="books-complete",
    query={"match": {"title": "wind"}},
)
print("=== Keyword search results ===")
for hit in resp["hits"]["hits"]:
    print(" ", hit["_score"], hit["_source"]["title"])

# Semantic search.
resp = es.search(
    index="books-complete",
    query={"semantic": {"field": "description", "query": "surviving alone in space"}},
)
print("=== Semantic search results ===")
for hit in resp["hits"]["hits"]:
    print(" ", hit["_score"], hit["_source"]["title"])

# Hybrid search with keyword and semantic queries.
resp = es.search(
    index="books-complete",
    query={"bool": {"should": [
        {"match": {"description.text": "friendship"}},
        {"semantic": {"field": "description", "query": "friendship"}},
    ]}},
)
print("\n=== Hybrid search results ===")
for hit in resp["hits"]["hits"]:
    print(" ", hit["_score"], hit["_source"]["title"])

# Count books per decade.
resp = es.esql.query(query="""
    FROM "books-complete"
    | STATS books = COUNT(*) BY decade = release_year - (release_year % 10)
    | SORT decade ASC
    | LIMIT 10
""")

cols = {c["name"]: i for i, c in enumerate(resp["columns"])}
print("\n=== Books by decade ===")
for row in resp["values"]:
    print(f"{row[cols['decade']]}s: {row[cols['books']]}")
```

:::

::::

::::{tab-item} TypeScript
:sync: typescript

Save the script as `quickstart.ts` in the project directory, then run it:

```bash
npx tsx quickstart.ts
```

:::{dropdown} Complete runnable script

```typescript
import { Client } from "@elastic/elasticsearch";

interface Book {
  title: string;
}

const es = new Client({
  node: process.env.ES_URL,
  auth: { apiKey: process.env.ES_API_KEY! },
});

// Declare the semantically searchable field. Other fields are inferred on ingest.
await es.indices.create({
  index: "books-complete",
  mappings: { properties: { description: { type: "semantic_text", fields: { text: { type: "text" } } } } },
});

// Index the sample data.
const books = [
  { title: "The Left Hand of Darkness", author: "Ursula K. Le Guin", release_year: 1969,
    description: "An envoy visits an icy planet whose people have no fixed gender, feeling out politics and friendship across a deep cultural gap." },
  { title: "Project Hail Mary", author: "Andy Weir", release_year: 2021,
    description: "A lone astronaut wakes with amnesia on a spaceship and has to stop a disaster that threatens all life on Earth." },
  { title: "The Name of the Wind", author: "Patrick Rothfuss", release_year: 2007,
    description: "A gifted young musician and magician tells the story of his rise from orphan to legend." },
  { title: "Klara and the Sun", author: "Kazuo Ishiguro", release_year: 2021,
    description: "An artificial friend watches human love and loneliness while hoping a child will pick her." },
  { title: "Dune", author: "Frank Herbert", release_year: 1965,
    description: "On a desert planet prized for a rare spice, a young heir is pulled into a war over ecology, religion, and power." },
];
const bulkResult = await es.helpers.bulk({
  datasource: books,
  onDocument: () => ({ index: { _index: "books-complete" } }),
  refreshOnCompletion: true,
});
if (bulkResult.failed > 0) {
  throw new Error(`${bulkResult.failed} book(s) failed to index`);
}

// Keyword search.
let resp = await es.search<Book>({
  index: "books-complete",
  query: { match: { title: "wind" } },
});
console.log("=== Keyword search results ===");
for (const hit of resp.hits.hits) {
  console.log(" ", hit._score, hit._source?.title);
}

// Semantic search.
resp = await es.search<Book>({
  index: "books-complete",
  query: { semantic: { field: "description", query: "surviving alone in space" } },
});
console.log("=== Semantic search results ===");
for (const hit of resp.hits.hits) {
  console.log(" ", hit._score, hit._source?.title);
}

// Hybrid search with keyword and semantic queries.
resp = await es.search<Book>({
  index: "books-complete",
  query: { bool: { should: [
    { match: { "description.text": "friendship" } },
    { semantic: { field: "description", query: "friendship" } },
  ] } },
});
console.log("\n=== Hybrid search results ===");
for (const hit of resp.hits.hits) {
  console.log(" ", hit._score, hit._source?.title);
}

// Count books per decade.
const agg = await es.esql.query({ query: `
  FROM "books-complete"
  | STATS books = COUNT(*) BY decade = release_year - (release_year % 10)
  | KEEP decade, books
  | SORT decade ASC
` });
console.log("\n=== Books by decade ===", agg.values);
```

:::

::::

::::{tab-item} PHP
:sync: php

Save the script as `quickstart.php` in the directory that contains `vendor/`, then run it:

```bash
php quickstart.php
```

:::{dropdown} Complete runnable script

```php
<?php

require __DIR__ . "/vendor/autoload.php";

use Elastic\Elasticsearch\ClientBuilder;

$es = ClientBuilder::create()
    ->setHosts([getenv("ES_URL")])
    ->setApiKey(getenv("ES_API_KEY"))
    ->build();

$es->indices()->create([
    "index" => "books-complete",
    "body" => [
        "mappings" => [
            "properties" => [
                "description" => [
                    "type" => "semantic_text",
                    "fields" => ["text" => ["type" => "text"]],
                ],
            ],
        ],
    ],
]);

$books = [
    [
        "title" => "The Left Hand of Darkness",
        "author" => "Ursula K. Le Guin",
        "release_year" => 1969,
        "description" => "An envoy visits an icy planet whose people have no fixed gender, feeling out politics and friendship across a deep cultural gap.",
    ],
    [
        "title" => "Project Hail Mary",
        "author" => "Andy Weir",
        "release_year" => 2021,
        "description" => "A lone astronaut wakes with amnesia on a spaceship and has to stop a disaster that threatens all life on Earth.",
    ],
    [
        "title" => "The Name of the Wind",
        "author" => "Patrick Rothfuss",
        "release_year" => 2007,
        "description" => "A gifted young musician and magician tells the story of his rise from orphan to legend.",
    ],
    [
        "title" => "Klara and the Sun",
        "author" => "Kazuo Ishiguro",
        "release_year" => 2021,
        "description" => "An artificial friend watches human love and loneliness while hoping a child will pick her.",
    ],
    [
        "title" => "Dune",
        "author" => "Frank Herbert",
        "release_year" => 1965,
        "description" => "On a desert planet prized for a rare spice, a young heir is pulled into a war over ecology, religion, and power.",
    ],
];

$operations = [];
foreach ($books as $book) {
    $operations[] = ["index" => ["_index" => "books-complete"]];
    $operations[] = $book;
}

$bulkResponse = $es->bulk([
    "refresh" => "wait_for",
    "body" => $operations,
]);
if ($bulkResponse["errors"]) {
    throw new RuntimeException("One or more books failed to index");
}

$response = $es->search([
    "index" => "books-complete",
    "body" => [
        "query" => [
            "match" => [
                "title" => "wind",
            ],
        ],
    ],
]);
echo "=== Keyword search results ===\n";
foreach ($response["hits"]["hits"] as $hit) {
    echo "  " . $hit["_score"] . " " . $hit["_source"]["title"] . "\n";
}

$response = $es->search([
    "index" => "books-complete",
    "body" => [
        "query" => [
            "semantic" => [
                "field" => "description",
                "query" => "surviving alone in space",
            ],
        ],
    ],
]);
echo "=== Semantic search results ===\n";
foreach ($response["hits"]["hits"] as $hit) {
    echo "  " . $hit["_score"] . " " . $hit["_source"]["title"] . "\n";
}

$response = $es->search([
    "index" => "books-complete",
    "body" => [
        "query" => [
            "bool" => [
                "should" => [
                    ["match" => ["description.text" => "friendship"]],
                    ["semantic" => [
                        "field" => "description",
                        "query" => "friendship",
                    ]],
                ],
            ],
        ],
    ],
]);
echo "\n=== Hybrid search results ===\n";
foreach ($response["hits"]["hits"] as $hit) {
    echo "  " . $hit["_score"] . " " . $hit["_source"]["title"] . "\n";
}

$response = $es->esql()->query([
    "body" => [
        "query" => <<<'ESQL'
            FROM "books-complete"
            | STATS books = COUNT(*) BY decade = release_year - (release_year % 10)
            | KEEP decade, books
            | SORT decade ASC
            ESQL,
    ],
]);
echo "\n=== Books by decade ===\n";
foreach ($response["values"] as [$decade, $count]) {
    echo "  " . $decade . "s: " . $count . "\n";
}
```

:::

::::

::::{tab-item} Ruby
:sync: ruby

Save the script as `quickstart.rb` in the directory that contains the `Gemfile`, then run it:

```bash
bundle exec ruby quickstart.rb
```

:::{dropdown} Complete runnable script

```ruby
require "elasticsearch"

es = Elasticsearch::Client.new(
  url: ENV.fetch("ES_URL"),
  api_key: ENV.fetch("ES_API_KEY")
)

es.indices.create(
  index: "books-complete",
  body: {
    mappings: {
      properties: {
        description: {
          type: "semantic_text",
          fields: { text: { type: "text" } }
        }
      }
    }
  }
)

books = [
  {
    title: "The Left Hand of Darkness",
    author: "Ursula K. Le Guin",
    release_year: 1969,
    description: "An envoy visits an icy planet whose people have no fixed gender, feeling out politics and friendship across a deep cultural gap."
  },
  {
    title: "Project Hail Mary",
    author: "Andy Weir",
    release_year: 2021,
    description: "A lone astronaut wakes with amnesia on a spaceship and has to stop a disaster that threatens all life on Earth."
  },
  {
    title: "The Name of the Wind",
    author: "Patrick Rothfuss",
    release_year: 2007,
    description: "A gifted young musician and magician tells the story of his rise from orphan to legend."
  },
  {
    title: "Klara and the Sun",
    author: "Kazuo Ishiguro",
    release_year: 2021,
    description: "An artificial friend watches human love and loneliness while hoping a child will pick her."
  },
  {
    title: "Dune",
    author: "Frank Herbert",
    release_year: 1965,
    description: "On a desert planet prized for a rare spice, a young heir is pulled into a war over ecology, religion, and power."
  }
]

operations = books.flat_map do |book|
  [
    { index: { _index: "books-complete" } },
    book
  ]
end
bulk_response = es.bulk(body: operations, refresh: "wait_for")
raise "One or more books failed to index" if bulk_response["errors"]

response = es.search(
  index: "books-complete",
  body: {
    query: {
      match: {
        title: "wind"
      }
    }
  }
)
puts "=== Keyword search results ==="
response["hits"]["hits"].each do |hit|
  puts "  #{hit["_score"]} #{hit["_source"]["title"]}"
end

response = es.search(
  index: "books-complete",
  body: {
    query: {
      semantic: {
        field: "description",
        query: "surviving alone in space"
      }
    }
  }
)
puts "=== Semantic search results ==="
response["hits"]["hits"].each do |hit|
  puts "  #{hit["_score"]} #{hit["_source"]["title"]}"
end

response = es.search(
  index: "books-complete",
  body: {
    query: {
      bool: {
        should: [
          { match: { "description.text": "friendship" } },
          {
            semantic: {
              field: "description",
              query: "friendship"
            }
          }
        ]
      }
    }
  }
)
puts "\n=== Hybrid search results ==="
response["hits"]["hits"].each do |hit|
  puts "  #{hit["_score"]} #{hit["_source"]["title"]}"
end

response = es.esql.query(
  body: {
    query: <<~ESQL
      FROM "books-complete"
      | STATS books = COUNT(*) BY decade = release_year - (release_year % 10)
      | KEEP decade, books
      | SORT decade ASC
    ESQL
  }
)
puts "\n=== Books by decade ==="
response["values"].each do |decade, count|
  puts "  #{decade}s: #{count}"
end
```

:::

::::

::::{tab-item} C# (.NET)
:sync: csharp

Replace the contents of the generated `Program.cs` with the script, then run it:

```bash
dotnet run
```

:::{dropdown} Complete runnable script

```csharp
using System.Text.Json;
using System.Text.Json.Serialization;
using Elastic.Clients.Elasticsearch;
using Elastic.Clients.Elasticsearch.Core.Bulk;
using Elastic.Clients.Elasticsearch.Esql;
using Elastic.Transport;

var url = Environment.GetEnvironmentVariable("ES_URL")
    ?? throw new InvalidOperationException("ES_URL is not set.");
var apiKey = Environment.GetEnvironmentVariable("ES_API_KEY")
    ?? throw new InvalidOperationException("ES_API_KEY is not set.");

var settings = new ElasticsearchClientSettings(new Uri(url))
    .Authentication(new ApiKey(apiKey));
var es = new ElasticsearchClient(settings);

await es.Indices.CreateAsync<Book>("books-complete", c => c
    .Mappings(m => m
        .Properties(p => p
            .SemanticText(b => b.Description, st => st
                .Fields(f => f.Text("text"))
            )
        )
    )
);

var books = new List<Book>
{
    new(
        "The Left Hand of Darkness",
        "Ursula K. Le Guin",
        1969,
        "An envoy visits an icy planet whose people have no fixed gender, feeling out politics and friendship across a deep cultural gap."
    ),
    new(
        "Project Hail Mary",
        "Andy Weir",
        2021,
        "A lone astronaut wakes with amnesia on a spaceship and has to stop a disaster that threatens all life on Earth."
    ),
    new(
        "The Name of the Wind",
        "Patrick Rothfuss",
        2007,
        "A gifted young musician and magician tells the story of his rise from orphan to legend."
    ),
    new(
        "Klara and the Sun",
        "Kazuo Ishiguro",
        2021,
        "An artificial friend watches human love and loneliness while hoping a child will pick her."
    ),
    new(
        "Dune",
        "Frank Herbert",
        1965,
        "On a desert planet prized for a rare spice, a young heir is pulled into a war over ecology, religion, and power."
    )
};

var operations = new BulkOperationsCollection();
foreach (var book in books)
{
    operations.Add(new BulkIndexOperation<Book>(book)
    {
        Index = "books-complete"
    });
}
var bulkResponse = await es.BulkAsync(new BulkRequest
{
    Refresh = Refresh.WaitFor,
    Operations = operations
});
if (!bulkResponse.IsValidResponse || bulkResponse.Errors)
{
    throw new Exception("One or more books failed to index");
}

var response = await es.SearchAsync<Book>(s => s
    .Indices("books-complete")
    .Query(q => q
        .Match(match => match
            .Field(book => book.Title)
            .Query("wind")
        )
    )
);
Console.WriteLine("=== Keyword search results ===");
foreach (var hit in response.Hits)
{
    Console.WriteLine($"  {hit.Score} {hit.Source?.Title}");
}

response = await es.SearchAsync<Book>(s => s
    .Indices("books-complete")
    .Query(q => q
        .Semantic(semantic => semantic
            .Field("description")
            .Query("surviving alone in space")
        )
    )
);
Console.WriteLine("=== Semantic search results ===");
foreach (var hit in response.Hits)
{
    Console.WriteLine($"  {hit.Score} {hit.Source?.Title}");
}

response = await es.SearchAsync<Book>(s => s
    .Indices("books-complete")
    .Query(q => q
        .Bool(b => b
            .Should(
                should => should
                    .Match(match => match
                        .Field("description.text")
                        .Query("friendship")
                    ),
                should => should
                    .Semantic(semantic => semantic
                        .Field("description")
                        .Query("friendship")
                    )
            )
        )
    )
);
Console.WriteLine("\n=== Hybrid search results ===");
foreach (var hit in response.Hits)
{
    Console.WriteLine($"  {hit.Score} {hit.Source?.Title}");
}

var aggregation = await es.Esql.QueryAsync(r => r
    .Query("""
        FROM "books-complete"
        | STATS books = COUNT(*) BY decade = release_year - (release_year % 10)
        | KEEP decade, books
        | SORT decade ASC
        """)
    .Format(EsqlFormat.Json)
);
using var result = JsonDocument.Parse(aggregation.Body);
Console.WriteLine("\n=== Books by decade ===");
foreach (var row in result.RootElement.GetProperty("values").EnumerateArray())
{
    Console.WriteLine($"  {row[0]}s: {row[1]}");
}

public record Book(
    [property: JsonPropertyName("title")] string Title,
    [property: JsonPropertyName("author")] string Author,
    [property: JsonPropertyName("release_year")] int ReleaseYear,
    [property: JsonPropertyName("description")] string Description
);
```

:::

::::

::::{tab-item} Java
:sync: java

When you [set up the Java client](#vector-full-text-search-install-sdk), the `gradle init` command created a sample application and a test for it. Replace `app/src/main/java/quickstart/App.java` with this script, and delete `app/src/test/java/quickstart/AppTest.java` because it only tests the original sample application. Then run the script from the project root:

```bash
gradle run
```

:::{dropdown} Complete runnable script

```java
package quickstart;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.StringReader;
import java.util.List;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.elasticsearch._types.Refresh;
import co.elastic.clients.elasticsearch.core.BulkRequest;
import co.elastic.clients.elasticsearch.core.BulkResponse;
import co.elastic.clients.elasticsearch.core.SearchResponse;
import co.elastic.clients.elasticsearch.core.search.Hit;
import co.elastic.clients.elasticsearch.esql.EsqlFormat;
import co.elastic.clients.transport.endpoints.BinaryResponse;

public class App {
    record Book(
        String title,
        String author,
        int release_year,
        String description
    ) {}

    public static void main(String[] args) throws Exception {
        try (ElasticsearchClient es = ElasticsearchClient.of(b -> b
            .host(System.getenv("ES_URL"))
            .apiKey(System.getenv("ES_API_KEY"))
        )) {
            es.indices().create(c -> c
                .index("books-complete")
                .withJson(new StringReader("""
                    {
                      "mappings": {
                        "properties": {
                          "description": {
                            "type": "semantic_text",
                            "fields": {"text": {"type": "text"}}
                          }
                        }
                      }
                    }
                    """))
            );

            List<Book> books = List.of(
                new Book(
                    "The Left Hand of Darkness",
                    "Ursula K. Le Guin",
                    1969,
                    "An envoy visits an icy planet whose people have no fixed gender, feeling out politics and friendship across a deep cultural gap."
                ),
                new Book(
                    "Project Hail Mary",
                    "Andy Weir",
                    2021,
                    "A lone astronaut wakes with amnesia on a spaceship and has to stop a disaster that threatens all life on Earth."
                ),
                new Book(
                    "The Name of the Wind",
                    "Patrick Rothfuss",
                    2007,
                    "A gifted young musician and magician tells the story of his rise from orphan to legend."
                ),
                new Book(
                    "Klara and the Sun",
                    "Kazuo Ishiguro",
                    2021,
                    "An artificial friend watches human love and loneliness while hoping a child will pick her."
                ),
                new Book(
                    "Dune",
                    "Frank Herbert",
                    1965,
                    "On a desert planet prized for a rare spice, a young heir is pulled into a war over ecology, religion, and power."
                )
            );

            BulkRequest.Builder bulk = new BulkRequest.Builder()
                .refresh(Refresh.WaitFor);
            for (Book book : books) {
                bulk.operations(op -> op
                    .index(idx -> idx
                        .index("books-complete")
                        .document(book)
                    )
                );
            }
            BulkResponse bulkResponse = es.bulk(bulk.build());
            if (bulkResponse.errors()) {
                throw new RuntimeException("One or more books failed to index");
            }

            String keywordQuery = """
                {
                  "query": {
                    "match": {
                      "title": "wind"
                    }
                  }
                }
                """;
            SearchResponse<Book> response = es.search(s -> s
                    .index("books-complete")
                    .withJson(new StringReader(keywordQuery)),
                Book.class
            );
            System.out.println("=== Keyword search results ===");
            for (Hit<Book> hit : response.hits().hits()) {
                System.out.println("  " + hit.score() + " " + hit.source().title());
            }

            String semanticQuery = """
                {
                  "query": {
                    "semantic": {
                      "field": "description",
                      "query": "surviving alone in space"
                    }
                  }
                }
                """;
            response = es.search(s -> s
                    .index("books-complete")
                    .withJson(new StringReader(semanticQuery)),
                Book.class
            );
            System.out.println("=== Semantic search results ===");
            for (Hit<Book> hit : response.hits().hits()) {
                System.out.println("  " + hit.score() + " " + hit.source().title());
            }

            String hybridQuery = """
                {
                  "query": {
                    "bool": {
                      "should": [
                        {
                          "match": {
                            "description.text": "friendship"
                          }
                        },
                        {
                          "semantic": {
                            "field": "description",
                            "query": "friendship"
                          }
                        }
                      ]
                    }
                  }
                }
                """;
            response = es.search(s -> s
                    .index("books-complete")
                    .withJson(new StringReader(hybridQuery)),
                Book.class
            );
            System.out.println("\n=== Hybrid search results ===");
            for (Hit<Book> hit : response.hits().hits()) {
                System.out.println("  " + hit.score() + " " + hit.source().title());
            }

            String esql = """
                FROM "books-complete"
                | STATS books = COUNT(*) BY decade = release_year - (release_year % 10)
                | KEEP decade, books
                | SORT decade ASC
                """;
            BinaryResponse aggregation = es.esql().query(q -> q
                .query(esql)
                .format(EsqlFormat.Csv)
            );
            System.out.println("\n=== Books by decade ===");
            try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(aggregation.content())
            )) {
                reader.lines().skip(1).forEach(line -> {
                    String[] values = line.split(",", -1);
                    System.out.println("  " + values[0] + "s: " + values[1]);
                });
            }
        }
    }
}
```

:::

::::

::::{tab-item} Go
:sync: go

Save the script as `main.go` in the module directory, then run it:

```bash
go run .
```

:::{dropdown} Complete runnable script

```go
package main

import (
	"bytes"
	"context"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"strings"

	"github.com/elastic/go-elasticsearch/v9"
	"github.com/elastic/go-elasticsearch/v9/esutil"
	"github.com/elastic/go-elasticsearch/v9/typedapi/types/enums/esqlformat"
)

type book struct {
	Title       string `json:"title"`
	Author      string `json:"author"`
	ReleaseYear int    `json:"release_year"`
	Description string `json:"description"`
}

func printSearch(es *elasticsearch.Client, query string) {
	res, err := es.Search(
		es.Search.WithContext(context.Background()),
		es.Search.WithIndex("books-complete"),
		es.Search.WithBody(strings.NewReader(query)),
	)
	if err != nil {
		log.Fatal(err)
	}
	defer res.Body.Close()
	if res.IsError() {
		log.Fatal(res)
	}

	var response struct {
		Hits struct {
			Hits []struct {
				Score  float64 `json:"_score"`
				Source book    `json:"_source"`
			} `json:"hits"`
		} `json:"hits"`
	}
	if err := json.NewDecoder(res.Body).Decode(&response); err != nil {
		log.Fatal(err)
	}

	for _, hit := range response.Hits.Hits {
		fmt.Println(" ", hit.Score, hit.Source.Title)
	}
}

func main() {
	es, err := elasticsearch.New(
		elasticsearch.WithAddresses(os.Getenv("ES_URL")),
		elasticsearch.WithAPIKey(os.Getenv("ES_API_KEY")),
	)
	if err != nil {
		log.Fatal(err)
	}

	mapping := strings.NewReader(`{
	  "mappings": {
	    "properties": {
	      "description": {
	        "type": "semantic_text",
	        "fields": {"text": {"type": "text"}}
	      }
	    }
	  }
	}`)
	res, err := es.Indices.Create(
		"books-complete",
		es.Indices.Create.WithBody(mapping),
	)
	if err != nil {
		log.Fatal(err)
	}
	if res.IsError() {
		log.Fatal(res)
	}
	res.Body.Close()

	books := []book{
		{
			Title: "The Left Hand of Darkness", Author: "Ursula K. Le Guin",
			ReleaseYear: 1969,
			Description: "An envoy visits an icy planet whose people have no fixed gender, feeling out politics and friendship across a deep cultural gap.",
		},
		{
			Title: "Project Hail Mary", Author: "Andy Weir",
			ReleaseYear: 2021,
			Description: "A lone astronaut wakes with amnesia on a spaceship and has to stop a disaster that threatens all life on Earth.",
		},
		{
			Title: "The Name of the Wind", Author: "Patrick Rothfuss",
			ReleaseYear: 2007,
			Description: "A gifted young musician and magician tells the story of his rise from orphan to legend.",
		},
		{
			Title: "Klara and the Sun", Author: "Kazuo Ishiguro",
			ReleaseYear: 2021,
			Description: "An artificial friend watches human love and loneliness while hoping a child will pick her.",
		},
		{
			Title: "Dune", Author: "Frank Herbert",
			ReleaseYear: 1965,
			Description: "On a desert planet prized for a rare spice, a young heir is pulled into a war over ecology, religion, and power.",
		},
	}

	indexer, err := esutil.NewBulkIndexer(esutil.BulkIndexerConfig{
		Client:  es,
		Index:   "books-complete",
		Refresh: "wait_for",
	})
	if err != nil {
		log.Fatal(err)
	}
	for _, item := range books {
		body, err := json.Marshal(item)
		if err != nil {
			log.Fatal(err)
		}
		if err := indexer.Add(context.Background(), esutil.BulkIndexerItem{
			Action: "index",
			Body:   bytes.NewReader(body),
		}); err != nil {
			log.Fatal(err)
		}
	}
	if err := indexer.Close(context.Background()); err != nil {
		log.Fatal(err)
	}
	if indexer.Stats().NumFailed > 0 {
		log.Fatalf("%d book(s) failed to index", indexer.Stats().NumFailed)
	}

	fmt.Println("=== Keyword search results ===")
	printSearch(es, `{
	  "query": {
	    "match": {
	      "title": "wind"
	    }
	  }
	}`)

	fmt.Println("=== Semantic search results ===")
	printSearch(es, `{
	  "query": {
	    "semantic": {
	      "field": "description",
	      "query": "surviving alone in space"
	    }
	  }
	}`)

	fmt.Println("\n=== Hybrid search results ===")
	printSearch(es, `{
	  "query": {
	    "bool": {
	      "should": [
	        {
	          "match": {
	            "description.text": "friendship"
	          }
	        },
	        {
	          "semantic": {
	            "field": "description",
	            "query": "friendship"
	          }
	        }
	      ]
	    }
	  }
	}`)

	typed, err := elasticsearch.NewTyped(
		elasticsearch.WithAddresses(os.Getenv("ES_URL")),
		elasticsearch.WithAPIKey(os.Getenv("ES_API_KEY")),
	)
	if err != nil {
		log.Fatal(err)
	}
	query := "FROM \"books-complete\"\n" +
		"\t\t| STATS books = COUNT(*) BY decade = release_year - (release_year % 10)\n" +
		"\t\t| KEEP decade, books\n" +
		"\t\t| SORT decade ASC"
	aggregation, err := typed.Esql.Query().
		Query(query).
		Format(esqlformat.Csv).
		Do(context.Background())
	if err != nil {
		log.Fatal(err)
	}
	rows, err := csv.NewReader(bytes.NewReader(aggregation)).ReadAll()
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("\n=== Books by decade ===")
	for _, row := range rows[1:] {
		fmt.Printf("  %ss: %s\n", row[0], row[1])
	}
}
```

:::

::::

::::{tab-item} Console
:sync: console

:::{dropdown} Complete runnable script

```console
PUT books-complete
{
  "mappings": {
    "properties": {
      "description": {
        "type": "semantic_text",
        "fields": {"text": {"type": "text"}}
      }
    }
  }
}

POST books-complete/_bulk?refresh=wait_for
{ "index": {} }
{ "title": "The Left Hand of Darkness", "author": "Ursula K. Le Guin", "release_year": 1969, "description": "An envoy visits an icy planet whose people have no fixed gender, feeling out politics and friendship across a deep cultural gap." }
{ "index": {} }
{ "title": "Project Hail Mary", "author": "Andy Weir", "release_year": 2021, "description": "A lone astronaut wakes with amnesia on a spaceship and has to stop a disaster that threatens all life on Earth." }
{ "index": {} }
{ "title": "The Name of the Wind", "author": "Patrick Rothfuss", "release_year": 2007, "description": "A gifted young musician and magician tells the story of his rise from orphan to legend." }
{ "index": {} }
{ "title": "Klara and the Sun", "author": "Kazuo Ishiguro", "release_year": 2021, "description": "An artificial friend watches human love and loneliness while hoping a child will pick her." }
{ "index": {} }
{ "title": "Dune", "author": "Frank Herbert", "release_year": 1965, "description": "On a desert planet prized for a rare spice, a young heir is pulled into a war over ecology, religion, and power." }

GET books-complete/_search
{
  "query": {
    "match": {
      "title": "wind"
    }
  }
}

GET books-complete/_search
{
  "query": {
    "semantic": {
      "field": "description",
      "query": "surviving alone in space"
    }
  }
}

GET books-complete/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "match": {
            "description.text": "friendship"
          }
        },
        {
          "semantic": {
            "field": "description",
            "query": "friendship"
          }
        }
      ]
    }
  }
}

POST _query
{
  "query": """
    FROM books-complete
    | STATS books = COUNT(*) BY decade = release_year - (release_year % 10)
    | SORT decade ASC
    | LIMIT 10
  """
}
```

:::

::::

::::{tab-item} curl
:sync: curl

:::{dropdown} Complete runnable script

```bash
curl -X PUT "$ES_URL/books-complete" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "mappings": {
      "properties": {
        "description": {
          "type": "semantic_text",
          "fields": {"text": {"type": "text"}}
        }
      }
    }
  }'

curl -X POST "$ES_URL/books-complete/_bulk?refresh=wait_for" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/x-ndjson" \
  --data-binary @- <<'EOF'
{ "index": {} }
{ "title": "The Left Hand of Darkness", "author": "Ursula K. Le Guin", "release_year": 1969, "description": "An envoy visits an icy planet whose people have no fixed gender, feeling out politics and friendship across a deep cultural gap." }
{ "index": {} }
{ "title": "Project Hail Mary", "author": "Andy Weir", "release_year": 2021, "description": "A lone astronaut wakes with amnesia on a spaceship and has to stop a disaster that threatens all life on Earth." }
{ "index": {} }
{ "title": "The Name of the Wind", "author": "Patrick Rothfuss", "release_year": 2007, "description": "A gifted young musician and magician tells the story of his rise from orphan to legend." }
{ "index": {} }
{ "title": "Klara and the Sun", "author": "Kazuo Ishiguro", "release_year": 2021, "description": "An artificial friend watches human love and loneliness while hoping a child will pick her." }
{ "index": {} }
{ "title": "Dune", "author": "Frank Herbert", "release_year": 1965, "description": "On a desert planet prized for a rare spice, a young heir is pulled into a war over ecology, religion, and power." }
EOF

curl -X GET "$ES_URL/books-complete/_search" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "match": {
        "title": "wind"
      }
    }
  }'

curl -X GET "$ES_URL/books-complete/_search" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "semantic": {
        "field": "description",
        "query": "surviving alone in space"
      }
    }
  }'

curl -X GET "$ES_URL/books-complete/_search" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "bool": {
        "should": [
          {
            "match": {
              "description.text": "friendship"
            }
          },
          {
            "semantic": {
              "field": "description",
              "query": "friendship"
            }
          }
        ]
      }
    }
  }'

curl -X POST "$ES_URL/_query" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "FROM books-complete | STATS books = COUNT(*) BY decade = release_year - (release_year % 10) | SORT decade ASC | LIMIT 10"
  }'
```

:::

::::

:::::

## Next steps [vector-full-text-search-next-steps]

- [](/solutions/search/ingest-for-search.md): Compare ways to get your content into {{es}} for search, including clients, crawlers, and connectors.
- [](/solutions/search/search-approaches.md): Compare search techniques in {{es}}, including full-text, semantic, vector, and hybrid search, and choose one for your use case.
