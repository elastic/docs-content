---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-openshift-agent.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Grant host access permission to Elastic Agent [k8s-openshift-agent]

Deploying Elastic Agent on Openshift may require additional permissions depending on the type of [integration](/reference/fleet/index.md) Elastic Agent is supposed to run. In any case, Elastic Agent uses a [hostPath](https://kubernetes.io/docs/concepts/storage/volumes/#hostpath) volume as its data directory on OpenShift to maintain a stable identity. Therefore, the Service Account used for Elastic Agent needs permissions to use hostPath volumes.

{{agent}} must also run as root with a privileged container to write to this directory. For this, add the Service Account to the `privileged` [Security Context Constraint](https://docs.openshift.com/container-platform/4.12/authentication/managing-security-context-constraints.html) (SCC).

The following example assumes that Elastic Agent is deployed in the Namespace `elastic` with the ServiceAccount `elastic-agent`. You can replace these values according to your environment.

::::{note}
If you used the examples from the [recipes directory](https://github.com/elastic/cloud-on-k8s/tree/{{version.eck | M.M}}/config/recipes/elastic-agent), the ServiceAccount may already exist.
::::


1. Create a dedicated ServiceAccount:

    ```shell
    oc create serviceaccount elastic-agent -n elastic
    ```

2. Add the ServiceAccount to the `privileged` SCC:

    ```shell
    oc adm policy add-scc-to-user privileged -z elastic-agent -n elastic
    ```

3. Update the Elastic Agent manifest to use the new ServiceAccount, for example:

    ```yaml subs=true
    apiVersion: agent.k8s.elastic.co/v1alpha1
    kind: Agent
    metadata:
      name: my-agent
    spec:
      version: {{version.stack}}
      daemonSet:
        podTemplate:
          spec:
            serviceAccountName: elastic-agent
            securityContext:
              runAsUser: 0 <1>
            containers:
            - name: agent
              securityContext:
                privileged: true <2>
    ```

    1. Runs the container as root. The `hostaccess` SCC rejects Pods that run as root.
    2. Runs the container as privileged. Without it, SELinux denies the container access to the data directory on the node, and {{agent}} fails to start with an error similar to `mkdir /usr/share/elastic-agent/state/data: permission denied`.


