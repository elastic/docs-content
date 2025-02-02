---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-enterprise-search-quickstart.html
---

# Quickstart [k8s-enterprise-search-quickstart]

1. Apply the following specification to deploy Enterprise Search. ECK automatically configures the secured connection to an Elasticsearch cluster named `quickstart`, created in [Elasticsearch quickstart](deploy-an-orchestrator.md).

    ```yaml
    cat <<EOF | kubectl apply -f -
    apiVersion: enterprisesearch.k8s.elastic.co/v1
    kind: EnterpriseSearch
    metadata:
      name: enterprise-search-quickstart
    spec:
      version: 8.16.1
      count: 1
      elasticsearchRef:
        name: quickstart
    EOF
    ```

    ::::{note}
    Workplace Search in versions 7.7 up to and including 7.8 required an Enterprise license on ECK. You can start with a 30-day [trial license](../../license/manage-your-license-in-eck.md).
    ::::

2. Monitor the Enterprise Search deployment.

    Retrieve details about the Enterprise Search deployment:

    ```sh
    kubectl get enterprisesearch
    ```

    ```sh
    NAME                            HEALTH    NODES    VERSION   AGE
    enterprise-search-quickstart    green     1        8.16.1      8m
    ```

    List all the Pods belonging to a given deployment:

    ```sh
    kubectl get pods --selector='enterprisesearch.k8s.elastic.co/name=enterprise-search-quickstart'
    ```

    ```sh
    NAME                                                READY   STATUS    RESTARTS   AGE
    enterprise-search-quickstart-ent-58b84db85-dl7c6    1/1     Running   0          2m50s
    ```

3. Access logs for that Pod:

    ```sh
    kubectl logs -f enterprise-search-quickstart-ent-58b84db85-dl7c6
    ```

4. Access Enterprise Search.

    A ClusterIP Service is automatically created for the deployment, and can be used to access the Enterprise Search API from within the Kubernetes cluster:

    ```sh
    kubectl get service enterprise-search-quickstart-ent-http
    ```

    Use `kubectl port-forward` to access Enterprise Search from your local workstation:

    ```sh
    kubectl port-forward service/enterprise-search-quickstart-ent-http 3002
    ```

    Open `https://localhost:3002` in your browser.

    ::::{note}
    Your browser will show a warning because the self-signed certificate configured by default is not verified by a known certificate authority and not trusted by your browser. Acknowledge the warning for the purposes of this quickstart, but for a production deployment we recommend [configuring valid certificates](configuration-enterprise-search.md#k8s-enterprise-search-expose).
    ::::


    Login as the `elastic` user created [with the Elasticsearch cluster](deploy-an-orchestrator.md). Its password can be obtained with:

    ```sh
    kubectl get secret quickstart-es-elastic-user -o=jsonpath='{.data.elastic}' | base64 --decode; echo
    ```

5. Access the Enterprise Search UI in Kibana.

    Starting with version 7.14.0, the Enterprise Search UI is accessible in Kibana.

    Apply the following specification to deploy Kibana, configured to connect to both Elasticsearch and Enterprise Search:

    ```yaml
    cat <<EOF | kubectl apply -f -
    apiVersion: kibana.k8s.elastic.co/v1
    kind: Kibana
    metadata:
      name: quickstart
    spec:
      version: 8.16.1
      count: 1
      elasticsearchRef:
        name: quickstart
      enterpriseSearchRef:
        name: enterprise-search-quickstart
    EOF
    ```

    Use `kubectl port-forward` to access Kibana from your local workstation:

    ```sh
    kubectl port-forward service/quickstart-kb-http 5601
    ```

    Open `https://localhost:5601` in your browser and navigate to the Enterprise Search UI.
