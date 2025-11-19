```bash
curl -X DELETE "$ELASTICSEARCH_URL/books" \
  -H "Authorization: ApiKey $ELASTIC_API_KEY"
curl -X DELETE "$ELASTICSEARCH_URL/my-explicit-mappings-books" \
  -H "Authorization: ApiKey $ELASTIC_API_KEY"
```

% WARNING: This snippet is auto-generated. Do not edit directly.
% See https://github.com/leemthompo/python-console-converter/blob/main/README.md
