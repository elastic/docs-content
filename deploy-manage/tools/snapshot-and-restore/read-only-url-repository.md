---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-read-only-repository.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Read-only URL repository [snapshots-read-only-repository]

You can use a URL repository to give a cluster read-only access to snapshot data exposed through a URL, including `file`, `http`, `https`, and `ftp` locations. Because URL repositories are always read-only, they're a safer and more convenient alternative to registering a read-only shared filesystem repository.

Use {{kib}} or the [create snapshot repository API]({{es-apis}}operation/operation-snapshot-create-repository) to register a URL repository.

```console
PUT _snapshot/my_read_only_url_repository
{
  "type": "url",
  "settings": {
    "url": "file:/mount/backups/my_fs_backup_location"
  }
}
```

## Repository settings [read-only-url-repository-settings]


The `url` repository type supports a number of settings to customize how data is stored, which may be specified when creating the repository.

Repository settings cover the snapshot root URL (including supported protocols), HTTP retries and timeouts for remote URLs, compression, throughput limits, and the maximum number of snapshots. Remote `http`, `https`, and `ftp` URLs must be allowed by the [`repositories.url.allowed_urls`](elasticsearch://reference/elasticsearch/configuration-reference/url-repository-settings.md#repositories-url-allowed) setting.
For a complete list of all read-only URL repository settings, refer to [Read-only URL repository settings](elasticsearch://reference/elasticsearch/configuration-reference/url-repository-settings.md#repository-url-repository-settings).
