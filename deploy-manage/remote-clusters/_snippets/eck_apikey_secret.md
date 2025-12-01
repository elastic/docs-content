The following command creates a secret with the API key encoded value obtained in the previous step:

```sh
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: remote-api-keys
type: Opaque
stringData:
  cluster.remote.<remote-cluster-name>.credentials: <encoded value> <1>
EOF
```
1. For the `<remote-cluster-name>`, enter the alias of your choice. This alias is used when connecting to the remote cluster. It must be lowercase and only contain letters, numbers, dashes, and underscores.

