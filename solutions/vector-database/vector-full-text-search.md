---
navigation_title: Vector and full-text search
description: Step-by-step tutorial for connecting an application to an Elasticsearch Vector Database project, indexing data, and running full-text, semantic, hybrid, and ES|QL searches.
applies_to:
  serverless: ga
products:
  - id: elasticsearch
  - id: cloud-serverless
type: tutorial
---

# Elasticsearch vector and full-text search in 10 minutes [vector-full-text-search-quickstart]

Elasticsearch is a search and vector engine that supports full-text, semantic, and hybrid search over your data.

This guide uses official {{es}} clients to take you from an empty Vector Database project to real search results in about 10 minutes. By the end, you have a `books` index, semantic and hybrid search results, an aggregation, and a [complete script](#vector-full-text-search-complete-script) to use in your app.

Are you an agent? Use the [elasticsearch-onboarding skill](https://github.com/elastic/agent-skills/tree/main/skills/elasticsearch/elasticsearch-onboarding).

## Create a Vector Database project [vector-full-text-search-create-project]

Create a free [Elasticsearch Vector Database project](https://cloud.elastic.co/projects/create/elasticsearch?use_case=vector_search). It's serverless and built for search and vector workloads, so you don't need to size or manage a cluster.

The project takes about a minute to start. The **Getting started** page then displays the **Project endpoint** and a generated API key. Copy both values.

## Connect to your project [vector-full-text-search-connect]

Set the project endpoint and API key as environment variables:

:::::{tab-set}

::::{tab-item} macOS and Linux

```bash
export ES_URL="https://YOUR-PROJECT.es.REGION.aws.elastic.cloud:443"
export ES_API_KEY="YOUR_API_KEY"
```

::::

::::{tab-item} Windows PowerShell

```powershell
$Env:ES_URL = "https://YOUR-PROJECT.es.REGION.aws.elastic.cloud:443"
$Env:ES_API_KEY = "YOUR_API_KEY"
```

::::

:::::

:::{important}
Never hard-code credentials or commit them to source control. For local development, store the values in a `.env` file, configure your application to load it, and add `.env` to your `.gitignore` file.
:::

## Install a client [vector-full-text-search-install-sdk]

Install the client for your language. For a list of available clients, refer to [{{es}} clients](/reference/elasticsearch-clients/index.md).

:::::{tab-set}
:group: languages

::::{tab-item} Python
:sync: python

```bash
pip install elasticsearch
```

For supported Python versions and other requirements, refer to the [Python client documentation](elasticsearch-py://reference/index.md).

::::

::::{tab-item} TypeScript
:sync: typescript

```bash
npm init --yes
npm pkg set type=module
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
gem install elasticsearch
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

```groovy subs=true
dependencies {
    implementation "co.elastic.clients:elasticsearch-java:{{version.stack}}"
}
```

For supported Java versions and other requirements, refer to the [Java client documentation](elasticsearch-java://reference/index.md).

::::

::::{tab-item} Go
:sync: go

```bash
go get github.com/elastic/go-elasticsearch/v9
```

For supported Go versions and other requirements, refer to the [Go client installation documentation](https://www.elastic.co/docs/reference/elasticsearch/clients/go/installation).

::::

:::::

## Initialize the {{es}} client

Use the environment variables to create the client and check the connection:

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

print(es.info())
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

console.log(await es.info());
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

print_r($es->info()->asArray());
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

puts es.info
```

::::

::::{tab-item} C#/.NET
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

var response = await es.InfoAsync();
Console.WriteLine(response);
```

::::

::::{tab-item} Java
:sync: java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.StringReader;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.elasticsearch._types.Refresh;
import co.elastic.clients.elasticsearch.core.BulkRequest;
import co.elastic.clients.elasticsearch.core.SearchResponse;
import co.elastic.clients.elasticsearch.core.search.Hit;
import co.elastic.clients.elasticsearch.esql.EsqlFormat;
import co.elastic.clients.transport.endpoints.BinaryResponse;

String serverUrl = System.getenv("ES_URL");
String apiKey = System.getenv("ES_API_KEY");

ElasticsearchClient es = ElasticsearchClient.of(b -> b
    .host(serverUrl)
    .apiKey(apiKey)
);

System.out.println(es.info());
es.close();
```

::::

::::{tab-item} Go
:sync: go

```go
package main

import (
	"bytes"
	"context"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"os"
	"strings"

	"github.com/elastic/go-elasticsearch/v9"
	"github.com/elastic/go-elasticsearch/v9/esutil"
	"github.com/elastic/go-elasticsearch/v9/typedapi/types/enums/esqlformat"
)

func main() {
	es, err := elasticsearch.New(
		elasticsearch.WithAddresses(os.Getenv("ES_URL")),
		elasticsearch.WithAPIKey(os.Getenv("ES_API_KEY")),
	)
	if err != nil {
		log.Fatal(err)
	}

	res, err := es.Info()
	if err != nil {
		log.Fatal(err)
	}
	defer res.Body.Close()
	if res.IsError() {
		log.Fatal(res)
	}

	if _, err := io.Copy(os.Stdout, res.Body); err != nil {
		log.Fatal(err)
	}
}
```

::::

:::::

:::{dropdown} Verify the connection

The response contains information about your project:

```text
{
  "name": "serverless",
  "version": {
    "number": "...",
    "build_flavor": "serverless"
  }
}
```

This response confirms that the client authenticated and connected to your Vector Database project. A `401` means the API key is incorrect. A timeout means the URL is incorrect or unreachable.

:::

## Create an index and add data [vector-full-text-search-add-data]

Create the `books` index and index five books.

### Create the index

{{es}} uses [dynamic mapping](/manage-data/data-store/mapping/dynamic-mapping.md) to determine field types from the first documents you index. The only field you need to define is `description`, which you set to `semantic_text` before indexing so you can search it by meaning.

:::{note}
[`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) automatically embeds text at ingest time using an {{infer}} endpoint. The {{infer}} endpoint connects to an embedding model that converts indexed text and search queries into vectors. When you search the field, {{es}} embeds your query the same way and matches on meaning. For example, "space rescue" can match "stranded astronaut" with no words in common.



:::

:::::{tab-set}
:group: languages

::::{tab-item} Python
:sync: python

```python
es.indices.create(
    index="books",
    mappings={
        "properties": {
            "description": {
                "type": "semantic_text", <1>
            }
        }
    },
)
```

1. In this example, `semantic_text` uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints). The model used by this endpoint is multilingual, so you can index and search text in multiple languages. To use custom models, refer to [Configure {{infer}} endpoints for `semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints).

:::{dropdown} Verify the index was created

The response is `True`.

```python
print(es.indices.exists(index="books"))
```

:::

::::

::::{tab-item} TypeScript
:sync: typescript

```typescript
await es.indices.create({
  index: "books",
  mappings: {
    properties: {
      description: {
        type: "semantic_text", <1>
      },
    },
  },
});
```

1. In this example, `semantic_text` uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints). The model used by this endpoint is multilingual, so you can index and search text in multiple languages. To use custom models, refer to [Configure {{infer}} endpoints for `semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints).

:::{dropdown} Verify the index was created

The response is `true`.

```typescript
console.log(await es.indices.exists({ index: "books" }));
```

:::

::::

::::{tab-item} PHP
:sync: php

```php
$es->indices()->create([
    "index" => "books",
    "body" => [
        "mappings" => [
            "properties" => [
                "description" => [
                    "type" => "semantic_text", <1>
                ],
            ],
        ],
    ],
]);
```

1. In this example, `semantic_text` uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints). The model used by this endpoint is multilingual, so you can index and search text in multiple languages. To use custom models, refer to [Configure {{infer}} endpoints for `semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints).

:::{dropdown} Verify the index was created

The response is `true`.

```php
$response = $es->indices()->exists(["index" => "books"]);
var_dump($response->asBool());
```

:::

::::

::::{tab-item} Ruby
:sync: ruby

```ruby
es.indices.create(
  index: "books",
  body: {
    mappings: {
      properties: {
        description: {
          type: "semantic_text" <1>
        }
      }
    }
  }
)
```

1. In this example, `semantic_text` uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints). The model used by this endpoint is multilingual, so you can index and search text in multiple languages. To use custom models, refer to [Configure {{infer}} endpoints for `semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints).

:::{dropdown} Verify the index was created

The response is `true`.

```ruby
puts es.indices.exists(index: "books")
```

:::

::::

::::{tab-item} C#/.NET
:sync: csharp

```csharp
await es.Indices.CreateAsync<Book>("books", c => c
    .Mappings(m => m
        .Properties(p => p
            .SemanticText(b => b.Description) <1>
        )
    )
);
```

1. In this example, `semantic_text` uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints). The model used by this endpoint is multilingual, so you can index and search text in multiple languages. To use custom models, refer to [Configure {{infer}} endpoints for `semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints).

:::{dropdown} Verify the index was created

The response is `True`.

```csharp
var response = await es.Indices.ExistsAsync("books");
Console.WriteLine(response.Exists);
```

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
            "properties": {
              "description": {
                "type": "semantic_text" <1>
              }
            }
          }
        }
        """))
);
```

1. In this example, `semantic_text` uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints). The model used by this endpoint is multilingual, so you can index and search text in multiple languages. To use custom models, refer to [Configure {{infer}} endpoints for `semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints).

:::{dropdown} Verify the index was created

The response is `true`.

```java
var response = es.indices().exists(e -> e.index("books"));
System.out.println(response.value());
```

:::

::::

::::{tab-item} Go
:sync: go

```go
res, err := es.Indices.Create(
	"books",
	es.Indices.Create.WithBody(strings.NewReader(`{
	  "mappings": {
	    "properties": {
	      "description": {
	        "type": "semantic_text" <1>
	      }
	    }
	  }
	}`)),
)
if err != nil {
	panic(err)
}
defer res.Body.Close()
```

1. In this example, `semantic_text` uses a [default {{infer}} endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints). The model used by this endpoint is multilingual, so you can index and search text in multiple languages. To use custom models, refer to [Configure {{infer}} endpoints for `semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#configure-inference-endpoints).

:::{dropdown} Verify the index was created

The response is `true`.

```go
res, err := es.Indices.Exists([]string{"books"})
if err != nil {
	panic(err)
}
defer res.Body.Close()

fmt.Println(res.StatusCode == 200)
```

:::

::::

:::::

### Add the data

Load some data. This example indexes five books in one bulk request:

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

helpers.bulk(es, ({"_index": "books", "_source": b} for b in books), refresh="wait_for")
```

:::{dropdown} Verify the indexed data

The count is `5`.

```python
response = es.count(index="books")
print(response["count"])
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

await es.bulk({
  refresh: "wait_for",
  operations: books.flatMap((book) => [
    { index: { _index: "books" } },
    book,
  ]),
});
```

:::{dropdown} Verify the indexed data

The count is `5`.

```typescript
const response = await es.count({ index: "books" });
console.log(response.count);
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

$es->bulk([
    "refresh" => "wait_for",
    "body" => $operations,
]);
```

:::{dropdown} Verify the indexed data

The count is `5`.

```php
$response = $es->count(["index" => "books"]);
echo $response["count"] . "\n";
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

es.bulk(
  body: operations,
  refresh: "wait_for"
)
```

:::{dropdown} Verify the indexed data

The count is `5`.

```ruby
response = es.count(index: "books")
puts response["count"]
```

:::

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

:::{dropdown} Verify the indexed data

The count is `5`.

```csharp
var response = await es.CountAsync(new CountRequest("books"));
Console.WriteLine(response.Count);
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

es.bulk(bulk.build());
```

:::{dropdown} Verify the indexed data

The count is `5`.

```java
var response = es.count(c -> c.index("books"));
System.out.println(response.count());
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

:::{dropdown} Verify the indexed data

The count is `5`.

```go
res, err := es.Count(es.Count.WithIndex("books"))
if err != nil {
	panic(err)
}
defer res.Body.Close()

var response struct {
	Count int `json:"count"`
}
if err := json.NewDecoder(res.Body).Decode(&response); err != nil {
	panic(err)
}
fmt.Println(response.Count)
```

:::

::::

:::::

:::{tip}
If you want to experiment with a larger dataset, use the [1,000-book sample dataset](https://elastic.co/sample-data/books-1k.json).
:::

## Run search [vector-full-text-search-search]

Use the indexed book data to run semantic and hybrid searches. Semantic search matches meaning, while hybrid search combines semantic and keyword matching.

### Semantic search [vector-full-text-search-semantic]

Run a semantic search against the `description` field:

:::::{tab-set}
:group: languages

::::{tab-item} Python
:sync: python

```python
es = Elasticsearch(
    os.environ["ES_URL"],
    api_key=os.environ["ES_API_KEY"],
)

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

const es = new Client({
  node: process.env.ES_URL,
  auth: { apiKey: process.env.ES_API_KEY! },
});

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
$es = ClientBuilder::create()
    ->setHosts([getenv("ES_URL")])
    ->setApiKey(getenv("ES_API_KEY"))
    ->build();

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
es = Elasticsearch::Client.new(
  url: ENV.fetch("ES_URL"),
  api_key: ENV.fetch("ES_API_KEY")
)

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
var url = Environment.GetEnvironmentVariable("ES_URL")
    ?? throw new InvalidOperationException("ES_URL is not set.");
var apiKey = Environment.GetEnvironmentVariable("ES_API_KEY")
    ?? throw new InvalidOperationException("ES_API_KEY is not set.");

var settings = new ElasticsearchClientSettings(new Uri(url))
    .Authentication(new ApiKey(apiKey));
var es = new ElasticsearchClient(settings);

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
record Book(
    String id,
    String title,
    String author,
    int release_year,
    String description
) {}

String serverUrl = System.getenv("ES_URL");
String apiKey = System.getenv("ES_API_KEY");

ElasticsearchClient es = ElasticsearchClient.of(b -> b
    .host(serverUrl)
    .apiKey(apiKey)
);

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

es.close();
```

::::

::::{tab-item} Go
:sync: go

```go
func main() {
	es, err := elasticsearch.New(
		elasticsearch.WithAddresses(os.Getenv("ES_URL")),
		elasticsearch.WithAPIKey(os.Getenv("ES_API_KEY")),
	)
	if err != nil {
		log.Fatal(err)
	}

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
}
```

::::

:::::

**Project Hail Mary** ranks first.

### Hybrid search [vector-full-text-search-hybrid]

Run a hybrid search that uses full-text search on the `title` field and semantic search on the `description` field:

:::::{tab-set}
:group: languages

::::{tab-item} Python
:sync: python

```python
es = Elasticsearch(
    os.environ["ES_URL"],
    api_key=os.environ["ES_API_KEY"],
)

resp = es.search(
    index="books",
    query={
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

::::

::::{tab-item} TypeScript
:sync: typescript

```typescript
interface Book {
  title: string;
}

const es = new Client({
  node: process.env.ES_URL,
  auth: { apiKey: process.env.ES_API_KEY! },
});

const resp = await es.search<Book>({
  index: "books",
  query: {
    bool: {
      should: [
        {
          match: {
            title: "wind",
          },
        },
        {
          semantic: {
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

::::

::::{tab-item} PHP
:sync: php

```php
$es = ClientBuilder::create()
    ->setHosts([getenv("ES_URL")])
    ->setApiKey(getenv("ES_API_KEY"))
    ->build();

$response = $es->search([
    "index" => "books",
    "body" => [
        "query" => [
            "bool" => [
                "should" => [
                    [
                        "match" => [
                            "title" => "wind",
                        ],
                    ],
                    [
                        "semantic" => [
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

::::

::::{tab-item} Ruby
:sync: ruby

```ruby
es = Elasticsearch::Client.new(
  url: ENV.fetch("ES_URL"),
  api_key: ENV.fetch("ES_API_KEY")
)

response = es.search(
  index: "books",
  body: {
    query: {
      bool: {
        should: [
          {
            match: {
              title: "wind"
            }
          },
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

response["hits"]["hits"].each do |hit|
  puts "#{hit["_score"]} #{hit["_source"]["title"]}"
end
```

::::

::::{tab-item} C#/.NET
:sync: csharp

```csharp
var url = Environment.GetEnvironmentVariable("ES_URL")
    ?? throw new InvalidOperationException("ES_URL is not set.");
var apiKey = Environment.GetEnvironmentVariable("ES_API_KEY")
    ?? throw new InvalidOperationException("ES_API_KEY is not set.");

var settings = new ElasticsearchClientSettings(new Uri(url))
    .Authentication(new ApiKey(apiKey));
var es = new ElasticsearchClient(settings);

var response = await es.SearchAsync<SearchBook>(s => s
    .Indices("books")
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
record Book(
    String id,
    String title,
    String author,
    int release_year,
    String description
) {}

String serverUrl = System.getenv("ES_URL");
String apiKey = System.getenv("ES_API_KEY");

ElasticsearchClient es = ElasticsearchClient.of(b -> b
    .host(serverUrl)
    .apiKey(apiKey)
);

String query = """
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

