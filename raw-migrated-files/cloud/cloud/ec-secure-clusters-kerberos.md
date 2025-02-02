# Secure your clusters with Kerberos [ec-secure-clusters-kerberos]

You can secure your Elasticsearch clusters and Kibana instances in a deployment by using the Kerberos-5 protocol to authenticate users.


## Before you begin [ec_before_you_begin_13]

The steps in this section require an understanding of Kerberos. To learn more about Kerberos, check our documentation on [configuring Elasticsearch for Kerberos authentication](https://www.elastic.co/guide/en/elasticsearch/reference/current/kerberos-realm.html).


## Configure the cluster to use Kerberos [ec-configure-kerberos-settings]

With a custom bundle containing the Kerberos files and changes to the cluster configuration, you can enforce user authentication through the Kerberos protocol.

1. Create or use an existing deployment that includes a Kibana instance.
2. Create a [custom bundle](../../../deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md) that contains your `krb5.conf` and `keytab` files, and add it to your cluster.

    ::::{tip}
    You should use these exact filenames for Elasticsearch Service to recognize the file in the bundle.
    ::::

3. Edit your cluster configuration, sometimes also referred to as the deployment plan, to define Kerberos settings as described in [Elasticsearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/kerberos-realm.html).

    ```sh
    xpack.security.authc.realms.kerberos.cloud-krb:
       order: 2
       keytab.path: es.keytab
       remove_realm_name: false
    ```

    ::::{important}
    The name of the realm must be `cloud-krb`, and the order must be 2: `xpack.security.authc.realms.kerberos.cloud-krb.order: 2`
    ::::

4. Update Kibana in the [user settings configuration](../../../deploy-manage/deploy/elastic-cloud/edit-stack-settings.md) to use Kerberos as the authentication provider:

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

