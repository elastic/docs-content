---
navigation_title: Vector and full-text search
description: Step-by-step tutorial for connecting an application to an Elasticsearch Vector Database project, indexing data, and running full-text, semantic, hybrid, and ES|QL searches.
applies_to:
  vectordb: ga
---

# {{es}} vector and full-text search in 10 minutes [vector-full-text-search-quickstart]

{{es}} is a search and vector engine that supports full-text, semantic, and hybrid search over your data. This guide uses official {{es}} clients to take you from an empty Vector Database project to real search results in about 10 minutes.

Use it if you're new to search in {{es}} or want to experiment with meaning-based retrieval alongside keyword matching.

:::{tip}
Are you an agent? Use the [elasticsearch-onboarding skill](https://github.com/elastic/agent-skills/tree/main/skills/elasticsearch/elasticsearch-onboarding).
:::

## Create a Vector Database project [vector-full-text-search-create-project]

Create a free [{{es}} Vector Database project](https://cloud.elastic.co/projects/create/elasticsearch?use_case=vector_search). It's serverless and built for search and vector workloads, so you don't need to size or manage a cluster.

The project takes about a minute to start. The **Getting started** page then displays the **Project endpoint** and a generated API key. Copy both values.

:::{tip}
You can also find the **Project endpoint** and API keys on the **Home** page. To find the **Home** page, use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Select **Connection details** ![Connection details icon](/solutions/images/connection-details-icon.svg "") to view your endpoint and manage API keys.
:::

## Connect to your project [vector-full-text-search-connect]

Set the project endpoint and API key as environment variables:

:::::{tab-set}
:group: operating-systems

::::{tab-item} macOS and Linux
:sync: macos-linux

```bash
export ES_URL="<YOUR_PROJECT_URL>" <1>
export ES_API_KEY="YOUR_API_KEY"
```

1. For example, `https://my-project.es.us-east-1.aws.elastic.cloud:443`.

::::

::::{tab-item} Windows PowerShell
:sync: windows-powershell

```powershell
$Env:ES_URL = "<YOUR_PROJECT_URL>" <1>
$Env:ES_API_KEY = "YOUR_API_KEY"
```

1. For example, `https://my-project.es.us-east-1.aws.elastic.cloud:443`.

::::

:::::

## Install and initialize an {{es}} client [vector-full-text-search-install-sdk]

Install the client for your language. For a list of available clients, refer to [{{es}} clients](/reference/elasticsearch-clients/index.md).

:::::{tab-set}
:group: languages

::::{tab-item} Python
:sync: python

```bash
pip install elasticsearch
```

For supported Python versions and other requirements, refer to the [Python client documentation](elasticsearch-py://reference/getting-started.md#_requirements).

::::

::::{tab-item} TypeScript
:sync: typescript

```bash
npm install @elastic/elasticsearch
npm install --save-dev typescript tsx
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
bundle add elasticsearch
```

For supported Ruby versions and other requirements, refer to the [Ruby client installation documentation](elasticsearch-ruby://reference/installation.md).

::::

::::{tab-item} C#/.NET
:sync: csharp

```bash
dotnet add package Elastic.Clients.Elasticsearch
```

For supported .NET versions and other requirements, refer to the [.NET client documentation](elasticsearch-net://reference/index.md).

::::

::::{tab-item} Java
:sync: java

Add the client dependency and the runnable example's main class to the generated `build.gradle` file:

```groovy
dependencies {
    implementation "co.elastic.clients:elasticsearch-java:VERSION"
}

application {
    mainClass = "quickstart.App"
}
```

Replace `VERSION` with the version from the [latest Java client release](https://github.com/elastic/elasticsearch-java/releases). For supported Java versions and other requirements, refer to the [Java client documentation](elasticsearch-java://reference/index.md).

::::

::::{tab-item} Go
:sync: go

```bash
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

::::{tab-item} C#/.NET
:sync: csharp

```csharp
using Elastic.Clients.Elasticsearch;
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

import co.elastic.clients.elasticsearch.ElasticsearchClient;

public class App {
    public static void main(String[] args) throws Exception {
        String serverUrl = System.getenv("ES_URL");
        String apiKey = System.getenv("ES_API_KEY");

        ElasticsearchClient es = ElasticsearchClient.of(b -> b
            .host(serverUrl)
            .apiKey(apiKey)
        );
    }
}
```

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

## Create an index and add data [vector-full-text-search-add-data]

Create the `books` index and add the sample data.

:::::{tab-set}
:group: languages

::::{tab-item} Console
:sync: console

```console
PUT books
{
  "mappings": {
    "properties": { <1>
      "description": {
        "type": "semantic_text" <2>
      }
    }
  }
}
```

1. {{es}} uses [dynamic mapping](/manage-data/data-store/mapping/dynamic-mapping.md) to determine field types from the first documents you index. The only field you need to define is `description`, which you set to `semantic_text` before indexing so you can search it by meaning.
2. In this example, `semantic_text` uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints). The model used by this endpoint is multilingual, so you can index and search text in multiple languages. To use custom models, refer to [Configure {{infer}} endpoints for `semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints).

:::{note}
[`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) automatically embeds text at ingest time using an {{infer}} endpoint. The {{infer}} endpoint connects to an embedding model that converts indexed text and search queries into vectors.
:::

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
          "type": "semantic_text" <2>
        }
      }
    }
  }'
```

1. {{es}} uses [dynamic mapping](/manage-data/data-store/mapping/dynamic-mapping.md) to determine field types from the first documents you index. The only field you need to define is `description`, which you set to `semantic_text` before indexing so you can search it by meaning.
2. In this example, `semantic_text` uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints). The model used by this endpoint is multilingual, so you can index and search text in multiple languages. To use custom models, refer to [Configure {{infer}} endpoints for `semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints).

:::{note}
[`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) automatically embeds text at ingest time using an {{infer}} endpoint. The {{infer}} endpoint connects to an embedding model that converts indexed text and search queries into vectors.
:::

::::

::::{tab-item} Python
:sync: python

```python
es.indices.create(
    index="books",
    mappings={
        "properties": { <1>
            "description": {
                "type": "semantic_text", <2>
            }
        }
    },
)
```

1. {{es}} uses [dynamic mapping](/manage-data/data-store/mapping/dynamic-mapping.md) to determine field types from the first documents you index. The only field you need to define is `description`, which you set to `semantic_text` before indexing so you can search it by meaning.
2. [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) automatically embeds text at ingest time using an {{infer}} endpoint. The {{infer}} endpoint connects to an embedding model that converts indexed text and search queries into vectors. <br>
In this example, `semantic_text` uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints). The model used by this endpoint is multilingual, so you can index and search text in multiple languages. To use custom models, refer to [Configure {{infer}} endpoints for `semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints). <br> <br>



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
      },
    },
  },
});
```

1. {{es}} uses [dynamic mapping](/manage-data/data-store/mapping/dynamic-mapping.md) to determine field types from the first documents you index. The only field you need to define is `description`, which you set to `semantic_text` before indexing so you can search it by meaning.
2. In this example, `semantic_text` uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints). The model used by this endpoint is multilingual, so you can index and search text in multiple languages. To use custom models, refer to [Configure {{infer}} endpoints for `semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints).

:::{note}
[`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) automatically embeds text at ingest time using an {{infer}} endpoint. The {{infer}} endpoint connects to an embedding model that converts indexed text and search queries into vectors.
:::

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
                ],
            ],
        ],
    ],
]);
```

1. {{es}} uses [dynamic mapping](/manage-data/data-store/mapping/dynamic-mapping.md) to determine field types from the first documents you index. The only field you need to define is `description`, which you set to `semantic_text` before indexing so you can search it by meaning.
2. In this example, `semantic_text` uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints). The model used by this endpoint is multilingual, so you can index and search text in multiple languages. To use custom models, refer to [Configure {{infer}} endpoints for `semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints).

