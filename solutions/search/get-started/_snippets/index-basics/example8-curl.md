```bash
curl -X GET "$ELASTICSEARCH_URL/books/_search" \
  -H "Authorization: ApiKey $ELASTIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":{"match":{"name":"brave"}}}'
```
