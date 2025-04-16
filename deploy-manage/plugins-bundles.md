---
applies_to:
  deployment:
    ece:
    eck:
    self:
    ess:
  serverless:
---

# Plugins and bundles

prob should just fix plugins section https://www.elastic.co/docs/reference/elasticsearch/plugins/plugin-management 

<!--
## cloud hosted
https://www.elastic.co/docs/deploy-manage/deploy/elastic-cloud/add-plugins-extensions
https://www.elastic.co/docs/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles
https://www.elastic.co/docs/deploy-manage/deploy/elastic-cloud/manage-plugins-extensions-through-api

## cloud enterprise
https://www.elastic.co/docs/deploy-manage/deploy/cloud-enterprise/add-plugins
https://www.elastic.co/docs/deploy-manage/deploy/cloud-enterprise/add-custom-bundles-plugins

## eck
https://www.elastic.co/docs/deploy-manage/deploy/cloud-on-k8s/custom-configuration-files-plugins
https://www.elastic.co/docs/deploy-manage/deploy/cloud-on-k8s/k8s-kibana-plugins

## self
https://www.elastic.co/docs/deploy-manage/deploy/self-managed/plugins
https://www.elastic.co/docs/reference/elasticsearch/plugins/installation
https://www.elastic.co/docs/reference/elasticsearch/plugins/plugin-management-custom-url
https://www.elastic.co/docs/reference/elasticsearch/plugins/installing-multiple-plugins
https://www.elastic.co/docs/reference/elasticsearch/plugins/mandatory-plugins
https://www.elastic.co/docs/reference/elasticsearch/plugins/listing-removing-updating
https://www.elastic.co/docs/reference/elasticsearch/plugins/_other_command_line_parameters
https://www.elastic.co/docs/reference/elasticsearch/plugins/_plugins_directory
https://www.elastic.co/docs/reference/elasticsearch/plugins/manage-plugins-using-configuration-file
https://www.elastic.co/docs/reference/elasticsearch/plugins/cloud/ec-custom-bundles
https://www.elastic.co/docs/reference/elasticsearch/plugins/cloud/ec-plugins-guide

## all
https://www.elastic.co/docs/reference/elasticsearch/plugins/plugin-management
-->

If you're using {{ece}} or {{ech}}, then you must [upload this file as a custom bundle](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md) before it can be referenced. If you're using {{eck}}, then install the file as a [custom configuration file](/deploy-manage/deploy/cloud-on-k8s/custom-configuration-files-plugins.md#use-a-volume-and-volume-mount-together-with-a-configmap-or-secret). If you're using a self-managed cluster, then the file must be present on each node.