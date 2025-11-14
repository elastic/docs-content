```php
$resp = $client->bulk([
    "refresh" => "wait_for",
    "body" => array(
        [
            "index" => [
                "_index" => "network-logs",
            ],
        ],
        [
            "@timestamp" => "2025-05-20T08:25:00Z",
            "source" => [
                "ip" => "10.1.1.50",
                "port" => 52341,
            ],
            "destination" => [
                "ip" => "185.220.101.45",
                "port" => 443,
            ],
            "network" => [
                "bytes" => 2048,
                "protocol" => "tcp",
            ],
            "host" => [
                "name" => "WS-001",
            ],
        ],
        [
            "index" => [
                "_index" => "network-logs",
            ],
        ],
        [
            "@timestamp" => "2025-05-20T11:15:00Z",
            "source" => [
                "ip" => "10.1.3.5",
                "port" => 54892,
            ],
            "destination" => [
                "ip" => "185.220.101.45",
                "port" => 443,
            ],
            "network" => [
                "bytes" => 50000000,
                "protocol" => "tcp",
            ],
            "host" => [
                "name" => "DB-001",
            ],
        ],
        [
            "index" => [
                "_index" => "network-logs",
            ],
        ],
        [
            "@timestamp" => "2025-05-20T02:40:00Z",
            "source" => [
                "ip" => "10.1.4.10",
                "port" => 61234,
            ],
            "destination" => [
                "ip" => "185.220.101.45",
                "port" => 443,
            ],
            "network" => [
                "bytes" => 500000000,
                "protocol" => "tcp",
            ],
            "host" => [
                "name" => "DC-001",
            ],
        ],
    ),
]);
echo $resp->asString();

```
