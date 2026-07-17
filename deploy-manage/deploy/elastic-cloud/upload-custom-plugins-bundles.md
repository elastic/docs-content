---
navigation_title: Custom plugins and bundles
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-custom-bundles.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-custom-bundles.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Upload custom plugins and bundles

::::{note}
This page applies to {{ech}} deployments only. {{serverless-full}} projects do not support custom plugin or bundle uploads, including dictionary files used for synonyms, stop words, or [language analyzers](elasticsearch://reference/text-analysis/analysis-lang-analyzer.md).

If you use {{serverless-short}} and need to manage synonyms, use the [synonyms APIs]({{es-serverless-apis}}group/endpoint-synonyms) or refer to [Search with synonyms](/solutions/search/full-text/search-with-synonyms.md). For how {{ech}} and Serverless differ on plugins, bundles, and dictionary options, see [Compare {{ech}} and Serverless](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md#elasticsearch-differences-custom-plugins-and-bundles).
::::

There are several cases where you might need your own files to be made available to your {{es}} cluster’s nodes:

* Your own custom plugins, or third-party plugins that are not amongst the [officially available plugins](/deploy-manage/deploy/elastic-cloud/add-plugins-provided-with-ech.md).
* Custom dictionaries, such as synonyms, stop words, compound words, and so on.
* Cluster configuration files, such as an Identity Provider metadata file used when you [secure your clusters with SAML](../../../deploy-manage/users-roles/cluster-or-deployment-auth/saml.md).

To facilitate this, we make it possible to upload a ZIP file that contains the files you want to make available. Uploaded files are stored using Amazon’s highly-available S3 service. This is necessary so we do not have to rely on the availability of third-party services, such as the official plugin repository, when provisioning nodes.

Custom plugins and bundles are collectively referred to as extensions.

## Before you begin [ec_before_you_begin_7]

The selected plugins/bundles are downloaded and provided when a node starts. Changing a plugin does not change it for nodes already running it. Refer to [Replace an extension](#ec-update-bundles-and-plugins).

With great power comes great responsibility: your plugins can extend your deployment with new functionality, but also break it. Be careful. We obviously cannot guarantee that your custom code works.

::::{important}
You cannot edit or delete a custom extension after it has been used in a deployment. To remove it from your deployment, you can disable the extension and update your deployment configuration.
::::


Uploaded files cannot be bigger than 20MB for most subscription levels, for Platinum and Enterprise the limit is 8GB.

It is important that plugins and dictionaries that you reference in mappings and configurations are available at all times. For example, if you try to upgrade {{es}} and de-select a dictionary that is referenced in your mapping, the new nodes will be unable to recover the cluster state and function. This is true even if the dictionary is referenced by an empty index you do not actually use.


## Prepare your files for upload [ec-prepare-custom-bundles]

Plugins are uploaded as ZIP files. You need to choose whether your uploaded file should be treated as a *plugin* or as a *bundle*. Bundles are not installed as plugins. If you need to upload both a custom plugin and custom dictionaries, upload them separately.

To prepare your files, create one of the following:

Plugins
:   A plugin is a ZIP file that contains a plugin descriptor file and binaries.

    The plugin descriptor file is called either `stable-plugin-descriptor.properties` for plugins built against the stable plugin API, or `plugin-descriptor.properties` for plugins built against the classic plugin API. A plugin ZIP file should only contain one plugin descriptor file.

    {{es}} assumes that the uploaded ZIP file contains binaries. If it finds any source code, it fails with an error message, causing provisioning to fail. Make sure you upload binaries, and not source code.

    ::::{note}
    Plugins larger than 5GB should have the plugin descriptor file at the top of the archive. This order can be achieved by specifying at time of creating the ZIP file:

    ```sh
    zip -r name-of-plugin.zip name-of-descriptor-file.properties *
    ```

    ::::


Bundles
:   The entire content of a bundle is made available to the node by extracting to the {{es}} container’s `/app/config` directory. This is useful to make custom dictionaries available. Dictionaries should be placed in a `/dictionaries` folder in the root path of your ZIP file.

    Here are some examples of bundles:

    **Script**

    ```text
    $ tree .
    .
    └── scripts
        └── test.js
    ```

    The script `test.js` can be referred in queries as `"script": "test"`.

    **Dictionary of synonyms**

    ```text
    $ tree .
    .
    └── dictionaries
        └── synonyms.txt
    ```

    The dictionary `synonyms.txt` can be used as `synonyms.txt` or using the full path `/app/config/synonyms.txt` in the `synonyms_path` of the `synonym-filter`.

    To learn more about analyzing with synonyms, check [Synonym token filter](elasticsearch://reference/text-analysis/analysis-synonym-tokenfilter.md) and [Formatting Synonyms](https://www.elastic.co/guide/en/elasticsearch/guide/2.x/synonym-formats.html).

    **GeoIP database bundle**

    ```text
    $ tree .
    .
    └── ingest-geoip
        └── MyGeoLite2-City.mmdb
    ```

    Note that the extension must be `-(City|Country|ASN).mmdb`, and it must be a different name than the original file name `GeoLite2-City.mmdb` which already exists in {{ech}}. To use this bundle, you can refer it in the GeoIP ingest pipeline as `MyGeoLite2-City.mmdb` under `database_file`.



## Add your extension [ec-add-your-plugin]

You must upload your files before you can apply them to your cluster configuration:

1. Log in to [{{ecloud}}](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From the navigation menu, select **Extensions**.
3. Click **Upload extension**.
4. Complete the extension fields, including the {{es}} version.

    * Plugins must use full version notation down to the patch level, such as `7.10.1`. You cannot use wildcards. This version notation should match the version in your plugin’s plugin descriptor file. For classic plugins, it should also match the target deployment version.
    * Bundles should specify major or minor versions with wildcards, such as `7.*` or `*`. Wildcards are recommended to ensure the bundle is compatible across all versions of these releases.
5. Click **Create extension**.

After creating your extension, you can [enable it on an existing {{es}} deployment](#ec-update-bundles) or enable it when creating new deployments.

::::{note}
Creating extensions larger than 200MB must be done through the API. Refer to [Upload an extension using the API](#ec-extension-api-usage-guide).
::::



## Enable extensions on a deployment [ec-update-bundles]

After uploading your files, you can enable them when creating a new {{es}} deployment. For existing deployments, enable them from the deployment edit page:

:::{include} _snippets/enable-extensions-on-deployment.md
:::


## Replace an extension [ec-update-bundles-and-plugins]

While you can update the ZIP file for any plugin or bundle, these are downloaded and made available only when a node is started.

If the extension is not in use by any deployments, you can update the files or extension details. However, if the extension is in use, and if you need to update it with a new file, it is recommended to [create a new extension](#ec-add-your-plugin) rather than updating the existing one that is in use.

By following this method, only the one node would be down even if the extension file is faulty. This would ensure that HA clusters remain available.

This method also supports having a test/staging deployment to test out the extension changes before applying them on a production deployment.

You may delete the old extension after updating the deployment successfully.

To replace an extension with a new file version:

1. Prepare a new plugin or bundle.
2. On the **Extensions** page, [upload a new extension](#ec-add-your-plugin).
3. Follow the steps in [Enable extensions on a deployment](#ec-update-bundles). On the **Extensions** tab, select the new extension and deselect the old one before you save.

### Considerations for updating an in-use extension

* Be careful when updating an extension. If you update an existing extension with a new file, and if the file is broken for any reason, all the nodes could be impacted, as either a restart or a move node could make even HA clusters non-available. Also, shards of your indices may become unassigned if there's anything wrong with the bundle, for example if a file referenced by an index is missing due to the update.
* If you need to update your extension, instead of updating an existing extension with a new file directly, create a new extension to test the behavior first, verify its validity, and then apply it to your deployment.

## Upload an extension using the API [ec-extension-api-usage-guide]

Use the extensions API to upload plugins and bundles programmatically. You must use the API for extensions larger than 200MB; the Cloud UI supports uploads up to that size. You must also use the API for automation or when your ZIP file is not reachable from a public URL in a single request.

Before you start, create an [{{ecloud}} API key](/deploy-manage/api-keys/elastic-cloud-api-keys.md). To manage extensions after upload, add them to a deployment, update metadata, or delete them. Refer to [Managing plugins and extensions through the API](manage-plugins-extensions-through-api.md). For the complete HTTP reference, see [Extensions API]({{cloud-apis}}group/endpoint-extensions).

### Upload from a local file [ec_method_1_use_http_post_to_create_metadata_and_then_upload_the_file_using_http_put]

Create the extension metadata first, then upload the ZIP file in a second request.

1. Create metadata:

```text
curl -XPOST \
-H "Authorization: ApiKey $EC_API_KEY" \
-H 'content-type:application/json' \
https://api.elastic-cloud.com/api/v1/deployments/extensions \
-d'{
  "name" : "synonyms-v1",
  "description" : "The best synonyms ever",
  "extension_type" : "bundle",
  "version" : "7.*"
}'
```

2.  Upload the file:

```text
curl -XPUT \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/deployments/extensions/$extension_id" \
-T /tmp/synonyms.zip
```

If you are using a client that does not have native `application/zip` handling like `curl`, be sure to use the equivalent of the following with `content-type: multipart/form-data`:

```text
curl -XPUT \
-H 'Expect:' \
-H 'content-type: multipart/form-data' \
-H "Authorization: ApiKey $EC_API_KEY" \
"https://api.elastic-cloud.com/api/v1/deployments/extensions/$extension_id" -F "file=@/tmp/synonyms.zip"
```

For example, using the Python `requests` module, the `PUT` request would be as follows:

```text
import requests
files = {'file': open('/tmp/synonyms.zip','rb')}
r = requests.put('https://api.elastic-cloud.com/api/v1/deployments/extensions/{}'.format(extension_id), files=files, headers= {'Authorization': 'ApiKey {}'.format(EC_API_KEY)})
```


### Upload from a download URL [ec_method_2_single_step_use_a_download_url_so_that_the_api_server_downloads_the_object_at_the_specified_url]

When your ZIP is hosted at a publicly accessible URL, create the extension in one request. {{ecloud}} downloads and validates the file from the URL you provide. This method is required for plugins larger than 200MB.

```text
curl -XPOST \
-H "Authorization: ApiKey $EC_API_KEY" \
-H 'content-type:application/json' \
https://api.elastic-cloud.com/api/v1/deployments/extensions \
-d'{
  "name" : "anylysis_icu",
  "description" : "Helpful description",
  "extension_type" : "plugin",
  "version" : "7.13.2",
  "download_url": "https://artifacts.elastic.co/downloads/elasticsearch-plugins/analysis-icu/analysis-icu-7.13.2.zip"
}'
```