:::{note}
[`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) automatically embeds text at ingest time using an {{infer}} endpoint. The {{infer}} endpoint connects to an embedding model that converts indexed text and search queries into vectors.
:::

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
          type: "semantic_text" <2>
        }
      }
    }
  }
)
```

1. {{es}} uses [dynamic mapping](/manage-data/data-store/mapping/dynamic-mapping.md) to determine field types from the first documents you index. The only field you need to define is `description`, which you set to `semantic_text` before indexing so you can search it by meaning.
2. In this example, `semantic_text` uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints). The model used by this endpoint is multilingual, so you can index and search text in multiple languages. To use custom models, refer to [Configure {{infer}} endpoints for `semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints).

:::{note}
[`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) automatically embeds text at ingest time using an {{infer}} endpoint. The {{infer}} endpoint connects to an embedding model that converts indexed text and search queries into vectors.
:::

::::

::::{tab-item} C#/.NET
:sync: csharp

```csharp
await es.Indices.CreateAsync<Book>("books", c => c
    .Mappings(m => m
        .Properties(p => p <1>
            .SemanticText(b => b.Description) <2>
        )
    )
);
```

1. {{es}} uses [dynamic mapping](/manage-data/data-store/mapping/dynamic-mapping.md) to determine field types from the first documents you index. The only field you need to define is `description`, which you set to `semantic_text` before indexing so you can search it by meaning.
2. In this example, `semantic_text` uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints). The model used by this endpoint is multilingual, so you can index and search text in multiple languages. To use custom models, refer to [Configure {{infer}} endpoints for `semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints).

:::{note}
[`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) automatically embeds text at ingest time using an {{infer}} endpoint. The {{infer}} endpoint connects to an embedding model that converts indexed text and search queries into vectors.
:::

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
                "type": "semantic_text" <2>
              }
            }
          }
        }
        """))
);
```

1. {{es}} uses [dynamic mapping](/manage-data/data-store/mapping/dynamic-mapping.md) to determine field types from the first documents you index. The only field you need to define is `description`, which you set to `semantic_text` before indexing so you can search it by meaning.
2. In this example, `semantic_text` uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints). The model used by this endpoint is multilingual, so you can index and search text in multiple languages. To use custom models, refer to [Configure {{infer}} endpoints for `semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints).

:::{note}
[`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) automatically embeds text at ingest time using an {{infer}} endpoint. The {{infer}} endpoint connects to an embedding model that converts indexed text and search queries into vectors.
:::

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
	        "type": "semantic_text" <2>
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

1. {{es}} uses [dynamic mapping](/manage-data/data-store/mapping/dynamic-mapping.md) to determine field types from the first documents you index. The only field you need to define is `description`, which you set to `semantic_text` before indexing so you can search it by meaning.
2. In this example, `semantic_text` uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints). The model used by this endpoint is multilingual, so you can index and search text in multiple languages. To use custom models, refer to [Configure {{infer}} endpoints for `semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints).

:::{note}
[`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) automatically embeds text at ingest time using an {{infer}} endpoint. The {{infer}} endpoint connects to an embedding model that converts indexed text and search queries into vectors.
:::

::::

:::::

Next, index five books in one bulk request:

:::::{tab-set}
:group: languages

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

::::

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

helpers.bulk(es, ({"_index": "books", "_source": b} for b in books), refresh="wait_for")
```

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

await es.bulk({
  refresh: "wait_for",
  operations: books.flatMap((book) => [
    { index: { _index: "books" } },
    book,
  ]),
});
```

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

$es->bulk([
    "refresh" => "wait_for",
    "body" => $operations,
]);
```

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

es.bulk(
  body: operations,
  refresh: "wait_for"
)
```

::::

::::{tab-item} C#/.NET
:sync: csharp

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

await es.BulkAsync(new BulkRequest
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

es.bulk(bulk.build());
```

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

::::

:::::

## Run search [vector-full-text-search-search]

Use the indexed book data to run semantic and hybrid searches. Semantic search matches meaning, while hybrid search combines semantic and keyword matching.

### Semantic search [vector-full-text-search-semantic]

Run a semantic search against the `description` field:

:::::{tab-set}
:group: languages

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

::::{tab-item} C#/.NET
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

:::::

:::{dropdown} Example output
The first result is:

```text
SCORE Project Hail Mary
```

**Project Hail Mary** ranks first because its description includes "A lone astronaut," which is semantically similar to "surviving alone in space" even though the wording differs.
:::

### Hybrid search [vector-full-text-search-hybrid]

Run a hybrid search that uses full-text search on the `title` field and semantic search on the `description` field:

:::::{tab-set}
:group: languages

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
            "title": "wind"
          }
        },
        {
          "semantic": { <2>
            "field": "description",
            "query": "young magician coming of age"
          }
        }
      ]
    }
  }
}
```

1. The `match` clause performs full-text search on `title` and scores how well the analyzed text matches `wind`.
2. The `semantic` clause searches `description` by meaning and contributes its semantic similarity score.

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
              "title": "wind"
            }
          },
          {
            "semantic": { <2>
              "field": "description",
              "query": "young magician coming of age"
            }
          }
        ]
      }
    }
  }'
```

1. The `match` clause performs full-text search on `title` and scores how well the analyzed text matches `wind`.
2. The `semantic` clause searches `description` by meaning and contributes its semantic similarity score.

::::

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
                        "title": "wind"
                    }
                },
                {
                    "semantic": { <2>
                        "field": "description",
                        "query": "young magician coming of age",
                    }
                },
            ]
        }
    },
)

for hit in resp["hits"]["hits"]:
    print(hit["_score"], hit["_source"]["title"])
```

1. The `match` clause performs full-text search on `title` and scores how well the analyzed text matches `wind`.
2. The `semantic` clause searches `description` by meaning and contributes its semantic similarity score.

::::

::::{tab-item} TypeScript
:sync: typescript

```typescript
const resp = await es.search<Book>({
  index: "books",
  query: {
    bool: {
      should: [
        {
          match: { <1>
            title: "wind",
          },
        },
        {
          semantic: { <2>
            field: "description",
            query: "young magician coming of age",
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

1. The `match` clause performs full-text search on `title` and scores how well the analyzed text matches `wind`.
2. The `semantic` clause searches `description` by meaning and contributes its semantic similarity score.

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
                            "title" => "wind",
                        ],
                    ],
                    [
                        "semantic" => [ <2>
                            "field" => "description",
                            "query" => "young magician coming of age",
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

1. The `match` clause performs full-text search on `title` and scores how well the analyzed text matches `wind`.
2. The `semantic` clause searches `description` by meaning and contributes its semantic similarity score.

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
              title: "wind"
            }
          },
          {
            semantic: { <2>
              field: "description",
              query: "young magician coming of age"
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

1. The `match` clause performs full-text search on `title` and scores how well the analyzed text matches `wind`.
2. The `semantic` clause searches `description` by meaning and contributes its semantic similarity score.

::::

::::{tab-item} C#/.NET
:sync: csharp

```csharp
var response = await es.SearchAsync<SearchBook>(s => s
    .Indices("books")
    .Query(q => q
        .Bool(b => b
            .Should(
                should => should
                    .Match(match => match <1>
                        .Field(book => book.Title)
                        .Query("wind")
                    ),
                should => should
                    .Semantic(semantic => semantic <2>
                        .Field("description")
                        .Query("young magician coming of age")
                    )
            )
        )
    )
);

foreach (var hit in response.Hits)
{
    Console.WriteLine($"{hit.Score} {hit.Source?.Title}");
}

```

1. The `match` clause performs full-text search on `title` and scores how well the analyzed text matches `wind`.
2. The `semantic` clause searches `description` by meaning and contributes its semantic similarity score.

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
                "title": "wind"
              }
            },
            {
              "semantic": { <2>
                "field": "description",
                "query": "young magician coming of age"
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

1. The `match` clause performs full-text search on `title` and scores how well the analyzed text matches `wind`.
2. The `semantic` clause searches `description` by meaning and contributes its semantic similarity score.

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
	            "title": "wind"
	          }
	        },
	        {
	          "semantic": { <2>
	            "field": "description",
	            "query": "young magician coming of age"
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

1. The `match` clause performs full-text search on `title` and scores how well the analyzed text matches `wind`.
2. The `semantic` clause searches `description` by meaning and contributes its semantic similarity score.

::::

:::::

:::{dropdown} Example output
The first result is:

```text
SCORE The Name of the Wind
```

**The Name of the Wind** ranks first because its title matches `wind`, and its description of a gifted young magician's rise from orphan to legend is semantically similar to `young magician coming of age`. Because the book matches both clauses, its full-text and semantic scores combine.
:::

## Aggregate the data with {{esql}} [vector-full-text-search-esql]

With [aggregations](/explore-analyze/query-filter/aggregations.md), you can summarize groups of data, such as the number of books released in each decade. Use [{{esql}}](elasticsearch://reference/query-languages/esql.md), a piped query language, to run this aggregation:

:::::{tab-set}
:group: languages

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

::::{tab-item} C#/.NET
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

:::::

:::{dropdown} Example output
The output contains one row per decade:

```text
1960s: 2
2000s: 1
2020s: 2
```
:::

## Complete runnable script [vector-full-text-search-complete-script]

1. [Create a Vector Database project](#vector-full-text-search-create-project).
2. [Connect to your project](#vector-full-text-search-connect).
3. [Install and initialize the client](#vector-full-text-search-install-sdk) for your language.
4. Select your language, expand the complete script, and run it.

:::::{tab-set}
:group: languages

::::{tab-item} Python
:sync: python

:::{dropdown} Complete runnable script

```python
import os
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch(os.environ["ES_URL"], api_key=os.environ["ES_API_KEY"])

# Declare the semantically searchable field. Other fields are inferred on ingest.
es.indices.create(
    index="books-complete",
    mappings={"properties": {"description": {"type": "semantic_text"}}},
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
helpers.bulk(es, ({"_index": "books-complete", "_source": b} for b in books), refresh="wait_for")

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
        {"match": {"title": "wind"}},
        {"semantic": {"field": "description", "query": "young magician coming of age"}},
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
  mappings: { properties: { description: { type: "semantic_text" } } },
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
await es.helpers.bulk({
  datasource: books,
  onDocument: () => ({ index: { _index: "books-complete" } }),
  refreshOnCompletion: true,
});

// Semantic search.
let resp = await es.search<Book>({
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
    { match: { title: "wind" } },
    { semantic: { field: "description", query: "young magician coming of age" } },
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

$es->bulk([
    "refresh" => "wait_for",
    "body" => $operations,
]);

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
                    ["match" => ["title" => "wind"]],
                    ["semantic" => [
                        "field" => "description",
                        "query" => "young magician coming of age",
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
          type: "semantic_text"
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
es.bulk(body: operations, refresh: "wait_for")

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
          { match: { title: "wind" } },
          {
            semantic: {
              field: "description",
              query: "young magician coming of age"
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

::::{tab-item} C#/.NET
:sync: csharp

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
            .SemanticText(b => b.Description)
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
await es.BulkAsync(new BulkRequest
{
    Refresh = Refresh.WaitFor,
    Operations = operations
});

var response = await es.SearchAsync<Book>(s => s
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
                        .Field(book => book.Title)
                        .Query("wind")
                    ),
                should => should
                    .Semantic(semantic => semantic
                        .Field("description")
                        .Query("young magician coming of age")
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
        ElasticsearchClient es = ElasticsearchClient.of(b -> b
            .host(System.getenv("ES_URL"))
            .apiKey(System.getenv("ES_API_KEY"))
        );

        es.indices().create(c -> c
            .index("books-complete")
            .withJson(new StringReader("""
                {
                  "mappings": {
                    "properties": {
                      "description": {
                        "type": "semantic_text"
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
        es.bulk(bulk.build());

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
        SearchResponse<Book> response = es.search(s -> s
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
                        "title": "wind"
                      }
                    },
                    {
                      "semantic": {
                        "field": "description",
                        "query": "young magician coming of age"
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

        es.close();
    }
}
```

:::

::::

::::{tab-item} Go
:sync: go

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
	        "type": "semantic_text"
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
	            "title": "wind"
	          }
	        },
	        {
	          "semantic": {
	            "field": "description",
	            "query": "young magician coming of age"
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

:::::

## Next steps [vector-full-text-search-next-steps]

If you want to continue using your Vector Database project, select a next step based on your goal. 

### Learn the fundamentals

- [Vector search](/solutions/search/vector.md): Learn about vectors, embeddings, vector fields, and similarity search in {{es}}.
- [Compare Elastic {{infer-cap}} Service models](/explore-analyze/elastic-inference/eis-supported-models.md#embedding-models): Learn about the embedding models available through the Elastic {{infer-cap}} Service and compare their capabilities.

### Tune search

- [Learn about chunking strategies](/explore-analyze/elastic-inference/inference-api.md#infer-chunking-config): Learn how to split long text for {{infer}} using sentence, word, recursive, or custom chunking.
- [Tune retrieval with ranking and reranking](/solutions/search/ranking.md): Learn how to improve result ordering with multi-stage ranking and reranking.
- [Plan quantization and sizing](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization): Learn how quantization reduces vector memory and storage requirements and compare the available quantization types.

### Try another tutorial

- [Build multimodal search in {{es}}](/solutions/search/multimodal-search/multimodal-search-tutorial.md): Learn how to index images and search them with text, image, and PDF input.

To learn how continued usage is billed, refer to [{{serverless-short}} project billing dimensions](/deploy-manage/cloud-organization/billing/serverless-project-billing-dimensions.md). If you don't plan to continue using the project, [delete it](/deploy-manage/uninstall/delete-a-cloud-deployment.md#serverless) to avoid additional usage charges.