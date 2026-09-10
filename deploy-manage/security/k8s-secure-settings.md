---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-kibana-secure-settings.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-es-secure-settings.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Secure settings on ECK

With the help of ECK operator, you can specify {{es}} and {{kib}} [secure settings](/deploy-manage/security/secure-settings.md) to your deployments through [Kubernetes secrets](https://kubernetes.io/docs/concepts/configuration/secret/).

The secrets should contain a key-value pair for each secure setting you want to add. ECK watches the referenced secrets for changes and delivers them to your {{es}} or {{kib}} Pods. By default, each update triggers a rolling restart of the affected Pods to repopulate the keystore.

You also can opt in to [updating secure settings without a restart](#k8s-es-secure-settings-hot-reload).

## {{es}} secure settings [k8s-es-secure-settings]

Reference one or more Kubernetes secrets from `spec.secureSettings` so ECK can inject secure settings into your {{es}} Pods. You can [add secrets to the resource](#k8s_basic_usage), [map secret keys to keystore setting names](#k8s_projection_of_secret_keys_to_specific_paths), and [update secure settings without a rolling restart](#k8s-es-secure-settings-hot-reload).

### Reference secrets in the Elasticsearch resource [k8s_basic_usage]

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

### Project secret keys to specific paths [k8s_projection_of_secret_keys_to_specific_paths]

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

### Update secure settings without a restart [k8s-es-secure-settings-hot-reload]
```{applies_to}
deployment:
  eck: ga 3.5+
```

By default, every change to a `spec.secureSettings` source secret triggers a rolling restart of the {{es}} cluster because the keystore init container must re-run to repopulate the keystore. For {{es}} 9.5 and later, ECK supports an opt-in file-based delivery mechanism that eliminates this restart: secrets are written into the {{es}} file-based settings path and {{es}} reloads them in place when the file changes.

To enable file-based delivery, add the following annotation to your {{es}} resource:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
  annotations:
    eck.k8s.elastic.co/file-based-secure-settings: "true"
spec:
  version: {{version.stack}}
  nodeSets:
  - name: default
    count: 3
  secureSettings:
  - secretName: s3-credentials
```

When the annotation is set and the cluster is running {{es}} 9.5+, ECK delivers all `spec.secureSettings` entries through {{es}} file-based settings instead of the keystore init container. Updating a source secret no longer triggers a rolling restart. Instead, {{es}} applies the updated credentials in place on each node. Note that enabling or disabling the annotation itself causes a one-time rolling restart, because it changes the Pod template by adding or removing the keystore init container.

When the annotation is absent or the cluster is running {{es}} earlier than 9.5, the existing keystore init container path is used unchanged.

::::{important}
Only use this annotation when all entries in `spec.secureSettings` are [reloadable settings](/deploy-manage/security/secure-settings.md#reloadable-secure-settings). Settings that must be present in the keystore at startup, such as OIDC `client_secret`, SAML key passphrases, and `xpack.watcher.encryption_key`, will cause {{es}} to fail to start if the keystore is absent.
::::

## {{kib}} secure settings [k8s-kibana-secure-settings]

Similar to {{es}} secure settings, you can use Kubernetes secrets to manage keystore settings for {{kib}}.

For example, you can provide your own encryption key for {{kib}} as follows:

1. Create a secret containing the desired setting:

    ```yaml
    kubectl create secret generic kibana-secret-settings \
     --from-literal=xpack.security.encryptionKey=94d2263b1ead716ae228277049f19975aff864fb4fcfe419c95123c1e90938cd
    ```

    :::{warning}
    Always ensure the setting is listed in the [{{kib}} configuration reference](kibana://reference/configuration-reference.md) and that the value you provide matches the expected format before adding it to the keystore. Specifying invalid, unsupported, or incorrect settings will prevent {{kib}} from starting successfully.
    :::

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

:::{admonition} {{kib}} encryption settings
ECK automatically generates values for the following settings:

* [`xpack.security.encryptionKey`](kibana://reference/configuration-reference/security-settings.md#xpack-security-encryptionkey)
* [`xpack.reporting.encryptionKey`](kibana://reference/configuration-reference/reporting-settings.md#encryption-keys)
* [`xpack.encryptedSavedObjects.encryptionKey`](/deploy-manage/security/secure-saved-objects.md)

You can override these generated values by providing your own encryption keys through secure settings.

For more details about multi-instance requirements, retrieving generated keys, and key rotation, refer to [{{kib}} encryption keys on ECK](/deploy-manage/deploy/cloud-on-k8s/k8s-kibana-advanced-configuration.md#k8s-kibana-encryption-keys).
:::

## More examples [k8s_more_examples]

Check [How to create automated snapshots](/deploy-manage/tools/snapshot-and-restore/cloud-on-k8s.md) for an example use case that illustrates how secure settings can be used to set up automated {{es}} snapshots to a GCS storage bucket.
