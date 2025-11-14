```ruby
response = client.indices.create(
  index: "process-logs",
  body: {
    "mappings": {
      "properties": {
        "@timestamp": {
          "type": "date"
        },
        "process": {
          "properties": {
            "name": {
              "type": "keyword"
            },
            "command_line": {
              "type": "text"
            },
            "parent": {
              "properties": {
                "name": {
                  "type": "keyword"
                }
              }
            }
          }
        },
        "user": {
          "properties": {
            "name": {
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
    }
  }
)
print(resp)

```
