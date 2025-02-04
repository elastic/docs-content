# Install {{kib}} [install]


## {{kib}} on Elastic Cloud [_kib_on_elastic_cloud] 

If you are using Elastic Cloud, you access Kibana with a single click. (You can [sign up for a free trial](https://cloud.elastic.co/registration?page=docs&placement=docs-body) and start exploring data in minutes.)


## Install {{kib}} yourself [_install_kib_yourself] 

::::{tip} 
For a step-by-step example of setting up the {{stack}} on your own premises, try out our tutorial: [Installing a self-managed Elastic Stack](../../../deploy-manage/deploy/self-managed/installing-elasticsearch.md).
::::


::::{note} 
Starting with version 6.0.0, Kibana only supports 64 bit operating systems.
::::


Kibana is provided in the following package formats:

`tar.gz`/`zip`
:   The `tar.gz` packages are provided for installation on Linux and Darwin and are the easiest choice for getting started with Kibana.

    The `zip` package is the only supported package for Windows.

    [Install from archive on Linux or macOS](../../../deploy-manage/deploy/self-managed/install-from-archive-on-linux-macos.md) or [Install on Windows](../../../deploy-manage/deploy/self-managed/install-on-windows.md)


`deb`
:   The `deb` package is suitable for Debian, Ubuntu, and other Debian-based systems.  Debian packages may be downloaded from the Elastic website or from our Debian repository.

    [Install with Debian package](../../../deploy-manage/deploy/self-managed/install-with-debian-package.md)


`rpm`
:   The `rpm` package is suitable for installation on Red Hat, SLES, OpenSuSE and other RPM-based systems.  RPMs may be downloaded from the Elastic website or from our RPM repository.

    [Install with RPM](../../../deploy-manage/deploy/self-managed/install-with-rpm.md)


`docker`
:   Images are available for running Kibana as a Docker container. They may be downloaded from the Elastic Docker Registry.

    [Running Kibana on Docker](../../../deploy-manage/deploy/self-managed/install-with-docker.md)


::::{important} 
If your Elasticsearch installation is protected by [{{stack-security-features}}](https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-security.html) see [Configuring security in {{kib}}](../../../deploy-manage/security.md) for additional setup instructions.
::::







