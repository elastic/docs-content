---
applies:
  eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-storage-recommendations.html
---

# Storage recommendations [k8s-storage-recommendations]

ECK does not come with its own storage mechanism for Elasticsearch data. It is compatible with any Kubernetes storage option. It is recommended to use PersistentVolumes, by configuring the [VolumeClaimTemplates](volume-claim-templates.md) section of the Elasticsearch resource.

Multiple PersistentVolume storage classes are available, depending on your Kubernetes setup. Their specifications impact Elasticsearch performance and operations. Evaluate the trade-offs among the various options and choose the solution that best fits your needs.


## Network-attached or Local PersistentVolumes [k8s_network_attached_or_local_persistentvolumes]

PersistentVolumes can be of two types: **Network-attached** or **Local**. ECK handles them in the same way, but they have different performance, price and operational characteristics.

* **Network-attached PersistentVolumes** can generally be attached to a Pod regardless of the host they are scheduled on. They provide a major operational benefit: if the host goes down, or needs to be replaced, the Pod can simply be deleted. Kubernetes reschedules it automatically on a different host, generally in the same region, and reattaches the same volume. This can take only a few seconds, and does not require any human intervention.
* **Local PersistentVolumes** are bound to a particular host, and map a directory on the filesystem. They provide a major operational overhead: once bound to a Local PersistentVolume, a Pod can only be scheduled on the same host. If that host goes down, or needs to be replaced, the Pod cannot be scheduled on a different host. It remains in a `Pending` state until the host is available, or until the PersistentVolumeClaim is manually deleted. For that reason, Local PersistentVolumes bring more operational overhead.

In both cases, the performance depends on the underlying hardware and implementation. In general, local SSDs give the best performance. The fastest network-attached volumes from major Cloud providers can also provide acceptable performance, depending on your Elasticsearch use cases. To better evaluate your performance requirements, you can [benchmark](https://github.com/elastic/rally) your storage options against the expected Elasticsearch usage.


## Local PersistentVolumes operations [k8s_local_persistentvolumes_operations]


### Host maintenance [k8s_host_maintenance]

To take a host out of the Kubernetes cluster temporarily, it is common to cordon, then drain it. Kubernetes deletes Elasticsearch Pods scheduled on that host automatically, as long as the [PodDisruptionBudget](pod-disruption-budget.md) allows it. By default, ECK manages a PodDisruptionBudget that allows one Pod to be taken down, as long as the cluster has a green health. Once deleted, that Pod cannot be scheduled again on the cordoned host: the Pod stays `Pending`, waiting for that host to come back online. The next Pod can be automatically deleted when the Elasticsearch cluster health becomes green again.

Some hosted Kubernetes offerings only respect the PodDisruptionBudget for a certain amount of time, before killing all Pods on the node. For example, [GKE automated version upgrade](https://cloud.google.com/kubernetes-engine/docs/concepts/cluster-upgrades) rotates all nodes without preserving local volumes, and respects the PodDisruptionBudget for a maximum of one hour. In such cases it is preferable to [manually handle the cluster version upgrade](https://cloud.google.com/kubernetes-engine/docs/concepts/cluster-upgrades#upgrading_manually).


### Host removal [k8s_host_removal]

If a host has a failure, or is permanently removed, its local data is likely lost. The corresponding Pod stays `Pending` because it can no longer attach the PersistentVolume. To schedule the Pod on a different host with a new empty volume, you have to manually remove both the PersistenteVolumeClaim and the Pod. A new Pod is automatically created with a new PersistentVolumeClaim, which is then matched with a PersistentVolume. Then, Elasticsearch shard replication makes sure that data is recovered on the new instance.


## Local PersistentVolume provisioners [k8s_local_persistentvolume_provisioners]

You can provision Local PersistentVolumes in one of the following ways:

* **Manual provisioning**: Manually [create PersistentVolume resources](https://kubernetes.io/blog/2018/04/13/local-persistent-volumes-beta/#creating-a-local-persistent-volume), matching a local path to a specific host. Data must be manually removed once the PersistentVolumes are released.
* **Static provisioning**: Run a program that automatically discovers the existing partitions on each host, and creates the corresponding PersistentVolume resources. The [Local PersistentVolume Static Provisioner](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner) is a great way to get started.
* **Dynamic provisioning**: [OpenEBS](https://openebs.io) and [TopoLVM](https://github.com/topolvm/topolvm) are examples of components you can install into your Kubernetes cluster to manage the provisioning of persistent volumes from local disks attached to the nodes. These tools leverage technologies like LVM and ZFS to dynamically allocate persistent volumes from storage pools made out of local disks. Depending on the technology used, bonus features like dynamic volume resizing, thin-provisioning and, snapshots are also available with some of these offerings. Installation of these components might require initial setup work on your Kubernetes cluster like installing filesystem utilities on all nodes, creating RAID configurations for the disks or even installing API extensions like custom schedulers. Some managed Kubernetes offerings might have restrictions that make it difficult to perform some of those setup steps. Check the documentation of the Kubernetes provider and the storage provisioner to ensure that they are compatible with each other.


## Storage class settings [k8s_storage_class_settings]


### volumeBindingMode: WaitForFirstConsumer [k8s_volumebindingmode_waitforfirstconsumer]

In the PersistentVolume StorageClass, it is important to set [`volumeBindingMode: WaitForFirstConsumer`](https://kubernetes.io/docs/concepts/storage/storage-classes/#volume-binding-mode), otherwise a Pod might be scheduled on a host that cannot access the existing PersistentVolume. This setting isn’t always applied by default on Cloud providers StorageClasses, but in most cases it is possible to create (or patch) StorageClasses to add the setting.


### Reclaim policy [k8s_reclaim_policy]

The reclaim policy of a StorageClass specifies whether a PersistentVolume should be automatically deleted once its corresponding PersistentVolumeClaim is deleted. It can be set to `Delete` or `Retain`.

ECK automatically deletes PersistentVolumeClaims when they are no longer needed, following a cluster downscale or deletion. However, ECK does not delete PersistentVolumes. The system cannot reuse a PersistentVolume with existing data from a different cluster. In this case Elasticsearch does not start, as it detects data that belongs to a different cluster. For this reason, it is recommended to use the `Delete` reclaim policy.
