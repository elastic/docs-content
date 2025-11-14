```php
$resp = $client->indices()->create([
    "index" => "threat-intel",
    "body" => [
        "mappings" => [
            "properties" => [
                "indicator.value" => [
                    "type" => "keyword",
                ],
                "indicator.type" => [
                    "type" => "keyword",
                ],
                "threat.name" => [
                    "type" => "keyword",
                ],
                "threat.severity" => [
                    "type" => "keyword",
                ],
            ],
        ],
        "settings" => [
            "index.mode" => "lookup",
        ],
    ],
]);
echo $resp->asString();

```
