---
navigation_title: Deploy a {{kib}} instance
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-deploy-kibana.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Deploy a {{kib}} instance [k8s-deploy-kibana]

To deploy a simple {{kib}} specification, with one {{kib}} instance:

1. Specify a {{kib}} instance and associate it with your {{es}} `quickstart` cluster created previously under [Deploying an {{es}} cluster](elasticsearch-deployment-quickstart.md):

    ```yaml subs=true
    cat <<EOF | kubectl apply -f -
    apiVersion: kibana.k8s.elastic.co/v1
    kind: Kibana
    metadata:
      name: quickstart
    spec:
      version: {{version.stack}}
      count: 1
      elasticsearchRef:
        name: quickstart
    EOF
    ```

2. Monitor {{kib}} health and creation progress.

    Similar to {{es}}, you can retrieve details about {{kib}} instances with [`get`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/):

    ```sh
    kubectl get kibana
    ```

    And the associated Pods:

    ```sh
    kubectl get pod --selector='kibana.k8s.elastic.co/name=quickstart'
    ```

    {{kib}} will be status `available` once [`get`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/) reports `green`. If it experiences issues starting up, use [`logs`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_logs/) against the pod in order to make sure the {{kib}} server is [ready](/troubleshoot/kibana/error-server-not-ready.md).

3. Access {{kib}}.

    A `ClusterIP` Service is automatically created for {{kib}}:

    ```sh
    kubectl get service quickstart-kb-http
    ```

    Use `kubectl port-forward` to access {{kib}} from your local workstation:

    ```sh
    kubectl port-forward service/quickstart-kb-http 5601
    ```

    Open `https://localhost:5601` in your browser. Your browser will show a warning because the self-signed certificate configured by default is not verified by a known certificate authority and not trusted by your browser. You can temporarily acknowledge the warning for the purposes of this quick start but it is highly recommended that you [configure valid certificates](/deploy-manage/security/k8s-https-settings.md#k8s-setting-up-your-own-certificate) for any production deployments.

    Login as the `elastic` user. The password can be obtained with the following command:

    ```sh
    kubectl get secret quickstart-es-elastic-user -o=jsonpath='{.data.elastic}' | base64 --decode; echo
    ```


For a full description of each `CustomResourceDefinition` (CRD), refer to the [API reference](cloud-on-k8s://reference/api-docs.md) or view the CRD files in the [project repository](https://github.com/elastic/cloud-on-k8s/tree/{{version.eck | M.M}}/config/crds). You can also retrieve information about a CRD from the instance. For example, describe the {{kib}} CRD specification with [`describe`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_describe/):

```sh
kubectl describe crd kibana
```

## Next steps

This completes the quickstart of deploying an {{kib}} instance on top of [the ECK operator](install-using-yaml-manifest-quickstart.md) and [deployed {{es}} cluster](elasticsearch-deployment-quickstart.md).

We recommend continuing to:
* [Updating your deployment](update-deployments.md).
* For more {{kib}} configuration options, refer to [{{kib}} configuration on ECK](kibana-configuration.md) and [](./configure-deployments.md).


