```php
$resp = $client->indices()->create([
    "index" => "asset-inventory",
    "body" => [
        "mappings" => [
            "properties" => [
                "host.name" => [
                    "type" => "keyword",
                ],
                "asset.criticality" => [
                    "type" => "keyword",
                ],
                "asset.owner" => [
                    "type" => "keyword",
                ],
                "asset.department" => [
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
