% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

```python
resp = client.indices.create(
    index="network-logs",
    mappings={
        "properties": {
            "@timestamp": {
                "type": "date"
            },
            "source": {
                "properties": {
                    "ip": {
                        "type": "ip"
                    },
                    "port": {
                        "type": "integer"
                    }
                }
            },
            "destination": {
                "properties": {
                    "ip": {
                        "type": "ip"
                    },
                    "port": {
                        "type": "integer"
                    }
                }
            },
            "network": {
                "properties": {
                    "bytes": {
                        "type": "long"
                    },
                    "protocol": {
                        "type": "keyword"
                    }
                }
            },
            "host": {
                "properties": {
                    "name": {
                        "type": "keyword"
                    }
                }
            }
        }
    },
)
print(resp)

```
