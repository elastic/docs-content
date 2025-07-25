You can also use the hardened [Wolfi](https://wolfi.dev/) image for additional security. Using Wolfi images requires Docker version 20.10.10 or higher.

To use the Wolfi image, append `-wolfi` to the image tag in the Docker command.

For example:

```sh subs=true
docker pull docker.elastic.co/elasticsearch/elasticsearch-wolfi:{{version.stack}}
```