```console
PUT /my-explicit-mappings-books
{
  "mappings": {
    "dynamic": false,  <1>
    "properties": {  <2>
      "name": { "type": "text" },
      "author": { "type": "text" },
      "release_date": { "type": "date", "format": "yyyy-MM-dd" },
      "page_count": { "type": "integer" }
    }
  }
}
```

1. `dynamic`: Turns off dynamic mapping for the index. If you don't define fields in the mapping, they'll still be stored in the document's `_source` field, but you can't index or search them.
2. `properties`: Defines the fields and their corresponding data types.
