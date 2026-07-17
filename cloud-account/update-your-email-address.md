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

If you have separate {{ecloud}} accounts for different organizations and want to consolidate to a single account, ask an organization owner in each organization to [reconcile your accounts](/deploy-manage/cloud-organization/manage-multiple-organizations.md#reconcile-email).

:::{note}
If you belong to any organization that enforces a specific authentication method (such as SAML SSO, Google Sign-In, or Microsoft Sign-In), you can't change your primary email address using the procedures on this page. This restriction applies even if other organizations you belong to don't enforce a login method.
:::

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

## Changing your email address with a Microsoft Marketplace account

If your organization is associated with [Microsoft Marketplace](../deploy-manage/deploy/elastic-cloud/azure-native-isv-service.md), you can’t change your primary email address using the above methods. Instead, [invite another user](../deploy-manage/users-roles/cloud-organization/manage-users.md) with the desired email address to join your organization.