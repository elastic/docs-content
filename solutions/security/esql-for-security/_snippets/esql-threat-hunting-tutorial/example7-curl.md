% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

```bash
curl -X PUT "$ELASTICSEARCH_URL/asset-inventory" \
  -H "Authorization: ApiKey $ELASTIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"mappings":{"properties":{"host.name":{"type":"keyword"},"asset.criticality":{"type":"keyword"},"asset.owner":{"type":"keyword"},"asset.department":{"type":"keyword"}}},"settings":{"index.mode":"lookup"}}'
```
