---
applies_to:
  stack: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Filesource provider [filesource-provider]

Watches for changes of specified files and updates the values of the variables when the content of the files changes.

This allows information from the filesystem to be used as variables in the {{agent}} configuration. This information is allowed only when the provider has been explicitly configured to read this information from the disk. The policy cannot just read any file, it has to be explicitly configured to allow it.

For example, the following configuration watches for changes to `file1`:

```yaml
providers:
  filesource:
    sources:
      file1:
        path: ./file1

inputs:
 - id: filestream
   type: filestream
   paths:
     - ${filesource.file1}
```
