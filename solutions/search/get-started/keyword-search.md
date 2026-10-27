---
navigation_title: Keyword search
description: Step-by-step tutorial for creating an index, indexing documents, and running a keyword search from an Elasticsearch client, Console, or curl.
applies_to:
  stack: all
  serverless: all
products:
  - id: elasticsearch
---

# Quickstart: Keyword search in {{es}} [keyword-search-quickstart]

Keyword search matches the words in a query against the words in your documents. This guide uses official {{es}} clients to create an index, index three documents, and run a keyword query.

:::{tip}
Are you an agent? Use the [elasticsearch-onboarding skill](https://github.com/elastic/agent-skills/tree/main/skills/elasticsearch/elasticsearch-onboarding).
:::

## Before you begin [keyword-search-prerequisites]

You need a running {{es}} deployment. The fastest way to follow this quickstart is to create an [{{es}} {{vectordb}} project](/solutions/vector-database.md). New users can [sign up for a free 14-day trial](https://cloud.elastic.co/serverless-registration?onboarding_token=vector). For other deployment types, refer to [Quick start options](/get-started/deployment-options.md#quick-start-options).

You also need the {{es}} endpoint and an API key. To find them, refer to [](/solutions/elasticsearch-solution-project/search-connection-details.md).

## Connect to {{es}} [keyword-search-connect]

Set the {{es}} endpoint and API key as environment variables:

:::::{tab-set}
:group: operating-systems

::::{tab-item} macOS and Linux
:sync: macos-linux

```bash
export ES_URL="<YOUR_ES_URL>" <1>
export ES_API_KEY="YOUR_API_KEY"
```

1. For example, `https://my-deployment.es.us-east-1.aws.elastic.cloud:443`.

::::

::::{tab-item} Windows PowerShell
:sync: windows-powershell

```powershell
$Env:ES_URL = "<YOUR_ES_URL>" <1>
$Env:ES_API_KEY = "YOUR_API_KEY"
```

1. For example, `https://my-deployment.es.us-east-1.aws.elastic.cloud:443`.

::::

:::::

## Install and initialize an {{es}} client [keyword-search-install]

Install the client for your language. For a list of available clients, refer to [{{es}} clients](/reference/elasticsearch-clients/index.md). Console and curl call the REST API directly, so skip this step if you use those.

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

## Create an index [keyword-search-create-index]

Create the `national-parks` index with one [`text`](elasticsearch://reference/elasticsearch/mapping-reference/text.md) field. {{es}} analyzes `text` fields so a later keyword query can match individual words.

:::::{tab-set}
:group: languages

::::{tab-item} Python
:sync: python

```python
es.indices.create(
    index="national-parks",
    mappings={
        "properties": {
            "text": {"type": "text"},
        },
    },
)
```

::::

::::{tab-item} TypeScript
:sync: typescript

```typescript
await es.indices.create({
  index: "national-parks",
  mappings: {
    properties: {
      text: { type: "text" },
    },
  },
});
```

::::

::::{tab-item} PHP
:sync: php

```php
$es->indices()->create([
    "index" => "national-parks",
    "body" => [
        "mappings" => [
            "properties" => [
                "text" => [
                    "type" => "text",
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
  index: "national-parks",
  body: {
    mappings: {
      properties: {
        text: {
          type: "text"
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
await es.Indices.CreateAsync<Park>("national-parks", c => c
    .Mappings(m => m
        .Properties(p => p
            .Text(park => park.Text)
        )
    )
);

public record Park(string Text);
```

::::

::::{tab-item} Java
:sync: java

```java
es.indices().create(c -> c
    .index("national-parks")
    .withJson(new StringReader("""
        {
          "mappings": {
            "properties": {
              "text": {
                "type": "text"
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
	"national-parks",
	es.Indices.Create.WithBody(strings.NewReader(`{
	  "mappings": {
	    "properties": {
	      "text": {
	        "type": "text"
	      }
	    }
	  }
	}`)),
)
if err != nil {
	log.Fatal(err)
}
if createResponse.IsError() {
	log.Fatal(createResponse)
}
createResponse.Body.Close()
```

::::

::::{tab-item} Console
:sync: console

```console
PUT national-parks
{
  "mappings": {
    "properties": {
      "text": {
        "type": "text"
      }
    }
  }
}
```

::::

::::{tab-item} curl
:sync: curl

```bash
curl -X PUT "$ES_URL/national-parks" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "mappings": {
      "properties": {
        "text": {
          "type": "text"
        }
      }
    }
  }'
```

::::

:::::

## Index documents [keyword-search-index-documents]

Index three national park descriptions in one bulk request:

:::::{tab-set}
:group: languages

::::{tab-item} Python
:sync: python

```python
parks = [
    {"text": "Yellowstone National Park is one of the largest national parks in the United States. It ranges from the Wyoming to Montana and Idaho, and contains an area of 2,219,791 acress across three different states. Its most famous for hosting the geyser Old Faithful and is centered on the Yellowstone Caldera, the largest super volcano on the American continent. Yellowstone is host to hundreds of species of animal, many of which are endangered or threatened. Most notably, it contains free-ranging herds of bison and elk, alongside bears, cougars and wolves. The national park receives over 4.5 million visitors annually and is a UNESCO World Heritage Site."},
    {"text": "Yosemite National Park is a United States National Park, covering over 750,000 acres of land in California. A UNESCO World Heritage Site, the park is best known for its granite cliffs, waterfalls and giant sequoia trees. Yosemite hosts over four million visitors in most years, with a peak of five million visitors in 2016. The park is home to a diverse range of wildlife, including mule deer, black bears, and the endangered Sierra Nevada bighorn sheep. The park has 1,200 square miles of wilderness, and is a popular destination for rock climbers, with over 3,000 feet of vertical granite to climb. Its most famous and cliff is the El Capitan, a 3,000 feet monolith along its tallest face."},
    {"text": "Rocky Mountain National Park  is one of the most popular national parks in the United States. It receives over 4.5 million visitors annually, and is known for its mountainous terrain, including Longs Peak, which is the highest peak in the park. The park is home to a variety of wildlife, including elk, mule deer, moose, and bighorn sheep. The park is also home to a variety of ecosystems, including montane, subalpine, and alpine tundra. The park is a popular destination for hiking, camping, and wildlife viewing, and is a UNESCO World Heritage Site."},
]

helpers.bulk(
    es,
    ({"_index": "national-parks", "_source": park} for park in parks),
    refresh="wait_for",
)
```

::::

::::{tab-item} TypeScript
:sync: typescript

```typescript
const parks = [
  {
    text: "Yellowstone National Park is one of the largest national parks in the United States. It ranges from the Wyoming to Montana and Idaho, and contains an area of 2,219,791 acress across three different states. Its most famous for hosting the geyser Old Faithful and is centered on the Yellowstone Caldera, the largest super volcano on the American continent. Yellowstone is host to hundreds of species of animal, many of which are endangered or threatened. Most notably, it contains free-ranging herds of bison and elk, alongside bears, cougars and wolves. The national park receives over 4.5 million visitors annually and is a UNESCO World Heritage Site.",
  },
  {
    text: "Yosemite National Park is a United States National Park, covering over 750,000 acres of land in California. A UNESCO World Heritage Site, the park is best known for its granite cliffs, waterfalls and giant sequoia trees. Yosemite hosts over four million visitors in most years, with a peak of five million visitors in 2016. The park is home to a diverse range of wildlife, including mule deer, black bears, and the endangered Sierra Nevada bighorn sheep. The park has 1,200 square miles of wilderness, and is a popular destination for rock climbers, with over 3,000 feet of vertical granite to climb. Its most famous and cliff is the El Capitan, a 3,000 feet monolith along its tallest face.",
  },
  {
    text: "Rocky Mountain National Park  is one of the most popular national parks in the United States. It receives over 4.5 million visitors annually, and is known for its mountainous terrain, including Longs Peak, which is the highest peak in the park. The park is home to a variety of wildlife, including elk, mule deer, moose, and bighorn sheep. The park is also home to a variety of ecosystems, including montane, subalpine, and alpine tundra. The park is a popular destination for hiking, camping, and wildlife viewing, and is a UNESCO World Heritage Site.",
  },
];

await es.bulk({
  refresh: "wait_for",
  operations: parks.flatMap((park) => [
    { index: { _index: "national-parks" } },
    park,
  ]),
});
```

::::

::::{tab-item} PHP
:sync: php

```php
$parks = [
    [
        "text" => "Yellowstone National Park is one of the largest national parks in the United States. It ranges from the Wyoming to Montana and Idaho, and contains an area of 2,219,791 acress across three different states. Its most famous for hosting the geyser Old Faithful and is centered on the Yellowstone Caldera, the largest super volcano on the American continent. Yellowstone is host to hundreds of species of animal, many of which are endangered or threatened. Most notably, it contains free-ranging herds of bison and elk, alongside bears, cougars and wolves. The national park receives over 4.5 million visitors annually and is a UNESCO World Heritage Site.",
    ],
    [
        "text" => "Yosemite National Park is a United States National Park, covering over 750,000 acres of land in California. A UNESCO World Heritage Site, the park is best known for its granite cliffs, waterfalls and giant sequoia trees. Yosemite hosts over four million visitors in most years, with a peak of five million visitors in 2016. The park is home to a diverse range of wildlife, including mule deer, black bears, and the endangered Sierra Nevada bighorn sheep. The park has 1,200 square miles of wilderness, and is a popular destination for rock climbers, with over 3,000 feet of vertical granite to climb. Its most famous and cliff is the El Capitan, a 3,000 feet monolith along its tallest face.",
    ],
    [
        "text" => "Rocky Mountain National Park  is one of the most popular national parks in the United States. It receives over 4.5 million visitors annually, and is known for its mountainous terrain, including Longs Peak, which is the highest peak in the park. The park is home to a variety of wildlife, including elk, mule deer, moose, and bighorn sheep. The park is also home to a variety of ecosystems, including montane, subalpine, and alpine tundra. The park is a popular destination for hiking, camping, and wildlife viewing, and is a UNESCO World Heritage Site.",
    ],
];

$operations = [];
foreach ($parks as $park) {
    $operations[] = [
        "index" => [
            "_index" => "national-parks",
        ],
    ];
    $operations[] = $park;
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
parks = [
  {
    text: "Yellowstone National Park is one of the largest national parks in the United States. It ranges from the Wyoming to Montana and Idaho, and contains an area of 2,219,791 acress across three different states. Its most famous for hosting the geyser Old Faithful and is centered on the Yellowstone Caldera, the largest super volcano on the American continent. Yellowstone is host to hundreds of species of animal, many of which are endangered or threatened. Most notably, it contains free-ranging herds of bison and elk, alongside bears, cougars and wolves. The national park receives over 4.5 million visitors annually and is a UNESCO World Heritage Site."
  },
  {
    text: "Yosemite National Park is a United States National Park, covering over 750,000 acres of land in California. A UNESCO World Heritage Site, the park is best known for its granite cliffs, waterfalls and giant sequoia trees. Yosemite hosts over four million visitors in most years, with a peak of five million visitors in 2016. The park is home to a diverse range of wildlife, including mule deer, black bears, and the endangered Sierra Nevada bighorn sheep. The park has 1,200 square miles of wilderness, and is a popular destination for rock climbers, with over 3,000 feet of vertical granite to climb. Its most famous and cliff is the El Capitan, a 3,000 feet monolith along its tallest face."
  },
  {
    text: "Rocky Mountain National Park  is one of the most popular national parks in the United States. It receives over 4.5 million visitors annually, and is known for its mountainous terrain, including Longs Peak, which is the highest peak in the park. The park is home to a variety of wildlife, including elk, mule deer, moose, and bighorn sheep. The park is also home to a variety of ecosystems, including montane, subalpine, and alpine tundra. The park is a popular destination for hiking, camping, and wildlife viewing, and is a UNESCO World Heritage Site."
  }
]

operations = parks.flat_map do |park|
  [
    { index: { _index: "national-parks" } },
    park
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
var parks = new[]
{
    new Park("Yellowstone National Park is one of the largest national parks in the United States. It ranges from the Wyoming to Montana and Idaho, and contains an area of 2,219,791 acress across three different states. Its most famous for hosting the geyser Old Faithful and is centered on the Yellowstone Caldera, the largest super volcano on the American continent. Yellowstone is host to hundreds of species of animal, many of which are endangered or threatened. Most notably, it contains free-ranging herds of bison and elk, alongside bears, cougars and wolves. The national park receives over 4.5 million visitors annually and is a UNESCO World Heritage Site."),
    new Park("Yosemite National Park is a United States National Park, covering over 750,000 acres of land in California. A UNESCO World Heritage Site, the park is best known for its granite cliffs, waterfalls and giant sequoia trees. Yosemite hosts over four million visitors in most years, with a peak of five million visitors in 2016. The park is home to a diverse range of wildlife, including mule deer, black bears, and the endangered Sierra Nevada bighorn sheep. The park has 1,200 square miles of wilderness, and is a popular destination for rock climbers, with over 3,000 feet of vertical granite to climb. Its most famous and cliff is the El Capitan, a 3,000 feet monolith along its tallest face."),
    new Park("Rocky Mountain National Park  is one of the most popular national parks in the United States. It receives over 4.5 million visitors annually, and is known for its mountainous terrain, including Longs Peak, which is the highest peak in the park. The park is home to a variety of wildlife, including elk, mule deer, moose, and bighorn sheep. The park is also home to a variety of ecosystems, including montane, subalpine, and alpine tundra. The park is a popular destination for hiking, camping, and wildlife viewing, and is a UNESCO World Heritage Site.")
};

var operations = new BulkOperationsCollection();
foreach (var park in parks)
{
    operations.Add(new BulkIndexOperation<Park>(park)
    {
        Index = "national-parks"
    });
}

await es.BulkAsync(new BulkRequest
{
    Refresh = Refresh.WaitFor,
    Operations = operations
});

public record Park(string Text);
```

::::

::::{tab-item} Java
:sync: java

```java
record Park(String text) {}

Park[] parks = {
    new Park("Yellowstone National Park is one of the largest national parks in the United States. It ranges from the Wyoming to Montana and Idaho, and contains an area of 2,219,791 acress across three different states. Its most famous for hosting the geyser Old Faithful and is centered on the Yellowstone Caldera, the largest super volcano on the American continent. Yellowstone is host to hundreds of species of animal, many of which are endangered or threatened. Most notably, it contains free-ranging herds of bison and elk, alongside bears, cougars and wolves. The national park receives over 4.5 million visitors annually and is a UNESCO World Heritage Site."),
    new Park("Yosemite National Park is a United States National Park, covering over 750,000 acres of land in California. A UNESCO World Heritage Site, the park is best known for its granite cliffs, waterfalls and giant sequoia trees. Yosemite hosts over four million visitors in most years, with a peak of five million visitors in 2016. The park is home to a diverse range of wildlife, including mule deer, black bears, and the endangered Sierra Nevada bighorn sheep. The park has 1,200 square miles of wilderness, and is a popular destination for rock climbers, with over 3,000 feet of vertical granite to climb. Its most famous and cliff is the El Capitan, a 3,000 feet monolith along its tallest face."),
    new Park("Rocky Mountain National Park  is one of the most popular national parks in the United States. It receives over 4.5 million visitors annually, and is known for its mountainous terrain, including Longs Peak, which is the highest peak in the park. The park is home to a variety of wildlife, including elk, mule deer, moose, and bighorn sheep. The park is also home to a variety of ecosystems, including montane, subalpine, and alpine tundra. The park is a popular destination for hiking, camping, and wildlife viewing, and is a UNESCO World Heritage Site.")
};

BulkRequest.Builder bulk = new BulkRequest.Builder()
    .refresh(Refresh.WaitFor);

for (Park park : parks) {
    bulk.operations(op -> op
        .index(idx -> idx
            .index("national-parks")
            .document(park)
        )
    );
}

es.bulk(bulk.build());
```

::::

::::{tab-item} Go
:sync: go

```go
type Park struct {
	Text string `json:"text"`
}

parks := []Park{
	{
		Text: "Yellowstone National Park is one of the largest national parks in the United States. It ranges from the Wyoming to Montana and Idaho, and contains an area of 2,219,791 acress across three different states. Its most famous for hosting the geyser Old Faithful and is centered on the Yellowstone Caldera, the largest super volcano on the American continent. Yellowstone is host to hundreds of species of animal, many of which are endangered or threatened. Most notably, it contains free-ranging herds of bison and elk, alongside bears, cougars and wolves. The national park receives over 4.5 million visitors annually and is a UNESCO World Heritage Site.",
	},
	{
		Text: "Yosemite National Park is a United States National Park, covering over 750,000 acres of land in California. A UNESCO World Heritage Site, the park is best known for its granite cliffs, waterfalls and giant sequoia trees. Yosemite hosts over four million visitors in most years, with a peak of five million visitors in 2016. The park is home to a diverse range of wildlife, including mule deer, black bears, and the endangered Sierra Nevada bighorn sheep. The park has 1,200 square miles of wilderness, and is a popular destination for rock climbers, with over 3,000 feet of vertical granite to climb. Its most famous and cliff is the El Capitan, a 3,000 feet monolith along its tallest face.",
	},
	{
		Text: "Rocky Mountain National Park  is one of the most popular national parks in the United States. It receives over 4.5 million visitors annually, and is known for its mountainous terrain, including Longs Peak, which is the highest peak in the park. The park is home to a variety of wildlife, including elk, mule deer, moose, and bighorn sheep. The park is also home to a variety of ecosystems, including montane, subalpine, and alpine tundra. The park is a popular destination for hiking, camping, and wildlife viewing, and is a UNESCO World Heritage Site.",
	},
}

indexer, err := esutil.NewBulkIndexer(esutil.BulkIndexerConfig{
	Client:  es,
	Index:   "national-parks",
	Refresh: "wait_for",
})
if err != nil {
	log.Fatal(err)
}

ctx := context.Background()
for _, park := range parks {
	data, err := json.Marshal(park)
	if err != nil {
		log.Fatal(err)
	}

	err = indexer.Add(ctx, esutil.BulkIndexerItem{
		Action: "index",
		Body:   bytes.NewReader(data),
	})
	if err != nil {
		log.Fatal(err)
	}
}

if err := indexer.Close(ctx); err != nil {
	log.Fatal(err)
}
```

::::

::::{tab-item} Console
:sync: console

```console
POST national-parks/_bulk?refresh=wait_for
{ "index": {} }
{ "text": "Yellowstone National Park is one of the largest national parks in the United States. It ranges from the Wyoming to Montana and Idaho, and contains an area of 2,219,791 acress across three different states. Its most famous for hosting the geyser Old Faithful and is centered on the Yellowstone Caldera, the largest super volcano on the American continent. Yellowstone is host to hundreds of species of animal, many of which are endangered or threatened. Most notably, it contains free-ranging herds of bison and elk, alongside bears, cougars and wolves. The national park receives over 4.5 million visitors annually and is a UNESCO World Heritage Site." }
{ "index": {} }
{ "text": "Yosemite National Park is a United States National Park, covering over 750,000 acres of land in California. A UNESCO World Heritage Site, the park is best known for its granite cliffs, waterfalls and giant sequoia trees. Yosemite hosts over four million visitors in most years, with a peak of five million visitors in 2016. The park is home to a diverse range of wildlife, including mule deer, black bears, and the endangered Sierra Nevada bighorn sheep. The park has 1,200 square miles of wilderness, and is a popular destination for rock climbers, with over 3,000 feet of vertical granite to climb. Its most famous and cliff is the El Capitan, a 3,000 feet monolith along its tallest face." }
{ "index": {} }
{ "text": "Rocky Mountain National Park  is one of the most popular national parks in the United States. It receives over 4.5 million visitors annually, and is known for its mountainous terrain, including Longs Peak, which is the highest peak in the park. The park is home to a variety of wildlife, including elk, mule deer, moose, and bighorn sheep. The park is also home to a variety of ecosystems, including montane, subalpine, and alpine tundra. The park is a popular destination for hiking, camping, and wildlife viewing, and is a UNESCO World Heritage Site." }
```

::::

::::{tab-item} curl
:sync: curl

```bash
curl -X POST "$ES_URL/national-parks/_bulk?refresh=wait_for" \
  -H "Authorization: ApiKey $ES_API_KEY" \
  -H "Content-Type: application/x-ndjson" \
  --data-binary @- <<'EOF'
{ "index": {} }
{ "text": "Yellowstone National Park is one of the largest national parks in the United States. It ranges from the Wyoming to Montana and Idaho, and contains an area of 2,219,791 acress across three different states. Its most famous for hosting the geyser Old Faithful and is centered on the Yellowstone Caldera, the largest super volcano on the American continent. Yellowstone is host to hundreds of species of animal, many of which are endangered or threatened. Most notably, it contains free-ranging herds of bison and elk, alongside bears, cougars and wolves. The national park receives over 4.5 million visitors annually and is a UNESCO World Heritage Site." }
{ "index": {} }
{ "text": "Yosemite National Park is a United States National Park, covering over 750,000 acres of land in California. A UNESCO World Heritage Site, the park is best known for its granite cliffs, waterfalls and giant sequoia trees. Yosemite hosts over four million visitors in most years, with a peak of five million visitors in 2016. The park is home to a diverse range of wildlife, including mule deer, black bears, and the endangered Sierra Nevada bighorn sheep. The park has 1,200 square miles of wilderness, and is a popular destination for rock climbers, with over 3,000 feet of vertical granite to climb. Its most famous and cliff is the El Capitan, a 3,000 feet monolith along its tallest face." }
{ "index": {} }
{ "text": "Rocky Mountain National Park  is one of the most popular national parks in the United States. It receives over 4.5 million visitors annually, and is known for its mountainous terrain, including Longs Peak, which is the highest peak in the park. The park is home to a variety of wildlife, including elk, mule deer, moose, and bighorn sheep. The park is also home to a variety of ecosystems, including montane, subalpine, and alpine tundra. The park is a popular destination for hiking, camping, and wildlife viewing, and is a UNESCO World Heritage Site." }
EOF
```

::::

:::::

## Run a keyword search [keyword-search-query]

Use [{{esql}}](elasticsearch://reference/query-languages/esql.md) to return documents whose `text` field matches `yosemite`:

:::::{tab-set}
:group: languages

::::{tab-item} Python
:sync: python

```python
resp = es.esql.query(query="""
    FROM national-parks
    | WHERE MATCH(text, "yosemite")
    | KEEP text
    | LIMIT 5
""")

for row in resp["values"]:
    print(row[0])
```

::::

::::{tab-item} TypeScript
:sync: typescript

```typescript
const resp = await es.esql.query({
  query: `
    FROM national-parks
    | WHERE MATCH(text, "yosemite")
    | KEEP text
    | LIMIT 5
  `,
});

for (const [text] of resp.values ?? []) {
  console.log(text);
}
```

::::

::::{tab-item} PHP
:sync: php

```php
$response = $es->esql()->query([
    "body" => [
        "query" => <<<'ESQL'
            FROM national-parks
            | WHERE MATCH(text, "yosemite")
            | KEEP text
            | LIMIT 5
            ESQL,
    ],
]);

foreach ($response["values"] as [$text]) {
    echo $text . "\n";
}
```

::::

::::{tab-item} Ruby
:sync: ruby

```ruby
response = es.esql.query(
  body: {
    query: <<~ESQL
      FROM national-parks
      | WHERE MATCH(text, "yosemite")
      | KEEP text
      | LIMIT 5
    ESQL
  }
)

response["values"].each do |row|
  puts row[0]
end
```

::::

::::{tab-item} C#/.NET
:sync: csharp

```csharp
var response = await es.Esql.QueryAsync(r => r
    .Query("""
        FROM national-parks
        | WHERE MATCH(text, "yosemite")
        | KEEP text
        | LIMIT 5
        """)
    .Format(EsqlFormat.Json)
);

using var result = JsonDocument.Parse(response.Body);
foreach (
    var row in result.RootElement.GetProperty("values").EnumerateArray()
)
{
    Console.WriteLine(row[0]);
}
```

::::

::::{tab-item} Java
:sync: java

```java
String query = """
    FROM national-parks
    | WHERE MATCH(text, "yosemite")
    | KEEP text
    | LIMIT 5
    """;

BinaryResponse response = es.esql().query(q -> q
    .query(query)
    .format(EsqlFormat.Csv)
);

try (BufferedReader reader = new BufferedReader(
    new InputStreamReader(response.content())
)) {
    reader.lines().skip(1).forEach(System.out::println);
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

query := `FROM national-parks
		| WHERE MATCH(text, "yosemite")
		| KEEP text
		| LIMIT 5`

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
	fmt.Println(row[0])
}
```

::::

::::{tab-item} Console
:sync: console

```console
POST _query
{
  "query": """
    FROM national-parks
    | WHERE MATCH(text, "yosemite")
    | KEEP text
    | LIMIT 5
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
    "query": "FROM national-parks | WHERE MATCH(text, \"yosemite\") | KEEP text | LIMIT 5"
  }'
```

::::

:::::

:::{dropdown} Example output
The query returns the Yosemite description, because that document contains the word `yosemite`:

```text
Yosemite National Park is a United States National Park, covering over 750,000 acres of land in California. A UNESCO World Heritage Site, the park is best known for its granite cliffs, waterfalls and giant sequoia trees. Yosemite hosts over four million visitors in most years, with a peak of five million visitors in 2016. The park is home to a diverse range of wildlife, including mule deer, black bears, and the endangered Sierra Nevada bighorn sheep. The park has 1,200 square miles of wilderness, and is a popular destination for rock climbers, with over 3,000 feet of vertical granite to climb. Its most famous and cliff is the El Capitan, a 3,000 feet monolith along its tallest face.
```
:::

## Delete the index [keyword-search-delete]

When you finish and no longer need the sample data, delete the index.

:::{warning}
Deleting an index permanently deletes its documents, shards, and metadata.
:::

:::::{tab-set}
:group: languages

::::{tab-item} Python
:sync: python

```python
es.indices.delete(index="national-parks")
```

::::

::::{tab-item} TypeScript
:sync: typescript

```typescript
await es.indices.delete({ index: "national-parks" });
```

::::

::::{tab-item} PHP
:sync: php

```php
$es->indices()->delete([
    "index" => "national-parks",
]);
```

::::

::::{tab-item} Ruby
:sync: ruby

```ruby
es.indices.delete(index: "national-parks")
```

::::

::::{tab-item} C#/.NET
:sync: csharp

```csharp
await es.Indices.DeleteAsync("national-parks");
```

::::

::::{tab-item} Java
:sync: java

```java
es.indices().delete(d -> d.index("national-parks"));
```

::::

::::{tab-item} Go
:sync: go

```go
deleteResponse, err := es.Indices.Delete([]string{"national-parks"})
if err != nil {
	log.Fatal(err)
}
defer deleteResponse.Body.Close()
```

::::

::::{tab-item} Console
:sync: console

```console
DELETE national-parks
```

::::

::::{tab-item} curl
:sync: curl

```bash
curl -X DELETE "$ES_URL/national-parks" \
  -H "Authorization: ApiKey $ES_API_KEY"
```

::::

:::::

## Next steps

This quickstart covered keyword search from a client. To combine it with semantic search, go to [](/solutions/search/get-started/semantic-search.md).

For a deeper dive, refer to the following resources:

- [Search and filter with Query DSL](elasticsearch://reference/query-languages/query-dsl/full-text-filter-tutorial.md)
- [Get started with {{esql}} queries](elasticsearch://reference/query-languages/esql/esql-getting-started.md)
- [{{es}} clients](/reference/elasticsearch-clients/index.md)
