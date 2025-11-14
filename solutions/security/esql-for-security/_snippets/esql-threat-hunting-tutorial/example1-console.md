```console
PUT /windows-security-logs
{
  "mappings": {
    "properties": {
      "@timestamp": {"type": "date"},
      "event": {
        "properties": {
          "code": {"type": "keyword"}, # Event codes like 4624 (successful logon) and 4625 (failed logon) are stored as keywords for exact matching.
          "action": {"type": "keyword"}
        }
      },
      "user": {
        "properties": {
          "name": {"type": "keyword"},
          "domain": {"type": "keyword"}
        }
      },
      "host": {
        "properties": {
          "name": {"type": "keyword"},
          "ip": {"type": "ip"}
        }
      },
      "source": {
        "properties": {
          "ip": {"type": "ip"}
        }
      },
      "logon": {
        "properties": {
          "type": {"type": "keyword"}
        }
      }
    }
  }
}
```
