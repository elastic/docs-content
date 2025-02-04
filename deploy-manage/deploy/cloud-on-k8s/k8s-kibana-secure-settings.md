---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-kibana-secure-settings.html
---

# Secure settings [k8s-kibana-secure-settings]

[Similar to {{es}}](../../security/secure-settings.md), you can use Kubernetes secrets to manage secure settings for {{kib}}.

For example, you can define a custom encryption key for {{kib}} as follows:

1. Create a secret containing the desired setting:

    ```yaml
    kubectl create secret generic kibana-secret-settings \
     --from-literal=xpack.security.encryptionKey=94d2263b1ead716ae228277049f19975aff864fb4fcfe419c95123c1e90938cd
    ```

2. Add a reference to the secret in the `secureSettings` section:

    ```yaml
    apiVersion: kibana.k8s.elastic.co/v1
    kind: Kibana
    metadata:
      name: kibana-sample
    spec:
      version: 8.16.1
      count: 3
      elasticsearchRef:
        name: "elasticsearch-sample"
      secureSettings:
      - secretName: kibana-secret-settings
    ```


