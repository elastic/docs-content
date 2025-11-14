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
