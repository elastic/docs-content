# Install ECE offline [ece-install-offline]

Installing ECE on hosts without internet access is commonly referred to as an *offline* or *air-gapped installation*. Before you start, you must:

* Download the Elasticsearch and Kibana images and installation script from Elastic and load them on your hosts, or push them to your private Docker registry. You need to download both the Elastic Stack pack and the Docker images for the same version.

    ```
    The versioning of Elasticsearch and Kibana is synchronized and versions where the major, minor, and patch levels match can be used together. Differences in build versions indicated by a dash do not affect compatibility.
    ```

* Be part of the `docker` group to run the installation script. You should not install Elastic Cloud Enterprise as the `root` user.
* Set up your [wildcard DNS record](../../../deploy-manage/deploy/cloud-enterprise/ece-wildcard-dns.md).
* Set up and run a local copy of the Elastic Package Repository, otherwise your deployments with APM server and Elastic agent won’t work. Refer to the [Running EPR in airgapped environments](https://www.elastic.co/guide/en/fleet/current/air-gapped.html#air-gapped-diy-epr) documentation.
* Deployment End-of-life (EOL) information relies on the connection to [https://www.elastic.co/support/eol.json](https://www.elastic.co/support/eol.json). If EOL information is updated, Elastic may require you to reconnect to [https://www.elastic.co/support/eol.json](https://www.elastic.co/support/eol.json) over the Internet to get this information reflected.

When you are ready to install ECE, you can proceed:

* [With your private Docker registry](../../../deploy-manage/deploy/cloud-enterprise/ece-install-offline-with-registry.md)
* [Without your private Docker registry](../../../deploy-manage/deploy/cloud-enterprise/ece-install-offline-no-registry.md)




