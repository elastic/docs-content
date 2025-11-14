```ruby
response = client.search(
  index: "books",
  body: {
    "query": {
      "match": {
        "name": "brave"
      }
    }
  }
)
print(resp)

```
