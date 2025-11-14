```ruby
require "elasticsearch"

client = Elasticsearch::Client.new(
  host: ENV["ELASTICSEARCH_URL"],
  api_key: ENV["ELASTIC_API_KEY"]
)

response = client.indices.create(
  index: "books"
)
print(resp)

```
