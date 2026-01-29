% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

```bash
curl -X PUT "$ELASTICSEARCH_URL/process-logs" \
  -H "Authorization: ApiKey $ELASTIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"mappings":{"properties":{"@timestamp":{"type":"date"},"process":{"properties":{"name":{"type":"keyword"},"command_line":{"type":"text"},"parent":{"properties":{"name":{"type":"keyword"}}}}},"user":{"properties":{"name":{"type":"keyword"}}},"host":{"properties":{"name":{"type":"keyword"}}}}}}'
```
