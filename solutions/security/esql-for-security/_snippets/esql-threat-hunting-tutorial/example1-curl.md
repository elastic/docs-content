% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

```bash
curl -X PUT "$ELASTICSEARCH_URL/windows-security-logs" \
  -H "Authorization: ApiKey $ELASTIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"mappings":{"properties":{"@timestamp":{"type":"date"},"event":{"properties":{"code":{"type":"keyword"},"action":{"type":"keyword"}}},"user":{"properties":{"name":{"type":"keyword"},"domain":{"type":"keyword"}}},"host":{"properties":{"name":{"type":"keyword"},"ip":{"type":"ip"}}},"source":{"properties":{"ip":{"type":"ip"}}},"logon":{"properties":{"type":{"type":"keyword"}}}}}}'
```
