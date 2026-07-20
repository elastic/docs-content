---
description: Change the Kibana interface language from your user menu or profile.
applies_to:
  stack: beta 9.5
  serverless: beta
products:
  - id: kibana
  - id: cloud-serverless
type: how-to
---


# Change the interface language in Kibana

Kibana can display its interface in several languages. From the application header, you can select the language you prefer. The languages available to you depend on what the deployment administrator has enabled.

:::{tip}
If you're using {{ecloud}}, this setting only applies to the Kibana UI of your serverless projects and hosted deployments.
:::

## Before you begin

- You must be signed in to Kibana.
- Your deployment must offer at least one language in the per-user language picker. If you don't see a **Language** option, an administrator has disabled the picker for your deployment.

## Change your interface language

1. Open the user menu from the header.
2. Select **Language**.

   :::{note}
   On self-managed deployments of {{kib}}, this option is located on your profile page. To access it, select **Edit profile** from the header's user menu, then find the **Language** section.
   :::

3. Select your preferred language from the **Display language** menu.
4. Select **Save changes**.
5. Refresh the page to apply the selected language.

After you save, Kibana shows a confirmation that the language settings were updated. The new language takes effect after you refresh the page.

## How Kibana picks a language

If you haven't saved a language preference, Kibana resolves the interface language in this order:

1. Your profile preference, if you have set one.
2. The language Kibana most recently used in this browser, stored in a `KBN_LOCALE` cookie.
3. An administrator-configured default language, when that default is set to a value other than English. This server-wide choice takes precedence over browser detection.
4. Your browser's preferred languages (from the `Accept-Language` header), when one of them matches a language enabled for the deployment. Matching can be exact or by language: for example, `fr` or `fr-CH` can resolve to a configured `fr-FR`.
5. The deployment's default language (English unless an administrator has changed it).

`KBN_LOCALE` is a strictly-necessary preference cookie. It does not track you, store identity, or enable cross-site activity. Kibana sets it automatically so anonymous pages and signed-out browsing can keep using the same language.

## Related pages

- [Use dark mode in Kibana](dark-mode.md)
- [Use high-contrast mode in Kibana](high-contrast.md)
- [Internationalization settings in Kibana](kibana://reference/configuration-reference/internationalization-settings.md): for administrators who configure available languages and the default locale
