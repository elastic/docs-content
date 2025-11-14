```console
PUT /asset-inventory
{
  "mappings": {
    "properties": {
      "host.name": {"type": "keyword"},
      "asset.criticality": {"type": "keyword"},
      "asset.owner": {"type": "keyword"},
      "asset.department": {"type": "keyword"}
    }
  },
  "settings": {
    "index.mode": "lookup" 
  }
}
```
