```php
$resp = $client->indices()->delete([
    "index" => "books",
]);
echo $resp->asString();

$resp1 = $client->indices()->delete([
    "index" => "my-explicit-mappings-books",
]);
echo $resp1->asString();

```

% WARNING: This snippet is auto-generated. Do not edit directly.
% See https://github.com/leemthompo/python-console-converter/blob/main/README.md
