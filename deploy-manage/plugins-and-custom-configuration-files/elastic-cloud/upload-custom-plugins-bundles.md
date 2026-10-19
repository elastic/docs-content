---
navigation_title: Custom plugins and bundles
description: Upload custom plugins and configuration bundles so every node in your Elastic Cloud Hosted deployment can use them.
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-custom-bundles.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-custom-bundles.html
applies_to:
  deployment:
    ech: ga
products:
  - id: cloud-hosted
---

# Upload custom plugins and bundles

Upload a ZIP file when you need a custom or third-party plugin that {{ech}} does not provide, or custom configuration files such as dictionaries and SAML metadata. In the {{ecloud}} console and API, these uploads are *extensions*.

Uploaded files are stored in highly available object storage so {{ecloud}} does not depend on third-party services, such as a public plugin repository, when provisioning nodes.

## Before you begin [ec_before_you_begin_7]

Before you upload your first custom plugin or bundle, review the following considerations:

* The selected plugins and bundles are downloaded and provided when a node starts. Changing a plugin does not change it for nodes already running it. Refer to [Replace an extension](#ec-update-bundles-and-plugins).

* Custom plugins can add capabilities to your deployment, but they can also cause failures. Elastic does not guarantee that custom code will work correctly.

* You cannot edit or delete a custom extension after it has been used in a deployment. To remove it from your deployment, you can disable the extension and update your deployment configuration.

* Your extension file size limit depends on your subscription level. For Platinum and Enterprise subscriptions, the limit is 8GB. For all other subscription levels, the limit is 20MB.

* It is important that plugins and dictionaries that you reference in mappings and configurations are available at all times. For example, if you try to upgrade {{es}} and de-select a dictionary that is referenced in your mapping, the new nodes will be unable to recover the cluster state and function. This is true even if the dictionary is referenced by an empty index you do not actually use.


## Prepare your files for upload [ec-prepare-custom-bundles]

Plugins are uploaded as ZIP files. You need to choose whether your uploaded file should be treated as a *plugin* or as a *bundle*. Bundles are not installed as plugins. If you need to upload both a custom plugin and custom dictionaries, upload them separately.

To prepare your files, create one of the following:

Plugins
:   Use a plugin to add functionality to {{es}}: a custom or third-party plugin that {{ech}} does not provide, or one that you write yourself.

    :::{include} /deploy-manage/plugins-and-custom-configuration-files/_snippets/plugin-structure.md
    :::

    ::::{note}
    Plugins larger than 5GB should have the plugin descriptor file at the top of the archive. This order can be achieved by specifying at time of creating the ZIP file:

    ```sh
    zip -r name-of-plugin.zip name-of-descriptor-file.properties *
    ```

    ::::


Bundles
:   Use a bundle to make configuration files, such as custom dictionaries or SAML metadata, available to every node.

    :::{include} /deploy-manage/plugins-and-custom-configuration-files/_snippets/bundle-structure.md
    :::

    Dictionaries are the exception. Place them in a `/dictionaries` folder in the root path of your ZIP file, and their contents are extracted directly to `/app/config` rather than to an `/app/config/dictionaries` subfolder.

    Here are some examples of bundles:

    <!--
    A `scripts` bundle example was removed here. File scripts were removed from Elasticsearch
    in 6.0 (elastic/elasticsearch#24627) and ScriptType defines only INLINE and STORED, so
    `"script": "test"` can no longer resolve a file on disk. The Cloud runner still copies a
    `scripts` folder to /app/config/scripts, but Elasticsearch never reads it. Don't re-add
    the example; stored scripts use the _scripts API and are unrelated to bundles.
    -->

    **Dictionary of synonyms**

    ```text
    $ tree .
    .
    └── dictionaries
        └── synonyms.txt
    ```

    <!--
    The bare `synonyms.txt` path is correct, even though `synonyms_path` normally resolves
    relative to the config directory.
    Other folders such as `saml`, `truststore`, and `ingest-geoip` keep their folder name, so
    `dictionaries` is the only exception. Don't "correct" this to `dictionaries/synonyms.txt`.
    -->
    
    The dictionary `synonyms.txt` can be used as `synonyms.txt` or using the full path `/app/config/synonyms.txt` in the `synonyms_path` of the synonym token filter.

    To learn more about analyzing with synonyms, check [Synonym token filter](elasticsearch://reference/text-analysis/analysis-synonym-tokenfilter.md) and [Formatting Synonyms](https://www.elastic.co/guide/en/elasticsearch/guide/2.x/synonym-formats.html).

    <!--
    The "Formatting Synonyms" link points at the 2.x Definitive Guide, which is EOL and
    carries a "no longer updated" banner. It's kept only because it documents rule merging
    and greedy matching, which the current reference docs don't cover. The synonym formats
    themselves are already covered by the "Synonym token filter" link above, so this link
    becomes redundant once https://github.com/elastic/elasticsearch/issues/160145 is
    resolved. Remove it then. This is the last elastic.co/guide/ link in docs-content.
    -->

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
3. Click **Create extension**.
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

:::{include} /deploy-manage/deploy/elastic-cloud/_snippets/enable-extensions-on-deployment.md
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

Before you start, create an [{{ecloud}} API key](/deploy-manage/api-keys/elastic-cloud-api-keys.md). You can then create an extension in one of two ways:

* [Stream the file from a download URL](manage-plugins-extensions-through-api.md#ec-extension-guide-create-option1), in a single request. This method is required for plugins larger than 200MB.
* [Upload the file from a local file path](manage-plugins-extensions-through-api.md#ec-extension-guide-create-option2), by creating the extension metadata first and uploading the ZIP file in a second request.

To add an extension to a deployment, update its metadata, or delete it afterwards using the {{ecloud}} API, refer to [](manage-plugins-extensions-through-api.md). For the complete HTTP reference, see [Extensions API]({{cloud-apis}}group/endpoint-extensions).
