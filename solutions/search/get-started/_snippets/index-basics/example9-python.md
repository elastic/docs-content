```python
resp = client.indices.delete(
    index="books",
)
print(resp)

resp1 = client.indices.delete(
    index="my-explicit-mappings-books",
)
print(resp1)

```
