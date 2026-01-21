---
navigation_title: Limitations
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-limitations.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Watcher limitations [watcher-limitations]

## Watches are not updated when file based scripts change [_watches_are_not_updated_when_file_based_scripts_change]

When you refer to a file script in a watch, the watch itself is not updated if you change the script on the filesystem.

Currently, the only way to reload a file script in a watch is to delete the watch and recreate it.

## Security integration [_security_integration]

When the {{security-features}} are enabled, a watch stores information about what the user who stored the watch is allowed to execute **at that time**. This means, if those permissions change over time, the watch will still be able to execute with the permissions that existed when the watch was created.
