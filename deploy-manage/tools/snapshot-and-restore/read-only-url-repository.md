---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-read-only-repository.html
applies_to:
  deployment:
    self:
---

# Read-only URL repository [snapshots-read-only-repository]

::::{note}
This repository type is only available if you run {{es}} on your own hardware. If you use {{ech}}, see [{{ech}} repository types](self-managed.md).
::::


You can use a URL repository to give a cluster read-only access to a shared file system. Since URL repositories are always read-only, they’re a safer and more convenient alternative to registering a read-only shared filesystem repository.

Use {{kib}} or the [create snapshot repository API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-create-repository) to register a URL repository.

```console
PUT _snapshot/my_read_only_url_repository
{
  "type": "url",
  "settings": {
    "url": "file:/mount/backups/my_fs_backup_location"
  }
}
```
%  TEST[skip:no access to url file path]

## Repository settings [read-only-url-repository-settings]

`chunk_size`
:   (Optional, [byte value](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#byte-units)) Maximum size of files in snapshots. In snapshots, files larger than this are broken down into chunks of this size or smaller. Defaults to `null` (unlimited file size).

`http_max_retries`
:   (Optional, integer) Maximum number of retries for `http` and `https` URLs. Defaults to `5`.

`http_socket_timeout`
:   (Optional, [time value](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#time-units)) Maximum wait time for data transfers over a connection. Defaults to `50s`.

`compress`
:   (Optional, Boolean) If `true`, metadata files, such as index mappings and settings, are compressed in snapshots. Data files are not compressed. Defaults to `true`.

`max_number_of_snapshots`
:   (Optional, integer) Maximum number of snapshots the repository can contain. Defaults to `Integer.MAX_VALUE`, which is `2^31-1` or `2147483647`.

`max_restore_bytes_per_sec`
:   (Optional, [byte value](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#byte-units)) Maximum snapshot restore rate per node. Defaults to unlimited. Note that restores are also throttled through [recovery settings](elasticsearch://reference/elasticsearch/configuration-reference/index-recovery-settings.md).

`max_snapshot_bytes_per_sec`
:   (Optional, [byte value](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#byte-units)) Maximum snapshot creation rate per node. Defaults to `40mb` per second. Note that if the [recovery settings for managed services](elasticsearch://reference/elasticsearch/configuration-reference/index-recovery-settings.md#recovery-settings-for-managed-services) are set, then it defaults to unlimited, and the rate is additionally throttled through [recovery settings](elasticsearch://reference/elasticsearch/configuration-reference/index-recovery-settings.md).

`url`
:   (Required, string) URL location of the root of the shared filesystem repository. The following protocols are supported:

* `file`
* `ftp`
* `http`
* `https`
* `jar`

URLs using the `http`, `https`, or `ftp` protocols must be explicitly allowed with the [`repositories.url.allowed_urls`](elasticsearch://reference/elasticsearch/configuration-reference/snapshot-restore-settings.md#repositories-url-allowed) cluster setting. This setting supports wildcards in the place of a host, path, query, or fragment in the URL.

URLs using the `file` protocol must point to the location of a shared filesystem accessible to all master and data nodes in the cluster. This location must be registered in the `path.repo` setting. You don’t need to register URLs using the `ftp`, `http`, `https`, or `jar` protocols in the `path.repo` setting.



