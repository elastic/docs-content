---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-update-email-address.html
applies_to:
  serverless: ga
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Update your email address [ec-update-email-address]

Each {{ecloud}} account has a primary email associated with it. By default, the primary email address is used to sign up for {{ecloud}} and to log in. If needed, you can change this primary email address.

Your email address is used to uniquely identify you. It can’t be used for more than one {{ecloud}} account, whether that account is a trial account, a standard {{ecloud}} account, or a subscription account through a marketplace. However, a single {{ecloud}} account can belong to [multiple organizations](/cloud-account/switch-organizations.md).
 
## Change your email address (native sign-in)

If you log in using a standard email and password, follow these steps to update your email address:

1. To edit your account settings, select the user icon on the header bar and select **Settings**.
2. In the **Email address** section, select **edit**.
3. Enter a new email address and your current password.

    An email is sent to the new address with a link to confirm the change. If you don’t get the email after a few minutes, check your spam folder.

## Change your email address (Google or Microsoft sign-in)

If you log in using Google or Microsoft Sign-In, follow these steps to update your email address:

1. Go to the [Forgot password](https://cloud.elastic.co/forgot) page and enter your email address.
2. Follow the instructions in the "Reset your password" email.
3. In the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), update your [User settings](https://cloud.elastic.co/user/settings) to the new email address.

## Changing your email address with an Azure Marketplace account

If your organization is associated with [Azure Marketplace](../deploy-manage/deploy/elastic-cloud/azure-native-isv-service.md), you can’t change your primary email address using the above methods. Instead, [invite another user](../deploy-manage/users-roles/cloud-organization/manage-users.md) with the desired email address to join your organization.

## Sign up using an existing email address [sign-up-existing]

% is this still needed at all?

In some situations, you might want to create a new {{ecloud}} account using an email address that is already associated with an existing account. To sign up to {{ecloud}} using an email address associated with another {{ecloud}} account, you must remove the email address from your previous account and replace it with a new address.

:::{note}
You don't need to follow this procedure if you want to [join an additional organization](/cloud-account/join-or-leave-an-organization.md) or [create a new organization](/deploy-manage/cloud-organization/manage-multiple-organizations.md#create-a-new-organization). One account can belong to and own multiple organizations.
:::

1. Use your current email address (for example, `my.preferred.address@foobar.com`) to log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Follow the steps from one of the procedures on this page to update that email address to another email address, such as `my.alternate.address@gmail.com`.

You can now use the email address from step 1 to [sign up for a new account](/deploy-manage/deploy/elastic-cloud/create-an-organization.md).