---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/encrypting-data.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Encrypting sensitive data in Watcher [encrypting-data]

Watches might have access to sensitive data such as HTTP basic authentication information or details about your SMTP email service. You can encrypt this data by generating a key and adding some secure settings on each node in your cluster.

Every `password` field that is used in your watch within an HTTP basic authentication block - for example within a webhook, an HTTP input or when using the reporting email attachment - will not be stored as plain text anymore. Also be aware, that there is no way to configure your own fields in a watch to be encrypted.

To encrypt sensitive data in {{watcher}}:

1. Use the [elasticsearch-syskeygen](elasticsearch://reference/elasticsearch/command-line-tools/syskeygen.md) command to create a system key file.
2. Copy the `system_key` file to all of the nodes in your cluster.
   ::::{important}
   The system key is a symmetric key, so the same key must be used on every node in the cluster.
   ::::

3. Set the [`xpack.watcher.encrypt_sensitive_data` setting](elasticsearch://reference/elasticsearch/configuration-reference/watcher-settings.md):

    ```sh
    xpack.watcher.encrypt_sensitive_data: true
    ```

4. Set the [`xpack.watcher.encryption_key` setting](elasticsearch://reference/elasticsearch/configuration-reference/watcher-settings.md) in the [{{es}} keystore](../../../deploy-manage/security/secure-settings.md) on each node in the cluster.

    For example, run the following command to import the `system_key` file on each node:

    ```sh
    bin/elasticsearch-keystore add-file xpack.watcher.encryption_key <filepath>/system_key
    ```

5. Delete the `system_key` file on each node in the cluster.

::::{note}
Existing watches are not affected by these changes. Only watches that you create after following these steps have encryption enabled.
::::
