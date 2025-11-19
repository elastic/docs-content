---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-change-login-method.html
applies_to:
  serverless: all
  deployment:
    ess: all
products:
  - id: cloud-hosted
---

# Add a login method [ec-change-login-method]

When you create your account, you can choose one of the the following methods to log in:

* A password-based login
* Log in with Google
* Log in with Microsoft

After your account is created, you and can an additional login method. You can’t remove a login method after it’s added.

:::{warning}
When you have both a password-based login and a social login like Google or Microsoft set up, logging in with Google or Microsoft will unset your password-based login password. The next time you use password-based login, you'll be asked to reset your password.
:::

## Enable password-based login [ec_enable_password_based_login]

To enable password-based login in addition to Google or Microsoft sign-in, go to the [Forgot password](https://cloud.elastic.co/forgot) page and enter your email address. This will trigger the forgot password flow and will allow you to create a password for your account.

After you create a password, log in. You’ll be prompted to [enable multifactor authentication](multifactor-authentication.md).

You will now be able to change the email address in your [user settings](https://cloud.elastic.co/user/settings). Refer to [Update your email address](/cloud-account/update-your-email-address.md) for more information.

## Enable Google or Microsoft sign-in [ec_enable_google_or_microsoft_sign_in]

To enable Google or Microsoft sign-in in addition to password-based login, go to the [Login](https://cloud.elastic.co/login) page and select **Log in with Google** or **Log in with Microsoft**.