SearchResponse<Book> response = es.search(s -> s
        .index("books")
        .withJson(new StringReader(query)),
    Book.class
);

for (Hit<Book> hit : response.hits().hits()) {
    System.out.println(hit.score() + " " + hit.source().title());
}

es.close();
```

::::

::::{tab-item} Go
:sync: go

```go
func main() {
	es, err := elasticsearch.New(
		elasticsearch.WithAddresses(os.Getenv("ES_URL")),
		elasticsearch.WithAPIKey(os.Getenv("ES_API_KEY")),
	)
	if err != nil {
		log.Fatal(err)
	}

	query := strings.NewReader(`{
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
}
```

::::

:::::

The `match` clause scores exact title words and the `semantic` clause scores meaning. **The Name of the Wind** ranks first.

## Aggregate the data with ES|QL [vector-full-text-search-esql]

With [aggregations](/explore-analyze/query-filter/aggregations.md), you can summarize groups of data, such as the number of books released in each decade. Use [{{esql}}](elasticsearch://reference/query-languages/esql.md), a piped query language, to run this aggregation:

:::::{tab-set}
:group: languages

::::{tab-item} Python
:sync: python

```python
es = Elasticsearch(
    os.environ["ES_URL"],
    api_key=os.environ["ES_API_KEY"],
)

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
const es = new Client({
  node: process.env.ES_URL,
  auth: { apiKey: process.env.ES_API_KEY! },
});

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
$es = ClientBuilder::create()
    ->setHosts([getenv("ES_URL")])
    ->setApiKey(getenv("ES_API_KEY"))
    ->build();

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
es = Elasticsearch::Client.new(
  url: ENV.fetch("ES_URL"),
  api_key: ENV.fetch("ES_API_KEY")
)

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
var url = Environment.GetEnvironmentVariable("ES_URL")
    ?? throw new InvalidOperationException("ES_URL is not set.");
var apiKey = Environment.GetEnvironmentVariable("ES_API_KEY")
    ?? throw new InvalidOperationException("ES_API_KEY is not set.");

var settings = new ElasticsearchClientSettings(new Uri(url))
    .Authentication(new ApiKey(apiKey));
var es = new ElasticsearchClient(settings);

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
String serverUrl = System.getenv("ES_URL");
String apiKey = System.getenv("ES_API_KEY");

ElasticsearchClient es = ElasticsearchClient.of(b -> b
    .host(serverUrl)
    .apiKey(apiKey)
);

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

es.close();
```

::::

::::{tab-item} Go
:sync: go

```go
func main() {
	es, err := elasticsearch.NewTyped(
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

	response, err := es.Esql.Query().
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

The complete example combines everything in one file. Set `ES_URL` and `ES_API_KEY`, then run it.

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
    index="books",
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
helpers.bulk(es, ({"_index": "books", "_source": b} for b in books), refresh="wait_for")

# Semantic search.
resp = es.search(
    index="books",
    query={"semantic": {"field": "description", "query": "surviving alone in space"}},
)
print("Semantic:")
for hit in resp["hits"]["hits"]:
    print(" ", hit["_score"], hit["_source"]["title"])

# Hybrid search with keyword and semantic queries.
resp = es.search(
    index="books",
    query={"bool": {"should": [
        {"match": {"title": "wind"}},
        {"semantic": {"field": "description", "query": "young magician coming of age"}},
    ]}},
)
print("\nHybrid:")
for hit in resp["hits"]["hits"]:
    print(" ", hit["_score"], hit["_source"]["title"])

# Count books per decade.
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
  index: "books",
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
  onDocument: () => ({ index: { _index: "books" } }),
  refreshOnCompletion: true,
});

// Semantic search.
let resp = await es.search<Book>({
  index: "books",
  query: { semantic: { field: "description", query: "surviving alone in space" } },
});
console.log("Semantic:");
for (const hit of resp.hits.hits) {
  console.log(" ", hit._score, hit._source?.title);
}

// Hybrid search with keyword and semantic queries.
resp = await es.search<Book>({
  index: "books",
  query: { bool: { should: [
    { match: { title: "wind" } },
    { semantic: { field: "description", query: "young magician coming of age" } },
  ] } },
});
console.log("\nHybrid:");
for (const hit of resp.hits.hits) {
  console.log(" ", hit._score, hit._source?.title);
}

// Count books per decade.
const agg = await es.esql.query({ query: `
  FROM books
  | STATS books = COUNT(*) BY decade = release_year - (release_year % 10)
  | KEEP decade, books
  | SORT decade ASC
` });
console.log("\nBy decade:", agg.values);
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
    "index" => "books",
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
    $operations[] = ["index" => ["_index" => "books"]];
    $operations[] = $book;
}

$es->bulk([
    "refresh" => "wait_for",
    "body" => $operations,
]);

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
echo "Semantic:\n";
foreach ($response["hits"]["hits"] as $hit) {
    echo "  " . $hit["_score"] . " " . $hit["_source"]["title"] . "\n";
}

$response = $es->search([
    "index" => "books",
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
echo "\nHybrid:\n";
foreach ($response["hits"]["hits"] as $hit) {
    echo "  " . $hit["_score"] . " " . $hit["_source"]["title"] . "\n";
}

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
echo "\nBy decade:\n";
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
  index: "books",
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
    { index: { _index: "books" } },
    book
  ]
end
es.bulk(body: operations, refresh: "wait_for")

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
puts "Semantic:"
response["hits"]["hits"].each do |hit|
  puts "  #{hit["_score"]} #{hit["_source"]["title"]}"
end

response = es.search(
  index: "books",
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
puts "\nHybrid:"
response["hits"]["hits"].each do |hit|
  puts "  #{hit["_score"]} #{hit["_source"]["title"]}"
end

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
puts "\nBy decade:"
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

await es.Indices.CreateAsync<Book>("books", c => c
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
        Index = "books"
    });
}
await es.BulkAsync(new BulkRequest
{
    Refresh = Refresh.WaitFor,
    Operations = operations
});

var response = await es.SearchAsync<Book>(s => s
    .Indices("books")
    .Query(q => q
        .Semantic(semantic => semantic
            .Field("description")
            .Query("surviving alone in space")
        )
    )
);
Console.WriteLine("Semantic:");
foreach (var hit in response.Hits)
{
    Console.WriteLine($"  {hit.Score} {hit.Source?.Title}");
}

response = await es.SearchAsync<Book>(s => s
    .Indices("books")
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
Console.WriteLine("\nHybrid:");
foreach (var hit in response.Hits)
{
    Console.WriteLine($"  {hit.Score} {hit.Source?.Title}");
}

var aggregation = await es.Esql.QueryAsync(r => r
    .Query("""
        FROM books
        | STATS books = COUNT(*) BY decade = release_year - (release_year % 10)
        | KEEP decade, books
        | SORT decade ASC
        """)
    .Format(EsqlFormat.Json)
);
using var result = JsonDocument.Parse(aggregation.Body);
Console.WriteLine("\nBy decade:");
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

public class Main {
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
            .index("books")
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
                    .index("books")
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
                .index("books")
                .withJson(new StringReader(semanticQuery)),
            Book.class
        );
        System.out.println("Semantic:");
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
                .index("books")
                .withJson(new StringReader(hybridQuery)),
            Book.class
        );
        System.out.println("\nHybrid:");
        for (Hit<Book> hit : response.hits().hits()) {
            System.out.println("  " + hit.score() + " " + hit.source().title());
        }

        String esql = """
            FROM books
            | STATS books = COUNT(*) BY decade = release_year - (release_year % 10)
            | KEEP decade, books
            | SORT decade ASC
            """;
        BinaryResponse aggregation = es.esql().query(q -> q
            .query(esql)
            .format(EsqlFormat.Csv)
        );
        System.out.println("\nBy decade:");
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
		es.Search.WithIndex("books"),
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
		"books",
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
		Index:   "books",
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

	fmt.Println("Semantic:")
	printSearch(es, `{
	  "query": {
	    "semantic": {
	      "field": "description",
	      "query": "surviving alone in space"
	    }
	  }
	}`)

	fmt.Println("\nHybrid:")
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
	query := `FROM books
		| STATS books = COUNT(*) BY decade = release_year - (release_year % 10)
		| KEEP decade, books
		| SORT decade ASC`
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
	fmt.Println("\nBy decade:")
	for _, row := range rows[1:] {
		fmt.Printf("  %ss: %s\n", row[0], row[1])
	}
}
```

:::

::::

:::::

## Next steps [vector-full-text-search-next-steps]

If you want to continue using your Vector Database project, use the following resources to explore more search workflows. To learn how continued usage is billed, refer to [Serverless project billing dimensions](/deploy-manage/cloud-organization/billing/serverless-project-billing-dimensions.md). If you don't plan to continue using the project, [delete it](/deploy-manage/uninstall/delete-a-cloud-deployment.md#serverless) to avoid additional usage charges.

- [Vector search](/solutions/search/vector.md): Learn about vectors, embeddings, vector fields, and similarity search in {{es}}.
- [Compare Elastic Inference Service models](/explore-analyze/elastic-inference/eis-supported-models.md#embedding-models): Learn about the embedding models available through the Elastic {{infer-cap}} Service and compare their capabilities.
- [Learn about chunking strategies](/explore-analyze/elastic-inference/inference-api.md#infer-chunking-config): Learn how to split long text for {{infer}} using sentence, word, recursive, or custom chunking.
- [Tune retrieval with ranking and reranking](/solutions/search/ranking.md): Learn how to improve result ordering with multi-stage ranking and reranking.
- [Plan quantization and sizing](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization): Learn how quantization reduces vector memory and storage requirements and compare the available quantization types.
- [Tutorial: Build multimodal search in Elasticsearch](/solutions/search/multimodal-search/multimodal-search-tutorial.md): Learn how to index images and search them with text, image, and PDF input.
