---
navigation_title: Update TLS certificates
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/update-node-certs.html
applies_to:
  deployment:
    self: all
products:
  - id: elasticsearch
---

# Update TLS certificates [update-node-certs]

This guide explains how to update TLS certificates in your cluster, the scenarios that require updates, and how to update certificate files and apply the changes.

## When to update [update-node-certs-when]

You might need to update your TLS certificates in the following scenarios:

* **You are adding new nodes to your secured cluster.** In this case, you need to generate certificates for the new nodes, preferably using the same Certificate Authority (CA).

* **A security breach has broken the trust of your certificate chain.** This situation usually requires generating new certificates signed by a new CA.

* **Your current node certificates will expire soon.** In this case, you need to generate new certificates for all nodes, using the same CA if it remains valid, or a new CA if the current one is also expiring.
  
  Use the [SSL certificate](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ssl-certificates) API to check when your certificates are expiring.

  ```console
  GET _ssl/certificates
  ```

  ::::{tip}
  You can check your certificate's expiration date using third party tool [OpenSSL](https://wiki.openssl.org/index.php/Command_Line_Utilities):

  ```bash
  openssl x509 -in /path/to/your/certificate.crt -noout -enddate
  ```
  ::::
  
## Update certficate files [update-node-certs-update]

Before updating certificates, you will need to determine which scenario applies to your Certificate Authority (CA):

* Same CA: You have the original certificate and key that you used to sign the existing nodes' certificates and you still trust it. You can [use it to sign the new certificates](same-ca.md).

* Different CA: You need to generate a new or update trust to a different Certificate Authority. You can [sign node certificates with your new CA](different-ca.md).

Depending on which certificates you determine need addressed, you might need to update the certificates for the [transport layer](https://www.elastic.co/docs/deploy-manage/security/set-up-basic-security), the [HTTP layer](https://www.elastic.co/docs/deploy-manage/security/set-up-basic-security-plus-https), or both. 

If you determine you need to generate new certificates, then you might accomplish this by:

* reaching out to your IT team for organizationally approved certificates
* using the [elasticsearch-certutil](https://www.elastic.co/docs/reference/elasticsearch/command-line-tools/certutil)

## Apply updated certificates [update-node-certs-apply]

To apply the new certificates to your cluster, either update the configuration on each node and perform a [rolling restart](../maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-rolling) of the cluster, or update the certificate files in place and allow {{es}} to automatically reload them.

### (Recommended) Rolling restart [use-rolling-restarts]

You must complete a rolling restart if you modify any of the following:

* the [`elasticsearch.yml`](/deploy-manage/stack-settings.md) configuration
* passwords for the certificate keys 
* passwords stored in the [keystore secure settings](secure-settings.md) 

### Automatically apply keystore [update-node-certs-apply-keystore]

To do an in-place update, copy the new certificate and key files (or keystore) into the {{es}} [configuration directory](/deploy-manage/deploy/self-managed/configure-elasticsearch.md). To use this method you must use the same file names. {{es}} monitors the SSL resources for updates on a five-second interval and will automatically detect changes and reload the keys and certificates. 

::::{note}
While it’s possible to do an in-place update for security certificates, using a [rolling restart](../maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-rolling) on your cluster is safer and recommended. An in-place update avoids some complications of a rolling restart, but incurs the following risks:

* If you use PEM files, your certificate and key are in separate files. You must update both files *simultaneously* or the node might experience a temporary period where it cannot establish new connections.
* Updating the certificate and key does not automatically force existing connections to refresh. This means that even if you make a mistake, a node can seem like it’s functioning but only because it still has existing connections. It’s possible that a node will be unable to connect with other nodes, rendering it unable to recover from a network outage or node restart.
::::
