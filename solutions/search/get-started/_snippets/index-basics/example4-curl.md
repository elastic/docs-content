```bash
curl -X POST "$ELASTICSEARCH_URL/books/_doc" \
  -H "Authorization: ApiKey $ELASTIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"The Great Gatsby","author":"F. Scott Fitzgerald","release_date":"1925-04-10","page_count":180,"language":"EN"}'
```
