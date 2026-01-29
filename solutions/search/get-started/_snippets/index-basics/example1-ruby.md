% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

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
