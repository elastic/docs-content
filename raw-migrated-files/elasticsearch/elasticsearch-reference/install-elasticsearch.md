# Installing Elasticsearch [install-elasticsearch]


## {{ecloud}} [hosted-elasticsearch-service]

{{ecloud}} offers all of the features of {{es}}, {{kib}}, and  Elastic’s {{observability}}, and {{elastic-sec}} solutions as a hosted service available on AWS, GCP, and Azure.

To set up Elasticsearch in {{ecloud}}, sign up for a [free {{ecloud}} trial](https://cloud.elastic.co/registration?page=docs&placement=docs-body).


## Self-managed {{es}} options [elasticsearch-deployment-options]

If you want to install and manage {{es}} yourself, you can:

* Run {{es}} using a [Linux, MacOS, or Windows install package](../../../deploy-manage/deploy/self-managed/installing-elasticsearch.md#elasticsearch-install-packages).
* Run {{es}} in a [Docker container](../../../deploy-manage/deploy/self-managed/installing-elasticsearch.md#elasticsearch-docker-images).
* Set up and manage {{es}}, {{kib}}, {{agent}}, and the rest of the Elastic Stack on Kubernetes with [{{eck}}](https://www.elastic.co/guide/en/cloud-on-k8s/current).

::::{tip}
To try out Elasticsearch on your own machine, we recommend using Docker and running both Elasticsearch and Kibana. For more information, see [Run Elasticsearch locally](../../../solutions/search/get-started.md). Please note that this setup is **not suitable for production use**.
::::



## Elasticsearch install packages [elasticsearch-install-packages]

Elasticsearch is provided in the following package formats:

Linux and MacOS `tar.gz` archives
:   The `tar.gz` archives are available for installation on any Linux distribution and MacOS.

    [Install {{es}} from archive on Linux or MacOS](../../../deploy-manage/deploy/self-managed/install-elasticsearch-from-archive-on-linux-macos.md)


Windows `.zip` archive
:   The `zip` archive is suitable for installation on Windows.

    [Install {{es}} with `.zip` on Windows](../../../deploy-manage/deploy/self-managed/install-elasticsearch-with-zip-on-windows.md)


`deb`
:   The `deb` package is suitable for Debian, Ubuntu, and other Debian-based systems. Debian packages may be downloaded from the Elasticsearch website or from our Debian repository.

    [Install Elasticsearch with Debian Package](../../../deploy-manage/deploy/self-managed/install-elasticsearch-with-debian-package.md)


`rpm`
:   The `rpm` package is suitable for installation on Red Hat, Centos, SLES, OpenSuSE and other RPM-based systems. RPMs may be downloaded from the Elasticsearch website or from our RPM repository.

    [Install Elasticsearch with RPM](../../../deploy-manage/deploy/self-managed/install-elasticsearch-with-rpm.md)


::::{tip}
For a step-by-step example of setting up the {{stack}} on your own premises, try out our tutorial: [Installing a self-managed Elastic Stack](../../../deploy-manage/deploy/self-managed/installing-elasticsearch.md).
::::



## Elasticsearch container images [elasticsearch-docker-images]

You can also run {{es}} inside a container image.

`docker`
:   Docker container images may be downloaded from the Elastic Docker Registry.

    [Install {{es}} with Docker](../../../deploy-manage/deploy/self-managed/install-elasticsearch-with-docker.md)



## Java (JVM) Version [jvm-version]

{{es}} is built using Java, and includes a bundled version of [OpenJDK](https://openjdk.java.net) within each distribution. We strongly recommend using the bundled JVM in all installations of {{es}}.

The bundled JVM is treated the same as any other dependency of {{es}} in terms of support and maintenance. This means that Elastic takes responsibility for keeping it up to date, and reacts to security issues and bug reports as needed to address vulnerabilities and other bugs in {{es}}. Elastic’s support of the bundled JVM is subject to Elastic’s [support policy](https://www.elastic.co/support_policy) and [end-of-life schedule](https://www.elastic.co/support/eol) and is independent of the support policy and end-of-life schedule offered by the original supplier of the JVM. Elastic does not support using the bundled JVM for purposes other than running {{es}}.

::::{tip}
{{es}} uses only a subset of the features offered by the JVM. Bugs and security issues in the bundled JVM often relate to features that {{es}} does not use. Such issues do not apply to {{es}}. Elastic analyzes reports of security vulnerabilities in all its dependencies, including in the bundled JVM, and will issue an [Elastic Security Advisory](https://www.elastic.co/community/security) if such an advisory is needed.
::::


If you decide to run {{es}} using a version of Java that is different from the bundled one, prefer to use the latest release of a [LTS version of Java](https://www.oracle.com/technetwork/java/eol-135779.md) which is [listed in the support matrix](https://elastic.co/support/matrix). Although such a configuration is supported, if you encounter a security issue or other bug in your chosen JVM then Elastic may not be able to help unless the issue is also present in the bundled JVM. Instead, you must seek assistance directly from the supplier of your chosen JVM. You must also take responsibility for reacting to security and bug announcements from the supplier of your chosen JVM. {{es}} may not perform optimally if using a JVM other than the bundled one. {{es}} is closely coupled to certain OpenJDK-specific features, so it may not work correctly with JVMs that are not OpenJDK. {{es}} will refuse to start if you attempt to use a known-bad JVM version.

To use your own version of Java, set the `ES_JAVA_HOME` environment variable to the path to your own JVM installation. The bundled JVM is located within the `jdk` subdirectory of the {{es}} home directory. You may remove this directory if using your own JVM.


## JVM and Java agents [jvm-agents]

Don’t use third-party Java agents that attach to the JVM. These agents can reduce {{es}} performance, including freezing or crashing nodes.
