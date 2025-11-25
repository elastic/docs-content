% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

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
