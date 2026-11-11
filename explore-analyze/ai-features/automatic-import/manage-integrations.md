---
navigation_title: Manage integrations
description: Track, edit, and approve new versions of the integrations you create with Automatic Import, and download them to use on another cluster or project.
type: how-to
applies_to:
  serverless: ga
  stack: ga 9.4+
products:
  - id: kibana
  - id: cloud-serverless
  - id: security
  - id: observability
---

# Manage integrations created with Automatic Import [automatic-import-manage]

Use **Manage my integrations** to track, edit, and reuse the integrations that you [create with Automatic Import](/explore-analyze/ai-features/automatic-import/create-integration.md). To open it, find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select **Manage my integrations**. The list shows each integration's data streams, version, analysis status, and approval status.

The list doesn't include integrations created in {{stack}} 9.0–9.3 or uploaded as `.zip` packages. Those appear on the **Installed integrations** tab.

## Before you begin [automatic-import-manage-prerequisites]

Make sure that you meet the [Automatic Import requirements](/explore-analyze/ai-features/automatic-import.md#automatic-import-requirements).

## Edit an integration [automatic-import-edit]

You can edit an integration only on the cluster or project where you created it.

1. In **Manage my integrations**, open the integration's **Actions** menu and select **Edit**.
2. Make your changes:

   - Update the integration details.
   - Add a data stream with **Add Data Stream**.
   - Re-analyze a data stream. The new pipeline replaces the current one, including any edits that you saved. If the re-analysis fails, the current pipeline stays.
   - Delete a data stream.

3. Approve and install the integration, as described in [Review, approve, and install the integration](/explore-analyze/ai-features/automatic-import/create-integration.md#automatic-import-approve). If the integration was already approved, this creates a new version.
4. If agent policies already use the integration, [upgrade their integration policies](/reference/fleet/upgrade-integration.md#upgrade-integration-policies-manually). Installing a new version doesn't upgrade them.

Edit the pipeline in Automatic Import, not on the **Ingest Pipelines** page. Changes that you make on the **Ingest Pipelines** page don't carry over to the next version that you install.

## Use an integration on another cluster or project [automatic-import-reuse]

You can download an integration's package when every data stream shows **Success**.

1. On the cluster or project where you created the integration, open **Manage my integrations**.
2. Open the integration's **Actions** menu and select **Download .zip package**.
3. On the other cluster or project, find **Integrations**. In the **Can't find an integration?** panel, select **upload an integration package**.
4. Upload the `.zip` package, then select **Add to Elastic**.

The upload fails if the cluster or project already has an integration with the same name, unless that integration is an earlier version of a package that you uploaded.

To update the integration, edit it where you created it, then download and upload the new package. {{fleet}} doesn't offer **Upgrade to latest version** for uploaded integrations, so [upgrade the integration policies](/reference/fleet/upgrade-integration.md#upgrade-integration-policies-manually) after you upload.

In {{stack}} 9.4.0–9.4.7 and 9.5.0–9.5.4, the upload page also rejects later versions of a package that you uploaded. On these versions, upload the new package with the {{fleet}} API instead, as shown in [Upload a new integration](integrations://extend/upload-new-integration.md).
