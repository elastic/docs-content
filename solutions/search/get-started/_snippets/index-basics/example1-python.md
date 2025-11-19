```python
import os
from elasticsearch import Elasticsearch

client = Elasticsearch(
    hosts=[os.getenv("ELASTICSEARCH_URL")],
    api_key=os.getenv("ELASTIC_API_KEY"),
)

resp = client.indices.create(
    index="books",
)
print(resp)

```

% WARNING: This snippet is auto-generated. Do not edit directly.
% See https://github.com/leemthompo/python-console-converter/blob/main/README.md
