---
navigation_title: Add custom bundles and plugins
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-add-custom-bundle-plugin.html
applies_to:
  deployment:
    ece:
products:
  - id: cloud-enterprise
---

# Add custom bundles and plugins to your deployment [ece-add-custom-bundle-plugin]

ECE allows you to add custom plugins or external files as bundled ZIP files to your {{es}} instances. These ZIP files must be referenced through an HTTP or HTTPS URL.

::::{important}
* When referencing plugins or bundles, URLs using `https` with a certificate signed by an internal Certificate Authority (CA) are **not supported**. Either use a publicly trusted certificate, or fall back to the `http` scheme.
* Avoid using the same URL to serve newer versions of a plugin or bundle, as this may cause different nodes within the same cluster to run different plugin versions. Whenever you update the content of the bundle or plugin, use a new URL in the deployment configuration as well.
* If the URL becomes unreachable (if the URL changes at remote end, or connectivity to the remote web server has issues) you might encounter boot loops if {{es}} instances are restarted.
::::

Follow these steps to configure custom bundles and plugins to your {{es}} clusters, making them available to all {{es}} instances:

* Update your {{es}} cluster using the [advanced configuration editor](../../../deploy-manage/deploy/cloud-enterprise/advanced-cluster-configuration.md):
  * For bundles, modify the `resources.elasticsearch.plan.elasticsearch.user_bundles` JSON attribute.
  * For plugins, modify the `resources.elasticsearch.plan.elasticsearch.user_plugins` JSON attribute.

Here are some examples of custom bundles you can add:

