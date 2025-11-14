```bash
curl -X PUT "$ELASTICSEARCH_URL/my-explicit-mappings-books" \
  -H "Authorization: ApiKey $ELASTIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"mappings":{"dynamic":false,"properties":{"name":{"type":"text"},"author":{"type":"text"},"release_date":{"type":"date","format":"yyyy-MM-dd"},"page_count":{"type":"integer"}}}}'
```
