---
navigation_title: "Knowledge base artifact repo for AI assistants"
applies_to:
  self: ga
products:
  - id: kibana
  - id: security
  - id: observability
  - id: elasticsearch
description: Host AI assistant knowledge base artifacts via S3-compatible storage, CDN, or local paths when Kibana cannot reach Elastic’s public URL, then set the repository URL and install from the assistant UI.
---

# Host a knowledge base artifact repo for AI assistants [host-knowledge-base-artifact-repo-for-ai-assistants]

When {{kib}} can't use Elastic’s [public artifact URL](https://kibana-knowledge-base-artifacts.elastic.co/), which is common for deployments in air-gapped or restricted networks, you must deploy the knowledge base artifact repository manually. You do that by mirroring Elastic’s versioned knowledge base artifact ZIP files to infrastructure that {{kib}} can reach.

This page walks you through hosting those ZIP files, configuring the repository URL in {{kib}}, and installing knowledge base content from the AI assistant so assistants can use Elastic product documentation without reaching Elastic’s public artifact host.

## Choose a hosting option [choose-a-hosting-option-for-knowledge-base-artifacts]

Use this list to figure out the best deployment and hosting setup for your environment, then go to the [Deploy the repository](#deploy-the-knowledge-base-artifact-repository) section for detailed steps.

* **S3-compatible bucket**: You store the artifact ZIP files in an S3-compatible bucket over HTTPS and the bucket exposes a normal object listing at the repository root, so {{kib}} can discover the ZIPs without you maintaining a separate listing XML file (unlike the CDN option).
* **CDN**: You serve the ZIP files through a CDN and publish S3-style listing XML yourself, served as the folder’s default document or directory index.
* {applies_to}`self: ga 9.1+` **Local files on the {{kib}} host**: The ZIP files exist only on the {{kib}} host filesystem and you configure a `file://` repository URL.

## Deploy the repository [deploy-the-knowledge-base-artifact-repository]

Choose the tab that matches your deployment and hosting setup:

:::::::{tab-set}

::::::{tab-item} S3-compatible bucket

:::::{stepper}

::::{step} Get the product documentation ZIP files for your {{kib}} version

:::{tip}
Check which stack version you’re running (for example, 9.0). The `{{versionMajor}}.{{versionMinor}}` segment in each file name must match that release. If it doesn’t match your {{kib}} release, or the file names differ from what Elastic publishes for that release, installation will fail.
:::

Elastic publishes knowledge base artifact ZIP files for each minor version, one each for {{es}}, {{kib}}, {{observability}}, and {{elastic-sec}}. File names follow this pattern:

```yaml
kb-product-doc-{{productName}}-{{versionMajor}}.{{versionMinor}}.zip
```

For example, when {{kib}} is 9.0, the ZIP files are:

* `kb-product-doc-elasticsearch-9.0.zip`
* `kb-product-doc-kibana-9.0.zip`
* `kb-product-doc-observability-9.0.zip`
* `kb-product-doc-security-9.0.zip`

Download the ZIP files from [kibana-knowledge-base-artifacts.elastic.co](https://kibana-knowledge-base-artifacts.elastic.co/) when you can reach that host, or copy them from another trusted source that already hosts the same ZIP files if you’re fully offline.

::::

::::{step} Upload the ZIP files to your bucket

Configure the bucket root so its listing matches `https://kibana-knowledge-base-artifacts.elastic.co/` and lists all ZIPs. Over HTTPS, use S3-style listing from a compatible bucket.

:::{important}
For S3-compatible storage, a single HTTPS repository root must expose the bucket’s list response (the same S3-style listing {{kib}} would get from `ListObjects`-style APIs) and the object keys at that same root. **Do not** rely on a separate path for the ZIPs. Object key names must match the ZIP file names from the previous step so each listing entry resolves to a downloadable file.
:::

::::

::::{step} Set the repository URL in {{kib}}

In `kibana.yml`, set [`xpack.productDocBase.artifactRepositoryUrl`](kibana://reference/configuration-reference/ai-assistant-settings.md) to the bucket root’s HTTPS URL (the base that serves both the listing and the ZIPs). **Do not** point it at a subdirectory of that root.

```yaml
# Replace with your bucket’s HTTPS base URL (repository root only)
xpack.productDocBase.artifactRepositoryUrl: "<MY_CUSTOM_REPOSITORY_URL>"
```

::::

::::{step} Restart {{kib}}

[Stop and restart](/deploy-manage/maintenance/start-stop-services/start-stop-kibana.md) {{kib}}. The new `artifactRepositoryUrl` value isn’t applied until {{kib}} fully restarts.

::::

::::{step} Install knowledge base content from the AI assistant UI

The steps to install knowledge base content depend on the assistant that you use:

* **AI Assistant for Security**: Refer to [Give AI Assistant access to Elastic’s product documentation](/solutions/security/ai/ai-assistant-knowledge-base.md#elastic-docs).
* **AI Assistant for Observability and Search**: Refer to [Add Elastic documentation](/solutions/observability/ai/observability-ai-assistant.md#obs-ai-product-documentation).

::::

:::::

::::::

::::::{tab-item} CDN

:::::{stepper}

::::{step} Get the product documentation ZIP files for your {{kib}} version

:::{tip}
Check which stack version you’re running (for example, 9.0). The `{{versionMajor}}.{{versionMinor}}` segment in each file name must match that release. If it doesn’t match your {{kib}} release, or the file names differ from what Elastic publishes for that release, installation will fail.
:::

Elastic publishes knowledge base artifact ZIP files for each minor version, one each for {{es}}, {{kib}}, {{observability}}, and {{elastic-sec}}. File names follow this pattern:

```yaml
kb-product-doc-{{productName}}-{{versionMajor}}.{{versionMinor}}.zip
```

For example, when {{kib}} is 9.0, the ZIP files are:

* `kb-product-doc-elasticsearch-9.0.zip`
* `kb-product-doc-kibana-9.0.zip`
* `kb-product-doc-observability-9.0.zip`
* `kb-product-doc-security-9.0.zip`

Download the ZIP files from [kibana-knowledge-base-artifacts.elastic.co](https://kibana-knowledge-base-artifacts.elastic.co/) when you can reach that host, or copy them from another trusted source that already hosts the same ZIP files if you’re fully offline.

::::

::::{step} Upload the ZIP files to the CDN

Put all ZIP files in one folder on the CDN origin (or backing storage) so they share a single HTTPS base path. You add the listing XML in the next step and wire the CDN to serve it as that folder’s index.

::::

::::{step} Create and upload the bucket listing

Copy the template, set each `<Key>` to your real file names and minor version (for {{kib}} 9.1, replace `9.0` in the example with `9.1` everywhere in the keys).

```xml
<ListBucketResult>
    <Name>kibana-ai-assistant-kb-artifacts</Name>
    <IsTruncated>false</IsTruncated>
    <Contents>
        <Key>kb-product-doc-elasticsearch-9.0.zip</Key>
    </Contents>
    <Contents>
        <Key>kb-product-doc-kibana-9.0.zip</Key>
    </Contents>
    <Contents>
        <Key>kb-product-doc-observability-9.0.zip</Key>
    </Contents>
    <Contents>
        <Key>kb-product-doc-security-9.0.zip</Key>
    </Contents>
</ListBucketResult>
```

Place the XML in the same folder as the ZIP files. Configure the CDN so a request to that folder’s base URL returns this XML (often as the index or default document).

:::{important}
On a CDN, each `<Key>` must match a real ZIP file name in that origin folder, and the XML must be what clients get when they request the folder URL (default document or directory index). {{kib}} reads that listing from the same HTTPS base path it uses to download the ZIPs, so don’t split the listing and the ZIP files across different URLs or path roots.
:::

::::

::::{step} Set the repository URL in {{kib}}

Set [`xpack.productDocBase.artifactRepositoryUrl`](kibana://reference/configuration-reference/ai-assistant-settings.md) to that folder’s HTTPS base URL (the URL whose index serves the XML). Don’t append an extra path past that root.

```yaml
# Replace with your CDN folder’s HTTPS base URL (repository root only)
xpack.productDocBase.artifactRepositoryUrl: "<MY_CUSTOM_REPOSITORY_URL>"
```

::::

::::{step} Restart {{kib}}

[Stop and restart](/deploy-manage/maintenance/start-stop-services/start-stop-kibana.md) {{kib}}.

::::

::::{step} Install knowledge base content from the AI assistant UI

The steps to install knowledge base content depend on the assistant that you use:

* **AI Assistant for Security**: Refer to [Give AI Assistant access to Elastic’s product documentation](/solutions/security/ai/ai-assistant-knowledge-base.md#elastic-docs).
* **AI Assistant for Observability and Search**: Refer to [Add Elastic documentation](/solutions/observability/ai/observability-ai-assistant.md#obs-ai-product-documentation).

::::

:::::

::::::

::::::{tab-item} Local files on the {{kib}} host

```{applies_to}
self: ga 9.1+
```

:::::{stepper}

::::{step} Get the product documentation ZIP files for your {{kib}} version

:::{tip}
Check which stack version you’re running (for example, 9.0). The `{{versionMajor}}.{{versionMinor}}` segment in each file name must match that release. If it doesn’t match your {{kib}} release, or the file names differ from what Elastic publishes for that release, installation will fail.
:::

Put the version-matched ZIP files in one directory on the {{kib}} host. File names use this pattern:

```yaml
kb-product-doc-{{productName}}-{{versionMajor}}.{{versionMinor}}.zip
```

For example, when {{kib}} is 9.0:

* `kb-product-doc-elasticsearch-9.0.zip`
* `kb-product-doc-kibana-9.0.zip`
* `kb-product-doc-observability-9.0.zip`
* `kb-product-doc-security-9.0.zip`

Download the ZIP files from [kibana-knowledge-base-artifacts.elastic.co](https://kibana-knowledge-base-artifacts.elastic.co/) when you can reach that host, or copy them from another trusted source that already hosts the same ZIP files if you’re fully offline.

::::

::::{step} Set the repository URL in {{kib}}

Set [`xpack.productDocBase.artifactRepositoryUrl`](kibana://reference/configuration-reference/ai-assistant-settings.md) to the `file://` URL of that directory.

:::{important}
With a `file://` repository, the directory must sit on the {{kib}} host, or on storage mounted there. It must also be readable by the user that runs {{kib}}. Use the `file://` URL of the folder that directly contains the ZIPs. **Do not** point at a parent directory. File names must stay exactly as in the previous step, or {{kib}} won’t pick up the ZIP files.
:::

::::

::::{step} Restart {{kib}}

[Stop and restart](/deploy-manage/maintenance/start-stop-services/start-stop-kibana.md) {{kib}}.

::::

::::{step} Install knowledge base content from the AI assistant UI

The steps to install knowledge base content depend on the assistant that you use:

* **AI Assistant for Security**: Refer to [Give AI Assistant access to Elastic’s product documentation](/solutions/security/ai/ai-assistant-knowledge-base.md#elastic-docs).
* **AI Assistant for Observability and Search**: Refer to [Add Elastic documentation](/solutions/observability/ai/observability-ai-assistant.md#obs-ai-product-documentation).

::::

:::::

::::::

:::::::
