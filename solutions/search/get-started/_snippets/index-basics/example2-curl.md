```bash
curl -X POST "$ELASTICSEARCH_URL/books/_doc" \
  -H "Authorization: ApiKey $ELASTIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"Snow Crash","author":"Neal Stephenson","release_date":"1992-06-01","page_count":470}'
```
