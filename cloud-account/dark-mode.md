---
applies_to:
  stack: all
  serverless: all
---

# Use dark mode in Kibana

The dark mode changes Kibana's default light appearance to a darker color theme. From the application header, you can turn on dark mode or synchronize the color mode with your operating system settings.

:::{tip}
If you're using {{ecloud}}, this setting only applies to the Kibana UI of your serverless projects and hosted deployments. If you'd like to change the {{ecloud}} Console color theme too, you must do so separately from its respective interface.
:::

## Change your color mode preferences

1. Open the user menu from the header.
2. Select **Appearance**.
   
   :::{note}
   On self-managed deployments of {{kib}}, this option is located on your profile page. To access it, select **Edit profile** from the header's user menu.
   :::

3. Choose a color mode:

    - **Light**: The default color mode of Kibana
    - **Dark**: The dark color mode of Kibana
    - **System**: Synchronizes Kibana's color mode with your system settings
    - **Space default**: Sets the color mode to the value defined in the [Space settings](kibana://reference/advanced-settings.md#kibana-general-settings)

      :::{admonition} Deprecated
      The **Space default** option will be removed in a future version and automatically replaced with the System color mode.
      :::

4. Select **Save changes**.
5. Refresh the page to apply the selected color mode.