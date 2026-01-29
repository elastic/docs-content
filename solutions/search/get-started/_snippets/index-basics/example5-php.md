% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

```php
$resp = $client->indices()->getMapping([
    "index" => "books",
]);
echo $resp->asString();

```
