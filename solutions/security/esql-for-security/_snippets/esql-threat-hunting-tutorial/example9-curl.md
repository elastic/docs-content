% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

```bash
curl -X PUT "$ELASTICSEARCH_URL/threat-intel" \
  -H "Authorization: ApiKey $ELASTIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"mappings":{"properties":{"indicator.value":{"type":"keyword"},"indicator.type":{"type":"keyword"},"threat.name":{"type":"keyword"},"threat.severity":{"type":"keyword"}}},"settings":{"index.mode":"lookup"}}'
```
