---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-jvm-heap-dumps.html
---

# JVM heap dumps [k8s-jvm-heap-dumps]

## Ensure sufficient storage [k8s_ensure_sufficient_storage]

Elasticsearch is [configured by default](https://www.elastic.co/guide/en/elasticsearch/reference/current/important-settings.html#heap-dump-path) to take heap dumps on out-of-memory exceptions to the default data directory. The default data directory is `/usr/share/elasticsearch/data` in the official Docker images that ECK uses. If you are running Elasticsearch with a large heap that is as large as the remaining space on the data volume, this can lead to a situation where Elasticsearch is no longer able to start. To avoid this scenario you have two options:

1. Choose a different path by setting `-XX:HeapDumpPath=` with the  `ES_JAVA_OPTS` variable to a path where a volume with sufficient storage space is mounted
2. [Resize the data volume](../../../deploy-manage/deploy/cloud-on-k8s/volume-claim-templates.md) to a sufficiently large size if your volume provisioner supports volume expansion


## Capturing JVM heap dumps [k8s_capturing_jvm_heap_dumps]

To take a heap dump before the JVM process runs out of memory you can execute the heap dump command directly in the Elasticsearch container:

```sh
kubectl exec $POD_NAME -- su elasticsearch -g root -c \
  '/usr/share/elasticsearch/jdk/bin/jmap -dump:format=b,file=data/heap.hprof $(pgrep -n java)'
```

If the Elasticsearch container is running with a random user ID, as for example on OpenShift, there is no need to substitute the user identity:

```sh
kubectl exec $POD_NAME -- bash -c \
  '/usr/share/elasticsearch/jdk/bin/jmap -dump:format=b,file=data/heap.hprof $(pgrep -n java)'
```


## Extracting heap dumps from the Elasticsearch container [k8s_extracting_heap_dumps_from_the_elasticsearch_container]

To retrieve heap dumps taken by the Elasticsearch JVM or by you, as described in the previous section, you can use the `kubectl cp` command:

```sh
kubectl cp $POD_NAME:/usr/share/elasticsearch/data/heap.hprof ./heap.hprof


# Remove the heap dump from the running container to free up space
kubectl exec $POD_NAME -- rm /usr/share/elasticsearch/data/heap.hprof
```


