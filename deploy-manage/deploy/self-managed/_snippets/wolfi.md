You can also use the hardened [Wolfi](https://wolfi.dev/) image for additional security. Using Wolfi images requires Docker version 20.10.10 or higher.

To use the Wolfi image, append `-wolfi` to the image tag in the Docker command.

For example:

::::{tab-set}
:group: docker
:::{tab-item} Latest
:sync: latest
```sh subs=true
docker pull docker.elastic.co/elasticsearch/elasticsearch-wolfi:{{version.stack}}
```
:::

:::{tab-item} Specific version
:sync: specific
```sh subs=true
docker pull docker.elastic.co/elasticsearch/elasticsearch-wolfi:<SPECIFIC.VERSION.NUMBER>
```
You can download and install a specific version of the {{stack}} by replacing `<SPECIFIC.VERSION.NUMBER>` with the version number you want. For example, you can replace `<SPECIFIC.VERSION.NUMBER>` with {{version.stack.base}}.
:::

::::