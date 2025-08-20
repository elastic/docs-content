---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-security-context.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Security context [k8s-security-context]

In Kubernetes, a [`securityContext`](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) defines privilege and access control settings for a Pod or Container. You can set up it through the `podTemplate` section of an Elastic resource specification.

## Default {{es}} security context [k8s_default_elasticsearch_security_context]

As of version 8.8.0, the {{es}} container and ECK managed sidecars and init containers are running with the following security context:

```yaml
securityContext:
  allowPrivilegeEscalation: false
  capabilities:
    drop:
    - ALL
  privileged: false
  readOnlyRootFilesystem: true <1>
```

1. `readOnlyRootFilesystem` is only enabled if the `elasticsearch-data` directory is mounted in a volume.



## Running older versions of {{es}} as non-root [k8s_running_older_versions_of_elasticsearch_as_non_root]

::::{note} 
when running on Red Hat OpenShift a random user ID is [automatically assigned](https://cloud.redhat.com/blog/a-guide-to-openshift-and-uids) and the following instructions do not apply.
::::


In versions of {{es}} before 8.0.0, the Elastisearch container is run as root and its entrypoint is responsible to run the {{es}} process with the `elasticsearch` user (defined with ID 1000). In the background, ECK uses an `initContainer` to make sure that the data volume is writable for the `elasticsearch` user.

To run the Elastisearch container as a non-root user, you need to configure the {{es}} manifest with an appropriate security context to make the data volume writable to the `elasticsearch` user by specifying the right group ID through the `fsGroup`.

Kubernetes recursively changes ownership and permissions for the contents of each volume to match the `fsGroup` specified in a Pod’s securityContext when that volume is mounted and makes all processes of the containers part of the supplementary group ID.

For example, if you force the Pod to run as user `1234`, you need to set `fsGroup` accordingly to `1234`:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
spec:
  nodeSets:
  - name: default
    count: 3
    podTemplate:
      spec:
        securityContext:
          runAsUser: 1234 <1>
          fsGroup: 1234 <2>
```

1. Any containers in the Pod run all processes with user ID `1234`.
2. All processes are also part of the supplementary group ID `1234`, that owns the Pod volumes.



