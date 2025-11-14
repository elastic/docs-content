```php
$resp = $client->index([
    "index" => "books",
    "body" => [
        "name" => "The Great Gatsby",
        "author" => "F. Scott Fitzgerald",
        "release_date" => "1925-04-10",
        "page_count" => 180,
        "language" => "EN",
    ],
]);
echo $resp->asString();

```
