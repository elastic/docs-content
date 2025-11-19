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

% WARNING: This snippet is auto-generated. Do not edit directly.
% See https://github.com/leemthompo/python-console-converter/blob/main/README.md
