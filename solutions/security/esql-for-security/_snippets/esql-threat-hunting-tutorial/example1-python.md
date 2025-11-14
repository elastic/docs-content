```python
import os
from elasticsearch import Elasticsearch

client = Elasticsearch(
    hosts=[os.getenv("ELASTICSEARCH_URL")],
    api_key=os.getenv("ELASTIC_API_KEY"),
)

resp = client.indices.create(
    index="windows-security-logs",
    mappings={
        "properties": {
            "@timestamp": {
                "type": "date"
            },
            "event": {
                "properties": {
                    "code": {
                        "type": "keyword"
                    },
                    "action": {
                        "type": "keyword"
                    }
                }
            },
            "user": {
                "properties": {
                    "name": {
                        "type": "keyword"
                    },
                    "domain": {
                        "type": "keyword"
                    }
                }
            },
            "host": {
                "properties": {
                    "name": {
                        "type": "keyword"
                    },
                    "ip": {
                        "type": "ip"
                    }
                }
            },
            "source": {
                "properties": {
                    "ip": {
                        "type": "ip"
                    }
                }
            },
            "logon": {
                "properties": {
                    "type": {
                        "type": "keyword"
                    }
                }
            }
        }
    },
)
print(resp)

```
