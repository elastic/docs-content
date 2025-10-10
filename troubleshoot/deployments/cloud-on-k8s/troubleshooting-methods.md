---
navigation_title: Resources and logs
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-troubleshooting-methods.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Troubleshoot ECK resources and logs  [k8s-troubleshooting-methods]

Most common issues can be identified and resolved by following these instructions:

* [View the list of resources](#k8s-get-resources)
* [Describe failing resources](#k8s-describe-failing-resources)
* [Enable ECK debug logs](#k8s-eck-debug-logs)
* [View logs](#k8s-view-logs)
* [Configure Elasticsearch timeouts](#k8s-resource-level-config)
* [Exclude a resource from reconciliation](#k8s-exclude-resource)
* [Get Kubernetes events](#k8s-get-k8s-events)
* [Exec into containers](#k8s-exec-into-containers)
* [Resizing persistent volumes](#k8s-resize-pv)
* [Suspend Elasticsearch](#k8s-suspend-elasticsearch)
* [Capture JVM heap dumps](#k8s-capture-jvm-heap-dumps)

If you are still unable to find a solution to your problem, ask for help:

If you are an existing Elastic customer with an active support contract, you can create a case in the [Elastic Support Portal](https://support.elastic.co/). Kindly attach an [ECK diagnostic](run-eck-diagnostics.md) when opening your case.

Alternatively, or if you do not have a support contract, and if you are unable to find a solution to your problem with the information provided in these documents, ask for help:

* [ECK Discuss forums](https://discuss.elastic.co/c/eck) to ask any question
* [Github issues](https://github.com/elastic/cloud-on-k8s/issues) for bugs and feature requests

:::{include} /deploy-manage/_snippets/autoops-callout-with-ech.md
:::

## View the list of resources [k8s-get-resources]

To deploy and manage the Elastic stack, ECK creates several resources in the namespace where the main resource is deployed.

For example, each Elasticsearch node and Kibana instance has a dedicated Pod. Check the status of the running Pods, and compare it with the expected instances:

```sh
kubectl get pods

NAME                                 READY     STATUS    RESTARTS   AGE
elasticsearch-sample-es-66sv6dvt7g   0/1       Pending   0          3s
elasticsearch-sample-es-9xzzhmgd4h   1/1       Running   0          27m
elasticsearch-sample-es-lgphkv9p67   0/1       Pending   0          3s
kibana-sample-kb-5468b8685d-c7mdp    0/1       Running   0          4s
```

Check the services:

```sh
kubectl get services

NAME                           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
elasticsearch-sample-es-http   ClusterIP   10.19.248.93    <none>        9200/TCP   2d
kibana-sample-kb-http          ClusterIP   10.19.246.116   <none>        5601/TCP   3d
```


## Describe failing resources [k8s-describe-failing-resources]

If an Elasticsearch node does not start up, it is probably because Kubernetes cannot schedule the associated Pod.

First, check the StatefulSets to verify if the current number of replicas match the desired number of replicas.

```sh
kubectl get statefulset

NAME                              DESIRED   CURRENT   AGE
elasticsearch-sample-es-default   1         1         4s
```

Then, check the Pod status. If a Pod fails to reach the `Running` status after a few seconds, something is preventing it from being scheduled or starting up:

```sh
kubectl get pods -l elasticsearch.k8s.elastic.co/statefulset-name=elasticsearch-sample-es-default

NAME                                 READY     STATUS    RESTARTS   AGE
elasticsearch-sample-es-66sv6dvt7g   0/1       Pending   0          3s
elasticsearch-sample-es-9xzzhmgd4h   1/1       Running   0          42s
elasticsearch-sample-es-lgphkv9p67   0/1       Pending   0          3s
kibana-sample-kb-5468b8685d-c7mdp    0/1       Running   0          4s
```

Pod `elasticsearch-sample-es-lgphkv9p67` isn’t scheduled. Run this command to get more insights:

```sh
kubectl describe pod elasticsearch-sample-es-lgphkv9p67

(...)
Events:
  Type     Reason             Age               From                Message
  ----     ------             ----              ----                -------
  Warning  FailedScheduling   1m (x6 over 1m)   default-scheduler   pod has unbound immediate PersistentVolumeClaims (repeated 2 times)
  Warning  FailedScheduling   1m (x6 over 1m)   default-scheduler   pod has unbound immediate PersistentVolumeClaims
  Warning  FailedScheduling   1m (x11 over 1m)  default-scheduler   0/3 nodes are available: 1 node(s) had no available volume zone, 2 Insufficient memory.
  Normal   NotTriggerScaleUp  4s (x11 over 1m)  cluster-autoscaler  pod didn't trigger scale-up (it wouldn't fit if a new node is added)
```

If you get an error with unbound persistent volume claims (PVCs), it means there is not currently a persistent volume that can satisfy the claim. If you are using automatically provisioned storage (for example Amazon EBS provisioner), sometimes the storage provider can take a few minutes to provision a volume, so this may resolve itself in a few minutes. You can also check the status by running `kubectl describe persistentvolumeclaims` to monitor events of the PVCs.


## Enable ECK debug logs [k8s-eck-debug-logs]

To enable `DEBUG` level logs on the operator, edit the `elastic-operator` StatefulSet and set the `--log-verbosity` flag to `1` as shown in this example:

```sh
kubectl edit statefulset.apps -n elastic-system elastic-operator
```

change the `args` array as follows:

```yaml
  spec:
    containers:
    - args:
      - manager
      - --log-verbosity=1
```

Once your change is saved, the operator is automatically restarted by the StatefulSet controller to apply the new settings.


## View logs [k8s-view-logs]


### View Elasticsearch logs [k8s-get-elasticsearch-logs]

Each Elasticsearch node name is mapped to the corresponding Pod name. To get the logs of a particular Elasticsearch node, just fetch the Pod logs:

```sh
kubectl logs -f elasticsearch-sample-es-lgphkv9p67

(...)
{"type": "server", "timestamp": "2019-07-22T08:48:10,859+0000", "level": "INFO", "component": "o.e.c.s.ClusterApplierService", "cluster.name": "elasticsearch-sample", "node.name": "elasticsearch-sample-es-lgphkv9p67", "cluster.uuid": "cX9uCx3uQrej9hMLGPhV0g", "node.id": "R_OcheBlRGeqme1IZzE4_Q",  "message": "added {{elasticsearch-sample-es-kqz4jmvj9p}{UGy5IX0UQcaKlztAoh4sLA}{3o_EUuZvRKW7R1C8b1zzzg}{10.16.2.232}{10.16.2.232:9300}{ml.machine_memory=27395555328, ml.max_open_jobs=20, xpack.installed=true},{elasticsearch-sample-es-stzz78k64p}{Sh_AzQcxRzeuIoOQWgru1w}{cwPoTFNnRAWtqsXWQtWbGA}{10.16.2.233}{10.16.2.233:9300}{ml.machine_memory=27395555328, ml.max_open_jobs=20, xpack.installed=true},}, term: 1, version: 164, reason: ApplyCommitRequest{term=1, version=164, sourceNode={elasticsearch-sample-es-9xzzhmgd4h}{tAi_bCPcSaO1OkLap4wmhQ}{E6VcWWWtSB2oo-2zmj9DMQ}{10.16.1.150}{10.16.1.150:9300}{ml.machine_memory=27395555328, ml.max_open_jobs=20, xpack.installed=true}}"  }
{"type": "server", "timestamp": "2019-07-22T08:48:22,224+0000", "level": "INFO", "component": "o.e.c.s.ClusterApplierService", "cluster.name": "elasticsearch-sample", "node.name": "elasticsearch-sample-es-lgphkv9p67", "cluster.uuid": "cX9uCx3uQrej9hMLGPhV0g", "node.id": "R_OcheBlRGeqme1IZzE4_Q",  "message": "added {{elasticsearch-sample-es-fn9wvxw6sh}{_tbAciHTStaAlUO6GtD9LA}{1g7_qsXwR0qjjfom05VwMA}{10.16.1.154}{10.16.1.154:9300}{ml.machine_memory=27395555328, ml.max_open_jobs=20, xpack.installed=true},}, term: 1, version: 169, reason: ApplyCommitRequest{term=1, version=169, sourceNode={elasticsearch-sample-es-9xzzhmgd4h}{tAi_bCPcSaO1OkLap4wmhQ}{E6VcWWWtSB2oo-2zmj9DMQ}{10.16.1.150}{10.16.1.150:9300}{ml.machine_memory=27395555328, ml.max_open_jobs=20, xpack.installed=true}}"  }
```

You can run the same command for Kibana and APM Server.


### View init container logs [k8s-get-init-container-logs]

An Elasticsearch Pod runs a few init containers to prepare the file system of the main Elasticsearch container. In some scenarios, the Pod may fail to run (`Status: Error` or `Status: CrashloopBackOff`) because one of the init containers is failing to run. Look at the [init container statuses and logs](https://kubernetes.io/docs/tasks/debug-application-cluster/debug-init-containers/) to get more details.


### View ECK logs [k8s-get-eck-logs]

Since the ECK operator is just a standard Pod running in the Kubernetes cluster, you can fetch its logs as you would for any other Pod:

```sh
kubectl -n elastic-system logs -f statefulset.apps/elastic-operator
```

The operator constantly attempts to reconcile Kubernetes resources to match the desired state. Logs with `INFO` level provide some insights about what is going on. Logs with `ERROR` level indicate something is not going as expected.

Due to [optimistic locking](https://github.com/eBay/Kubernetes/blob/master/docs/devel/api-conventions.md#concurrency-control-and-consistency), you can get errors reporting a conflict while updating a resource. You can ignore them, as the update goes through at the next reconciliation attempt, which will happen almost immediately.


## Configure Elasticsearch timeouts [k8s-resource-level-config]

The operator needs to communicate with each Elasticsearch cluster in order to perform orchestration tasks. The default timeout for such requests can be configured by setting the `elasticsearch-client-timeout` value as described in [*Configure ECK*](../../../deploy-manage/deploy/cloud-on-k8s/configure-eck.md). If you have a particularly overloaded Elasticsearch cluster that is taking longer to process API requests, you can temporarily change the timeout and frequency of API calls made by the operator to that single cluster by annotating the relevant `Elasticsearch` resource. The supported list of annotations are:

* `eck.k8s.elastic.co/es-client-timeout`: Request timeout for the API requests made by the Elasticsearch client. Defaults to 3 minutes.
* `eck.k8s.elastic.co/es-observer-interval`: How often Elasticsearch should be checked by the operator to obtain health information. Defaults to 10 seconds.

To set the Elasticsearch client timeout to 60 seconds for a cluster named `quickstart`, you can run the following command:

```sh
kubectl annotate elasticsearch quickstart eck.k8s.elastic.co/es-client-timeout=60s
```


## Exclude resources from reconciliation [k8s-exclude-resource]

For debugging purposes, you might want to temporarily prevent ECK from modifying Kubernetes resources belonging to a particular Elastic Stack resource. To do this, annotate the Elastic object with `eck.k8s.elastic.co/managed=false`. This annotation can be added to any of the following types of objects:

* Elasticsearch
* Kibana
* ApmServer

```yaml
metadata:
  annotations:
    eck.k8s.elastic.co/managed: "false"
```

Or in one line:

```sh
kubectl annotate elasticsearch quickstart --overwrite eck.k8s.elastic.co/managed=false
```


## Get Kubernetes events [k8s-get-k8s-events]

ECK will emit events when:

* important operations are performed (example: a new Elasticsearch Pod was created)
* something is wrong, and the user must be notified

Fetch Kubernetes events:

```sh
kubectl get events

(...)
28s       25m       58        elasticsearch-sample-es-p45nrjch29.15b3ae4cc4f7c00d   Pod                             Warning   FailedScheduling    default-scheduler                                         0/3 nodes are available: 1 node(s) had no available volume zone, 2 Insufficient memory.
28s       25m       52        elasticsearch-sample-es-wxpnzfhqbt.15b3ae4d86bc269f   Pod                             Warning   FailedScheduling    default-scheduler                                         0/3 nodes are available: 1 node(s) had no available volume zone, 2 Insufficient memory.
```

You can filter the events to show only those that are relevant to a particular Elasticsearch cluster:

```sh
kubectl get event --namespace default --field-selector involvedObject.name=elasticsearch-sample

LAST SEEN   FIRST SEEN   COUNT     NAME                                    KIND            SUBOBJECT   TYPE      REASON    SOURCE                     MESSAGE
30m         30m          1         elasticsearch-sample.15b3ae303baa93c0   Elasticsearch               Normal    Created   elasticsearch-controller   Created pod elasticsearch-sample-es-4q7q2k8cl7
30m         30m          1         elasticsearch-sample.15b3ae303bab4f40   Elasticsearch               Normal    Created   elasticsearch-controller   Created pod elasticsearch-sample-es-jg7dsfkcp8
30m         30m          1         elasticsearch-sample.15b3ae303babdfc8   Elasticsearch               Normal    Created   elasticsearch-controller   Created pod elasticsearch-sample-es-xrxsp54jd5
```

You can set filters for Kibana and APM Server too. Note that the default TTL for events in Kubernetes is 1h, so unless your cluster settings have been modified you will not get events older than 1h.


## Resizing persistent volumes [k8s-resize-pv]

To increase or decrease the size of a disk, you cannot change the size of the volumeClaimTemplate directly. This is because StatefulSets do not allow modifications to volumeClaimTemplates. To work around this, you can create a new nodeSet with the new size, and remove the old nodeSet from your Elasticsearch spec. For instance, just changing the name of nodeSet and the size in the existing Elasticsearch spec. ECK will automatically begin to migrate data to the new nodeSet and remove the old one when it is fully drained. Check the [StatefulSets orchestration](../../../deploy-manage/deploy/cloud-on-k8s/nodes-orchestration.md#k8s-statefulsets) documentation for more detail.

For a concrete example, imagine you started with this:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  nodeSets:
  - name: default
    count: 3
    config:
      node.store.allow_mmap: false
    volumeClaimTemplates:
    - metadata:
        name: elasticsearch-data
      spec:
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 5Gi
        storageClassName: standard
```

and want to increase it to 10Gi of storage. You can change the nodeSet name and the volume size like so:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  nodeSets:
  - name: default-10gi
    count: 3
    config:
      node.store.allow_mmap: false
    volumeClaimTemplates:
    - metadata:
        name: elasticsearch-data
      spec:
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 10Gi
        storageClassName: standard
```

and ECK will automatically create a new StatefulSet and begin migrating data into it.


## Exec into containers [k8s-exec-into-containers]

To troubleshoot a filesystem, configuration or a network issue, you can run Shell commands directly in the Elasticsearch container. You can do this with kubectl:

```sh
kubectl exec -ti elasticsearch-sample-es-p45nrjch29 bash
```

This can also be done for Kibana and APM Server.


## Suspend Elasticsearch [k8s-suspend-elasticsearch]

In exceptional cases, you might need to suspend the Elasticsearch process while using `kubectl exec` (as in the [previous section](#k8s-exec-into-containers)) to troubleshoot. One such example where Elasticsearch has to be stopped are the unsafe operations on Elasticsearch nodes that can be executed with the [elasticsearch-node](elasticsearch://reference/elasticsearch/command-line-tools/node-tool.md) tool.

To suspend an Elasticearch node, while keeping the corresponding Pod running, you can annotate the Elasticsearch resource with the `eck.k8s.elastic.co/suspend` annotation. The value should be a comma-separated list of the names of the Pods whose Elasticsearch process you want to suspend.

To suspend the second Pod in the `default` node set of a cluster called `quickstart` for example, you would use the following command:

```sh
kubectl annotate es quickstart eck.k8s.elastic.co/suspend=quickstart-es-default-1
```

You can then open a shell on the `elastic-internal-suspend` init container to troubleshoot:

```sh
kubectl exec -ti quickstart-es-default-1 -c elastic-internal-suspend -- bash
```

Once you are done with troubleshooting the node, you can resume normal operations by removing the annotation:

```sh
kubectl annotate es quickstart eck.k8s.elastic.co/suspend-
```


## Capture JVM heap dumps [k8s-capture-jvm-heap-dumps]

Elasticsearch runs on the JVM. It can be useful to capture a heap dump to troubleshoot garbage collection issues or suspected memory leaks or to share it with Elastic. Follow the specific instructions for [Elasticsearch](jvm-heap-dumps.md).

