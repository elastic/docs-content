* To use {{kib}}'s **Snapshot and Restore** feature, you must have the following permissions:

    * [Cluster privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster): `monitor`, `manage_slm`, `cluster:admin/snapshot`, and `cluster:admin/repository`
    * [Index privilege](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices): `monitor` privilege on all the indices

* To register a snapshot repository or restore a snapshot, the cluster’s global metadata must be writeable. Ensure there aren’t any [cluster blocks](elasticsearch://reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#cluster-read-only) that prevent write access. The restore operation ignores index blocks.