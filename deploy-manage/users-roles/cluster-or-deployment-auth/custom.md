---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/custom-realms.html
applies_to:
  deployment:
  stack: all
products:
  - id: elasticsearch
---

# Custom realms

If you are using an authentication system that is not supported out-of-the-box by the {{es}} {{security-features}}, you can create a custom realm to interact with it to authenticate users. You implement a custom realm as an SPI loaded security extension as part of an ordinary elasticsearch plugin.

## Implementing a custom realm [implementing-custom-realm]

Sample code that illustrates the structure and implementation of a custom realm is provided [in the `elasticsearch` repository](https://github.com/elastic/elasticsearch/tree/master/x-pack/qa/security-example-spi-extension) on GitHub. You can use this code as a starting point for creating your own realm.

To create a custom realm, you need to do the following:

1. Extend `org.elasticsearch.xpack.security.authc.Realm` to communicate with your authentication system to authenticate users.
2. Implement the `org.elasticsearch.xpack.security.authc.Realm.Factory` interface in a class that will be used to create the custom realm.
3. Extend `org.elasticsearch.xpack.security.authc.DefaultAuthenticationFailureHandler` to handle authentication failures when using your custom realm.

To package your custom realm as a plugin:

1. Implement an extension class for your realm that extends `org.elasticsearch.xpack.core.security.SecurityExtension`. There you need to override one or more of the following methods:

    ```java
    @Override
    public Map<String, Factory> getRealms() {
        ...
    }
    ```

    The `getRealms` method is used to provide a map of type names to the `Factory` that will be used to create the realm.

    ```java
    @Override
    public AuthenticationFailureHandler getAuthenticationFailureHandler() {
        ...
    }
    ```

    The `getAuthenticationFailureHandler` method is used to optionally provide a custom `AuthenticationFailureHandler`, which will control how the {{es}} {{security-features}} respond in certain authentication failure events.

    ```java
    @Override
    public List<String> getSettingsFilter() {
        ...
    }
    ```

    The `Plugin#getSettingsFilter` method returns a list of setting names that should be filtered from the settings APIs as they may contain sensitive credentials. Note this method is not part of the `SecurityExtension` interface, it’s available as part of the elasticsearch plugin main class.

2. Create a build configuration file for the plugin; Gradle is our recommendation.
3. Create a `META-INF/services/org.elasticsearch.xpack.core.security.SecurityExtension` descriptor file for the extension that contains the fully qualified class name of your `org.elasticsearch.xpack.core.security.SecurityExtension` implementation
4. Bundle all in a single zip file.


## Using a custom realm to authenticate users [using-custom-realm]

To use a custom realm:

1. Install the realm extension on each node in the cluster. 
   
   * If you're using a self-managed cluster, then run `bin/elasticsearch-plugin` with the `install` sub-command and specify the URL pointing to the zip file that contains the extension. For example:

        ```shell
        bin/elasticsearch-plugin install file:///<path>/my-realm-1.0.zip
        ```
    * If you're using {{ech}}, then refer to [](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md).
    * If you're using {{ece}}, then refer to [](/deploy-manage/deploy/cloud-enterprise/add-custom-bundles-plugins.md).
    * If you're using {{eck}}, then refer to [](/deploy-manage/deploy/cloud-on-k8s/custom-configuration-files-plugins.md).


2. Add a realm configuration of the appropriate realm type to [`elasticsearch.yml`](/deploy-manage/stack-settings.md) under the `xpack.security.authc.realms` namespace. You must define your realm within the namespace that matches the type defined by the extension. The options you can set depend on the settings exposed by the custom realm. At a minimum, you must explicitly set the `order` attribute to control the order in which the realms are consulted during authentication. You must also make sure each configured realm has a distinct `order` setting. In the event that two or more realms have the same `order`, the node will fail to start.

    ::::{important} 
    When you configure realms in `elasticsearch.yml`, only the realms you specify are used for authentication. If you also want to use the `native` or `file` realms, you must include them in the realm chain.
    ::::

3. Restart {{es}}.


