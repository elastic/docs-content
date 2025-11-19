% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

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
