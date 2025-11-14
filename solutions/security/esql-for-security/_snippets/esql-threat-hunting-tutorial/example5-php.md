```php
$resp = $client->indices()->create([
    "index" => "network-logs",
    "body" => [
        "mappings" => [
            "properties" => [
                "@timestamp" => [
                    "type" => "date",
                ],
                "source" => [
                    "properties" => [
                        "ip" => [
                            "type" => "ip",
                        ],
                        "port" => [
                            "type" => "integer",
                        ],
                    ],
                ],
                "destination" => [
                    "properties" => [
                        "ip" => [
                            "type" => "ip",
                        ],
                        "port" => [
                            "type" => "integer",
                        ],
                    ],
                ],
                "network" => [
                    "properties" => [
                        "bytes" => [
                            "type" => "long",
                        ],
                        "protocol" => [
                            "type" => "keyword",
                        ],
                    ],
                ],
                "host" => [
                    "properties" => [
                        "name" => [
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
