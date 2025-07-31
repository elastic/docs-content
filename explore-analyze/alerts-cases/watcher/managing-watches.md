---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/managing-watches.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Managing watches [managing-watches]

{{watcher}} provides as set of APIs you can use to manage your watches:

* Use the [create or update watch API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-watcher-put-watch) to add or update watches
* Use the [get watch API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-watcher-get-watch) to retrieve watches
* Use the [delete watch API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-watcher-delete-watch) to delete watches
* Use the [activate watch API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-watcher-activate-watch) to activate watches
* Use the [deactivate watch API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-watcher-deactivate-watch) to deactivate watches
* Use the [ack watch API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-watcher-ack-watch) to acknowledge watches

## Listing watches [listing-watches]

Currently there is not dedicated API for listing the stored watches. However, since {{watcher}} stores its watches in the `.watches` index, you can list them by executing a search on this index.

::::{important}
You can only perform read actions on the `.watches` index. You must use the {{watcher}} APIs to create, update, and delete watches. If {{es}} {{security-features}} are enabled, we recommend you only grant users `read` privileges on the `.watches` index.
::::

For example, the following returns the first 100 watches:

```console
GET /_watcher/_query/watches
{
  "size" : 100
}
```
