% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

```php
<?php

require(__DIR__ . "/vendor/autoload.php");

use Elastic\Elasticsearch\ClientBuilder;

$client = ClientBuilder::create()
    ->setHosts([getenv("ELASTICSEARCH_URL")])
    ->setApiKey(getenv("ELASTIC_API_KEY"))
    ->build();

$resp = $client->indices()->create([
    "index" => "windows-security-logs",
    "body" => [
        "mappings" => [
            "properties" => [
                "@timestamp" => [
                    "type" => "date",
                ],
                "event" => [
                    "properties" => [
                        "code" => [
                            "type" => "keyword",
                        ],
                        "action" => [
                            "type" => "keyword",
                        ],
                    ],
                ],
                "user" => [
                    "properties" => [
                        "name" => [
                            "type" => "keyword",
                        ],
                        "domain" => [
                            "type" => "keyword",
                        ],
                    ],
                ],
                "host" => [
                    "properties" => [
                        "name" => [
                            "type" => "keyword",
                        ],
                        "ip" => [
                            "type" => "ip",
                        ],
                    ],
                ],
                "source" => [
                    "properties" => [
                        "ip" => [
                            "type" => "ip",
                        ],
                    ],
                ],
                "logon" => [
                    "properties" => [
                        "type" => [
                            "type" => "keyword",
                        ],
                    ],
                ],
            ],
        ],
    ],
]);
echo $resp->asString();

```
