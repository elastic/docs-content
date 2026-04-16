```console
PUT /kibana_sample_data_agents
{
  "mappings": {
    "properties": {
      "name": { "type": "text" },
      "author": { "type": "text" },
      "release_date": { "type": "date" },
      "page_count": { "type": "integer" }
    }
  }
}
```
