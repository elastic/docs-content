---
navigation_title: Strong identity verification
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Strong identity verification on {{ech}}

Starting with {{stack}} 9.3, the [API key security model](./security-models.md) for remote cluster connections supports [strong identity verification](./security-models.md#remote-cluster-strong-verification). This adds an extra layer of security by allowing an API key to be used only by requests that present an allowed certificate identity, which the remote cluster validates during authentication.

::::{note}
This document explains how to enable strong identity verification for {{ech}} deployments. Use it as a companion to the standard remote cluster setup procedure: follow the steps to [configure remote clusters](./ec-enable-ccs.md#set-up-remote-clusters-with-ech) with API key authentication, and apply the settings in this guide. Some settings are independent, and others are marked with "When..." to indicate where they fit into the standard steps.
::::

## Prerequisites

Both the local and remote clusters must run {{stack}} 9.3 or later to use strong identity verification.

## Configure strong identity verification

To use strong identity verification, both the local and remote clusters must be configured to sign and verify cross-cluster request headers. All settings described in this guide are dynamic and can be configured using the [cluster settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) or as static [`elasticsearch.yml` configuration](/deploy-manage/stack-settings.md#configure-stack-settings) settings.

For a full list of available strong identity verification settings for remote clusters, refer to the [remote cluster settings reference](elasticsearch://reference/elasticsearch/configuration-reference/remote-clusters.md#remote-cluster-signing-settings).

### On the local cluster

When adding the remote cluster to the local cluster, you must configure it to sign cross-cluster requests with a TLS certificate–private key pair. You can either generate and use your own certificate for this purpose or reuse an existing certificate.

This example configures the local cluster to use the existing transport certificates to sign cross-cluster requests. These certificate files are present in all {{ecloud}} deployments:

```yaml
cluster.remote.<my_remote_cluster>.signing.certificate: "node.crt" <1>
cluster.remote.<my_remote_cluster>.signing.key: "node.key" <1>
```
1. Replace `<my_remote_cluster>` with your remote cluster alias.

If you use your own certificates, upload the certificate and key files [as a ZIP bundle](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md) and reference them in the settings:

```yaml
cluster.remote.<my_remote_cluster>.signing.certificate: "/app/config/<bundle-zip-directory>/<signing-cert.crt>" <1>
cluster.remote.<my_remote_cluster>.signing.key: "/app/config/<bundle-zip-directory>/<signing-key.key>" <1>
```
1. Replace `<my_remote_cluster>` with your remote cluster alias, and the paths with the paths to your certificate and key files included in the bundle.

### On the remote cluster

The certificate and key used by the local cluster to sign cross-cluster requests determine how the remote cluster must be configured. Specifically:

1. Add the certificate authority (CA) that issued the local cluster certificate to the `cluster.remote.signing.certificate_authorities` setting of the remote cluster:

  ```yaml
  cluster.remote.signing.certificate_authorities: "internal_tls_ca.crt" <1>
  ```
  1. This example uses the regional CA certificate file that is available in all {{ecloud}} deployments. This CA is unique per {{ecloud}} region and cloud provider.

  The CA file to configure depends on how the local cluster is set up:

  * If the local cluster uses the default transport certificates, and both the local and remote clusters belong to the same cloud provided and region on {{ecloud}}, you can use the `internal_tls_ca.crt` file that already exist in your cluster. No additional upload is required.

  * If the local cluster uses the default transport certificates, but the remote cluster belongs to a different {{ecloud}} provider or region, you must download the local cluster transport CA and upload it to the remote deployment as a bundle. To do that:
    1. Open your deployment management page in the Elastic Cloud UI and go to **Security**.
    1. Under **CA certificates**, select the download icon to save the CA into a local file.
    1. Add the CA certificate [as a ZIP bundle](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md) in your remote deployment, and reference the file in the `cluster.remote.signing.certificate_authorities` setting.

  * If you use custom certificates in the local cluster, upload the associated CA to the remote cluster [as a ZIP bundle](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md), and reference the file in the `cluster.remote.signing.certificate_authorities` setting.

1. When creating the cross-cluster API key on the remote cluster, you must specify a `certificate_identity` pattern that matches the Distinguished Name (DN) of the certificate used by the local cluster.

  :::{tip}
  In {{ecloud}}, the certificates of all {{es}} nodes follow this Distinguished Name (DN) format:  
  `CN=<node_id>.node.<cluster_id>.cluster.<scope_id>`.

  * The {{es}} `cluster_id` of your deployment can be found on the deployment page in the {{ecloud}} UI by selecting **Copy cluster ID**.  
  * The `scope_id` corresponds to the {{ecloud}} organization ID.
  :::

  This example creates a cross-cluster API key with a `certificate_identity` pattern that matches the default {{ecloud}} transport certificates for a specific `cluster_id`:

  ```console
  POST /_security/cross_cluster/api_key
  {
    "name": "my-cross-cluster-api-key",
    "access": {
      "search": [
        {
          "names": ["logs-*"]
        }
      ]
    },
    "certificate_identity": "CN=.*.node.<cluster-id>.cluster.*" <1>
  }
  ```
  1. If the local cluster uses custom certificates, adjust the pattern to match their DN instead.

  The `certificate_identity` field supports regular expressions that are matched against the certificate DN. For example:

  * `"CN=.*.example.com,O=Example Corp,C=US"` matches any certificate whose DN starts with a CN that ends in `example.com` and includes `O=Example Corp,C=US`.
  * `"CN=local-cluster.*,O=Example Corp,C=US"` matches any certificate whose DN starts with `CN=local-cluster` and includes `O=Example Corp,C=US`.
  * `"CN=.*.node.<cluster-id>.cluster.*"` matches the {{ecloud}} transport certificates for a given `cluster_id`.
  * `"CN=.*.node.*.cluster.<org-id>"` matches the {{ecloud}} transport certificates for all clusters in a given ECH organization.
