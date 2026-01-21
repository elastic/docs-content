---
navigation_title: Quickstart
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-elastic-agent-fleet-quickstart.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Quickstart: Running {{fleet}} on {{eck}} [k8s-elastic-agent-fleet-quickstart]

1. To deploy {{fleet-server}}, {{agents}}, {{es}}, and {{kib}}, apply the following specification:

    ```yaml
    cat <<EOF | kubectl apply -f -
    apiVersion: agent.k8s.elastic.co/v1alpha1
    kind: Agent
    metadata:
      name: fleet-server-quickstart
      namespace: default
    spec:
      version: {{version.stack}}
      kibanaRef:
        name: kibana-quickstart
      elasticsearchRefs:
      - name: elasticsearch-quickstart
      mode: fleet
      fleetServerEnabled: true
      policyID: eck-fleet-server
      deployment:
        replicas: 1
        podTemplate:
          spec:
            serviceAccountName: elastic-agent
            automountServiceAccountToken: true
            securityContext:
              runAsUser: 0 <1>
    ---
    apiVersion: agent.k8s.elastic.co/v1alpha1
    kind: Agent
    metadata:
      name: elastic-agent-quickstart
      namespace: default
    spec:
      version: {{version.stack}}
      kibanaRef:
        name: kibana-quickstart
      fleetServerRef:
        name: fleet-server-quickstart
      mode: fleet
      policyID: eck-agent
      daemonSet:
        podTemplate:
          spec:
            serviceAccountName: elastic-agent
            automountServiceAccountToken: true
            securityContext:
              runAsUser: 0 <1>
            volumes:
            - name: agent-data
              emptyDir: {}
    ---
    apiVersion: kibana.k8s.elastic.co/v1
    kind: Kibana
    metadata:
      name: kibana-quickstart
      namespace: default
    spec:
      version: {{version.stack}}
      count: 1
      elasticsearchRef:
        name: elasticsearch-quickstart
      config:
        xpack.fleet.agents.elasticsearch.hosts: ["<ELASTICSEARCH_HOST_URL>.default.svc:9200"]
        xpack.fleet.agents.fleet_server.hosts: ["<FLEET_SERVER_HOST_URL>.default.svc:8220"]
        xpack.fleet.packages:
          - name: system
            version: latest
          - name: elastic_agent
            version: latest
          - name: fleet_server
            version: latest
        xpack.fleet.agentPolicies:
          - name: Fleet Server on ECK policy
            id: eck-fleet-server
            namespace: default
            is_managed: true
            monitoring_enabled:
              - logs
              - metrics
            unenroll_timeout: 900
            package_policies:
            - name: fleet_server-1
              id: fleet_server-1
              package:
                name: fleet_server
          - name: Elastic Agent on ECK policy
            id: eck-agent
            namespace: default
            is_managed: true
            monitoring_enabled:
              - logs
              - metrics
            unenroll_timeout: 900
            package_policies:
              - name: system-1
                id: system-1
                package:
                  name: system
    ---
    apiVersion: elasticsearch.k8s.elastic.co/v1
    kind: Elasticsearch
    metadata:
      name: elasticsearch-quickstart
      namespace: default
    spec:
      version: {{version.stack}}
      nodeSets:
      - name: default
        count: 3
        config:
          node.store.allow_mmap: false
    ---
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRole
    metadata:
      name: elastic-agent
    rules:
    - apiGroups: [""] # "" indicates the core API group
      resources:
      - pods
      - nodes
      - namespaces
      verbs:
      - get
      - watch
      - list
    - apiGroups: ["coordination.k8s.io"]
      resources:
      - leases
      verbs:
      - get
      - create
      - update
    - apiGroups: ["apps"]
      resources:
      - replicasets
      verbs:
      - list
      - watch
    - apiGroups: ["batch"]
      resources:
      - jobs
      verbs:
      - list
      - watch
    ---
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: elastic-agent
      namespace: default
    ---
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRoleBinding
    metadata:
      name: elastic-agent
    subjects:
    - kind: ServiceAccount
      name: elastic-agent
      namespace: default
    roleRef:
      kind: ClusterRole
      name: elastic-agent
      apiGroup: rbac.authorization.k8s.io
    EOF
    ```

    1. The root user is required to persist state in a hostPath volume and to trust the {{es}} CA in {{fleet}} mode. See [Storing local state in host path volume](configuration-examples-standalone.md#k8s_storing_local_state_in_host_path_volume) for options to not run the Agent container as root.


    Check [Configuration Examples](configuration-examples-fleet.md) for more ready-to-use manifests.


ECK automatically configures secure connections between all components. {{fleet}} will be set up, and all agents are enrolled in the default policy.

1. Monitor the status of {{fleet-server}} and {{agent}}.

    ```sh
    kubectl get agent
    ```

    ```sh subs=true
    NAME                       HEALTH   AVAILABLE   EXPECTED   VERSION      AGE
    elastic-agent-quickstart   green    3           3          {{version.stack}}    14s
    fleet-server-quickstart    green    1           1          {{version.stack}}    19s
    ```

2. List all the Pods belonging to a given {{agent}} specification.

    ```sh
    kubectl get pods --selector='agent.k8s.elastic.co/name=elastic-agent-quickstart'
    ```

    ```sh
    NAME                                   READY   STATUS    RESTARTS   AGE
    elastic-agent-quickstart-agent-t49fd   1/1     Running   0          54s
    elastic-agent-quickstart-agent-xbcxr   1/1     Running   0          54s
    elastic-agent-quickstart-agent-zqp55   1/1     Running   0          54s
    ```

3. Access logs for one of the Pods.

    ```sh
    kubectl logs -f elastic-agent-quickstart-agent-xbcxr
    ```

4. Configure the policy used by {{agents}}. Check [{{agent}} policies](/reference/fleet/agent-policy.md) for more details.

