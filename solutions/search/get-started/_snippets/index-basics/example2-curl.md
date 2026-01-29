% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

```bash
curl -X POST "$ELASTICSEARCH_URL/books/_doc" \
  -H "Authorization: ApiKey $ELASTIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"Snow Crash","author":"Neal Stephenson","release_date":"1992-06-01","page_count":470}'
```
