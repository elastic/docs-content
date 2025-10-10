---
applies_to:
  deployment:
    self:
navigation_title: Configure
---

# Configure {{es}} with Docker [docker-configuration-methods]

When you run in Docker, the [{{es}} configuration files](/deploy-manage/deploy/self-managed/configure-elasticsearch.md#config-files-location) are loaded from `/usr/share/elasticsearch/config/`.

To use custom configuration files, you [bind-mount the files](#docker-config-bind-mount) over the configuration files in the image.

You can set individual {{es}} configuration parameters using Docker environment variables. The [sample compose file](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-compose.md) and the [single-node example](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-basic.md) use this method. You can use the setting name directly as the environment variable name. If you can't do this, for example because your orchestration platform forbids periods in environment variable names, then you can use an alternative style by converting the setting name as follows:

1. Change the setting name to uppercase
2. Prefix it with `ES_SETTING_`
3. Escape any underscores (`_`) by duplicating them
4. Convert all periods (`.`) to underscores (`_`)

For example, `-e bootstrap.memory_lock=true` becomes `-e ES_SETTING_BOOTSTRAP_MEMORY__LOCK=true`.

You can use the contents of a file to set the value of the `ELASTIC_PASSWORD` or `KEYSTORE_PASSWORD` environment variables, by suffixing the environment variable name with `_FILE`. This is useful for passing secrets such as passwords to {{es}} without specifying them directly.

For example, to set the {{es}} bootstrap password from a file, you can bind mount the file and set the `ELASTIC_PASSWORD_FILE` environment variable to the mount location. If you mount the password file to `/run/secrets/bootstrapPassword.txt`, specify:

```sh
-e ELASTIC_PASSWORD_FILE=/run/secrets/bootstrapPassword.txt
```

You can override the default command for the image to pass {{es}} configuration parameters as command line options. For example:

```sh
docker run <various parameters> bin/elasticsearch -Ecluster.name=mynewclustername
```

While bind-mounting your configuration files is usually the preferred method in production, you can also [create a custom Docker image](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-configure.md#_c_customized_image) that contains your configuration.

## Mounting {{es}} configuration files [docker-config-bind-mount]

Create custom config files and bind-mount them over the corresponding files in the Docker image. For example, to bind-mount `custom_elasticsearch.yml` with `docker run`, specify:

```sh
-v full_path_to/custom_elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml
```

If you bind-mount a custom `elasticsearch.yml` file, ensure it includes the `network.host: 0.0.0.0` setting. This setting ensures the node is reachable for HTTP and transport traffic, provided its ports are exposed. The Docker image’s built-in `elasticsearch.yml` file includes this setting by default.

::::{important}
The container **runs {{es}} as user `elasticsearch` using uid:gid `1000:0`**. Bind mounted host directories and files must be accessible by this user, and the data and log directories must be writable by this user.
::::



## Create an encrypted {{es}} keystore [docker-keystore-bind-mount]

By default, {{es}} will auto-generate a keystore file for [secure settings](/deploy-manage/security/secure-settings.md). This file is obfuscated but not encrypted.

To encrypt your secure settings with a password and have them persist outside the container, use a `docker run` command to manually create the keystore instead. The command must:

* Bind-mount the `config` directory. The command will create an `elasticsearch.keystore` file in this directory. To avoid errors, do not directly bind-mount the `elasticsearch.keystore` file.
* Use the `elasticsearch-keystore` tool with the `create -p` option. You’ll be prompted to enter a password for the keystore.

For example:

::::{tab-set}
:group: docker
:::{tab-item} Latest
:sync: latest
```sh subs=true
docker run -it --rm \
-v full_path_to/config:/usr/share/elasticsearch/config \
docker.elastic.co/elasticsearch/elasticsearch:{{version.stack}} \
bin/elasticsearch-keystore create -p
```
:::

:::{tab-item} Specific version
:sync: specific
Replace `<SPECIFIC.VERSION.NUMBER>` with the version of the Docker image you downloaded.
```sh subs=true
docker run -it --rm \
-v full_path_to/config:/usr/share/elasticsearch/config \
docker.elastic.co/elasticsearch/elasticsearch:<SPECIFIC.VERSION.NUMBER> \
bin/elasticsearch-keystore create -p
```
:::
::::

You can also use a `docker run` command to add or update secure settings in the keystore. You’ll be prompted to enter the setting values. If the keystore is encrypted, you’ll also be prompted to enter the keystore password.

::::{tab-set}
:group: docker
:::{tab-item} Latest
:sync: latest
```sh subs=true
docker run -it --rm \
-v full_path_to/config:/usr/share/elasticsearch/config \
docker.elastic.co/elasticsearch/elasticsearch:{{version.stack}} \
bin/elasticsearch-keystore \
add my.secure.setting \
my.other.secure.setting
```
:::

:::{tab-item} Specific version
:sync: specific
Replace `<SPECIFIC.VERSION.NUMBER>` with the version of the Docker image you downloaded.
```sh subs=true
docker run -it --rm \
-v full_path_to/config:/usr/share/elasticsearch/config \
docker.elastic.co/elasticsearch/elasticsearch:<SPECIFIC.VERSION.NUMBER> \
bin/elasticsearch-keystore \
add my.secure.setting \
my.other.secure.setting
```
:::
::::

If you’ve already created the keystore and don’t need to update it, you can bind-mount the `elasticsearch.keystore` file directly. You can use the `KEYSTORE_PASSWORD` environment variable to provide the keystore password to the container at startup. For example, a `docker run` command might have the following options:

```sh
-v full_path_to/config/elasticsearch.keystore:/usr/share/elasticsearch/config/elasticsearch.keystore
-e KEYSTORE_PASSWORD=mypassword
```

When you upgrade your cluster to a newer version, {{es}} will attempt to automatically upgrade the `elasticsearch.keystore` file to match. However, bind-mounted files are read-only, so {{es}} cannot automatically upgrade a bind-mounted `elasticsearch.keystore` file. Instead, if you are bind-mounting the `elasticsearch.keystore` file directly, you must use the `bin/elasticsearch-keystore upgrade` command to manually upgrade each node's keystore when you upgrade that node.

## Using custom Docker images [_c_customized_image]

In some environments, it might make more sense to prepare a custom image that contains your configuration. A `Dockerfile` to achieve this might be as simple as:

::::{tab-set}
:group: docker
:::{tab-item} Latest
:sync: latest
```sh subs=true
FROM docker.elastic.co/elasticsearch/elasticsearch:{{version.stack}}
COPY --chown=elasticsearch:elasticsearch elasticsearch.yml /usr/share/elasticsearch/config/
```
:::

:::{tab-item} Specific version
:sync: specific
Replace `<SPECIFIC.VERSION.NUMBER>` with the version of the Docker image you downloaded.
```sh subs=true
FROM docker.elastic.co/elasticsearch/elasticsearch:<SPECIFIC.VERSION.NUMBER>
COPY --chown=elasticsearch:elasticsearch elasticsearch.yml /usr/share/elasticsearch/config/
```
:::
::::

You could then build and run the image with:

```sh
docker build --tag=elasticsearch-custom .
docker run -ti -v /usr/share/elasticsearch/data elasticsearch-custom
```

Some plugins require additional security permissions. You must explicitly accept them either by:

* Attaching a `tty` when you run the Docker image and allowing the permissions when prompted.
* Inspecting the security permissions and accepting them (if appropriate) by adding the `--batch` flag to the plugin install command.

See [Plugin management](elasticsearch://reference/elasticsearch-plugins/_other_command_line_parameters.md) for more information.


## Troubleshoot Docker errors for {{es}} [troubleshoot-docker-errors]

Here’s how to resolve common errors when running {{es}} with Docker.


### elasticsearch.keystore is a directory [_elasticsearch_keystore_is_a_directory]

```txt
Exception in thread "main" org.elasticsearch.bootstrap.BootstrapException: java.io.IOException: Is a directory: SimpleFSIndexInput(path="/usr/share/elasticsearch/config/elasticsearch.keystore") Likely root cause: java.io.IOException: Is a directory
```

A [keystore-related](#docker-keystore-bind-mount) `docker run` command attempted to directly bind-mount an `elasticsearch.keystore` file that doesn’t exist. If you use the `-v` or `--volume` flag to mount a file that doesn’t exist, Docker instead creates a directory with the same name.

To resolve this error:

1. Delete the `elasticsearch.keystore` directory in the `config` directory.
2. Update the `-v` or `--volume` flag to point to the `config` directory path rather than the keystore file’s path. For an example, see [Create an encrypted {{es}} keystore](#docker-keystore-bind-mount).
3. Retry the command.


### elasticsearch.keystore: Device or resource busy [_elasticsearch_keystore_device_or_resource_busy]

```txt
Exception in thread "main" java.nio.file.FileSystemException: /usr/share/elasticsearch/config/elasticsearch.keystore.tmp -> /usr/share/elasticsearch/config/elasticsearch.keystore: Device or resource busy
```

A `docker run` command attempted to [update the keystore](#docker-keystore-bind-mount) while directly bind-mounting the `elasticsearch.keystore` file. To update the keystore, the container requires access to other files in the `config` directory, such as `keystore.tmp`.

To resolve this error:

1. Update the `-v` or `--volume` flag to point to the `config` directory path rather than the keystore file’s path. For an example, see [Create an encrypted {{es}} keystore](#docker-keystore-bind-mount).
2. Retry the command.
