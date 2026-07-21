* To use {{kib}}'s **Snapshot and Restore** feature, you must have the following permissions:

    * [Cluster privileges](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster): `monitor`, `manage_slm`, `cluster:admin/snapshot`, and `cluster:admin/repository`
    * {applies_to}`stack: ga 9.5` [Cluster privilege](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster): `cluster:admin/settings/update`, required only to set or change the default snapshot repository. Without it, you can still use **Snapshot and Restore**, but the controls for managing the default repository are hidden.
    * [Index privilege](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices): `monitor` privilege on all the indices

* To register a snapshot repository or restore a snapshot, the cluster’s global metadata must be writeable. Ensure there aren’t any [cluster blocks](elasticsearch://reference/elasticsearch/configuration-reference/miscellaneous-cluster-settings.md#cluster-read-only) that prevent write access. The restore operation ignores index blocks.
