# Secure your settings [ece-restful-api-examples-configuring-keystore]

Some of the settings that you configure in Elastic Cloud Enterprise are sensitive, and relying on file system permissions to protect these settings is insufficient. To protect your sensitive settings, such as passwords, you can use the Elasticsearch keystore.


## Before you begin [ece_before_you_begin_28]

To configure the keystore, you must meet the minimum criteria:

* To access the RESTful API for Elastic Cloud Enterprise, you must use your Elastic Cloud Enterprise credentials.

To learn more about the Elasticsearch keystore, refer to the [Elasticsearch documentation](/deploy-manage/security/secure-settings.md).


## Steps [ece_steps_9]

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
:   The Elasticsearch cluster ID as shown in the Cloud UI or obtained through the API

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

::::{tip}
To use GCS snapshots, the cluster must have the `repository-gcs` plugin enabled.
::::


Remove keys that are defined in the keystore:

```sh
curl -k -X PATCH -H "Authorization: ApiKey $ECE_API_KEY" https://$COORDINATOR_HOST:12443/api/v1/deployments/$DEPLOYMENT_ID/elasticsearch/$REF_ID/keystore \
{
  "secrets": {
    "KEY_TO_REMOVE": {}
  }
}
```


## Verify your credentials [ece_verify_your_credentials]

If your credentials are invalid, an administrator can verify that they are correct by checking the `keystore` field in the cluster metadata.

If the credential values are correct, but do not work, the keystore file could be out of sync on one or more nodes. To sync the keystore file, update the value for the key by using the patch API to delete the key from keystore, then add it back again.

