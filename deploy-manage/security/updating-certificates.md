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

You might need to update your TLS certificates if your current node certificates expire soon, you’re adding new nodes to your secured cluster, or a security breach has broken the trust of your certificate chain. Use the [SSL certificate](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ssl-certificates) API to check when your certificates are expiring.

In instances where you have access to the original Certificate Authority (CA) key and certificate that you used to sign your existing node certificates (and where you can still trust your CA), you can [use that CA to sign the new certificates](same-ca.md).

If you have to trust a new CA from your organization, or you need to generate a new CA yourself, you need to use this new CA to sign the new node certificates and instruct your nodes to trust the new CA. In this case, you’ll [sign node certificates with your new CA](different-ca.md) and instruct your nodes to trust this certificate chain.

Depending on which certificates are expiring, you might need to update the certificates for the transport layer, the HTTP layer, or both.

Regardless of the scenario, {{es}} monitors the SSL resources for updates by default, on a five-second interval. You can just copy the new certificate and key files (or keystore) into the {{es}} configuration directory and your nodes will detect the changes and reload the keys and certificates.

Because {{es}} doesn’t reload the `elasticsearch.yml` configuration, you must use **the same file names** if you want to take advantage of automatic certificate and key reloading.

If you need to update the [`elasticsearch.yml`](/deploy-manage/stack-settings.md) configuration or change passwords for keys or keystores that are stored in the [secure settings](secure-settings.md), then you must complete a [rolling restart](#use-rolling-restarts). {{es}} will not automatically reload changes for passwords stored in the secure settings.

::::{admonition} Rolling restarts are preferred
:name: use-rolling-restarts

While it’s possible to do an in-place update for security certificates, using a [rolling restart](../maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-rolling) on your cluster is safer. An in-place update avoids some complications of a rolling restart, but incurs the following risks:

* If you use PEM files, your certificate and key are in separate files. You must update both files *simultaneously* or the node might experience a temporary period where it cannot establish new connections.
* Updating the certificate and key does not automatically force existing connections to refresh. This means that even if you make a mistake, a node can seem like it’s functioning but only because it still has existing connections. It’s possible that a node will be unable to connect with other nodes, rendering it unable to recover from a network outage or node restart.

::::




