---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-connect-to-unmanaged-resources.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Connect to external Elastic resources [k8s-connect-to-unmanaged-resources]

Fields like `elasticsearchRef` or `kibanaRef` are useful to automatically establish connections between applications managed by the same ECK operator instance. It is however also possible to connect to applications managed by a different ECK operator instance, or to applications not managed by ECK, for example an {{ecloud}} deployment. This can be done by providing connection details and credentials in a `Secret` through the `secretName` attribute:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: external-es-ref
stringData:
  url: <ELASTIC_CLOUD_URL>
  username: "elastic"
  password: REDACTED
---
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: kibana-sample
spec:
  version: 8.14.0
  count: 1
  elasticsearchRef:
    secretName: external-es-ref
```

In the case of Elastic Agent you can also specify several named references:

```yaml subs=true
apiVersion: v1
kind: Secret
metadata:
  name: external-es-ref
stringData:
  url: <ELASTIC-CLOUD-URL>:443
  username: ""
  password: ""
  api-key: REDACTED
  ca.crt: REDACTED

apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  elasticsearchRefs:
  - outputName: default
    secretName: external-es-ref
  - outputName: monitoring
    secretName: external-es-ref2
```

The following fields are expected to be set in the referenced `Secret`:

* `url` (required): URL to be used to access the external resource.
* `username` (required): The username of the user to be authenticated to the Elastic resource.
* `password` (required): The password for the provided user.
* `ca.crt` (optional): The certificate authority to be used to connect to the external resource.

In the case of Agent and Beats resources the following field can also be used to connect to {{es}}:

* `api-key`: An API key to authenticate against the Elastic resource.

::::{note} 
The operator must be able to connect to the external resources to check version compatibility.
::::


