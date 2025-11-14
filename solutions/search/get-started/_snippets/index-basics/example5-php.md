```php
$resp = $client->indices()->getMapping([
    "index" => "books",
]);
echo $resp->asString();

```
