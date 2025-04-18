---
applies_to:
  stack: 
  deployment:
    eck: 
    ess: 
    ece: 
    self: 
navigation_title: "Error: updating number_of_replicas for indices"
# is mapped_pages needed for newly created docs?
---

# Fix error when updating number_of_replicas for indices in Elasticsearch [updating-number-of-replicas-for-indices-error]

```console
updating number_of_replicas to [] for indices [].
```

This error occurs when there's an attempt to update the number of replicas on one or more indices, but the value provided is either missing or invalid. This can be caused by syntax errors, incorrect data types, or trying to assign more replicas than available nodes can support.

## What it means

The number of replicas in an index determines how many copies of each shard exist. Changing the replica count affects cluster resilience and search performance. {{es}} allows you to adjust this dynamically, and logs the change with this message:

```console
updating number_of_replicas to [replica-count] for indices [index-list]
```

If the value is missing or malformed, the update fails.

## How to resolve it

1. **Use a valid integer** when setting `number_of_replicas`.
2. **Check node count** – You must have enough nodes to accommodate the requested replicas.
3. **Ensure correct syntax** when using the API:

   ```json
   PUT /my-index/_settings
   {
     "index": {
       "number_of_replicas": 2
     }
   }
   ```

4. If needed, **reduce the replica count** to match available resources.

## Dynamic replica allocation

{{es}} supports dynamic replica scaling using `index.auto_expand_replicas`. This allows replica counts to adjust based on the number of available nodes.

Example configuration:

```yaml
index.auto_expand_replicas: 0-5
```

With this setting, {{es}} will scale replicas from 0 up to 5 as nodes are added or removed.

To disable automatic expansion:

```yaml
index.auto_expand_replicas: false
```

## Additional considerations

- If the replica count is changing unexpectedly, verify your **index templates** and **cluster settings**.
- Update index templates to enforce consistent replica configuration for newly created indices.

