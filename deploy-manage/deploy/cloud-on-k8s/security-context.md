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



## {{es}} data volume ownership [k8s-es-data-volume-ownership]

The {{es}} process runs as a non-root user. For the process to write to the data volume, the volume must be writable for that user.

By default, ECK adds a Pod-level security context to {{es}} Pods. It sets `fsGroup: 1000`, which matches the group of the `elasticsearch` user in the {{es}} container image. Kubernetes then changes the group ownership of the volumes when it mounts them.

ECK doesn't add the default Pod security context in the following cases:

* The `set-default-security-context` operator flag is `false`.
* The flag is `auto-detect`, which is the default, and the operator detects that it runs on Red Hat OpenShift.

For more information about the flag, refer to [ECK configuration flags](cloud-on-k8s://reference/eck-configuration-flags.md).

If ECK doesn't set the default security context and your storage doesn't set the ownership of the volume, {{es}} can fail to start with an error similar to `failed to obtain node locks ... maybe these locations are not writable`. The `elastic-internal-init-filesystem` init container doesn't fix this, because it runs as a non-root user by default and can't change the ownership of the data volume. In these cases, set `fsGroup: 1000` explicitly in the `podTemplate` of your node sets:

```yaml
spec:
  nodeSets:
  - name: default
    count: 3
    podTemplate:
      spec:
        securityContext:
          fsGroup: 1000
```

::::{note}
This doesn't apply to Red Hat OpenShift. OpenShift assigns `fsGroup` from the range allocated to the namespace and rejects other values, unless the service account can use a security context constraint that allows any `fsGroup`.
::::


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



