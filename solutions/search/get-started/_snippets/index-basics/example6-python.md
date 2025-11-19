```python
resp = client.indices.create(
    index="my-explicit-mappings-books",
    mappings={
        "dynamic": False,
        "properties": {
            "name": {
                "type": "text"
            },
            "author": {
                "type": "text"
            },
            "release_date": {
                "type": "date",
                "format": "yyyy-MM-dd"
            },
            "page_count": {
                "type": "integer"
            }
        }
    },
)
print(resp)

```

% WARNING: This snippet is auto-generated. Do not edit directly.
% See https://github.com/leemthompo/python-console-converter/blob/main/README.md
