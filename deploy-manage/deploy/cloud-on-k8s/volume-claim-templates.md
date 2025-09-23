---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-volume-claim-templates.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Volume claim templates [k8s-volume-claim-templates]


### Specifying the volume claim settings [k8s_specifying_the_volume_claim_settings]

By default, the operator creates a [`PersistentVolumeClaim`](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) with a capacity of 1Gi for each pod in an {{es}} cluster to prevent data loss in case of accidental pod deletion. For production workloads, you should define your own volume claim template with the desired storage capacity and (optionally) the Kubernetes [storage class](https://kubernetes.io/docs/concepts/storage/storage-classes/) to associate with the persistent volume.

::::{important}
The name of the volume claim must always be `elasticsearch-data`. If you chose a different name you have to set up a corresponding volume mount matching the [data.path](/deploy-manage/deploy/self-managed/important-settings-configuration.md#path-settings) yourself ( `/usr/share/elasticsearch/data` by default).
::::


```yaml
spec:
  nodeSets:
  - name: default
    count: 3
    volumeClaimTemplates:
    - metadata:
        name: elasticsearch-data # Do not change this name unless you set up a volume mount for the data path.
      spec:
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 5Gi
        storageClassName: standard
```

## Controlling volume claim deletion [k8s_controlling_volume_claim_deletion]

ECK automatically deletes PersistentVolumeClaim resources if the owning {{es}} nodes are scaled down. The corresponding PersistentVolumes may be preserved, depending on the configured [storage class reclaim policy](https://kubernetes.io/docs/concepts/storage/storage-classes/#reclaim-policy).

In addition, you can control what ECK should do with the PersistentVolumeClaims if you delete the {{es}} cluster altogether through the `volumeClaimDeletePolicy` attribute.

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: es
spec:
  version: {{version.stack}}
  volumeClaimDeletePolicy: DeleteOnScaledownOnly
  nodeSets:
  - name: default
    count: 3
```

The possible values are `DeleteOnScaledownAndClusterDeletion` and `DeleteOnScaledownOnly`. By default `DeleteOnScaledownAndClusterDeletion` is in effect, which means that all PersistentVolumeClaims are deleted together with the {{es}} cluster. However, `DeleteOnScaledownOnly` keeps the PersistentVolumeClaims when deleting the {{es}} cluster. If you recreate a deleted cluster with the same name and node sets as before, the existing PersistentVolumeClaims will be adopted by the new cluster.


### Updating the volume claim settings [k8s-volume-claim-templates-update]

If the storage class allows [volume expansion](https://kubernetes.io/blog/2018/07/12/resizing-persistent-volumes-using-kubernetes/), you can increase the storage requests size in the volumeClaimTemplates. ECK will update the existing PersistentVolumeClaims accordingly, and recreate the StatefulSet automatically. If the volume driver supports `ExpandInUsePersistentVolumes`, the filesystem is resized online, without the need of restarting the {{es}} process, or re-creating the Pods. If the volume driver does not support `ExpandInUsePersistentVolumes`, Pods must be manually deleted after the resize, to be recreated automatically with the expanded filesystem.

Kubernetes forbids any other changes in the volumeClaimTemplates, such as [changing the storage class](https://kubernetes.io/docs/concepts/storage/storage-classes) or [decreasing the volume size](https://kubernetes.io/blog/2018/07/12/resizing-persistent-volumes-using-kubernetes/). To make these changes, you can create a new nodeSet with different settings, and remove the existing nodeSet. In practice, that’s equivalent to renaming the existing nodeSet while modifying its claim settings in a single update. Before removing Pods of the deleted nodeSet, ECK makes sure that data is migrated to other nodes.


### EmptyDir [k8s_emptydir]

::::{warning}
Don’t use `emptyDir` as it might generate permanent data loss.
::::


If you are not concerned about data loss, you can use an `emptyDir` volume for {{es}} data:

```yaml
spec:
  nodeSets:
  - name: data
    count: 10
    podTemplate:
      spec:
        volumes:
        - name: elasticsearch-data
          emptyDir: {}
```
