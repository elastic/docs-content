---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/managing-watches.html
---

# Managing watches [managing-watches]

{{watcher}} provides as set of APIs you can use to manage your watches:

* Use the [create or update watch API](https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-put-watch.html) to add or update watches
* Use the [get watch API](https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-get-watch.html) to retrieve watches
* Use the [delete watch API](https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-delete-watch.html) to delete watches
* Use the [activate watch API](https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-activate-watch.html) to activate watches
* Use the [deactivate watch API](https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-deactivate-watch.html) to deactivate watches
* Use the [ack watch API](https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-ack-watch.html) to acknowledge watches

## Listing watches [listing-watches]

Currently there is not dedicated API for listing the stored watches. However, since {{watcher}} stores its watches in the `.watches` index, you can list them by executing a search on this index.

::::{important}
You can only perform read actions on the `.watches` index. You must use the {{watcher}} APIs to create, update, and delete watches. If {{es}} {security-features} are enabled, we recommend you only grant users `read` privileges on the `.watches` index.
::::

For example, the following returns the first 100 watches:

```console
GET /_watcher/_query/watches
{
  "size" : 100
}
```
