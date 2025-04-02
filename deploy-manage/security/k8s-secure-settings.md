---
applies_to:
  deployment:
    eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-kibana-secure-settings.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-es-secure-settings.html
---

# Secure settings on ECK

With the help of ECK operator, you can specify {{es}} and {{kib}} [secure settings](/deploy-manage/security/secure-settings.md) to your deployments through [Kubernetes secrets](https://kubernetes.io/docs/concepts/configuration/secret/).

The secrets should contain a key-value pair for each secure setting you want to add. ECK automatically injects these settings into the keystore on each {{es}} or {{kib}} Pod before it starts. The ECK operator continues to watch the secrets for changes and will update the {{es}} or {{kib}} keystores when it detects a change.

To allow the operator to inject the settings into the application, you must reference your secrets in the `spec.secureSettings` field of your {{es}} or {{kib}} object definition. Next, you’ll find examples for both {{es}} and {{kib}}.

## Elasticsearch basic usage [k8s_basic_usage]

It is possible to reference several secrets:

```yaml
spec:
  secureSettings:
  - secretName: one-secure-settings-secret
  - secretName: two-secure-settings-secret
```

For the following secret, a `gcs.client.default.credentials_file` key will be created in {{es}}’s keystore with the provided value:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: one-secure-settings-secret
type: Opaque
stringData:
  gcs.client.default.credentials_file: |
    {
      "type": "service_account",
      "project_id": "your-project-id",
      "private_key_id": "...",
      "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
      "client_email": "service-account-for-your-repository@your-project-id.iam.gserviceaccount.com",
      "client_id": "...",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://accounts.google.com/o/oauth2/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-bucket@your-project-id.iam.gserviceaccount.com"
    }
```

::::{tip}
Note that by default [Kubernetes secrets](https://kubernetes.io/docs/concepts/configuration/secret/) are expecting the value to be base64 encoded unless under a `stringData` field.
::::

### Projection of secret keys to specific paths [k8s_projection_of_secret_keys_to_specific_paths]

You can export a subset of secret keys and also project keys to specific paths using the `entries`, `key` and `path` fields:

```yaml
spec:
  secureSettings:
  - secretName: gcs-secure-settings
    entries:
    - key: gcs.client.default.credentials_file
    - key: gcs_client_1
      path: gcs.client.client_1.credentials_file
    - key: gcs_client_2
      path: gcs.client.client_2.credentials_file
```

For the three entries listed in the `gcs-secure-settings` secret, three keys are created in {{es}}’s keystore:

* `gcs.client.default.credentials_file`
* `gcs.client.client_1.credentials_file`
* `gcs.client.client_2.credentials_file`

The referenced `gcs-secure-settings` secret now looks like this:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: gcs-secure-settings
type: Opaque
stringData:
  gcs.client.default.credentials_file: |
    {
      "type": "service_account",
      "project_id": "project-id-to-be-used-for-default-client",
      "private_key_id": "private key ID for default-client",
      "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
      "client_email": "service-account-for-your-repository@your-project-id.iam.gserviceaccount.com",
      "client_id": "client ID for the default client",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://accounts.google.com/o/oauth2/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-bucket@your-project-id.iam.gserviceaccount.com"
    }
  gcs_client_1: |
    {
      "type": "service_account",
      "project_id": "project-id-to-be-used-for-gcs_client_1",
      "private_key_id": "private key ID for gcs_client_1",
      "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
      "client_email": "service-account-for-your-repository@your-project-id.iam.gserviceaccount.com",
      "client_id": "client ID for the gcs_client_1 client",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://accounts.google.com/o/oauth2/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-bucket@your-project-id.iam.gserviceaccount.com"
    }
  gcs_client_2: |
    {
      "type": "service_account",
      "project_id": "project-id-to-be-used-for-gcs_client_2",
      "private_key_id": "private key ID for gcs_client_2",
      "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
      "client_email": "service-account-for-your-repository@your-project-id.iam.gserviceaccount.com",
      "client_id": "client ID for the gcs_client_2 client",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://accounts.google.com/o/oauth2/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-bucket@your-project-id.iam.gserviceaccount.com"
    }
```

## Kibana secure settings [k8s-kibana-secure-settings]

Similar to {{es}} secure settings, you can use Kubernetes secrets to manage keystore settings for {{kib}}.

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

## More examples [k8s_more_examples]

Check [How to create automated snapshots](/deploy-manage/tools/snapshot-and-restore/cloud-on-k8s.md) for an example use case that illustrates how secure settings can be used to set up automated {{es}} snapshots to a GCS storage bucket.
