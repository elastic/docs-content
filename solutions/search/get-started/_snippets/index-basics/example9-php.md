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
