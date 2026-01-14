% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

```php
$resp = $client->indices()->create([
    "index" => "user-context",
    "body" => [
        "mappings" => [
            "properties" => [
                "user.name" => [
                    "type" => "keyword",
                ],
                "user.role" => [
                    "type" => "keyword",
                ],
                "user.department" => [
                    "type" => "keyword",
                ],
                "user.privileged" => [
                    "type" => "boolean",
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
