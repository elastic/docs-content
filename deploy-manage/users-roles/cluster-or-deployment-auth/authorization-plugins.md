---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/custom-roles-authorization.html
applies_to:
  stack: all
  serverless: unavailable
products:
  - id: elasticsearch
---

# Authorization plugins [custom-roles-authorization]

If you need to retrieve user roles from a system not supported out-of-the-box or if the authorization system that is provided by the {{es}} {{security-features}} does not meet your needs, a SPI loaded security extension can be implemented to customize role retrieval and/or the authorization system. The SPI loaded security extension is part of an ordinary elasticsearch plugin.

## Implementing a custom roles provider [implementing-custom-roles-provider]

To create a custom roles provider, you need to implement the interface `BiConsumer<Set<String>, ActionListener<Set<RoleDescriptor>>>`. The implementation consists of one method that takes a set of strings, which are the role names to resolve, and an `ActionListener`, on which the set of resolved role descriptors are passed on as the response.

Do not block on any I/O operations. It is the responsibility of the implementation to ensure asynchronous behavior and non-blocking calls, which is made easier by the fact that the `ActionListener` is provided on which to send the response when the roles have been resolved and the response is ready.

### Package a custom roles provider as a plugin [packaage-custom-roles-provider]

To package your custom roles provider as a plugin, implement an extension class for your roles provider that implements `org.elasticsearch.xpack.core.security.SecurityExtension`. There, you need to override one or more of the following methods:

```java
@Override
public List<BiConsumer<Set<String>, ActionListener<Set<RoleDescriptor>>>>
getRolesProviders(Settings settings, ResourceWatcherService resourceWatcherService) {
    ...
}
```

The `getRolesProviders` method is used to provide a list of custom roles providers that will be used to resolve role names, if the role names could not be resolved by the reserved roles or native roles stores. The list should be returned in the order that the custom role providers should be invoked to resolve roles. For example, if `getRolesProviders` returns two instances of roles providers, and both of them are able to resolve role `A`, then the resolved role descriptor that will be used for role `A` will be the one resolved by the first roles provider in the list.



## Implementing an authorization engine [implementing-authorization-engine]

Sample code that illustrates the structure and implementation of a custom authorization engine is provided in the [elasticsearch](https://github.com/elastic/elasticsearch/tree/master/plugins/examples/security-authorization-engine) repository on GitHub. You can use this code as a starting point for creating your own authorization engine.

To create an authorization engine, you need to do the following:

1. Implement the `org.elasticsearch.xpack.core.security.authz.AuthorizationEngine` interface in a class with the desired authorization behavior.
2. Implement the `org.elasticsearch.xpack.core.security.authz.Authorization.AuthorizationInfo` interface in a class that contains the necessary information to authorize the request.

### Package an authorization engine as a plugin [packaage-auth-engine]

To package your authorization engine as a plugin:

1. Implement an extension class for your authorization engine that extends `org.elasticsearch.xpack.core.security.SecurityExtension`. There you need to override the following method:

    ```java
    @Override
    public AuthorizationEngine getAuthorizationEngine(Settings settings) {
        ...
    }
    ```

    The `getAuthorizationEngine` method is used to provide the authorization engine implementation.


## Implement an {{es}} plugin [packing-extension-plugin]

To register the security extension for your custom roles provider or authorization engine, you need to also implement an {{es}} plugin that contains the extension:

1. Implement a plugin class that extends `org.elasticsearch.plugins.Plugin`
2. Create a build configuration file for the plugin; Gradle is our recommendation.
3. Create a `plugin-descriptor.properties` file as described in [Help for plugin authors](elasticsearch://extend/index.md).
4. Create a `META-INF/services/org.elasticsearch.xpack.core.security.SecurityExtension` descriptor file for the extension that contains the fully qualified class name of your `org.elasticsearch.xpack.core.security.SecurityExtension` implementation
5. Bundle all in a single zip file.

## Using the security extension [using-security-extension]

To use a security extension:

1. Install the plugin with the extension on each node in the cluster.
 
   * If you're using a self-managed cluster, then run `bin/elasticsearch-plugin` with the `install` sub-command and specify the URL pointing to the zip file that contains the extension. For example:

     ```shell
     bin/elasticsearch-plugin install file:///<path>/my-extension-plugin-1.0.zip
     ```
     
    * If you're using {{ech}}, then refer to [](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md).
    * If you're using {{ece}}, then refer to [](/deploy-manage/deploy/cloud-enterprise/add-custom-bundles-plugins.md).
    * If you're using {{eck}}, then refer to [](/deploy-manage/deploy/cloud-on-k8s/custom-configuration-files-plugins.md).

2. Add any configuration parameters for implementations in the extension to the [`elasticsearch.yml`](/deploy-manage/stack-settings.md) file. The settings are not namespaced and you have access to any settings when constructing the extensions, although it is recommended to have a namespacing convention for extensions to keep your `elasticsearch.yml` configuration easy to understand.

    For example, if you have a custom roles provider that resolves roles from reading a blob in an S3 bucket on AWS, then you would specify settings in `elasticsearch.yml` such as:

    ```js
    custom_roles_provider.s3_roles_provider.bucket: roles
    custom_roles_provider.s3_roles_provider.region: us-east-1
    custom_roles_provider.s3_roles_provider.secret_key: xxx
    custom_roles_provider.s3_roles_provider.access_key: xxx
    ```

    These settings are passed as arguments to the methods in the `SecurityExtension` interface.

3. Restart {{es}}.


