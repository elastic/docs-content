% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

```python
resp = client.search(
    index="books",
    query={
        "match": {
            "name": "brave"
        }
    },
)
print(resp)

```
