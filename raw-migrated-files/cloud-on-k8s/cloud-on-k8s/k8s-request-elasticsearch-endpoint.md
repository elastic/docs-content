# Access the Elasticsearch endpoint [k8s-request-elasticsearch-endpoint]

You can access the Elasticsearch endpoint within or outside the Kubernetes cluster.

**Within the Kubernetes cluster**

1. Retrieve the CA certificate.
2. Retrieve the password of the `elastic` user.

```sh
NAME=hulk

kubectl get secret "$NAME-es-http-certs-public" -o go-template='{{index .data "tls.crt" | base64decode }}' > tls.crt
PW=$(kubectl get secret "$NAME-es-elastic-user" -o go-template='{{.data.elastic | base64decode }}')

curl --cacert tls.crt -u elastic:$PW https://$NAME-es-http:9200/
```

**Outside the Kubernetes cluster**

1. Retrieve the CA certificate.
2. Retrieve the password of the `elastic` user.
3. Retrieve the IP of the `LoadBalancer` `Service`.

```sh
NAME=hulk

kubectl get secret "$NAME-es-http-certs-public" -o go-template='{{index .data "tls.crt" | base64decode }}' > tls.crt
IP=$(kubectl get svc "$NAME-es-http" -o jsonpath='{.status.loadBalancer.ingress[].ip}')
PW=$(kubectl get secret "$NAME-es-elastic-user" -o go-template='{{.data.elastic | base64decode }}')

curl --cacert tls.crt -u elastic:$PW https://$IP:9200/
```

