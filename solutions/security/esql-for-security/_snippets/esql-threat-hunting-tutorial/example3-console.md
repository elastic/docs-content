```console
PUT /process-logs
{
  "mappings": {
    "properties": {
      "@timestamp": {"type": "date"},
      "process": {
        "properties": {
          "name": {"type": "keyword"},
          "command_line": {"type": "text"}, # Command lines are stored as text fields to enable full-text search for suspicious parameters and encoded commands.
          "parent": {
            "properties": {
              "name": {"type": "keyword"}
            }
          }
        }
      },
      "user": {
        "properties": {
          "name": {"type": "keyword"}
        }
      },
      "host": {
        "properties": {
          "name": {"type": "keyword"}
        }
      }
    }
  }
}
```
