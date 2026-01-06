---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/cspm-get-started-azure.html
  - https://www.elastic.co/guide/en/serverless/current/security-cspm-get-started-azure.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Get started with CSPM for Azure

## Overview [cspm-overview-azure]

This page explains how to get started monitoring the security posture of your cloud assets using the Cloud Security Posture Management (CSPM) feature.

## Requirements

* Minimum privileges vary depending on whether you need to read, write, or manage CSPM data and integrations. Refer to [CSPM privilege requirements](/solutions/security/cloud/cspm-privilege-requirements.md).
* The CSPM integration is available to all {{ecloud}} users. On-premise deployments require [appropriate subscription](https://www.elastic.co/pricing) level.
* CSPM is supported only on AWS, GCP, and Azure commercial cloud platforms, and AWS GovCloud. Other government cloud platforms are not supported. To request support, [open a GitHub ticket](https://github.com/elastic/kibana/issues/new/choose).
* The user who gives the CSPM integration permissions in Azure must be an Azure subscription `admin`.




## Set up CSPM for Azure [cspm-setup-azure]

You can set up CSPM for Azure by enrolling an Azure organization (management group) containing multiple subscriptions, or by enrolling a single subscription. Either way, first add the CSPM integration, then enable cloud account access. 

The following deployment technologies are available: agentless and agent-based. 

* [Agentless deployment](/solutions/security/cloud/get-started-with-cspm-for-azure.md#cspm-azure-agentless) allows you to collect cloud posture data without having to manage the deployment of an agent in your cloud. 
* [Agent-based deployment](/solutions/security/cloud/get-started-with-cspm-for-azure.md#cspm-azure-agent-based) requires you to deploy and manage an agent in the cloud account you want to monitor.


## Agentless deployment [cspm-azure-agentless]

1. Find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Search for `CSPM`, then click on the result.
3. Click **Add Cloud Security Posture Management (CSPM)**.
4. Select **Azure**, then either **Azure Organization** to onboard your whole organization, or **Single Subscription** to onboard an individual subscription.
5. Give your integration a name and description that match the purpose or team of the Azure subscription/organization you want to monitor, for example, `dev-azure-account`.
6. (Optional) Expand the **Advanced options** menu and add a `Namespace` to the integration's data stream.

:::{include} _snippets/cspm-namespace.md
:::

7. For **Deployment options**, select **Agentless**.
8. Next, you’ll need to authenticate to Azure. The following methods are available:
    
    * Option 1: Cloud connector (recommended). {applies_to}`stack: preview 9.2` {applies_to}`serverless: preview`  
      Under **New connection**, expand the **Steps to create Managed User Identity in Azure** section. Complete the instructions to generate a `Client ID`, `Tenant ID`, and `Cloud Connector ID`, then enter them in {{kib}}.
    
    * Option 2: Azure Client ID with Client Secret. Provide a **Client ID**, **Tenant ID**, and **Client Secret**. To learn how to generate them, refer to [Service principal with client secret](/solutions/security/cloud/get-started-with-cspm-for-azure.md#cspm-azure-client-secret).


9. Once you’ve provided the necessary credentials, click **Save and continue** to finish deployment. Your data should start to appear within a few minutes.

## Agent-based deployment [cspm-azure-agent-based]


### Add your CSPM integration [cspm-add-and-name-integration-azure]

1. Find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Search for `CSPM`, then click on the result.
3. Click **Add Cloud Security Posture Management (CSPM)**.
4. In **Configure integration**, select **Azure**, then select either **Azure Organization** or **Single Subscription**, depending on which resources you want to monitor.
5. Give your integration a name that matches the purpose or team of the Azure resources you want to monitor, for example, `azure-CSPM-dev-1`.
6. (Optional) under **Advanced options**, you can add a `Namespace` to the integration's data stream.

:::{include} _snippets/cspm-namespace.md
:::
7. Under **Deployment options** select **Agent-based**.


### Set up cloud account access [cspm-set-up-cloud-access-section-azure]

::::{note}
To set up CSPM for an Azure organization or subscription, you will need admin privileges for that organization or subscription.
::::


For most users, the simplest option is to use an Azure Resource Manager (ARM) template to automatically provision the necessary resources and permissions in Azure. If you prefer a more hands-on approach or require a specific configuration not supported by the ARM template, you can use one of the manual setup options described on this page.


## ARM template setup (recommended) [cspm-set-up-ARM]

::::{note}
If you are deploying to an Azure organization, you need the following permissions: `Microsoft.Resources/deployments/*`, `Microsoft.Authorization/roleAssignments/write`. You also need to [elevate access to manage all Azure subscriptions and management groups](https://learn.microsoft.com/en-us/azure/role-based-access-control/elevate-access-global-admin).
::::


1. For **Setup Access**, select **ARM Template**.
2. In **Where to add this integration**:

    1. Select **New Hosts**.
    2. Name the {{agent}} policy. Use a name that matches the resources you want to monitor. For example, `azure-dev-policy`. Click **Save and continue**. The **ARM Template deployment** window appears.
    3. In a new tab, log in to the Azure portal, then return to {{kib}} and click **Launch ARM Template**. This will open the ARM template in Azure.
    4. If you are deploying to an Azure organization, select the management group you want to monitor from the drop-down menu. Next, enter the subscription ID of the subscription where you want to deploy the VM that will scan your resources.
    5. Copy the `Fleet URL` and `Enrollment Token` that appear in {{kib}} to the corresponding fields in the ARM Template, then click **Review + create**.
    6. (Optional) Change the `Resource Group Name` parameter. Otherwise the name of the resource group defaults to a timestamp prefixed with `cloudbeat-`.

3. Return to {{kib}} and wait for the confirmation of data received from your new integration. Then you can click **View Assets** to see your data.


## Manual setup [cspm-set-up-manual-azure]

For manual setup, multiple authentication methods are available:

* Managed identity (recommended)
* Service principal with client secret
* Service principal with client certificate


### Option 1: Managed identity (recommended) [cspm-azure-managed-identity-setup]

This method involves creating an Azure VM (or using an existing one), giving it read access to the resources you want to monitor with CSPM, and installing {{agent}} on it.

1. Go to the Azure portal to [create a new Azure VM](https://portal.azure.com/#create/Microsoft.VirtualMachine-ARM).
2. Follow the setup process, and make sure you enable **System assigned managed identity** in the **Management** tab.
3. Go to your Azure subscription list and select the subscription or management group you want to monitor with CSPM.
4. Go to **Access control (IAM)**, and select **Add Role Assignment**.
5. Select the `Reader` function role, assign access to **Managed Identity**, then select your VM.

After assigning the role:

1. Return to the **Add CSPM** page in {{kib}}.
2. For **Configure integration**, select **Azure**. For **Setup access**, select **Manual**.
3. For **Where to add this integration**, select **New hosts**.
4. Click **Save and continue**, then follow the instructions to install {{agent}} on your Azure VM.

Wait for the confirmation that {{kib}} received data from your new integration. Then you can click **View Assets** to see your data.


### Option 2: Service principal with client secret [cspm-azure-client-secret]

Before using this method, you must have set up a [Microsoft Entra application and service principal that can access resources](https://learn.microsoft.com/en-us/entra/identity-platform/howto-create-service-principal-portal#get-tenant-and-app-id-values-for-signing-in).

1. On the **Add Cloud Security Posture Management (CSPM) integration** page, scroll to the **Setup access** section, then select **Manual**.
2. For **Preferred manual method**, select **Service principal with Client Secret**.
3. Go to the **Registered apps** section of [Microsoft Entra ID](https://ms.portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/RegisteredApps).
4. Click on **New Registration**, name your app and click **Register**.
5. Copy your new app’s `Directory (tenant) ID` and `Application (client) ID`. Paste them into the corresponding fields in {{kib}}.
6. Return to the Azure portal. Select **Certificates & secrets**, then go to the **Client secrets** tab. Click **New client secret**.
7. Copy the new secret. Paste it into the corresponding field in {{kib}}.
8. Return to Azure. Go to your Azure subscription list and select the subscription or management group you want to monitor with CSPM.
9. Go to **Access control (IAM)** and select **Add Role Assignment**.
10. Select the `Reader` function role, assign access to **User, group, or service principal**, and select your new app.
11. Return to the **Add CSPM** page in {{kib}}.
12. For **Where to add this integration**, select **New hosts**.
13. Click **Save and continue**, then follow the instructions to install {{agent}} on your selected host.

Wait for the confirmation that {{kib}} received data from your new integration. Then you can click **View Assets** to see your data.


### Option 3: Service principal with client certificate [cspm-azure-client-certificate]

Before using this method, you must have set up a [Microsoft Entra application and service principal that can access resources](https://learn.microsoft.com/en-us/entra/identity-platform/howto-create-service-principal-portal#get-tenant-and-app-id-values-for-signing-in).

1. On the **Add Cloud Security Posture Management (CSPM) integration** page, for **Setup access**, select **Manual**.
2. For **Preferred manual method**, select **Service principal with client certificate**.
3. Go to the **Registered apps** section of [Microsoft Entra ID](https://ms.portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/RegisteredApps).
4. Click on **New Registration**, name your app and click **Register**.
5. Copy your new app’s `Directory (tenant) ID` and `Application (client) ID`. Paste them into the corresponding fields in {{kib}}.
6. Return to Azure. Go to your Azure subscription list and select the subscription or management group you want to monitor with CSPM.
7. Go to **Access control (IAM)** and select **Add Role Assignment**.
8. Select the `Reader` function role, assign access to **User, group, or service principal**, and select your new app.

Next, create a certificate. If you intend to use a password-protected certificate, you must use a pkcs12 certificate. Otherwise, you must use a pem certificate.

Create a pkcs12 certificate, for example:

```shell
# Create PEM file
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Create pkcs12 bundle using legacy flag (CLI will ask for export password)
openssl pkcs12 -legacy -export -out bundle.p12 -inkey key.pem -in cert.pem
```

Create a PEM certificate, for example:

```shell
# Generate certificate signing request (csr) and key
openssl req -new -newkey rsa:4096 -nodes -keyout cert.key -out cert.csr

# Generate PEM and self-sign with key
openssl x509 -req -sha256 -days 365 -in cert.csr -signkey cert.key -out signed.pem

# Create bundle
cat cert.key > bundle.pem
cat signed.pem >> bundle.pem
```

After creating your certificate:

1. Return to Azure.
2. Navigate to the **Certificates & secrets** menu. Select the **Certificates** tab.
3. Click **Upload certificate**.

    1. If you’re using a PEM certificate that was created using the example commands above, upload `signed.pem`.
    2. If you’re using a pkcs12 certificate that was created using the example commands above, upload `cert.pem`.

4. Upload the certificate bundle to the VM where you will deploy {{agent}}.

    1. If you’re using a PEM certificate that was created using the example commands above, upload `bundle.pem`.
    2. If you’re using a pkcs12 certificate that was created using the example commands above, upload `bundle.p12`.

5. Return to the **Add CSPM** page in {{kib}}.
6. For **Client Certificate Path**, enter the full path to the certificate that you uploaded to the host where you will install {{agent}}.
7. If you used a pkcs12 certificate, enter its password in **Client Certificate Password**.
8. For **Where to add this integration**, select **New hosts**.
9. Click **Save and continue**, then follow the instructions to install {{agent}} on your selected host.

Wait for the confirmation that {{kib}} received data from your new integration. Then you can click **View Assets** to see your data.
