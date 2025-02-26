---
navigation_title: "{{ece}}"
applies_to:
  ece: 
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-add-license.html
---

# Manage your license in {{ece}} [ece-add-license]

The use of Elastic Cloud Enterprise requires a valid license, which you can obtain from Elastic and add to your installation following the steps described in this document. When you first install ECE we automatically activate ECE with a trial license that is valid for 30 days.

Full ECE licenses that you obtain from Elastic enable all ECE hosted deployments with the same products, features, and support that are available at our Enterprise subscription level on Elastic Cloud for the respective stack version, as described on the [Subscriptions page](https://www.elastic.co/subscriptions/cloud).

::::{note}
The licenses used to activate the deployments might have a different expiration date than the license used to activate ECE. ECE manages the licenses of the hosted deployments and will automatically update the deployment license when needed.
::::


::::{note}
If you have a license from 2018 or earlier, you might receive a warning that your cluster license is about to expire. Don’t panic, it isn’t really. Elastic Cloud Enterprise manages the cluster licenses so that you don’t have to. In rare cases, such as when a cluster is overloaded, it can take longer for Elastic Cloud Enterprise to reapply the cluster license.
::::



## Licenses Expiration [ece_licenses_expiration]

Elastic Cloud Enterprise Licenses contains two types of licenses - the actual license for Elastic Cloud Enterprise that is validated to enable Elastic Cloud Enterprise features and the *cluster licenses*, which Elastic Cloud Enterprise installs into the individual clusters.

Elastic Cloud Enterprise installs those cluster licenses with an approximately 3 month window, and updates the cluster licenses automatically as they get within a month of expiration.

When the Elastic Cloud Enterprise license expires, and consequently the cluster license that’s currently installed for all managed clusters since it has the same expiration date, the following takes place:

* **Users cannot create new clusters or modify existing clusters**: They can only delete them. These clusters are still fully accessible for the client though.
* **X-Pack features are degraded**: For the details about what functionality will be reduced when cluster license expires, read more about the [Elastic Stack license expiration](https://www.elastic.co/guide/en/elastic-stack-overview/current/license-expiration.html).


## Download a license [ece_download_a_license]

To download a license from Elastic:

1. Locate the email sent to you from Elastic that includes the link to the license.
2. Open the link, accept the licensing agreement, and select **Send**.
3. Download the ECE license.


## Add a license [ece_add_a_license]

To add a license to your ECE installation:

1. [Log into the Cloud UI](../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Settings**.
3. Select **Update license** and choose the license file that you downloaded. License files are in the JSON format.
4. Select **Add license**.

    If the operation is successful, the license is added.



## Check your license expiry [ece_check_your_license_expiry]

To check your current license expiry date:

1. [Log into the Cloud UI](../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Settings**.
3. Check the **Expires** row under **License**:


## Request a trial extension [ece_request_a_trial_extension]

To request a trial license extension from Elastic:

1. Fill in the form at [https://www.elastic.co/contact](https://www.elastic.co/contact). Make sure to choose Elastic Cloud Enterprise as the area of interest and state that you request a trial license extension.

    Someone from Elastic will be in touch to respond to your trial extension request.



## Delete a license [ece_delete_a_license]

To delete an existing license for your ECE installation:

1. [Log into the Cloud UI](../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Platform** menu, select **Settings**.
3. In the **License** section, select **Delete license** and confirm the action.

