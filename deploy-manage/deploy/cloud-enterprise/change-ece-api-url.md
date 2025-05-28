---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-config-api-base-url.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Change the ECE API URL [ece-config-api-base-url]

You can configure the HTTPS URL used to access the ECE API. You can specify either a DNS host name or an IP address. The primary use for this is to enable [single sign-on](../../users-roles/cloud-enterprise-orchestrator/configure-sso-for-deployments.md) on your deployments, so you can log into {{kib}} automatically once logged in to ECE.

To change the ECE API URL in the Cloud UI:

1. [Log into the Cloud UI](log-into-cloud-ui.md).
2. From the **Platform** menu, select **Settings**.
3. Select **Edit** and update the API URL setting.
4. Select **Update** and then **Save** to confirm the change.

To set the API base URL during installation or upgrade you can supply the `--api-base-url` command line argument:

```sh
bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) install --api-base-url $ECE_HTTPS_URL

bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) upgrade --user admin --pass $PASSWORD --api-base-url $ECE_HTTPS_URL
```

For existing deployments, the new ECE API URL will take effect whenever the deployment configuration plan is next updated.

