---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/cspm-get-started-gcp.html
  - https://www.elastic.co/guide/en/serverless/current/security-cspm-get-started-gcp.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Get started with CSPM for GCP

## Overview [cspm-overview-gcp]

This page explains how to get started monitoring the security posture of your GCP cloud assets using the Cloud Security Posture Management (CSPM) feature.

## Requirements

* Minimum privileges vary depending on whether you need to read, write, or manage CSPM data and integrations. Refer to [CSPM privilege requirements](/solutions/security/cloud/cspm-privilege-requirements.md).
* The CSPM integration is available to all {{ecloud}} users. On-premise deployments require an [appropriate subscription](https://www.elastic.co/pricing) level.
* CSPM is supported only on AWS, GCP, and Azure commercial cloud platforms, and AWS GovCloud. Other government cloud platforms are not supported. To request support [open a GitHub issue](https://github.com/elastic/kibana/issues/new/choose).
* The user who gives the CSPM integration GCP permissions must be a GCP project `admin`.



## Set up CSPM for GCP [cspm-setup-gcp]

You can set up CSPM for GCP either by enrolling a single project, or by enrolling an organization containing multiple projects. Either way, you need to first add the CSPM integration, then enable cloud access. 

Two deployment technologies are available: agentless and agent-based. 

* [Agentless deployment](/solutions/security/cloud/asset-disc-azure.md#cad-azure-agentless) allows you to collect cloud posture data without having to manage the deployment of an agent in your cloud. 
* [Agent-based deployment](/solutions/security/cloud/asset-disc-azure.md#cad-azure-agent-based) requires you to deploy and manage an agent in the cloud project or projects you want to monitor.


## Agentless deployment [cspm-gcp-agentless]

1. Find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Search for `CSPM`, then click on the result.
3. Click **Add Cloud Security Posture Management (CSPM)**.
4. Under **Configure integration**, select **GCP**, then either **GCP Organization** to onboard your whole organization, or **Single Project** to onboard an individual project.
5. Give your integration a name and description that match the purpose or team of the GCP subscription/organization you want to monitor, for example, `dev-gcp-project`.
6. (Optional) Expand **Advanced options** and add a `Namespace` to the integration's data stream.

:::{include} _snippets/cspm-namespace.md
:::

7. For **Deployment options**, select **Agentless**.
8. Next, you’ll need to authenticate to GCP. Expand the **Steps to Generate GCP Account Credentials** section, then follow the instructions that appear to automatically create the necessary credentials using Google Cloud Shell.
9. Once you’ve provided the necessary credentials, click **Save and continue** to finish deployment. Your data should start to appear within a few minutes.

## Agent-based deployment [cspm-gcp-agent-based]


### Add your CSPM integration [cspm-add-and-name-integration-gcp]

1. Find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Search for `CSPM`, then click on the result.
3. Click **Add Cloud Security Posture Management (CSPM)**.
4. For **Configure integration**, select **GCP**, then either **GCP Organization** to onboard your whole organization, or **Single Project** to onboard an individual project.
5. Give your integration a name and description that match the purpose or team of the GCP project you want to monitor, for example, `dev-gcp-project`.
6. (Optional) Expand the **Advanced options** menu and add a `Namespace` to the integration's data stream.

::::{include} _snippets/cspm-namespace.md
::::
7. Under **Deployment options** select **Agent-based**.


### Set up cloud account access [cspm-set-up-cloud-access-section-gcp]

::::{note}
To set up CSPM for a GCP project, you need admin privileges for the project.
::::


For most users, the simplest option is to use a Google Cloud Shell script to automatically provision the necessary GCP resources and permissions. This method, as well as two manual options, are described next on this page.


## Cloud Shell script setup (recommended) [cspm-set-up-cloudshell]

1. For **Setup Access**, select **Google Cloud Shell**. Enter your GCP Project ID, and for GCP Organization deployments, your GCP Organization ID.
2. In **Where to add this integration**:

    1. Select **New Hosts**.
    2. Name the {{agent}} policy. Use a name that matches the purpose or team of the cloud project or projects you want to monitor. For example, `dev-gcp-project`.
    3. Click **Save and continue**, then **Add {{agent}} to your hosts**. The **Add agent** wizard appears and provides {{agent}} binaries, which you can download and deploy to a VM in GCP.

3. Click **Save and continue**.
4. Copy the command that appears, then click **Launch Google Cloud Shell**. It opens in a new window.
5. Check the box to trust Elastic’s `cloudbeat` repo, then click **Confirm**

:::{image} /solutions/images/security-cspm-cloudshell-trust.png
:alt: The cloud shell confirmation popup
:::

6. In Google Cloud Shell, execute the command you copied. Once it finishes, return to {{kib}} and wait for the confirmation of data received from your new integration. Then you can click **View Assets** to see your data.

::::{note}
If you encounter any issues running the command, return to {{kib}} and navigate again to Google Cloud Shell.
::::


::::{note}
During Cloud Shell setup, the CSPM integration adds roles to Google’s default service account, which enables custom role creation and attachment of the service account to a compute instance. After setup, these roles are removed from the service account. If you attempt to delete the deployment but find the deployment manager lacks necessary permissions, consider adding the missing roles to the service account: [Project IAM Admin](https://cloud.google.com/iam/docs/understanding-roles#resourcemanager.projectIamAdmin), [Role Administrator](https://cloud.google.com/iam/docs/understanding-roles#iam.roleAdmin).
::::



## Manual authentication (GCP organization) [cspm-set-up-manual-gcp-org]

To authenticate manually to monitor a GCP organization, you’ll need to create a new GCP service account, assign it the necessary roles, generate credentials, then provide those credentials to the CSPM integration.

Use the following commands, after replacing `<SA_NAME>` with the name of your new service account, `<ORG_ID>` with your GCP organization’s ID, and `<PROJECT_ID>` with the GCP project ID of the project where you want to provision the compute instance that will run CSPM.

Create a new service account:

```
gcloud iam service-accounts create <SA_NAME> \
    --description="Elastic agent service account for CSPM" \
    --display-name="Elastic agent service account for CSPM" \
    --project=<PROJECT_ID>
```

Assign the necessary roles to the service account:

```
gcloud organizations add-iam-policy-binding <ORG_ID> \
    --member=serviceAccount:<SA_NAME>@<PROJECT_ID>.iam.gserviceaccount.com \
    --role=roles/cloudasset.viewer

gcloud organizations add-iam-policy-binding <ORG_ID> \
    --member=serviceAccount:<SA_NAME>@<PROJECT_ID>.iam.gserviceaccount.com \
    --role=roles/browser
```

::::{important}
If running this command results in a warning related to conditions, try running it again with `--condition=None`.
::::

::::{note}
The `Cloud Asset Viewer` role grants read access to cloud asset metadata. The `Browser` role grants read access to the project hierarchy.
::::


Download the credentials JSON (first, replace `<KEY_FILE>` with the location where you want to save it):

```
gcloud iam service-accounts keys create <KEY_FILE> \
    --iam-account=<SA_NAME>@<PROJECT_ID>.iam.gserviceaccount.com
```

Keep the credentials JSON in a secure location; you will need it later.

Provide credentials to the CSPM integration:

1. On the CSPM setup screen, for **Setup Access**, select **Manual**.
2. Enter your GCP **Organization ID**. Enter the GCP **Project ID** of the project where you want to provision the compute instance that will run CSPM.
3. Select **Credentials JSON**, and enter the value you generated earlier.
4. For **Where to add this integration**, select **New Hosts**.
5. Name the {{agent}} policy. Use a name that matches the purpose or team of the cloud project or projects you want to monitor. For example, `dev-gcp-project`.
6. Click **Save and continue**, then follow the instructions to install {{agent}} in your chosen GCP project.

Wait for the confirmation that {{kib}} received data from your new integration. Then you can click **View Assets** to see your data.


## Manual authentication (GCP project) [cspm-set-up-manual-gcp-project]

To authenticate manually to monitor an individual GCP project, you’ll need to create a new GCP service account, assign it the necessary roles, generate credentials, then provide those credentials to the CSPM integration.

Use the following commands, after replacing `<SA_NAME>` with the name of your new service account, and `<PROJECT_ID>` with your GCP project ID.

Create a new service account:

```
gcloud iam service-accounts create <SA_NAME> \
    --description="Elastic agent service account for CSPM" \
    --display-name="Elastic agent service account for CSPM" \
    --project=<PROJECT_ID>
```

Assign the necessary roles to the service account:

```
gcloud projects add-iam-policy-binding <PROJECT_ID> \
    --member=serviceAccount:<SA_NAME>@<PROJECT_ID>.iam.gserviceaccount.com \
    --role=roles/cloudasset.viewer

gcloud projects add-iam-policy-binding <PROJECT_ID> \
    --member=serviceAccount:<SA_NAME>@<PROJECT_ID>.iam.gserviceaccount.com \
    --role=roles/browser
```

::::{important}
If running this command results in a warning related to conditions, try running it again with `--condition=None`.
::::

::::{note}
The `Cloud Asset Viewer` role grants read access to cloud asset metadata. The `Browser` role grants read access to the project hierarchy.
::::


Download the credentials JSON (first, replace `<KEY_FILE>` with the location where you want to save it):

```
gcloud iam service-accounts keys create <KEY_FILE> \
    --iam-account=<SA_NAME>@<PROJECT_ID>.iam.gserviceaccount.com
```

Keep the credentials JSON in a secure location; you will need it later.

Provide credentials to the CSPM integration:

1. On the CSPM setup screen, for **Setup Access**, select **Manual**.
2. Enter your GCP **Project ID**.
3. Select **Credentials JSON**, and enter the value you generated earlier.
4. For **Where to add this integration**, select **New Hosts**.
5. Name the {{agent}} policy. Use a name that matches the purpose or team of the cloud project or projects you want to monitor. For example, `dev-gcp-project`.
6. Click **Save and continue**, then follow the instructions to install {{agent}} in your chosen GCP project.

Wait for the confirmation that {{kib}} received data from your new integration. Then you can click **View Assets** to see your data.
