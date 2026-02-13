In this document, we examine how to ingest logs from Azure services using Filebeat and Elastic Agent.

We specifically address a multi-tenant scenario where credentials are stored within tenant T1, while the actual log events reside in a separate tenant, T2.

## Overview

We’ll set up a multi-tenant app registration and client secret in T1, provision it in T2, and then grant the enterprise app in T2 the necessary permissions to access Event Hubs and the Storage Account.

<!-- TODO: Add image showing multi-tenant architecture diagram with T1 and T2 tenants, Event Hubs, and Storage Account -->

## Workflow

### Set up a multi-tenant app registration and client secret in T1

* Create an application  
  * Related HTTPS documentation: [Create application \- Microsoft Graph v1.0](https://learn.microsoft.com/en-us/graph/api/application-post-applications?view=graph-rest-1.0&tabs=http) 

```shell
# log into the T1 tenant
az login --tenant aaaaaaaa-1111-1111-1111-111111111111 # T1


$ az ad app create \
  --display-name "My Multi-Tenant App" \
  --sign-in-audience AzureADMultipleOrgs

{
  "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#applications/$entity",
  "addIns": [],
  "api": {
    "acceptMappedClaims": null,
    "knownClientApplications": [],
    "oauth2PermissionScopes": [],
    "preAuthorizedApplications": [],
    "requestedAccessTokenVersion": null
  },
  "appId": "cccccccc-3333-3333-3333-333333333333",

  [...]
}

```

<!-- TODO: Add screenshot of Azure Portal showing multi-tenant app registration -->

* Reset the application’s password  
  * [application: addPassword \- Microsoft Graph v1.0](https://learn.microsoft.com/en-us/graph/api/application-addpassword?view=graph-rest-1.0&tabs=http)

```shell
$ az ad app credential reset \
  --id cccccccc-3333-3333-3333-333333333333 \
  --append \
  --display-name "Production Secret" \
  --years 1

{
  "appId": "cccccccc-3333-3333-3333-333333333333",
  "password": "<redacted>",
  "tenant": "aaaaaaaa-1111-1111-1111-111111111111"
}

```

### Provision enterprise app in T2

```shell
az login --tenant bbbbbbbb-2222-2222-2222-222222222222 # T2
```

* Create Service Principal  
  * [Create serviceprincipal \- Microsoft Graph v1.0](https://learn.microsoft.com/en-us/graph/api/serviceprincipal-post-serviceprincipals?view=graph-rest-1.0&tabs=http)

```shell
$ az ad sp create --id cccccccc-3333-3333-3333-333333333333
{
  "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#servicePrincipals/$entity",
  "accountEnabled": true,
  "addIns": [],
  "alternativeNames": [],
  "appDescription": null,
  "appDisplayName": "My Multi-Tenant App",
  "appId": "cccccccc-3333-3333-3333-333333333333",
  "appOwnerOrganizationId": "aaaaaaaa-1111-1111-1111-111111111111",
  "appRoleAssignmentRequired": false,
  "appRoles": [],
  "applicationTemplateId": null,
  "createdDateTime": "2026-02-03T18:34:19Z",
  "deletedDateTime": null,
  "description": null,
  "disabledByMicrosoftStatus": null,
  "displayName": "My Multi-Tenant App",
  "homepage": null,
  "id": "dddddddd-4444-4444-4444-444444444444",
  "info": {
    "logoUrl": null,
    "marketingUrl": null,
    "privacyStatementUrl": null,
    "supportUrl": null,
    "termsOfServiceUrl": null
  },
  "keyCredentials": [],
  "loginUrl": null,
  "logoutUrl": null,
  "notes": null,
  "notificationEmailAddresses": [],
  "oauth2PermissionScopes": [],
  "passwordCredentials": [],
  "preferredSingleSignOnMode": null,
  "preferredTokenSigningKeyThumbprint": null,
  "replyUrls": [],
  "resourceSpecificApplicationPermissions": [],
  "samlSingleSignOnSettings": null,
  "servicePrincipalNames": [
    "cccccccc-3333-3333-3333-333333333333"
  ],
  "servicePrincipalType": "Application",
  "signInAudience": "AzureADMultipleOrgs",
  "tags": [],
  "tokenEncryptionKeyId": null,
  "verifiedPublisher": {
    "addedDateTime": null,
    "displayName": null,
    "verifiedPublisherId": null
  }
}

```

### Event Hubs and the Storage Account

First, we need to create an Event Hubs namespace and a Storage Account.

* [Resource Groups \- Create Or Update \- REST API (Azure Resource Management) | Microsoft Learn](https://learn.microsoft.com/en-us/rest/api/resources/resource-groups/create-or-update)

```shell
export RESOURCE_GROUP="contoso-multi-tenant-demo"
export AZURE_LOCATION="eastus2"
export AZURE_EVENTHUB_NAMESPACE="contoso-multi-tenant-demo"
export AZURE_STORAGE_ACCOUNT_NAME="contosomultitenantdemo"

# Create a brand new resource group to host the resources
az group create --name $RESOURCE_GROUP --location $AZURE_LOCATION
```

#### Event Hubs namespace

Next, we need to create the Event Hubs’ namespace and hub

* [Namespaces \- Create Or Update \- REST API (Azure Event Hubs) | Microsoft Learn](https://learn.microsoft.com/en-us/rest/api/eventhub/namespaces/create-or-update?view=rest-eventhub-2024-01-01&tabs=HTTP)  
* [Create Event Hub | Microsoft Learn](https://learn.microsoft.com/en-us/rest/api/eventhub/create-event-hub)

```shell

# Create an event hubs namespace
az eventhubs namespace create \
  --name $AZURE_EVENTHUB_NAMESPACE \
  --resource-group $RESOURCE_GROUP \
  --location $AZURE_LOCATION \
  --sku Basic \
  --capacity 1

# Create the event hub
az eventhubs eventhub create \
  --name logs \
  --namespace-name $AZURE_EVENTHUB_NAMESPACE \
  --resource-group $RESOURCE_GROUP \
  --partition-count 2 \
  --retention-time-in-hours 1 \
  --cleanup-policy Delete
```

#### Storage Account

Then, we create the storage account.

* [Create an Azure Storage account using the REST APIs | Microsoft Learn](https://learn.microsoft.com/en-us/rest/api/storagerp/storage-sample-create-account)  
* [Storage Accounts \- Create \- REST API (Azure Storage Account) | Microsoft Learn](https://learn.microsoft.com/en-us/rest/api/storagerp/storage-accounts/create?view=rest-storagerp-2023-05-01&tabs=HTTP) 

```shell
# Create a storage account
az storage account create \
  --name $AZURE_STORAGE_ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $AZURE_LOCATION \
  --sku Standard_LRS \
  --kind StorageV2
```

### Assign roles to the application

Let’s grant the permission to receive messages from the event hub and read/write blobs to the storage account.

* [Assign Azure roles using the REST API \- Azure RBAC | Microsoft Learn](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-rest)  
* [Role Assignments \- Create \- REST API (Azure Authorization) | Microsoft Learn](https://learn.microsoft.com/en-us/rest/api/authorization/role-assignments/create?view=rest-authorization-2022-04-01&tabs=HTTP) 

```shell
# Assign the "Azure Event Hubs Data Receiver" to the multi-tenant application.
az role assignment create \
  --role "Azure Event Hubs Data Receiver" \
  --assignee cccccccc-3333-3333-3333-333333333333 \
  --scope /subscriptions/eeeeeeee-5555-5555-5555-555555555555/resourceGroups/contoso-multi-tenant-demo/providers/Microsoft.EventHub/namespaces/contoso-multi-tenant-demo

# Assign the "Storage Blob Data Contributor" role
az role assignment create \
  --role "Storage Blob Data Contributor" \
  --assignee cccccccc-3333-3333-3333-333333333333 \
  --scope /subscriptions/eeeeeeee-5555-5555-5555-555555555555/resourceGroups/contoso-multi-tenant-demo/providers/Microsoft.Storage/storageAccounts/contosomultitenantdemo

```

### Collect logs using Filebeat

Here’s the Filebeat config file to access resources on T2 (or any other tenant) using the credentials on T1.

* [Azure eventhub input | Beats](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-input-azure-eventhub)

```
# x-pack/filebeat/filebeat.yml
filebeat.inputs:
- type: azure-eventhub
  enabled: true

  # The authentication type to use when connecting to Azure Event Hubs.
  #
  # Supported values are:
  # - connection_string (default)
  # - client_secret
  # 
  # Avaialble starting from Filebeat 8.19.10, 9.1.10, 9.2.4, or later.
  auth_type: client_secret
  
  # Entra ID (Azure AD tenant) and application (client) credentials.
  tenant_id: bbbbbbbb-2222-2222-2222-222222222222          # t2
  client_id: cccccccc-3333-3333-3333-333333333333          # t1
  client_secret: ${AZURE_CLIENT_SECRET}                    # t1

  # Event Hub configuration.  
  eventhub: logs
  eventhub_namespace: contoso-multi-tenant-demo.servicebus.windows.net  # t2
  consumer_group: $Default
  
  # Storage account information for checkpointing.
  storage_account: contosomultitenantdemo # t2

  # processor settings
  processor_version: v2
  migrate_checkpoint: true
  processor_update_interval: 10s
  processor_start_position: earliest
  partition_receive_timeout: 5s
  partition_receive_count: 100
```

Here’s an example of how to run Filebeat.

* [Filebeat command reference | Beats](https://www.elastic.co/docs/reference/beats/filebeat/command-line-options#run-command) 

```shell
filebeat -e -v -d "*" \
  --strict.perms=false \
  --path.home . \
  -E cloud.id=<redacted> \
  -E cloud.auth=<redacted> \
  -E gc_percent=100 \
  -E setup.ilm.enabled=false \
  -E setup.template.enabled=false \
  -E output.elasticsearch.allow_older_versions=true 
```

Next:

1. Posted a message to the event hub in T2  
   1. [Send event | Microsoft Learn](https://learn.microsoft.com/en-us/rest/api/eventhub/send-event)  
2. Received the same message

<!-- TODO: Add screenshot showing message sent to Event Hub and received successfully -->  




