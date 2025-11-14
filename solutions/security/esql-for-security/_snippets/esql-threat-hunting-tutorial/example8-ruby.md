```ruby
response = client.indices.create(
  index: "user-context",
  body: {
    "mappings": {
      "properties": {
        "user.name": {
          "type": "keyword"
        },
        "user.role": {
          "type": "keyword"
        },
        "user.department": {
          "type": "keyword"
        },
        "user.privileged": {
          "type": "boolean"
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
