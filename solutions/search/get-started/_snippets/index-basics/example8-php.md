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

% WARNING: This snippet is auto-generated. Do not edit directly.
% See https://github.com/leemthompo/python-console-converter/blob/main/README.md
