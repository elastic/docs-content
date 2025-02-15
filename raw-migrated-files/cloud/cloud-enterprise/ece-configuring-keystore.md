# Secure your settings [ece-configuring-keystore]

Some of the settings that you configure in Elastic Cloud Enterprise are sensitive, such as passwords, and relying on file system permissions to protect these settings is insufficient. To protect your sensitive settings, use the Elasticsearch keystore. With the Elasticsearch keystore, you can add a key and its secret value, then use the key in place of the secret value when you configure your sensitive settings.

There are three types of secrets that you can use:

* **Single string** - Associate a secret value to a setting.
* **Multiple strings** - Associate multiple keys to multiple secret values.
* **JSON block/file** - Associate multiple keys to multiple secret values in JSON format.


## Add secret values [ece-add-secret-values] 

Add keys and secret values to the keystore.

1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the deployments page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From your deployment menu, select **Security**.
4. Locate **Elasticsearch keystore** and select **Add settings**.
5. On the **Create setting** window, select the secret **Type**.
6. Configure the settings, then select **Save**.
7. All the modifications to the non-reloadable keystore take effect only after restarting Elasticsearch. Reloadable keystore changes take effect after issuing a [reload_secure_settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-reload-secure-settings) API request.

::::{important} 
Only some settings are designed to be read from the keystore. However, the keystore has no validation to block unsupported settings. Adding unsupported settings to the keystore causes [reload_secure_settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-reload-secure-settings) to fail and if not addressed, Elasticsearch will fail to start. To check whether a setting is supported in the keystore, look for a "Secure" qualifier in the [setting reference](../../../deploy-manage/security/secure-settings.md).
::::



## Delete secret values [ece-delete-keystore] 

When your keys and secret values are no longer needed, delete them from the keystore.

1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the deployments page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From your deployment menu, select **Security**.
4. From the **Existing keystores** list, use the delete icon next to the **Setting Name** that you want to delete.
5. On the **Confirm to delete** window, select **Confirm**.
6. All modifications to the non-reloadable keystore take effect only after restarting Elasticsearch. Reloadable keystore changes take effect after issuing a [reload_secure_settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-reload-secure-settings) API request.

