% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

```ruby
response = client.indices.create(
  index: "threat-intel",
  body: {
    "mappings": {
      "properties": {
        "indicator.value": {
          "type": "keyword"
        },
        "indicator.type": {
          "type": "keyword"
        },
        "threat.name": {
          "type": "keyword"
        },
        "threat.severity": {
          "type": "keyword"
        }
      }
    },
    "settings": {
      "index.mode": "lookup"
    }
  }
)
print(resp)

```
