---
navigation_title: Start and stop {{ilm-init}}
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/start-stop-ilm.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Start and stop index lifecycle management [start-stop-ilm]

Follow these steps to check the current {{ilm-init}} status, and to stop or restart it as needed.

### Get {{ilm-init}} status 

:::{include} /manage-data/_snippets/ilm-status.md
:::

### Stop {{ilm-init}} 

:::{include} /manage-data/_snippets/ilm-stop.md
:::

### Start {{ilm-init}} 

:::{include} /manage-data/_snippets/ilm-start.md
:::