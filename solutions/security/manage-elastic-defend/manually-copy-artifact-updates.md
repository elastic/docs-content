---
navigation_title: Manually copy artifact updates
description: Download the latest Elastic Endpoint global artifact updates and copy them to your air-gapped artifact server to keep endpoints current.
applies_to:
  stack: all
products:
  - id: security
---

# Manually copy artifact updates to an air-gapped server [manually-copy-artifact-updates]

In an air-gapped environment, {{elastic-endpoint}} can't download global artifact updates directly, so you need to copy them to your local artifact server yourself. To set up the server first, refer to [Host an air-gapped {{elastic-endpoint}} artifact server](/solutions/security/configure-elastic-defend/configure-offline-endpoints-air-gapped-environments.md#air-gapped-artifact-server).

Download the most recent artifact files from the Elastic global artifact server, then copy those files to your artifact server instance.

Below is an example script that downloads all the global artifact updates. There are different artifact files for each version of {{elastic-endpoint}}. Change the value of the `ENDPOINT_VERSION` variable in the example script to match the deployed version of {{elastic-endpoint}}.

```sh subs=true
export ENDPOINT_VERSION={{version.stack}} && wget -P downloads/endpoint/manifest https://artifacts.security.elastic.co/downloads/endpoint/manifest/artifacts-$ENDPOINT_VERSION.zip && zcat -q downloads/endpoint/manifest/artifacts-$ENDPOINT_VERSION.zip | jq -r '.artifacts | to_entries[] | .value.relative_url' | xargs -I@ curl "https://artifacts.security.elastic.co@" --create-dirs -o ".@"
```

This command will download files and directory structure that should be directly copied to the file server.

Elastic releases updates continuously as detection engines are improved. Therefore, we recommend updating air-gapped environments at least monthly to stay current with artifact updates.

To confirm that {{elastic-endpoint}} received the latest artifacts, refer to [Validate your self-hosted artifact server](/solutions/security/configure-elastic-defend/configure-offline-endpoints-air-gapped-environments.md#validate-artifact-server).
