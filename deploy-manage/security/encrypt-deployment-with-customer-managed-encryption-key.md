---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-encrypt-with-cmek.html
---

# Encrypt your deployment with a customer-managed encryption key [ec-encrypt-with-cmek]

By default, Elastic already encrypts your deployment data and snapshots at rest. You can reinforce this mechanism by providing your own encryption key, also known as Bring Your Own Key (BYOK). To do that, you need a customer-managed key that you set up and manage in your cloud provider’s Key Management Service (KMS).

::::{note}
Encryption at rest using customer-managed keys is only available for the Enterprise subscription level, when creating new deployments. The ability to edit encryption settings for existing deployments will be supported at a later date.
::::


Using a customer-managed key allows you to strengthen the security of your deployment data and snapshot data at rest. Note that if you use a custom snapshot repository different from the one provided by Elastic Cloud, these snapshots are not encrypted with your customer-managed key by default. The encryption happens at the file system level.


## How using a customer-managed key helps to improve your data security [ec_how_using_a_customer_managed_key_helps_to_improve_your_data_security]

Using a customer-managed key helps protect against threats related to the management and control of encryption keys. It does not directly protect against any specific types of attacks or threats. However, the ability to keep control over your own keys can help mitigate certain types of threats such as:

* **Insider threats.** By using a customer-managed key, Elastic does not have access to your encryption keys [1]. This can help prevent unauthorized access to data by insiders with malicious intent.
* **Compromised physical infrastructure.** If a data center is physically compromised, the hosts are shut off. With customer-managed key encryption, that’s a second layer of protection that any malicious intruder would have to bypass, in addition to the existing built-in hardware encryption.

Using a customer-managed key can help comply with regulations or security requirements, but it is not a complete security solution by itself. There are other types of threats that it does not protect against.

[1] You set up your customer-managed keys and their access in your key management service. When you provide a customer-managed key identifier to Elastic Cloud, we do not access or store the cryptographic material associated with that key. Customer-managed keys are not directly used to encrypt deployment or snapshot data. Elastic Cloud accesses your customer-managed keys to encrypt and decrypt data encryption keys, which, in turn, are used to encrypt the data.

When a deployment encrypted with a customer-managed key is deleted or terminated, its data is locked first before being deleted, ensuring a fully secure deletion process.


## Prerequisites [ec_prerequisites_3]

:::::::{tab-set}

