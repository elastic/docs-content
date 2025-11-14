```ruby
response = client.indices.delete(
  index: "books"
)
print(resp)

response1 = client.indices.delete(
  index: "my-explicit-mappings-books"
)
print(resp1)

```
