```ruby
require "elasticsearch"

client = Elasticsearch::Client.new(
  host: ENV["ELASTICSEARCH_URL"],
  api_key: ENV["ELASTIC_API_KEY"]
)

response = client.indices.create(
  index: "windows-security-logs",
  body: {
    "mappings": {
      "properties": {
        "@timestamp": {
          "type": "date"
        },
        "event": {
          "properties": {
            "code": {
              "type": "keyword"
            },
            "action": {
              "type": "keyword"
            }
          }
        },
        "user": {
          "properties": {
            "name": {
              "type": "keyword"
            },
            "domain": {
              "type": "keyword"
            }
          }
        },
        "host": {
          "properties": {
            "name": {
              "type": "keyword"
            },
            "ip": {
              "type": "ip"
            }
          }
        },
        "source": {
          "properties": {
            "ip": {
              "type": "ip"
            }
          }
        },
        "logon": {
          "properties": {
            "type": {
              "type": "keyword"
            }
          }
        }
      }
    }
  }
)
print(resp)

```
