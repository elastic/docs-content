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


# Change the interface language in {{kib}}

{{kib}} can display its interface in several languages. From the application header, you can select the language you prefer. The languages available to you depend on what the deployment administrator has enabled.

:::{tip}
If you're using {{ecloud}}, this setting only applies to the {{kib}} UI of your serverless projects and hosted deployments.
:::

## Change your interface language

1. Open the user menu from the header.
2. Select **Language**.

   :::{note}
   :applies_to: self:
   On self-managed deployments of {{kib}}, this option is located on your profile page. To access it, select **Edit profile** from the header's user menu, then find the **Language** section.
   :::

3. Select your preferred language from the **Display language** menu.
4. Select **Save changes**.
5. Refresh the page to apply the selected language.

If you don't see a **Language** option, an administrator has disabled language selection for your deployment.

## Related pages

- [Use dark mode in {{kib}}](dark-mode.md)
- [Use high-contrast mode in {{kib}}](high-contrast.md)
- [Internationalization settings in {{kib}}](kibana://reference/configuration-reference/internationalization-settings.md): for administrators who configure available languages, defaults, and how {{kib}} resolves language when a user hasn't set a preference
