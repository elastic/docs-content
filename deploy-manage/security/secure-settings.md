---
applies_to:
  deployment:
    ess: ga
    ece: ga
    eck: ga
    self: ga
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configuring-keystore.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-restful-api-examples-configuring-keystore.html
  - https://www.elastic.co/guide/en/cloud/current/ec-configuring-keystore.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-configuring-keystore.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-es-secure-settings.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/secure-settings.html
  - https://www.elastic.co/guide/en/kibana/current/secure-settings.html
---

# Secure your settings

$$$reloadable-secure-settings$$$

$$$ec-add-secret-values$$$

$$$change-password$$$

$$$creating-keystore$$$

Some settings are sensitive, and relying on filesystem permissions to protect their values is not sufficient. Depending on the settings you need to protect, you can use:

- [The {{es}} keystore](secure-settings.md#the-es-keystore) and the [`elasticsearch-keystore` tool](elasticsearch://reference/elasticsearch/command-line-tools/elasticsearch-keystore.md) to manage {{es}} settings.
- [The {{kib}} keystore](secure-settings.md#the-kib-keystore) and the `kibana-keystore` tool to manage {{kib}} settings.
- [Kubernetes secrets](secure-settings.md#kubernetes-secrets), if you are using {{eck}}.


:::{important} 
Only some settings are designed to be read from the keystore. However, the keystore has no validation to block unsupported settings. Adding unsupported settings to the keystore causes [reload_secure_settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-reload-secure-settings) to fail and if not addressed, {{es}} will fail to start. To check whether a setting is supported in the keystore, look for a "Secure" qualifier in the [setting reference](/reference/index.md).
:::

## The {{es}} keystore

With the {{es}} keystore, you can add a key and its secret value, then use the key in place of the secret value when you configure your sensitive settings.

:::::{tab-set}
:group: deployment-type

::::{tab-item} {{ecloud}}
:sync: cloud

There are three types of secrets that you can use:

* **Single string** - Associate a secret value to a setting.
* **Multiple strings** - Associate multiple keys to multiple secret values.
* **JSON block/file** - Associate multiple keys to multiple secret values in JSON format.


**Add secret values**

Add keys and secret values to the keystore.

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page in the **Hosted deployments** card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.

    On the **Deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. From your deployment menu, select **Security**.
4. Locate **{{es}} keystore** and select **Add settings**.
5. On the **Create setting** window, select the secret **Type**.
6. Configure the settings, then select **Save**.
7. All the modifications to the non-reloadable keystore take effect only after restarting {{es}}. Reloadable keystore changes take effect after issuing a [reload_secure_settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-reload-secure-settings) API request.


**Delete secret values**

When your keys and secret values are no longer needed, delete them from the keystore.

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page in the **Hosted deployments** card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.

    On the **Deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. From your deployment menu, select **Security**.
4. From the **Existing keystores** list, use the delete icon next to the **Setting Name** that you want to delete.
5. On the **Confirm to delete** window, select **Confirm**.
6. All modifications to the non-reloadable keystore take effect only after restarting {{es}}. Reloadable keystore changes take effect after issuing a [reload_secure_settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-reload-secure-settings) API request.

::::

::::{tab-item} {{ece}}
:sync: ece

There are three types of secrets that you can use:

* **Single string** - Associate a secret value to a setting.
* **Multiple strings** - Associate multiple keys to multiple secret values.
* **JSON block/file** - Associate multiple keys to multiple secret values in JSON format.


**Add secret values**

Add keys and secret values to the keystore.

1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From your deployment menu, select **Security**.
4. Locate **{{es}} keystore** and select **Add settings**.
5. On the **Create setting** window, select the secret **Type**.
6. Configure the settings, then select **Save**.
7. All the modifications to the non-reloadable keystore take effect only after restarting {{es}}. Reloadable keystore changes take effect after issuing a [reload_secure_settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-reload-secure-settings) API request.



**Delete secret values**

When your keys and secret values are no longer needed, delete them from the keystore.

1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From your deployment menu, select **Security**.
4. From the **Existing keystores** list, use the delete icon next to the **Setting Name** that you want to delete.
5. On the **Confirm to delete** window, select **Confirm**.
6. All modifications to the non-reloadable keystore take effect only after restarting {{es}}. Reloadable keystore changes take effect after issuing a [reload_secure_settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-reload-secure-settings) API request.

:::{dropdown} Using the API

**Steps**

Create the keystore:

```sh
curl -k -X PATCH -H "Authorization: ApiKey $ECE_API_KEY" https://$COORDINATOR_HOST:12443/api/v1/deployments/$DEPLOYMENT_ID/elasticsearch/$REF_ID/keystore \
{
  "secrets": {
    "s3.client.CLIENT_NAME.access_key": {
      "as_file": false
      "value": "ACCESS_KEY_VALUE"
    }
    "s3.client.CLIENT_NAME.secret_key": {
      "value": "SECRET_KEY_VALUE"
    }
  }
}
```

`ELASTICSEARCH_CLUSTER_ID`
:   The {{es}} cluster ID as shown in the Cloud UI or obtained through the API

List the keys defined in the keystore:

```sh
{
  "secrets": {
    "s3.client.CLIENT_NAME.access_key": {
      "as_file": false
    },
    "s3.client.CLIENT_NAME.secret_key": {
      "as_file": false
    }
  }
}
```

Create the credentials for an S3 or Minio repository:

```sh
curl -k -X PUT -H "Authorization: ApiKey $ECE_API_KEY" https://$COODINATOR_HOST:12443/api/v1/clusters/elasticsearch/$ELASTICSEARCH_CLUSTER_ID/_snapshot/s3-repo
{
  "type": "s3",
  "settings": {
    "bucket": "s3_REPOSITORY_NAME",
    "client": "CLIENT_NAME",
    "base_path": "PATH_NAME"
  }
}
```

Create the credentials for a GCS repository:

```sh
curl -k -X PUT -H "Authorization: ApiKey $ECE_API_KEY" https://$COORDINATOR_HOST:12443/api/v1/clusters/elasticsearch/ELASTICSEARCH_CLUSTER_ID/_snapshot/s3-repo
{
  "type": "gcs",
  "settings": {
    "bucket": "BUCKET_NAME",
    "base_path": "BASE_PATH_NAME",
    "client": "CLIENT_NAME"
  }
}
```

To use GCS snapshots, the cluster must have the `repository-gcs` plugin enabled.


Remove keys that are defined in the keystore:

```sh
curl -k -X PATCH -H "Authorization: ApiKey $ECE_API_KEY" https://$COORDINATOR_HOST:12443/api/v1/deployments/$DEPLOYMENT_ID/elasticsearch/$REF_ID/keystore \
{
  "secrets": {
    "KEY_TO_REMOVE": {}
  }
}
```


**Verify your credentials** 

If your credentials are invalid, an administrator can verify that they are correct by checking the `keystore` field in the cluster metadata.

If the credential values are correct, but do not work, the keystore file could be out of sync on one or more nodes. To sync the keystore file, update the value for the key by using the patch API to delete the key from keystore, then add it back again.

:::

::::

::::{tab-item} Self-managed
:sync: self-managed

All the modifications to the keystore take effect only after restarting {{es}}.

These settings, just like the regular ones in the `elasticsearch.yml` config file, need to be specified on each node in the cluster. Currently, all secure settings are node-specific settings that must have the same value on every node.


**Reloadable secure settings**

Just like the settings values in `elasticsearch.yml`, changes to the keystore contents are not automatically applied to the running {{es}} node. Re-reading settings requires a node restart. However, certain secure settings are marked as **reloadable**. Such settings can be re-read and applied on a running node.

You can define these settings before the node is started, or call the [Nodes reload secure settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-reload-secure-settings) after the settings are defined to apply them to a running node.

The values of all secure settings, **reloadable** or not, must be identical across all cluster nodes. After making the desired secure settings changes, using the `bin/elasticsearch-keystore add` command, call:

```console
POST _nodes/reload_secure_settings
{
  "secure_settings_password": "keystore-password" <1>
}
```

1. The password that the {{es}} keystore is encrypted with.


This API decrypts, re-reads the entire keystore and validates all settings on every cluster node, but only the **reloadable** secure settings are applied. Changes to other settings do not go into effect until the next restart. Once the call returns, the reload has been completed, meaning that all internal data structures dependent on these settings have been changed. Everything should look as if the settings had the new value from the start.

When changing multiple **reloadable** secure settings, modify all of them on each cluster node, then issue a [`reload_secure_settings`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-reload-secure-settings) call instead of reloading after each modification.

There are reloadable secure settings for:

* [The Azure repository plugin](/deploy-manage/tools/snapshot-and-restore/azure-repository.md)
* [The EC2 discovery plugin](elasticsearch://reference/elasticsearch-plugins/discovery-ec2-usage.md#_configuring_ec2_discovery)
* [The GCS repository plugin](/deploy-manage/tools/snapshot-and-restore/google-cloud-storage-repository.md)
* [The S3 repository plugin](/deploy-manage/tools/snapshot-and-restore/s3-repository.md)
* [Monitoring settings](elasticsearch://reference/elasticsearch/configuration-reference/monitoring-settings.md)
* [{{watcher}} settings](elasticsearch://reference/elasticsearch/configuration-reference/watcher-settings.md)
* [JWT realm](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-jwt-settings)
* [Active Directory realm](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-ad-settings)
* [LDAP realm](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-ldap-settings)
* [Remote cluster credentials for the API key based security model](/deploy-manage/remote-clusters/remote-clusters-settings.md#remote-cluster-credentials-setting)


::::

:::::

## The {{kib}} keystore
```{applies_to}
deployment:
  self: ga
```

Some settings are sensitive, and relying on filesystem permissions to protect their values is not sufficient. For this use case, {{kib}} provides a keystore, and the `kibana-keystore` tool to manage the settings in the keystore.

::::{note} 
* Run all commands as the user who runs {{kib}}.
* Any valid {{kib}} setting can be stored in the keystore securely. Unsupported, extraneous or invalid settings will cause {{kib}} to fail to start up.

::::

### Create the keystore [creating-keystore] 

To create the `kibana.keystore`, use the `create` command:

```sh
bin/kibana-keystore create
```

The file `kibana.keystore` will be created in the `config` directory defined by the environment variable `KBN_PATH_CONF`.

To create a password protected keystore use the `--password` flag.


### List settings in the keystore [list-settings] 

A list of the settings in the keystore is available with the `list` command:

```sh
bin/kibana-keystore list
```


### Add string settings [add-string-to-keystore] 

::::{note} 
Your input will be JSON-parsed to allow for object/array input configurations. To enforce string values, use "double quotes" around your input.
::::


Sensitive string settings, like authentication credentials for {{es}} can be added using the `add` command:

```sh
bin/kibana-keystore add the.setting.name.to.set
```

Once added to the keystore, these setting will be automatically applied to this instance of {{kib}} when started. For example if you do

```sh
bin/kibana-keystore add elasticsearch.username
```

you will be prompted to provide the value for elasticsearch.username. (Your input will show as asterisks.)

The tool will prompt for the value of the setting. To pass the value through stdin, use the `--stdin` flag:

```sh
cat /file/containing/setting/value | bin/kibana-keystore add the.setting.name.to.set --stdin
```


### Remove settings [remove-settings] 

To remove a setting from the keystore, use the `remove` command:

```sh
bin/kibana-keystore remove the.setting.name.to.remove
```


### Read settings [read-settings] 

To display the configured setting values, use the `show` command:

```sh
bin/kibana-keystore show setting.key
```


### Change password [change-password] 

To change the password of the keystore, use the `passwd` command:

```sh
bin/kibana-keystore passwd
```


### Has password [has-password] 

To check if the keystore is password protected, use the `has-passwd` command. An exit code of 0 will be returned if the keystore is password protected, and the command will fail otherwise.

```sh
bin/kibana-keystore has-passwd
```

## Kubernetes secrets
```{applies_to}
deployment:
  eck: ga
```

You can specify [secure settings](/deploy-manage/security/secure-settings.md) with [Kubernetes secrets](https://kubernetes.io/docs/concepts/configuration/secret/). The secrets should contain a key-value pair for each secure setting you want to add. ECK automatically injects these settings into the keystore on each {{es}} node before it starts {{es}}. The ECK operator continues to watch the secrets for changes and will update the {{es}} keystore when it detects a change.

### Basic usage [k8s_basic_usage]

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


### More examples [k8s_more_examples]

Check [How to create automated snapshots](/deploy-manage/tools/snapshot-and-restore/cloud-on-k8s.md) for an example use case that illustrates how secure settings can be used to set up automated {{es}} snapshots to a GCS storage bucket.


