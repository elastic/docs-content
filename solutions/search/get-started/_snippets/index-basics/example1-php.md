```php
<?php

require(__DIR__ . "/vendor/autoload.php");

use Elastic\Elasticsearch\ClientBuilder;

$client = ClientBuilder::create()
    ->setHosts([getenv("ELASTICSEARCH_URL")])
    ->setApiKey(getenv("ELASTIC_API_KEY"))
    ->build();

$resp = $client->indices()->create([
    "index" => "books",
]);
echo $resp->asString();

```
