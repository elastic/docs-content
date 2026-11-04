---
applies_to:
  stack:
  serverless:
navigation_title: Connect with an SDK
description: Install an official {{es}} language client, connect it with your endpoint and API key, and verify the connection.
type: how-to
---

# Connect to {{es}} with an SDK [connect-with-an-sdk]

You can use an official {{es}} client library to connect your application to {{es}} from code. This page shows how to install and initialize the client for each supported language.

:::{note}
To get started without installing a client, work with {{es}} data in the {{kib}} [{{dev-tools-app}} Console](/explore-analyze/query-filter/tools/console.md), or send requests with `curl`. For `curl` examples, refer to the [{{es}} API documentation]({{es-apis}}).
:::

## Before you begin

You need the following:

- A running {{es}} deployment or project. If you don't have one yet, refer to [](/solutions/search/set-up/get-elasticsearch-running-for-search.md).
- The {{es}} endpoint URL, which the client uses to reach {{es}}, and an API key, which the client uses to authenticate. If you don't have them yet, refer to [](/solutions/search/set-up/api-key-and-endpoints.md).

## Connect a client

The following steps show you how to set your endpoint and API key, install a client for your language, and verify the connection.

:::::::{stepper}

::::::{step} Set environment variables
:anchor: connect-with-an-sdk-connect

Set your {{es}} endpoint and API key as environment variables:

:::::{tab-set}
:group: operating-systems

::::{tab-item} macOS and Linux
:sync: macos-linux

```bash
export ES_URL="YOUR_PROJECT_URL" <1>
export ES_API_KEY="YOUR_API_KEY"
```

1. For example, `https://my-project.es.us-east-1.aws.elastic.cloud:443`.

::::

::::{tab-item} Windows PowerShell
:sync: windows-powershell

```powershell
$Env:ES_URL = "YOUR_PROJECT_URL" <1>
$Env:ES_API_KEY = "YOUR_API_KEY"
```

1. For example, `https://my-project.es.us-east-1.aws.elastic.cloud:443`.

::::

:::::

::::::

::::::{step} Install and initialize a client
:anchor: connect-with-an-sdk-install

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

In the generated `build.gradle` file, add the client dependency to the `dependencies` block and set `mainClass` in the `application` block:

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
from elasticsearch import Elasticsearch

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

::::::

::::::{step} Verify your connection
:anchor: connect-with-an-sdk-verify

Call the info API to confirm that your endpoint URL and API key work. A successful response includes the cluster name and version. The exact output depends on your client and your deployment.

:::::{tab-set}
:group: languages

::::{tab-item} Python
:sync: python

```python
print(es.info())
```

:::{dropdown} Example response

```python
{'name': 'instance-0000000000', 'cluster_name': 'my-deployment', 'cluster_uuid': 'QIpRB53HS1KSVYWtjP_rqg', 'version': {'number': '9.2.0', 'build_flavor': 'default', 'build_type': 'docker', 'build_hash': '25d88452371273dd27356c98598287b669a03eae', 'build_date': '2025-10-21T10:06:21.288851013Z', 'build_snapshot': False, 'lucene_version': '10.3.1', 'minimum_wire_compatibility_version': '8.19.0', 'minimum_index_compatibility_version': '8.0.0'}, 'tagline': 'You Know, for Search'}
```

:::

::::

::::{tab-item} TypeScript
:sync: typescript

```typescript
console.log(await es.info());
```

:::{dropdown} Example response

```typescript
{
  name: 'instance-0000000000',
  cluster_name: 'my-deployment',
  cluster_uuid: 'QIpRB53HS1KSVYWtjP_rqg',
  version: {
    number: '9.2.0',
    build_flavor: 'default',
    build_type: 'docker',
    build_hash: '25d88452371273dd27356c98598287b669a03eae',
    build_date: '2025-10-21T10:06:21.288851013Z',
    build_snapshot: false,
    lucene_version: '10.3.1',
    minimum_wire_compatibility_version: '8.19.0',
    minimum_index_compatibility_version: '8.0.0'
  },
  tagline: 'You Know, for Search'
}
```

:::

::::

::::{tab-item} PHP
:sync: php

```php
echo $es->info()->asString();
```

:::{dropdown} Example response

```json
{
  "name" : "instance-0000000000",
  "cluster_name" : "my-deployment",
  "cluster_uuid" : "QIpRB53HS1KSVYWtjP_rqg",
  "version" : {
    "number" : "9.2.0",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "25d88452371273dd27356c98598287b669a03eae",
    "build_date" : "2025-10-21T10:06:21.288851013Z",
    "build_snapshot" : false,
    "lucene_version" : "10.3.1",
    "minimum_wire_compatibility_version" : "8.19.0",
    "minimum_index_compatibility_version" : "8.0.0"
  },
  "tagline" : "You Know, for Search"
}
```

:::

::::

::::{tab-item} Ruby
:sync: ruby

```ruby
puts es.info
```

:::{dropdown} Example response

```ruby
{"name" => "instance-0000000000", "cluster_name" => "my-deployment", "cluster_uuid" => "QIpRB53HS1KSVYWtjP_rqg", "version" => {"number" => "9.2.0", "build_flavor" => "default", "build_type" => "docker", "build_hash" => "25d88452371273dd27356c98598287b669a03eae", "build_date" => "2025-10-21T10:06:21.288851013Z", "build_snapshot" => false, "lucene_version" => "10.3.1", "minimum_wire_compatibility_version" => "8.19.0", "minimum_index_compatibility_version" => "8.0.0"}, "tagline" => "You Know, for Search"}
```

:::

::::

::::{tab-item} C#/.NET
:sync: csharp

```csharp
var info = await es.InfoAsync();
Console.WriteLine($"{info.ClusterName} {info.Version.Number}");
```

:::{dropdown} Example response

```text
my-deployment 9.2.0
```

:::

::::

::::{tab-item} Java
:sync: java

```java
System.out.println(es.info());
es._transport().close();
```

:::{dropdown} Example response

```text
InfoResponse: {"cluster_name":"my-deployment","cluster_uuid":"QIpRB53HS1KSVYWtjP_rqg","name":"instance-0000000000","tagline":"You Know, for Search","version":{"build_date":"2025-10-21T10:06:21.288851013Z","build_flavor":"default","build_hash":"25d88452371273dd27356c98598287b669a03eae","build_snapshot":false,"build_type":"docker","lucene_version":"10.3.1","minimum_index_compatibility_version":"8.0.0","minimum_wire_compatibility_version":"8.19.0","number":"9.2.0"}}
```

:::

::::

::::{tab-item} Go
:sync: go

```go
res, err := es.Info()
if err != nil {
	log.Fatal(err)
}
defer res.Body.Close()
log.Println(res)
```

:::{dropdown} Example response

```text
[200 OK] {
  "name" : "instance-0000000000",
  "cluster_name" : "my-deployment",
  "cluster_uuid" : "QIpRB53HS1KSVYWtjP_rqg",
  "version" : {
    "number" : "9.2.0",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "25d88452371273dd27356c98598287b669a03eae",
    "build_date" : "2025-10-21T10:06:21.288851013Z",
    "build_snapshot" : false,
    "lucene_version" : "10.3.1",
    "minimum_wire_compatibility_version" : "8.19.0",
    "minimum_index_compatibility_version" : "8.0.0"
  },
  "tagline" : "You Know, for Search"
}
```

:::

::::

:::::

::::::

:::::::

## Next steps [connect-with-an-sdk-next]

{{es}} is up and running, and your application is connected. Next, learn how to ingest your own data in [](/solutions/search/ingest-for-search.md).
