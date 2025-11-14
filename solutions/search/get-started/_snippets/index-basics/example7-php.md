```php
$resp = $client->search([
    "index" => "books",
]);
echo $resp->asString();

```
