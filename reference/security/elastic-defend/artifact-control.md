---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/artifact-control.html
---

# Configure updates for protection artifacts [artifact-control]

On the **Protection updates** tab of the {{elastic-defend}} integration policy, you can configure how {{elastic-defend}} receives updates from Elastic with the latest threat detections, global exceptions, malware models, rule packages, and other protection artifacts. By default, these artifacts are automatically updated regularly, ensuring your environment is up to date with the latest protections.

You can disable automatic updates and freeze your protection artifacts to a specific date, allowing you to control when to receive and install the updates. For example, you might want to temporarily disable updates to ensure resource availability during a high-volume period, test updates in a controlled staging environment before rolling out to production, or roll back to a previous version of protections.

Protection artifacts will expire after 18 months, and you’ll no longer be able to select them as a deployed version. If you’re already using a specific version when it expires, you’ll keep using it until you either select a later non-expired version or re-enable automatic updates.

::::{warning}
It is strongly advised to keep automatic updates enabled to ensure the highest level of security for your environment. Proceed with caution if you decide to disable automatic updates.
::::


To configure the protection artifacts version deployed in your environment:

1. Find **Policies** in the navigation menu or by using the [global search field](/get-started/the-stack.md#kibana-navigation-search).
2. Select an {{elastic-defend}} integration policy, then select the **Protection updates** tab.
3. Turn off the **Enable automatic updates** toggle.
4. Use the **Version to deploy** date picker to select the date of the protection artifacts you want to use in your environment.
5. (Optional) Enter a **Note** to explain the reason for selecting a particular version of protection artifacts.
6. Select **Save**.
