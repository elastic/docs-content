---
applies_to:
  deployment:
    ess: preview
products:
  - id: cloud-hosted
navigation_title: Customer-managed encryption keys
---

# Customer-managed encryption keys for Azure Native Service [azure-native-isv-service-byok]

{{ech}} deployments created through the Azure Native Service are full-featured deployments that support the same security capabilities as any other {{ech}} deployment.

By default, Elastic already encrypts your deployment data and snapshots at rest. You can reinforce this mechanism by providing your own encryption key, also known as Bring Your Own Key (BYOK). For a full description of how this works and the security benefits it provides, refer to [Use a customer-managed encryption key](/deploy-manage/security/encrypt-deployment-with-customer-managed-encryption-key.md).

BYOK is not available as a configuration option when creating a deployment from the Azure portal. You can add a customer-managed key to your deployment after it is created, by accessing the {{ecloud}} console.

## Prerequisites

Before configuring BYOK, you need an RSA key in Azure Key Vault and the necessary permissions to create a service principal for {{ecloud}} in your Azure tenant. Refer to [BYOK prerequisites](/deploy-manage/security/encrypt-deployment-with-customer-managed-encryption-key.md#ec_prerequisites_3) for the full list.

## Add a customer-managed key to your deployment

1. In the Azure portal, navigate to your deployment's overview page.
2. Select the **Advanced Settings** link to open the {{ecloud}} console.
3. Follow the steps in [Encrypt an existing deployment with your key](/deploy-manage/security/encrypt-deployment-with-customer-managed-encryption-key.md#ec_encrypt_an_existing_deployment_with_a_customer_managed_key) to configure your deployment to use your key.
