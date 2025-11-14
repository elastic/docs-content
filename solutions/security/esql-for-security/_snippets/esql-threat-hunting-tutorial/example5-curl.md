```bash
curl -X PUT "$ELASTICSEARCH_URL/network-logs" \
  -H "Authorization: ApiKey $ELASTIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"mappings":{"properties":{"@timestamp":{"type":"date"},"source":{"properties":{"ip":{"type":"ip"},"port":{"type":"integer"}}},"destination":{"properties":{"ip":{"type":"ip"},"port":{"type":"integer"}}},"network":{"properties":{"bytes":{"type":"long"},"protocol":{"type":"keyword"}}},"host":{"properties":{"name":{"type":"keyword"}}}}}}'
```
