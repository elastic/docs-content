```bash
curl -X PUT "$ELASTICSEARCH_URL/user-context" \
  -H "Authorization: ApiKey $ELASTIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"mappings":{"properties":{"user.name":{"type":"keyword"},"user.role":{"type":"keyword"},"user.department":{"type":"keyword"},"user.privileged":{"type":"boolean"}}},"settings":{"index.mode":"lookup"}}'
```
