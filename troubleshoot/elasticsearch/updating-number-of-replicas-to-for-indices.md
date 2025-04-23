---
applies_to:
  stack: 
  deployment:
    eck: 
    ess: 
    ece: 
    self: 
navigation_title: "Error: updating number_of_replicas for indices"
---

# Fix error when updating number_of_replicas for indices in {{es}} [updating-number-of-replicas-for-indices-error]

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

- Use a valid integer when setting `number_of_replicas`.
- Make sure you have enough nodes to accommodate the requested replicas. If needed, reduce the replica count to match available resources.
- Check the syntax of your API request:

   ```bash
   PUT /my-index/_settings
   {
     "index": {
       "number_of_replicas": 2
     }
   }

## Dynamic replica allocation

Instead of directly updating the number of replicas, you can use dynamic replica scaling by configuring `index.auto_expand_replicas`. This setting adjusts the replica count based on the number of available nodes.

Example configuration:

```yaml
index.auto_expand_replicas: 0-5
```

To disable automatic expansion:

```yaml
index.auto_expand_replicas: false
```

## Tips

- If the replica count is changing unexpectedly, verify your index templates and cluster settings.
- To apply a consistent replica configuration to new indices, update the relevant index templates.

