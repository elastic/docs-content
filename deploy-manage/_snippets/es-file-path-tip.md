:::{tip}
When configuring a file path in an {{es}} setting, keep in mind:
* In self-managed clusters, file path settings are resolved relative to the {{es}} config directory. {{es}} monitors this file for changes and reloads the configuration whenever it is updated.
* If you're using {{ech}} or {{ece}}, upload the file before referencing it in the configuration. For {{ech}}, upload it [as a custom bundle](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md). For {{ece}}, follow the equivalent [ECE procedure](/deploy-manage/deploy/cloud-enterprise/add-custom-bundles-plugins.md).
* If you're using {{eck}}, install the file as a [custom configuration file](/deploy-manage/deploy/cloud-on-k8s/custom-configuration-files-plugins.md#use-a-volume-and-volume-mount-together-with-a-configmap-or-secret).
:::