::::::{tab-item} AWS
* Have permissions on AWS KMS to [create a symmetric AWS KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.md#symmetric-cmks) and to configure AWS IAM roles.
* Consider the cloud regions where you need your deployment to live. Refer to the [list of available regions, deployment templates, and instance configurations](asciidocalypse://docs/cloud/docs/reference/cloud-hosted/ec-regions-templates-instances.md) supported by Elastic Cloud.
::::::

::::::{tab-item} Azure
* Have the following permissions on Azure:

    * Permissions to [create an RSA key](https://learn.microsoft.com/en-us/azure/key-vault/keys/about-keys#key-types-and-protection-methods) in the Azure Key Vault where you want to store your key.
    * Membership in the **Application Administrator** role. This is required to create a new service principal for Elastic Cloud in your Azure tenant.
    * Permissions to [assign roles in your Key Vault using Access control (IAM)](https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide?tabs=azure-cli#prerequisites). This is required to grant the service principal access to your key.

* The Azure Key Vault where the RSA key will be stored must have [purge protection](https://learn.microsoft.com/en-us/azure/key-vault/general/soft-delete-overview#purge-protection) enabled to support the encryption of snapshots.
* Consider the cloud regions where you need your deployment to live. Refer to the [list of available regions, deployment templates, and instance configurations](asciidocalypse://docs/cloud/docs/reference/cloud-hosted/ec-regions-templates-instances.md) supported by Elastic Cloud.
::::::

::::::{tab-item} Google Cloud
* Consider the cloud regions where you need your deployment to live. Refer to the [list of available regions, deployment templates, and instance configurations](asciidocalypse://docs/cloud/docs/reference/cloud-hosted/ec-regions-templates-instances.md) supported by Elastic Cloud.
* Have the following permissions in Google Cloud KMS:

    * Permissions to [create a KMS key](https://cloud.google.com/kms/docs/create-key) on a key ring in the same region as your deployment. If you don’t have a key ring in the same region, or want to store the key in its own key ring, then you also need permissions to [create a key ring](https://cloud.google.com/kms/docs/create-key-ring).
    * Permissions to [manage access to your new key resource using IAM](https://cloud.google.com/kms/docs/iam). This is required to grant the service principals used by Elastic access to your key.
::::::

:::::::

## Know before you go [ec_know_before_you_go]

At this time, the following features are not supported:

* Encrypting existing deployments with a customer-managed key
* Disabling encryption on a deployment
* AWS:

    * Encrypting deployments using keys from [key stores external to AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/keystore-external.md)

* Azure:

    * Encrypting deployments using Azure EC or symmetric keys
    * Encrypting deployments using keys from [key stores external to Azure Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/keys/byok-specification)

* Google Cloud:

    * Encrypting deployments using [key stores external to Cloud KMS](https://cloud.google.com/kms/docs/ekm)



## Create an encryption key for your deployment [create-encryption-key]

:::::::{tab-set}

::::::{tab-item} AWS
1. Create a symmetric [single-region key](https://docs.aws.amazon.com/kms/latest/developerguide/create-keys.md) or [multi-region replica key](https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-replicate.md). The key must be available in each region in which you have deployments to encrypt. You can use the same key to encrypt multiple deployments. Later, you will need to provide the Amazon Resource Name (ARN) of that key or key alias to Elastic Cloud.

    ::::{note}
    Use an alias ARN instead of the key ARN itself if you plan on doing manual key rotations. When using a key ARN directly, only automatic rotations are supported.
    ::::

2. Apply a key policy with the settings required by Elastic Cloud to the key created in the previous step:

    ```json
    {
      "Sid": "ElasticKeyAccess",
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": [
        "kms:Decrypt", <1>
        "kms:Encrypt", <2>
        "kms:GetKeyRotationStatus", <3>
        "kms:GenerateDataKey", <4>
        "kms:DescribeKey" <5>
      ],
      "Resource": "*",
      "Condition": { <6>
        "ForAnyValue:StringLike": {
          "aws:PrincipalOrgPaths": "o-ygducmlz12/r-e5t3/ou-e5t3-fzpdq76p/ou-e5t3-ysfcmd95/ou-e5t3-hwt05su3/*"
       }
     }
    }
    ```

    1. [kms:Decrypt](https://docs.aws.amazon.com/kms/latest/APIReference/API_Decrypt.md) - This operation is used to decrypt data encryption keys stored on the deployment’s host, as well as decrypting snapshots stored in S3.
    2. [kms:Encrypt](https://docs.aws.amazon.com/kms/latest/APIReference/API_Encrypt.md) - This operation is used to encrypt the data encryption keys generated by the KMS as well as encrypting your snapshots.
    3. [kms:GetKeyRotationStatus](https://docs.aws.amazon.com/kms/latest/APIReference/API_GetKeyRotationStatus.md) - This operation is used to determine whether automatic key rotation is enabled.
    4. [kms:GenerateDataKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_GenerateDataKey.md) - This operation is used to generate a data encryption key along with an encrypted version of it. The system leverages the randomness provided by the KMS to produce the data encryption key and your actual customer-managed key to encrypt the data encryption key.
    5. [kms:DescribeKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.md) - This operation is used to check whether your key is properly configured for Elastic Cloud. In addition, Elastic Cloud uses this to check if a manual key rotation was performed by comparing underlying key IDs associated with an alias.
    6. This condition allows the accounts associated with the Elastic Cloud production infrastructure to access your key. Under typical circumstances, Elastic Cloud will only be accessing your key via two AWS accounts: the account your deployment’s host is in and the account your S3 bucket containing snapshots is in. However, determining these particular account IDs prior to the deployment creation is not possible at the moment. This encompasses all of the possibilities. For more on this, check the [AWS documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.md#condition-keys-principalorgpaths).
::::::

::::::{tab-item} Azure
1. Create an RSA key in your Key Vault. The key must be available in each region in which you have deployments to encrypt. You can use the same key to encrypt multiple deployments.
2. After the key is created, view the key and note the key identifier. It should look similar to the following:

    * `https://example-byok-key-vault.vault.azure.net/keys/test-key` (without version identifier)
    * `https://example-byok-key-vault.vault.azure.net/keys/test-key/1234` (with version identifier)

        Later, you will need to provide this identifier to Elastic Cloud.


::::{tip}
Provide your key identifier without the key version identifier so Elastic Cloud can [rotate the key](#rotate-a-customer-managed-key) on your behalf.
::::
::::::

::::::{tab-item} Google Cloud
1. [Create a new symmetric key](https://cloud.google.com/kms/docs/create-key) in Google Cloud KMS.

    The key must be in a key ring that’s in the same region as your deployment. Do not use key ring in a multi-region location.

2. After the key is created, view the key and [note its resource ID](https://cloud.google.com/kms/docs/getting-resource-ids#getting_the_id_for_a_key_and_version). The resource ID uses the following format:

    `projects/PROJECT_ID/locations/LOCATION/keyRings/KEY_RING/cryptoKeys/KEY_NAME`

    Later, you will need to provide this ID to Elastic Cloud.
::::::

:::::::

## Create a deployment encrypted with your key [ec_create_a_deployment_encrypted_with_your_key]

:::::::{tab-set}

::::::{tab-item} AWS
1. Create a new deployment. You can do it from the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), or from the API:

    * from the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body):

        * Select **Create deployment** from the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) home page.
        * In the **Settings**, set the **Cloud provider** to **Amazon Web Services** and select a region.
        * Expand the **Advanced settings** and turn on **Use a customer-managed encryption key**. An additional field appears to let you specify the ARN of the AWS KMS key or key alias you will use to encrypt your new deployment.
        * Configure the rest of your deployment to your convenience, and select **Create deployment**.

    * using the API:

        * Choose a **cloud region** and a **deployment template** (also called hardware profile) for your deployment from the [list of available regions, deployment templates, and instance configurations](asciidocalypse://docs/cloud/docs/reference/cloud-hosted/ec-regions-templates-instances.md).
        * [Get a valid Elastic Cloud API key](/deploy-manage/api-keys/elastic-cloud-api-keys.md) with the **Organization owner** role or the **Admin** role on deployments. These roles allow you to create new deployments.
        * Get the ARN of the symmetric AWS KMS key or of its alias. Use an alias if you are planning to do manual key rotations as specified in the [AWS documentation](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.md).
        * Use these parameters to create a new deployment with the [Elastic Cloud API](https://www.elastic.co/docs/api/doc/cloud/group/endpoint-deployments). For example:

            ```bash
            curl -XPOST \
            -H 'Content-Type: application/json' \
            -H "Authorization: ApiKey <replace with encoded API key>" \
            "https://api.elastic-cloud.com/api/v1/deployments?template_id=<replace with desired template ID>" \
            -d '
            {
              "name": "my-deployment",
              "version": "8.15.0",
              "region": "us-east-1",
              "settings": {
                "byok": {
                  "key_resource_path": "<replace with your key or alias ARN>"
                }
              }
            }
            ```

            ::::{tip}
            You can also create the deployment from a snapshot of a deployment that was initially not encrypted with a customer-managed key. You can use this as a workaround to encrypt existing data under new deployments using your key, until encrypting existing deployments with a customer-managed key is supported.
            ::::


The deployment is now created and encrypted using the specified key. Future snapshots will also be encrypted using that key.
::::::

::::::{tab-item} Azure
To create a new deployment with a customer-managed key in Azure, you need to perform actions in Elastic Cloud and in your Azure tenant.

**Step 1: Create a service principal for Elastic Cloud**

1. In Elastic Cloud, retrieve the Azure application ID:

    * Select **Create deployment** from the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) home page.
    * In the **Settings**, set the **Cloud provider** to **Azure** and select a region.
    * Expand the **Advanced settings** and turn on **Use a customer-managed encryption key**.
    * Copy the **Azure application ID**.

2. Using the ID that you copied, [create a new service principal](https://learn.microsoft.com/en-us/azure/storage/common/customer-managed-keys-configure-cross-tenant-existing-account?tabs=azure-portal#the-customer-installs-the-service-provider-application-in-the-customer-tenant) for Elastic Cloud in your Azure tenant. The service principal grants Elastic Cloud access to interact with your RSA key.

    For example, you might use the following Azure CLI command to create the service principal:

    ```bash
    az ad sp create --id <azure application ID>
    ```

    ::::{tip}
    The user performing this action needs to belong to the **Application Administrator** role.
    ::::


    After it’s created, the service principal appears as `ess-byok-multitenant-app-production` in your Azure tenant.

3. In your Azure Portal, view the key [that you created](#create-encryption-key). In the **Access control (IAM)** settings for the key, grant the service principal the role **Key Vault Crypto User**.

**Step 2: Create your deployment**<br>

After you have created the service principal and granted it the necessary permissions, you can finish creating your deployment. You can do so from the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), or from the API.

* Using the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body):

    * Select **Create deployment** from the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) home page.
    * In the **Settings**, set the **Cloud provider** to **Azure** and select a region.
    * Expand the **Advanced settings** and turn on **Use a customer-managed encryption key**.
    * Enter the Azure key identifier for the RSA key that you created.
    * Configure the rest of your deployment according to your requirements, and then select **Create deployment**.

* Using the API:

    * Choose a **cloud region** and a **deployment template** (also called hardware profile) for your deployment from the [list of available regions, deployment templates, and instance configurations](asciidocalypse://docs/cloud/docs/reference/cloud-hosted/ec-regions-templates-instances.md).

        * [Get a valid Elastic Cloud API key](/deploy-manage/api-keys/elastic-cloud-api-keys.md) with the **Organization owner** role or the **Admin** role on deployments. These roles allow you to create new deployments.
        * Use these parameters to create a new deployment with the [Elastic Cloud API](https://www.elastic.co/docs/api/doc/cloud/group/endpoint-deployments). For example:

            ```bash
            curl -XPOST \
            -H 'Content-Type: application/json' \
            -H "Authorization: ApiKey <replace with encoded API key>" \
            "https://api.elastic-cloud.com/api/v1/deployments?template_id=<replace with desired template ID>" \
            -d '
            {
              "name": "my-deployment",
              "version": "8.15.0",
              "region": "azure-eastus",
              "settings": {
                "byok": {
                  "key_resource_path": "<replace with your Azure key identifier>"
                }
              }
            }
            ```

            ::::{tip}
            You can also create the deployment from a snapshot of a deployment that was initially not encrypted with a customer-managed key. You can use this as a workaround to encrypt existing data under new deployments using your key, until encrypting existing deployments with a customer-managed key is supported.
            ::::


The deployment is now created and encrypted using the specified key. Future snapshots will also be encrypted using that key.
::::::

::::::{tab-item} Google Cloud
**Step 1: Grant service principals access to your key**

Elastic Cloud uses two service principals to encrypt and decrypt data using your key. You must grant these services access to your key before you create your deployment.

* **Google Cloud Platform cloud storage service agent**: Used for Elastic-managed snapshots stored on Google Cloud Storage.
* **Elastic service account**: Used for all other Elasticsearch data.

1. In Elastic Cloud, retrieve the email addresses for the service principals that will be used by Elastic:

    * Select **Create deployment** from the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) home page.
    * In the **Settings**, set the **Cloud provider** to **Google Cloud** and select a region.
    * Expand the **Advanced settings** and turn on **Use a customer-managed encryption key**.
    * Note the **Elastic service account** and **Google Cloud Platform storage service agent** email addresses.

2. For each email address that you copied, [grant them](https://cloud.google.com/kms/docs/iam#granting_roles_on_a_resource) the following roles on the key resource:

    * **Elastic service account**:

        * `cloudkms.cryptoKeyVersions.useToDecrypt`
        * `cloudkms.cryptoKeyVersions.useToEncrypt`
        * `cloudkms.cryptoKeys.get`

    * **Google Cloud Platform cloud storage service agent**:

        * `cloudkms.cryptoKeyVersions.useToDecrypt`
        * `cloudkms.cryptoKeyVersions.useToEncrypt`


::::{tip}
The user performing this action needs to belong to the **Owner** or **Cloud KMS Admin** role.
::::


**Step 2: Create your deployment**

After you have granted the Elastic principals the necessary roles, you can finish creating your deployment. You can do so from the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), or from the API.

* Using the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body):

    * Select **Create deployment** from the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) home page.
    * In the **Settings**, set the **Cloud provider** to **Google Cloud** and select a region.
    * Expand the **Advanced settings** and turn on **Use a customer-managed encryption key**.
    * Enter the resource ID for the key that you created.
    * Configure the rest of your deployment according to your requirements, and then select **Create deployment**.

* Using the API:

    * Choose a **cloud region** and a **deployment template** (also called hardware profile) for your deployment from the [list of available regions, deployment templates, and instance configurations](asciidocalypse://docs/cloud/docs/reference/cloud-hosted/ec-regions-templates-instances.md).

        * [Get a valid Elastic Cloud API key](/deploy-manage/api-keys/elastic-cloud-api-keys.md) with the **Organization owner** role or the **Admin** role on deployments. These roles allow you to create new deployments.
        * Use these parameters to create a new deployment with the [Elastic Cloud API](https://www.elastic.co/docs/api/doc/cloud/group/endpoint-deployments). For example:

            ```bash
            curl -XPOST \
            -H 'Content-Type: application/json' \
            -H "Authorization: ApiKey <replace with encoded API key>" \
            "https://api.elastic-cloud.com/api/v1/deployments?template_id=<replace with desired template ID>" \
            -d '
            {
              "name": "my-deployment",
              "version": "8.15.0",
              "region": "gcp-us-east1",
              "settings": {
                "byok": {
                  "key_resource_path": "<replace with your Google Cloud resource ID>"
                }
              }
            }
            ```

            ::::{tip}
            You can also create the deployment from a snapshot of a deployment that was initially not encrypted with a customer-managed key. You can use this as a workaround to encrypt existing data under new deployments using your key, until encrypting existing deployments with a customer-managed key is supported.
            ::::


The deployment is now created and encrypted using the specified key. Future snapshots will also be encrypted using that key.
::::::

:::::::
You can check that your hosted deployment is correctly encrypted with the key you specified. To do that, go to the deployment’s **Security** page and select **Manage encryption key** in **Encryption at rest**.


## Rotate a customer-managed key [rotate-a-customer-managed-key]

:::::::{tab-set}

::::::{tab-item} AWS
Elastic Cloud will automatically rotate the keys every 31 days as a security best practice.

You can also trigger a manual rotation [in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.md), which will take effect in Elastic Cloud within 30 minutes. **For manual rotations to work, you must use an alias when creating the deployment. We do not currently support [on-demand rotations](https://docs.aws.amazon.com/kms/latest/APIReference/API_RotateKeyOnDemand.md) but plan on supporting this in the future.**
::::::

::::::{tab-item} Azure
To rotate your key, you can [update your key version](https://learn.microsoft.com/en-us/azure/container-registry/tutorial-rotate-revoke-customer-managed-keys) or [configure a key rotation policy](https://learn.microsoft.com/en-us/azure/key-vault/keys/how-to-configure-key-rotation) in Azure Key Vault. In both cases, the rotation will take effect in Elastic Cloud within a day.

For rotations to work, you must provide your key identifier without the key version identifier when you create your deployment.

Elastic Cloud does not currently support rotating your key using a new key identifier.
::::::

::::::{tab-item} Google Cloud
Key rotations are triggered in Google Cloud. You can rotate your key [manually](https://cloud.google.com/kms/docs/rotate-key#manual) or [automatically](https://cloud.google.com/kms/docs/rotate-key#automatic). In both cases, the rotation will take effect in Elastic Cloud within a day.
::::::

:::::::

## Revoke a customer-managed key [ec_revoke_a_customer_managed_key]

Revoking a customer-managed key in your key management service can be a break-glass procedure in case of a security breach. Elastic Cloud gets an error if an encryption key is disabled, deleted, or if the appropriate role is removed from the IAM policy. Within 30 minutes maximum, Elastic Cloud locks the directories in which your deployment data live and prompts you to delete your deployment as an increased security measure.

If that happens and this is not intended, you can restore the key in the key management system. Your deployment operations will resume when the key can be reached again. For more details, check [Troubleshooting](#ec-encrypt-with-cmek-troubleshooting).

When a customer-managed key is permanently revoked and isn’t restored, the data stored in Elastic Cloud is effectively crypto-shredded.

In a future release of Elastic Cloud, you will be able to:

* Remove a customer-managed key and revert your deployment to using an Elastic-managed encryption.
* Edit the customer-managed key in use in a deployment to re-encrypt it with a different key.


## Encrypt an existing deployment using a new customer-managed key [ec_encrypt_an_existing_deployment_using_a_new_customer_managed_key]

Encrypting deployments with a customer-managed key is currently only possible for new deployments. In a future release of Elastic Cloud, you will be able to:

* Encrypt an existing Elastic Cloud deployment with a customer-managed key.
* Edit the customer-managed key in use in a deployment to re-encrypt it with a different key.


## Troubleshooting [ec-encrypt-with-cmek-troubleshooting]

**My deployment became inaccessible. What’s causing this?**

When Elastic Cloud can’t reach the encryption key, your deployment may become inaccessible. The most common reasons for this issue are:

* Connectivity issues between Elastic Cloud and the KMS.<br>

    When Elastic Cloud is unable to access the customer-managed key, Elastic is alerted and will work to identify the cause. Elastic does not pause or terminate deployment instances when detecting connectivity issues, but your deployment may be inaccessible until issues are fixed.

* The customer-managed key was deleted or revoked on the KMS.<br>

    Restore or recover your key, and if need be, rotate your key and associate a new key before deleting your old key. Elastic Cloud will send you alerts prompting you to restore the key if it cannot access your key and your deployment is not operational.<br>

    Within 30 minutes maximum, Elastic Cloud locks the directories in which your deployment data live and prompts you to delete your deployment as an increased security measure.<br>

    While it is locked, the deployment retains all data but is not readable or writable*:

    * If access to the key is never restored, the deployment data does not become accessible again
    * When restoring access to the key, the deployment becomes operational again:

        * If Elastic didn’t have to perform any platform operations on your instances during the locked period, operations are restored with minimum downtime.
        * If Elastic performed some platform operations on your instances during the locked period, restoring operations can require some downtime. It’s also possible that some data can’t be restored** depending on the available snapshots.


**During the locked directory period, Elastic may need to perform platform operations on the machines hosting your instances that result in data loss on the Elasticsearch data nodes but not the deployment snapshots.*

***Elastic recommends that you keep snapshots of your deployment in custom snapshot repositories in your own CSP account for data recovery purposes.*
