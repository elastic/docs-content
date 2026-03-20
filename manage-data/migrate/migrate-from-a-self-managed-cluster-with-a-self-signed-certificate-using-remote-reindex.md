---
navigation_title: Reindex using a private CA
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-remote-reindex.html
applies_to:
  serverless: unavailable
  deployment:
    ess: all
products:
  - id: cloud-hosted
---

# Reindex from a self-managed cluster using a private CA [ec-remote-reindex]

The following instructions explain how to configure remote reindex to {{ech}} from a self-managed cluster that uses non–publicly trusted TLS certificates, including self-signed certificates and certificates signed by a private certificate authority (CA).

Assume you have a self-managed source cluster named `Source` that uses TLS certificates which are not publicly trusted, and you want to migrate data from `Source` to a destination cluster on {{ech}}.

## Step 1: Prepare the `Source` CA to be used in an extension bundle [ec-remote-reindex-step1]

1. Obtain the CA of the `Source` cluster, or extract the certificate from the cluster by running the following command:

    ```text
    echo quit | openssl s_client -showcerts -servername "$SOURCE_SERVER_NAME" -connect "$SOURCE_SERVER:$PORT" > cacert.pem
    ```

2. Test `cecert.pem` you have just created with `curl`, this should return a successful response:

    ```text
    curl -XGET https://<SOURCE_SERVER>:<PORT> -u <username>:<password> --cacert cacert.pem
    ```

3. Create the folder `my_source_ca` to store the file `cacert.pem`, and compress the folder to `my_source_ca.zip`.

::::{note}
Both the folder and file names must correspond to the settings configured in [Step 4](#ec-remote-reindex-step4).
::::

## Step 2: Upload the zip bundle to your {{ecloud}} account [ec-remote-reindex-step2]

To upload your file, follow the steps in the section [Add your extension](../../deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md#ec-add-your-plugin). Enter wildcard `*` for **Version** in order to be compatible for all future upgrades, and select `A bundle containing dictionary or script` as **Type**.


## Step 3: Create a new {{ech}} deployment [ec-remote-reindex-step3]

From the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) create a new deployment. This will be the `Destination` cluster.

::::{note}
The `Destination` cluster should be the same or newer version as the `Source` cluster. If you already have a cluster available, you can skip this step.
::::


## Step 4: Enable the extension and add `reindex` settings on the `Destination` cluster [ec-remote-reindex-step4]

1. From your deployment page, go to the **Edit** page, click **Manage user settings and extensions**, select tab **Extensions** then enable `my_source_ca`.
2. Switch tab to **User settings**, append the following settings to the [`elasticsearch.yml`](/deploy-manage/stack-settings.md).  This step adds `source_server` to the `reindex.remote.whitelist`, points source CA bundle to be trusted by the `Destination` cluster using the setting `reindex.ssl.certificate_authorities`.

    ```text
    reindex.remote.whitelist: ["$SOURCE_SERVER:$PORT"]
    reindex.ssl.certificate_authorities: "/app/config/my_source_ca/cacert.pem"
    reindex.ssl.verification_mode: "full"
    ```

    ::::{note}
    Make sure `reindex.remote.whitelist` is in an array format.  All uploaded bundles will be uncompressed into `/app/config/` folder.  Ensure the file path corresponds to your uploaded bundle in [Step 1](#ec-remote-reindex-step1). You can optionally set `reindex.ssl.verification_mode` to `full`, `certificate` or `none` depending on the validity of hostname and the certificate path.  More details can be found in [reindex](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) setting.
    ::::

3. Click **Back** to the **Edit** page and scroll to the button of the page to **Save** changes.  This step will restart all Elasticsearch instances.


## Step 5: Reindex from remote `Source` cluster [ec-remote-reindex-step5]

You can now run a remote reindex operation on the {{ech}} `Destination` cluster from the `Source` cluster, as described in the [migration guide](/manage-data/migrate.md#ech-reindex-remote):

```text
POST _reindex
{
  "source": {
    "remote": {
      "host": "https://<SOURCE_SERVER>:<PORT>",
      "username": "username",
      "password": "xxx"
    },
    "index": "my_source_index"
  },
  "dest": {
    "index": "my_dest_index"
  }
}
```

::::{note}
If you have many sources to reindex, it’s is generally better to reindex them one at a time and run them in parallel rather than using a glob pattern to pick up multiple sources. Check [reindex from multiple sources](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) for more details.
::::
