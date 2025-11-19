```bash
curl -X POST "$ELASTICSEARCH_URL/_bulk" \
  -H "Authorization: ApiKey $ELASTIC_API_KEY" \
  -H "Content-Type: application/x-ndjson" \
  -d $'{"index":{"_index":"books"}}\n{"name":"Revelation Space","author":"Alastair Reynolds","release_date":"2000-03-15","page_count":585}\n{"index":{"_index":"books"}}\n{"name":"1984","author":"George Orwell","release_date":"1985-06-01","page_count":328}\n{"index":{"_index":"books"}}\n{"name":"Fahrenheit 451","author":"Ray Bradbury","release_date":"1953-10-15","page_count":227}\n{"index":{"_index":"books"}}\n{"name":"Brave New World","author":"Aldous Huxley","release_date":"1932-06-01","page_count":268}\n{"index":{"_index":"books"}}\n{"name":"The Handmaids Tale","author":"Margaret Atwood","release_date":"1985-06-01","page_count":311}\n'
```

% WARNING: This snippet is auto-generated. Do not edit directly.
% See https://github.com/leemthompo/python-console-converter/blob/main/README.md
