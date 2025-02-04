---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-file-descriptor.html
---

# File descriptor check [bootstrap-checks-file-descriptor]

File descriptors are a Unix construct for tracking open "files". In Unix though, [everything is a file](https://en.wikipedia.org/wiki/Everything_is_a_file). For example, "files" could be a physical file, a virtual file (e.g., `/proc/loadavg`), or network sockets. Elasticsearch requires lots of file descriptors (e.g., every shard is composed of multiple segments and other files, plus connections to other nodes, etc.). This bootstrap check is enforced on OS X and Linux. To pass the file descriptor check, you might have to configure [file descriptors](file-descriptors.md).

