---
navigation_title: "Host product documentation for AI assistant"
applies_to:
  stack: ga
  self: ga
products:
  - id: kibana
  - id: security
  - id: observability
  - id: elasticsearch
description: Mirror Elastic product documentation ZIP files on infrastructure Kibana can reach so Kibana can install them for the AI assistant when the public artifact repository is unavailable or blocked.
---

# Host product documentation artifacts for Elastic AI assistant [host-product-documentation-artifacts-ai-assistant]

Elastic packages product documentation for AI assistant as versioned ZIP files. When {{kib}} can reach Elastic’s public repository at [kibana-knowledge-base-artifacts.elastic.co](https://kibana-knowledge-base-artifacts.elastic.co/), {{kib}} downloads those ZIP files from that public host and you install product documentation using the AI assistant UI.

When {{kib}} can't reach that repository, you still use the same published ZIP files but host them as a documentation mirror on infrastructure that your deployment can reach. This is a common scenario for deployments on isolated, restricted, or air-gapped networks. 

The sections that follow cover how to prepare a documentation mirror, configure hosting, and install product documentation for the AI assistant.

## Prepare to host your documentation mirror [prepare-to-host-your-documentation-mirror]

A documentation mirror is your own copy of Elastic’s published product-documentation bundles. It includes the versioned ZIP files for your {{stack}} and the bucket-style listing {{kib}} uses to discover those file names. Typically, you would create a mirror when {{kib}} can't reach Elastic’s public host to download documentation because the deployment is on an isolated, restricted, or air-gapped network.

Before setting up a documentation mirror, review this section to understand the documentation files you need, mirror layout requirements and hosting options, and {{kib}} settings that control the mirror URL.

:::::{stepper}

::::{step} Get product documentation ZIP files for your {{kib}} version

1. **Identify the documentation ZIP version and file names for your {{kib}} release.**

   Check which stack version you are running (for example, 9.0). The `{{versionMajor}}.{{versionMinor}}` segment in each file name must match that release. If it does not match your {{kib}} release, or the file names differ from what Elastic publishes for that release, mirroring will not work.

   Elastic publishes four documentation bundles for each minor version, one each for {{es}}, {{kib}}, {{observability}}, and {{elastic-sec}}. File names follow this pattern:

   ```yaml
   kb-product-doc-{{productName}}-{{versionMajor}}.{{versionMinor}}.zip
   ```

   For example, when {{kib}} is 9.0, the four ZIP files are:

   * `kb-product-doc-elasticsearch-9.0.zip`
   * `kb-product-doc-kibana-9.0.zip`
   * `kb-product-doc-observability-9.0.zip`
   * `kb-product-doc-security-9.0.zip`

2. **Download or copy the documentation ZIP files.**

   Download all four from [kibana-knowledge-base-artifacts.elastic.co](https://kibana-knowledge-base-artifacts.elastic.co/) when you can reach that host, or copy them from another trusted source that already mirrored them if you are fully offline.

::::

::::{step} Understand mirror layout requirements and hosting options

At the mirror’s repository root, {{kib}} reads a bucket-style listing, then downloads each ZIP from that same URL. Before you connect {{kib}} to the mirror in the next step, confirm the layout {{kib}} expects, then choose how you will host it:

* **Repository layout**: Keep the bucket-style listing and the four ZIP files under one repository root, matching Elastic’s public host. {{kib}} uses that single base URL for both the listing and the downloads. Don't use a custom layout or modify the file names. If you do this, {{kib}} won't be able to find and download the ZIP files. 
* **Hosting**: Choose an S3-compatible bucket or a CDN with a listing file.

   {applies_to}`self: ga 9.1+` You also have the option to host the documentation as local files on the {{kib}} host.

::::

::::{step} Know which {{kib}} settings control the mirror URL

These settings tell {{kib}} which repository root to call:

* **`xpack.productDocBase.artifactRepositoryUrl`**: The base address {{kib}} uses to read the file listing and download the documentation ZIPs. You set this in `kibana.yml` (or your deployment’s equivalent).
* {applies_to}`self: ga 9.4+`**`xpack.productDocBase.artifactRepositoryProxyUrl`**: Only needed when {{kib}} has to go through an HTTP or HTTPS proxy to reach the mirror.

For defaults, allowed values, and more details, refer to [Knowledge base artifact settings for AI Assistants](kibana://reference/configuration-reference/ai-assistant-settings.md).

::::

:::::

## Configure your documentation mirror [configuring-product-doc-isolated-restricted-airgap]

Choose the tab that matches your setup and follow the steps to stage the ZIP files, point {{kib}} at your mirror, and complete the setup configuration.


:::::{tab-set}

::::{tab-item} S3-compatible bucket

### Host using an S3-compatible bucket

When {{kib}} can’t use Elastic’s public artifact host, hosting product documentation on an S3-compatible bucket is a common choice. You mirror the published ZIP files on an S3-compatible bucket that {{kib}} can reach over HTTPS inside your environment.

Unlike a CDN, such a bucket can expose S3’s listing API natively, so {{kib}} can read the bucket listing and download the ZIP files without a hand-maintained XML listing file. The following steps cover getting the artifacts, uploading them to your bucket, pointing {{kib}} at the repository URL, and completing setup.

1. **Get the four product documentation ZIP files for your {{kib}} version.**

   Download them from [kibana-knowledge-base-artifacts.elastic.co](https://kibana-knowledge-base-artifacts.elastic.co/) if your network can reach that host. If it can't, get the same files from another system or mirror and transfer them to your environment.

   {{kib}} only installs documentation when the ZIP file names and version segment match Elastic’s published artifacts for your stack. Without those files, the install can't succeed.

2. **Upload the ZIP files to your bucket and expose a listing.**

   Upload the four files to the bucket. Configure the bucket so its root exposes a listing comparable to Elastic’s public bucket, with your ZIP files visible in that index or listing view.

   {{kib}} reads that listing to discover the exact ZIP file names before it downloads them.

3. **Tell {{kib}} where to download the artifacts.**

   In `kibana.yml`, set [`xpack.productDocBase.artifactRepositoryUrl`](kibana://reference/configuration-reference/ai-assistant-settings.md) to the HTTPS base URL of the bucket you used in step 2. Use the base URL for the top of the mirror, which will be the same place the listing and the four ZIP files appear together. _Do not_ use a longer URL that points into a subfolder under that mirror.

   For example:

   ```yaml
   # Replace with your bucket’s HTTPS base URL (no extra path after the repository root)
   xpack.productDocBase.artifactRepositoryUrl: "<MY_CUSTOM_REPOSITORY_URL>"
   ```

   {{kib}} calls that single address to read the bucket listing and download the ZIP files; the wrong base URL breaks listing discovery or downloads.

4. **Restart {{kib}} so the configuration change takes effect.**

   [Stop and restart](/deploy-manage/maintenance/start-stop-services/start-stop-kibana.md)  {{kib}}. The new `artifactRepositoryUrl` value in your `kibana.yml` isn't applied until {{kib}} fully restarts.

5. **Install product documentation in the AI assistant UI.**

   The steps depend on which assistant you use:

   * **AI Assistant for Security**: Product documentation is available when you enable Knowledge Base. Refer to [Give AI Assistant access to Elastic’s product documentation](/solutions/security/ai/ai-assistant-knowledge-base.md#elastic-docs) to learn more.
   * **AI Assistant for Observability and Search**: On the **Settings** tab of AI Assistant Settings, use **Install Elastic Documentation**. Refer to [Add Elastic documentation](/solutions/observability/ai/observability-ai-assistant.md#obs-ai-product-documentation) to learn more.

::::

::::{tab-item} CDN

Unlike the S3-compatible bucket flow in the previous tab, a CDN can’t expose S3’s listing API natively. Instead, you must rebuild the same behavior with static files. This requires you to publish the ZIP artifacts and an XML file that mimics S3’s listing, configure the CDN so that folder URL returns the XML, then point {{kib}} at that HTTPS base URL. 

1. **Get the four product documentation ZIP files for your {{kib}} version.**

   Download them from [kibana-knowledge-base-artifacts.elastic.co](https://kibana-knowledge-base-artifacts.elastic.co/) if your network can reach that host. If it can't, get the same files from another system or mirror and transfer them into your environment.

   {{kib}} only installs documentation when the ZIP file names and version segment match Elastic’s published artifacts for your stack. Without those files, the install can't succeed.

2. **Stage the ZIP files on your CDN origin.**

   Upload all four files to one folder on the CDN origin or on the storage your CDN pulls from so they share a single base path. In the next step, you add a listing file to this same folder. Later you set [`xpack.productDocBase.artifactRepositoryUrl`](kibana://reference/configuration-reference/ai-assistant-settings.md) to that folder’s HTTPS URL.

   One folder under one HTTPS base URL lets {{kib}} request the listing and fetch each ZIP from the same base URL, which matches how the S3-compatible flow works.

3. **Create the listing file {{kib}} uses to discover the ZIP file names.**

   Copy the template below and set each `<Key>` to match your artifact file names and {{kib}} version. For example, for {{kib}} 9.1, replace every `9.0` in the keys with `9.1`.

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

   Put the XML file in the **same folder** as the four ZIP files. Configure the CDN so a request to the folder’s HTTPS URL returns this XML as the **directory index** (your provider may call this a default document or index file). The exact control varies by CDN.

   A CDN does not implement S3’s listing API, so this XML stands in for the listing a bucket would return. {{kib}} requests that listing from the folder base URL, then downloads each ZIP by name from the same origin. The keys in the XML must match the files you uploaded, and the CDN must serve the XML at that URL.

4. **Tell {{kib}} where to download the artifacts from your CDN mirror.**

   In `kibana.yml`, set `xpack.productDocBase.artifactRepositoryUrl` to the HTTPS base URL of the folder from step 2. It will be the same URL whose index serves the XML from step 3. Do not add an extra path segment beyond that folder.

   For example:

   ```yaml
   # Replace with your CDN folder’s HTTPS base URL (no extra path beyond the repository root)
   xpack.productDocBase.artifactRepositoryUrl: "<MY_CUSTOM_REPOSITORY_URL>"
   ```

   {{kib}} must use one base URL for both the listing response and the ZIP downloads; a deeper path breaks that contract.


5. **Restart {{kib}} so the configuration change takes effect.**

   [Stop and restart](/deploy-manage/maintenance/start-stop-services/start-stop-kibana.md) {{kib}}. The new `artifactRepositoryUrl` value in your `kibana.yml` isn't applied until {{kib}} fully restarts.

6. **Install product documentation in the AI assistant UI.**

   The steps depend on which assistant you use:

   * **AI Assistant for Security**: Product documentation is available when you enable Knowledge Base. Refer to [Give AI Assistant access to Elastic’s product documentation](/solutions/security/ai/ai-assistant-knowledge-base.md#elastic-docs) to learn more.
   * **AI Assistant for Observability and Search**: On the **Settings** tab of AI Assistant Settings, use **Install Elastic Documentation**. Refer to [Add Elastic documentation](/solutions/observability/ai/observability-ai-assistant.md#obs-ai-product-documentation) to learn more.

::::

::::{tab-item} Local files on the {{kib}} host

```{applies_to}
self: ga 9.1+
```

You can install product documentation by placing Elastic’s published ZIP files in a directory on the {{kib}} host that {{kib}} can read. {{kib}} uses those files to install the product documentation that AI assistant relies on when answering questions about Elastic products.

To set this up, configure [`xpack.productDocBase.artifactRepositoryUrl`](kibana://reference/configuration-reference/ai-assistant-settings.md) as a `file://` URL and place the ZIP files in that directory.

::::

:::::
