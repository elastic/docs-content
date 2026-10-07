---
applies_to:
  stack:
  serverless:
navigation_title: Connect through an SDK
description: Install an official Elasticsearch language client, connect it with your endpoint and API key, and verify the connection.
type: how-to
---

# Connect through an SDK [connect-through-an-sdk]

Install and configure an official {{es}} language client to connect to a project or cluster.

## Connect to your project [connect-through-an-sdk-connect]

To get your {{es}} endpoint and API key, refer to [API key and endpoints](/solutions/search/set-up/api-key-and-endpoints.md). Set them as environment variables:

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

## Install and initialize a client [connect-through-an-sdk-install]

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
import co.elastic.clients.elasticsearch.core.SearchResponse;
import co.elastic.clients.elasticsearch.core.search.Hit;
import co.elastic.clients.elasticsearch.esql.EsqlFormat;
import co.elastic.clients.transport.endpoints.BinaryResponse;

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

## Verify your connection [connect-through-an-sdk-verify]

To verify your connection, create an index, index some sample data, and check the document count.

1. Create an index called `books`:

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
                "type": "semantic_text",
            }
        }
    },
)
```

::::

::::{tab-item} TypeScript
:sync: typescript

```typescript
await es.indices.create({
  index: "books",
  mappings: {
    properties: {
      description: {
        type: "semantic_text",
      },
    },
  },
});
```

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
                    "type" => "semantic_text",
                ],
            ],
        ],
    ],
]);
```

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
          type: "semantic_text"
        }
      }
    }
  }
)
```

::::

::::{tab-item} C#/.NET
:sync: csharp

```csharp
await es.Indices.CreateAsync<Book>("books", c => c
    .Mappings(m => m
        .Properties(p => p
            .SemanticText(b => b.Description)
        )
    )
);
```

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
                "type": "semantic_text"
              }
            }
          }
        }
        """))
);
```

::::

::::{tab-item} Go
:sync: go

```go
createResponse, err := es.Indices.Create(
	"books",
	es.Indices.Create.WithBody(strings.NewReader(`{
	  "mappings": {
	    "properties": {
	      "description": {
	        "type": "semantic_text"
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

::::
:::::

2. Index five sample books in one bulk request:

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

:::::

3. Verify the documents were indexed:

:::::{tab-set}
:group: languages

::::{tab-item} Python
:sync: python

```python
es.count(index="books")
```

::::

::::{tab-item} TypeScript
:sync: typescript

```typescript
await es.count({ index: "books" });
```

::::

::::{tab-item} PHP
:sync: php

```php
$es->count([
    "index" => "books",
]);
```

::::

::::{tab-item} Ruby
:sync: ruby

```ruby
es.count(index: "books")
```

::::

::::{tab-item} C#/.NET
:sync: csharp

```csharp
await es.CountAsync(c => c.Indices("books"));
```

::::

::::{tab-item} Java
:sync: java

```java
es.count(c -> c.index("books"));
```

::::

::::{tab-item} Go
:sync: go

```go
countRes, err := es.Count(es.Count.WithIndex("books"))
if err != nil {
	log.Fatal(err)
}
countRes.Body.Close()
```

::::

:::::

The response returns a count of 5, which confirms that all five books were indexed.

## Next steps [connect-through-an-sdk-next]

{{es}} is up and running, and you have already indexed a small sample dataset. Next, learn how to ingest your own data at scale in [](/solutions/search/ingest-for-search.md).