- [Custom plugin](#ece-add-custom-plugin)
- [LDAP bundles](#ece-add-custom-bundle-example-LDAP)
- [SAML bundles](#ece-add-custom-bundle-example-SAML)
- [JVM truststore cacerts](#ece-add-custom-bundle-example-cacerts)
- [GeoIP database bundle](#ece-add-custom-bundle-example-geoip)
- [Synonym bundles](#ece-add-custom-bundle-example-synonyms)

## Add custom plugins to your deployment [ece-add-custom-plugin]

Custom plugins can include the official {{es}} plugins not provided with {{ece}}, any of the community-sourced plugins, or plugins that you write yourself.

1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. In the left side navigation select **Edit** from your deployment menu, then go to the bottom of the page and select [**Advanced Edit**](../../../deploy-manage/deploy/cloud-enterprise/advanced-cluster-configuration.md).
4. Within the **Deployment configuration** JSON find the section:

    `resources` > `elasticsearch` > `plan` > `elasticsearch`

    If there is an existing `user_plugins` section, then add the new plugin there, otherwise add a `user_plugins` section.

    ```sh
    {
    ...
      "resources": {
        "elasticsearch": [
         ...
            "plan": {
             ...
              "elasticsearch": {
                ...
                "user_bundles": [
                {
                    ....
                } ] ,
                "user_plugins": [
                  {
                    "url" : "<some static non_expirable url>", <1>
                    "name" : "plugin_name",
                    "elasticsearch_version" : "<es_version>" <2>
                  },
                  {
                    "url": "<MY_HOST_URL>/my-custom-plugin.zip",
                    "name": "my-custom-plugin",
                    "elasticsearch_version": "7.17.1"
                  }
                ]
              }
    ```
    1. The URL for the plugin must be always available. Make sure you host the plugin artifacts internally in a highly available environment. The URL must use the scheme `http` or `https`
    2. The version must match exactly your {{es}} version, such as `7.17.1`. Wildcards (*) are not allowed.

5. Save your changes.
6. To verify that all nodes have the plugins installed, use one of these commands: `GET /_nodes/plugins?filter_path=nodes.*.plugins` or `GET _cat/plugins?v`


## Example: Custom LDAP bundle [ece-add-custom-bundle-example-LDAP]

This example adds a custom LDAP bundle for deployment level role-based access control (RBAC). To set platform level RBAC, check [](../../../deploy-manage/users-roles/cloud-enterprise-orchestrator/manage-users-roles.md).

1. Prepare a custom bundle as a ZIP file that contains your keystore file with the private key and certificate inside of a `truststore` folder [in the same way that you would on {{ecloud}}](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md). This bundle allows all {{es}} containers to access the same keystore file through your `ssl.truststore` settings.
2. In the [advanced configuration editor](../../../deploy-manage/deploy/cloud-enterprise/advanced-cluster-configuration.md), update your new {{es}} cluster with the custom bundle you have just created. Modify the `user_bundles` JSON attribute of **each** {{es}} instance type as shown in the following example:

    ```sh
    {
    ...
      "resources": {
        "elasticsearch": [
         ...
            "plan": {
             ...
              "elasticsearch": {
                ...
                "user_bundles": [
                {
                  "name": "ldap-cert",
                  "url": "<MY_HOST_URL>/ldapcert.zip", <1>
                  "elasticsearch_version": "*"
                }
              ]
            }
            ...
    ```

    1. The URLs for the bundle ZIP files (`ldapcert.zip`) must be always available. Make sure you host the plugin artifacts internally in a highly available environment.

3. Custom bundles are unzipped in `/app/config/BUNDLE_DIRECTORY_STRUCTURE`, where `BUNDLE_DIRECTORY_STRUCTURE` is the directory structure within the bundle ZIP file itself. These file locations are needed in the next step.

    ```sh
    $ tree .
    .
    └── truststore
          └── keystore.ks
    ```

    In this example, the unzipped keystore file gets placed under `/app/config/truststore/keystore.ks`.

## Example: Custom SAML bundle [ece-add-custom-bundle-example-SAML]

This example adds a custom SAML bundle for deployment level role-based access control (RBAC). To set platform level RBAC, check [](../../../deploy-manage/users-roles/cloud-enterprise-orchestrator/manage-users-roles.md).

In this example, we assume the Identity Provider does not publish its SAML metadata at an HTTP URL, so we provide it through a custom bundle.

1. Prepare a ZIP file with a custom bundle that contains your Identity Provider’s metadata (`metadata.xml`). Place the file inside a `saml` folder within the ZIP (`saml/metadata.xml`).

    This bundle will allow all {{es}} containers to access the metadata file.

2. In the [advanced configuration editor](../../../deploy-manage/deploy/cloud-enterprise/advanced-cluster-configuration.md), update your {{es}} cluster configuration with the bundle you prepared in the previous step. Modify the `user_bundles` JSON attribute of **each** {{es}} instance type as shown in the following example:

    ```text
    {
    ...
      "resources": {
        "elasticsearch": [
          ...
            "plan": {
              ...
              "elasticsearch": {
                ...
                "user_bundles": [
                {
                  "name": "saml-metadata",
                  "url": "<MY_HOST_URL>/saml-metadata.zip", <1>
                  "elasticsearch_version": "*"
                }
              ]
            }
            ...
    ```

    1. The URL for the bundle ZIP file must be always available. Make sure you host the plugin artifacts internally in a highly available environment.

    Custom bundles are unzipped in `/app/config/BUNDLE_DIRECTORY_STRUCTURE`, where `BUNDLE_DIRECTORY_STRUCTURE` is the directory structure within the ZIP file itself. These file locations are needed in the next step.

    In this example, the SAML metadata file is located in the path `/app/config/saml/metadata.xml`:

    ```sh
    $ tree .
    .
    └── saml
          └── metadata.xml
    ```

3. Adjust your `saml` realm configuration accordingly through [](./edit-stack-settings.md):

    ```sh
        idp.metadata.path: /app/config/saml/metadata.xml <1>
    ```

    1. The path to the SAML metadata file that was uploaded

    Refer to [](../../users-roles/cluster-or-deployment-auth/saml.md) for more details on SAML authentication.

## Example: Custom JVM trust store bundle [ece-add-custom-bundle-example-cacerts]

If you are using SSL certificates signed by non-public certificate authorities, {{es}} is not able to communicate with the services using those certificates unless you import a custom JVM trust store containing the certificates of your signing authority into your {{ece}} installation. You’ll need the trust store to access snapshot repositories like MinIO, for your {{ece}} proxy, or to reindex from remote.

To import a JVM trust store:

1. Prepare the custom JVM trust store:

    1. Pull the certificate from the service you want to make accessible:

        ```sh
          openssl s_client -connect <server using the certificate> -showcerts <1>
        ```

        1. The server address (name and port number) of the service that you want {{es}} to be able to access. This command prints the entire certificate chain to `stdout`. You can choose a certificate at any level to be added to the trust store.

    2. Save it to a file with as a PEM extension.
    3. Locate your JRE’s default trust store, and copy it to the current directory:

        ```sh
          cp <default trust store location> cacerts <1>
        ```

        1. Default JVM trust store is typically located in `$JAVA_HOME/jre/libs/security/cacerts`


        ::::{tip}
        Default trust store contains certificates of many well known root authorities that are trusted by default. If you only want to include a limited list of CAs to trust, skip this step, and simply import specific certificates you want to trust into an empty store as shown next
        ::::

    4. Use keytool command from your JRE to import certificate(s) into the keystore:

        ```sh
        $JAVA_HOME/bin/keytool -keystore cacerts -storepass changeit -noprompt -importcert -file <certificate>.pem -alias <some alias> <1>
        ```

        1. The file where you saved the certificate to import, and an alias you assign to it, that is descriptive of the origin of the certificate


        ::::{important}
        We recommend that you keep file name and password for the trust store as JVM defaults (`cacerts` and `changeit` respectively). If you need to use different values, you need to add extra configuration, as detailed later in this document, in addition to adding the bundle.
        ::::

        You can have multiple certificates to the trust store, repeating the same command. There is only one JVM trust store per cluster currently supported. You cannot, for example, add multiple bundles with different JVM trust stores to the same cluster, they will not get merged. Add all certificates to be trusted to the same trust store

2. Create the bundle:

    ```sh
     zip cacerts.zip cacerts <1>
    ```
    1. The name of the zip archive is not significant


    ::::{tip}
    A bundle may contain other contents beyond the trust store if you prefer, but we recommend creating separate bundles for different purposes.
    ::::

3. In the [advanced configuration editor](../../../deploy-manage/deploy/cloud-enterprise/advanced-cluster-configuration.md), update your {{es}} cluster configuration with the bundle you prepared in the previous step. Modify the `user_bundles` JSON attribute of **each** {{es}} instance type as shown in the following example:

    ```sh
    {
    ...
      "resources": {
        "elasticsearch": [
         ...
            "plan": {
             ...
              "elasticsearch": {
                ...
                "user_bundles": [
                {
                  "name": "custom-ca-certs",
                  "url": "<MY_HOST_URL>/cacerts.zip", <1>
                  "elasticsearch_version": "*" <2>
                }
              ]
            }
        ...
    ```
    1. The URL for the bundle ZIP file must be always available. Make sure you host the plugin artefacts internally in a highly available environment.
    2. Wildcards are allowed here, since the certificates are independent from the {{es}} version.

4. (Optional) If you prefer to use a different file name and/or password for the trust store, you also need to add an additional configuration section to the cluster metadata before adding the bundle. This configuration should be added to the `Elasticsearch cluster data` section of the [advanced configuration](./advanced-cluster-configuration.md) page:

    ```sh
      "jvm_trust_store": {
        "name": "<filename included into bundle>", <1>
        "password": "<password used to create keystore>" <2>
      }
    ```
    1. The name of the trust store must match the filename included into the archive
    2. Password used to create the trust store

    ::::{important}
    * Use only alphanumeric characters, dashes, and underscores in both file name and password.
    * You do not need to do this step if you are using default filename and password (`cacerts` and `changeit` respectively) in your bundle.
    ::::

## Example: Custom GeoIP database bundle [ece-add-custom-bundle-example-geoip]

1. Prepare a ZIP file with a custom bundle that contains a: [GeoLite2 database](https://dev.maxmind.com/geoip/geoip2/geolite2). The folder has to be named `ingest-geoip`, and the file name can be anything that is appended `-(City|Country|ASN)` with the `mmdb` file extension, and it must have a different name than the original name `GeoLite2-City.mmdb`.

    The file `my-geoip-file.zip` should look like this:

    ```sh
    $ tree .
    .
    └── ingest-geoip
        └── MyGeoLite2-City.mmdb
    ```

2. Copy the ZIP file to a webserver that is reachable from any allocator in your environment.
3. In the [advanced configuration editor](../../../deploy-manage/deploy/cloud-enterprise/advanced-cluster-configuration.md), update your {{es}} cluster configuration with the bundle you prepared in the previous step. Modify the `user_bundles` JSON attribute of **each** {{es}} instance type as shown in the following example.

    ```sh
    {
    ...
      "resources": {
        "elasticsearch": [
         ...
            "plan": {
             ...
              "elasticsearch": {
                ...
                "user_bundles": [
                {
                  "name": "custom-geoip-db",
                  "url": "<MY_HOST_URL>/my-geoip-file.zip",
                  "elasticsearch_version": "*"
                }
              ]
            }
    ```

4. To use this bundle, you can refer it in the [GeoIP processor](elasticsearch://reference/enrich-processor/geoip-processor.md) of an ingest pipeline as `MyGeoLite2-City.mmdb` under `database_file` such as:

    ```sh
    ...
    {
      "geoip": {
        "field": ...
        "database_file": "MyGeoLite2-City.mmdb",
        ...
      }
    }
    ...
    ```

## Example: Custom synonyms bundle [ece-add-custom-bundle-example-synonyms]

1. Prepare a ZIP file with a custom bundle that contains a dictionary of synonyms in a text file.

    The file `synonyms.zip` should look like this:

    ```sh
    $ tree .
    .
    └── dictionaries
        └── synonyms.txt
    ```

2. Copy the ZIP file to a webserver that is reachable from any allocator in your environment.
3. In the [advanced configuration editor](../../../deploy-manage/deploy/cloud-enterprise/advanced-cluster-configuration.md), update your {{es}} cluster configuration with the bundle you prepared in the previous step. Modify the `user_bundles` JSON attribute of **each** {{es}} instance type as shown in the following example.

    ```sh
    {
    ...
      "resources": {
        "elasticsearch": [
         ...
            "plan": {
             ...
              "elasticsearch": {
                ...
                "user_bundles": [
                {
                  "name": "custom-synonyms",
                  "url": "<MY_HOST_URL>/synonyms.zip",
                  "elasticsearch_version": "*"
                }
              ]
            }
    ```

