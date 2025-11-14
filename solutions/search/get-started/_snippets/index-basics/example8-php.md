```php
$resp = $client->search([
    "index" => "books",
    "body" => [
        "query" => [
            "match" => [
                "name" => "brave",
            ],
        ],
    ],
]);
echo $resp->asString();

```
