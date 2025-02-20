# Secure your clusters with Kerberos [ece-secure-clusters-kerberos]

You can secure your Elasticsearch clusters and Kibana instances in a deployment by using the Kerberos-5 protocol to authenticate users.

::::{note}
The Kerberos credentials are valid against the deployment, not the ECE platform.
::::



## Before you begin [ece_before_you_begin_20]

The steps in this section require an understanding of Kerberos. To learn more about Kerberos, check our documentation on [configuring Elasticsearch for Kerberos authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/kerberos.md).


## Configure the cluster to use Kerberos [ece-configure-kerberos-settings]

With a custom bundle containing the Kerberos files and changes to the cluster configuration, you can enforce user authentication through the Kerberos protocol.

1. Create or use an existing deployment that includes a Kibana instance.
2. Create a [custom bundle](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch-plugins/cloud-enterprise/ece-add-plugins.md) that contains your `krb5.conf` and `keytab` files, and add it to your cluster.

    ::::{tip}
    You should use these exact filenames for Elastic Cloud Enterprise to recognize the file in the bundle.
    ::::

3. Edit your cluster configuration, sometimes also referred to as the deployment plan, to define Kerberos settings as described in [Elasticsearch documentation](/deploy-manage/users-roles/cluster-or-deployment-auth/kerberos.md).

    ```sh
    xpack.security.authc.realms.kerberos.cloud-krb:
       order: 2
       keytab.path: es.keytab
       remove_realm_name: false
    ```

4. Update Kibana in the [user settings configuration](../../../deploy-manage/deploy/cloud-enterprise/edit-stack-settings.md) to use Kerberos as the authentication provider:

    ```sh
    xpack.security.authc.providers:
      kerberos.kerberos1:
        order: 0
    ```

    This configuration disables all other realms and only allows users to authenticate with Kerberos. If you wish to allow your native realm users to authenticate, you need to also enable the `basic` `provider` like this:

    ```sh
    xpack.security.authc.providers:
      kerberos.kerberos1:
        order: 0
        description: "Log in with Kerberos" <1>
      basic.basic1:
        order: 1
    ```

    1. This arbitrary string defines how Kerberos login is titled in the Login Selector UI that is shown when you enable multiple authentication providers in Kibana. You can also configure the optional `icon` and `hint` settings for any authentication provider.

5. Use the Kibana endpoint URL to log in.

