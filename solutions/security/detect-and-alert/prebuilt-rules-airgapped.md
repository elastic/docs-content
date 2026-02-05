---
navigation_title: Prebuilt rules in air-gapped environments
applies_to:
  deployment:
    self: ga
    ece: ga
    eck: ga
products:
  - id: security
description: Learn how to install and update Elastic prebuilt detection rules in air-gapped environments using a self-hosted Package Registry or manual export and import.
---

# Install and update prebuilt rules in air-gapped environments [prebuilt-rules-airgapped]

{{kib}} downloads Elastic prebuilt rules from the {{package-registry}}. In air-gapped environments without internet access, you can use one of the following methods to install and update prebuilt rules:

* **[Use a self-hosted {{package-registry}}](#install-prebuilt-rules-airgapped)**: Host your own {{package-registry}} to provide rules to your air-gapped environment. This is the recommended approach for ongoing rule management and updates.
* **[Manually transfer prebuilt rules](#import-export-airgapped)**: Export rules from an internet-connected {{elastic-sec}} instance and import them into your air-gapped environment. This is a simpler approach for one-time transfers or when container infrastructure isn't available.

## Install prebuilt rules from your self-hosted registry [install-prebuilt-rules-airgapped]

This method requires hosting your own {{package-registry}} to provide prebuilt rules to your air-gapped {{kib}} instance. After setting up your registry, you can install and update prebuilt rules the same way as in a connected environment.

### Set up your self-hosted {{package-registry}} [setup-self-hosted-epr]

Before you can install prebuilt rules, you need to set up and run a self-hosted {{package-registry}} in your air-gapped environment.

::::{note}
The examples in this section use Docker commands. You can adapt them for other container runtimes.
::::

#### Choose your registry image

The {{package-registry}} is available as a Docker image with different tags. Choose the appropriate image based on your update strategy.

::::{important}
When choosing a {{package-registry}} image for production air-gapped environments, we recommend using one of the following options:

* **Versioned images**: Use images that match your {{stack}} version (for example, `docker.elastic.co/package-registry/distribution:{{version.stack}}`), as described in the [{{fleet}} documentation](/reference/fleet/air-gapped.md#air-gapped-diy-epr). This is the safest option for environments where you cannot immediately upgrade your {{stack}} when new versions are released.
* **Production images**: Use an image like `docker.elastic.co/package-registry/distribution:production` _only_ if you keep your air-gapped {{stack}} up-to-date. If you want to rely on the `production` image for the most recent {{fleet}} packages and prebuilt detection rules, upgrade your {{stack}} as soon as new versions are released. This minimizes the risk of encountering breaking changes between the {{package-registry}} and your {{stack}} version.
::::

:::::{stepper}

::::{step} Pull and transfer the image

1. On a system with internet access, pull your chosen {{package-registry}} distribution image:

    ```sh subs=true
    docker pull docker.elastic.co/package-registry/distribution:{{version.stack}}
    ```

    Or, if using the production image:

    ```sh
    docker pull docker.elastic.co/package-registry/distribution:production
    ```

2. Save the Docker image to a file:

    ```sh subs=true
    docker save -o package-registry.tar docker.elastic.co/package-registry/distribution:<image-tag>
    ```

    Replace `<image-tag>` with your chosen tag (for example, `{{version.stack}}` or `production`).

3. Transfer the image file to your air-gapped environment using your organization's approved file transfer method.

4. Load the image into your container runtime:

    ```sh
    docker load -i package-registry.tar
    ```
::::

::::{step} Start the {{package-registry}} container

Run the {{package-registry}} container:

```sh
docker run -d -p 8080:8080 --name package-registry docker.elastic.co/package-registry/distribution:<image-tag>
```

Replace `<image-tag>` with your chosen tag.

For more setup options and details, refer to [Host your own {{package-registry}}](/reference/fleet/air-gapped.md#air-gapped-diy-epr).
::::

::::{step} Configure {{kib}}

Configure {{kib}} to use your self-hosted {{package-registry}} and enable air-gapped mode. Add the following to your [`kibana.yml`](/deploy-manage/deploy/self-managed/configure-kibana.md) configuration file, then restart {{kib}}:

```yaml
xpack.fleet.registryUrl: "http://<your-registry-host>:8080"
xpack.fleet.isAirGapped: true
```

* [`xpack.fleet.registryUrl`](https://www.elastic.co/docs/reference/kibana/configuration-reference/fleet-settings): Points {{kib}} to your self-hosted registry. Replace `<your-registry-host>` with the hostname or IP address of your registry.
* [`xpack.fleet.isAirGapped`](https://www.elastic.co/docs/reference/kibana/configuration-reference/fleet-settings#general-fleet-settings-kb): Enables air-gapped mode, which allows {{fleet}} to skip requests or operations that require internet access.
::::

::::{step} Install the rules

1. In your air-gapped {{elastic-sec}} instance, find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to the Rules table.

2. Click **Add Elastic rules**. The available prebuilt rules from your self-hosted registry are displayed.

3. Install the rules you need:

    * To install all available rules, click **Install all**.
    * To install specific rules, select them and click **Install *x* selected rule(s)**.
    * To install and immediately enable rules, click the options menu (![Vertical boxes button](/solutions/images/security-boxesVertical.svg "")) and select **Install and enable**.

For more details about enabling installed rules, refer to [Install and enable Elastic prebuilt rules](/solutions/security/detect-and-alert/install-manage-elastic-prebuilt-rules.md#load-prebuilt-rules).
::::

:::::

## Update prebuilt rules in an air-gapped environment [update-prebuilt-rules-airgapped]

To update your prebuilt rules, first update your self-hosted {{package-registry}} with a newer distribution image, then install the rule updates in {{elastic-sec}}.

::::{important}
Elastic releases prebuilt rule updates continuously. To receive the latest updates in an air-gapped environment, we recommend updating your self-hosted {{package-registry}} at least monthly.
::::

:::::{stepper}

::::{step} Update your self-hosted {{package-registry}}
:anchor: update-air-gapped-epr

1. Follow the same process described in [Pull and transfer the image](#setup-self-hosted-epr) to pull a newer image version, save it, transfer it to your air-gapped environment, and load it.

2. Restart the {{package-registry}} container with the updated image:

    ```sh
    docker stop <container-name>
    docker rm <container-name>
    docker run -d -p 8080:8080 --name <container-name> docker.elastic.co/package-registry/distribution:<image-tag>
    ```

    Replace `<container-name>` with your container's name and `<image-tag>` with the appropriate version tag.
::::

::::{step} Install rule updates
:anchor: install-rule-updates-airgapped

After updating your registry, install the rule updates in your air-gapped {{elastic-sec}} instance:

1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to the Rules table.

2. If updates are available, the **Rule Updates** tab appears. Click it to view available updates.

3. Review the updates and install them:

    * To update all rules, click **Update all**.
    * To update specific rules, select them and click **Update *x* selected rule(s)**.
    * To review changes before updating, click a rule name to open the rule details flyout and compare versions.

For more details about updating prebuilt rules, refer to [Update Elastic prebuilt rules](/solutions/security/detect-and-alert/install-manage-elastic-prebuilt-rules.md#update-prebuilt-rules).
::::

:::::

## Manually transfer prebuilt rules to an air-gapped environment [import-export-airgapped]

If you cannot set up a self-hosted {{package-registry}}, you can manually export prebuilt rules from an internet-connected {{elastic-sec}} instance and import them into your air-gapped environment.

This method is useful when you don't have container infrastructure to host a {{package-registry}}, need to transfer a specific subset of rules, or want a simpler one-time transfer without ongoing registry maintenance.

::::{note}
When using the export import method:

* Rule actions and connectors are imported, but you must re-add sensitive connector credentials.
* Value lists that are used for rule exceptions are not included. You must export and import them separately. Refer to [Manage value lists](/solutions/security/detect-and-alert/create-manage-value-lists.md#edit-value-lists) for more details.

For more details on exporting and importing rules, refer to [Export and import rules](/solutions/security/detect-and-alert/manage-detection-rules.md#import-export-rules-ui).
::::

:::::{stepper}

::::{step} Export rules from an internet-connected instance
:anchor: export-rules-airgapped

1. On an internet-connected {{elastic-sec}} instance, [install the prebuilt rules](/solutions/security/detect-and-alert/install-manage-elastic-prebuilt-rules.md#load-prebuilt-rules) you need.

2. Export the rules:

    1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to the Rules table.
    2. Select the rules you want to export, or click **Select all** to select all rules.
    3. Click **Bulk actions** → **Export**.

3. Transfer the exported `.ndjson` file to your air-gapped environment using your organization's approved file transfer method.
::::

::::{step} Import rules into your air-gapped instance
:anchor: import-rules-airgapped

1. In your air-gapped {{elastic-sec}} instance, find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to the Rules table.

2. Click **Import rules** above the Rules table.

3. Drag and drop the `.ndjson` file containing the exported rules.

4. (Optional) Select overwrite options if you're updating existing rules.

5. Click **Import** to add the rules.
::::

::::{step} Update rules
:anchor: update-rules-export-import

1. To get rule updates, repeat this export import process after [updating your prebuilt rules](/solutions/security/detect-and-alert/install-manage-elastic-prebuilt-rules.md#update-prebuilt-rules) on the internet-connected instance. 
2. When importing rules, select **Overwrite existing detection rules with conflicting "rule_id"** to update existing rules.
::::

:::::

## Related documentation [prebuilt-rules-airgapped-related]

* [Run {{agents}} in an air-gapped environment](/reference/fleet/air-gapped.md): Guidance for setting up {{fleet}} and integrations in air-gapped environments.
* [Air gapped install](/deploy-manage/deploy/self-managed/air-gapped-install.md): An overview of air-gapped setup for the entire {{stack}}.
* [Configure offline endpoints and air-gapped environments](/solutions/security/configure-elastic-defend/configure-offline-endpoints-air-gapped-environments.md): How to set up {{elastic-endpoint}} artifact updates in air-gapped environments.

