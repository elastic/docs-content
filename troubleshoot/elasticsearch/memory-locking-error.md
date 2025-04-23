---
applies_to:
  stack: 
  deployment:
    eck: 
    ess: 
    ece: 
    self: 
navigation_title: "Error: Memory locking requested but memory is not locked"
---

# Fix memory locking error in Elasticsearch [memory-locking-error]

```console
Error: memory locking requested for elasticsearch process but memory is not locked
```


This error indicates that {{es}} attempted to lock its memory to prevent swapping but failed. Swapping can severely impact performance and stability by introducing large garbage collection (GC) pauses.

You can fix this by reviewing your memory swapping options, and adjust as needed.

## What it means

{{es}} uses the `bootstrap.memory_lock: true` setting to request that its memory be locked into RAM, preventing the OS from swapping it to disk. If this lock fails due to missing system permissions or improper configuration, {{es}} logs this error.

## How to resolve it

1. **Enable memory lock in configuration**:

   Edit `elasticsearch.yml` and set:

   ```yaml
   bootstrap.memory_lock: true
   ```

2. **Verify the memory lock status**:

   Run the following:

   ```console
   GET _nodes?filter_path=**.mlockall
   ```

   A successful configuration will return:

   ```json
   {
     "nodes" : {
       "<node_id>" : {
         "process" : {
           "mlockall" : true
         }
       }
     }
   }
   ```

   If the value is `false`, further [system-level configuration](https://www.elastic.co/guide/en/elasticsearch/reference/current/setup-configuration-memory.html) is required.
