---
navigation_title: How traffic filter rules work in ECE
applies_to:
  deployment:
    ece: ga
---

# Traffic filter rules in {{ece}}

By default, in {{ece}}, all your deployments are accessible over the public internet.

Filtering rules are created at the orchestrator level. Rules are grouped into rule sets, and then are associated with one or more deployments to take effect. After you associate at least one traffic filter with a deployment, traffic that does not match any filtering rules for the deployment is denied.

Traffic filters apply to external traffic only. Internal traffic is managed by ECE. For example, {{kib}} can connect to {{es}}, as well as internal services which manage the deployment. Other deployments can’t connect to deployments protected by traffic filters.

Traffic filters operate on the proxy. Requests rejected by the traffic filters are not forwarded to the deployment. The proxy responds to the client with `403 Forbidden`.

## Logic

Rule sets work as follows:

- You can assign multiple rule sets to a single deployment. The rule sets can be of different types. In case of multiple rule sets, traffic can match ANY of them. If none of the rule sets match, the request is rejected with `403 Forbidden`.

- Traffic filter rule sets, when associated with a deployment, will apply to all deployment endpoints, such as {{es}}, {{kib}}, APM Server, and others.

- Any traffic filter rule set assigned to a deployment overrides the default behavior of *allow all access over the public internet endpoint*. The implication is that if you make a mistake putting in the traffic source (for example, specified the wrong IP address) the deployment will be effectively locked down to any of your traffic. You can use the UI to adjust or remove the rule sets.

- You can mark a rule set as *default*. It is automatically attached to all new deployments that you create in its region. You can detach default rule sets from deployments after they are created. Note that a *default* rule set is not automatically attached to existing deployments.

## Restrictions

- You can have a maximum of 512 rule sets per organization and 128 rules in each rule set.

- Traffic filter rule sets are bound to a single region. The rule sets can be assigned only to deployments in the same region. If you want to associate a rule set with deployments in multiple regions, then you have to create the same rule set in all the regions you want to apply it to.

- Domain-based filtering rules are not allowed for Cloud traffic filtering, because the original IP is hidden behind the proxy. Only IP-based filtering rules are allowed.

## Review the rule sets associated with a deployment

1. Log in to the [Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.
3. Select the **Security** tab on the left-hand side menu bar.

Traffic filter rule sets are listed under **Traffic filters**.

On this page, you can view and remove existing filters and attach new filters.

## Identify default rule sets

To identify which rule sets are automatically applied to new deployments in your account:

1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).

2. From the **Platform** menu, select **Security**.

3. Select each of the rule sets — **Include by default** is checked when this rule set is automatically applied to all new deployments in its region.

## View rejected requests

Requests rejected by traffic filter have status code `403 Forbidden` and one of the following in the response body:

```json
{"ok":false,"message":"Forbidden"}
```

```json
{"ok":false,"message":"Forbidden due to traffic filtering. Please see the Elastic documentation on Traffic Filtering for more information."}
```

Additionally, traffic filter rejections are logged in ECE proxy logs as `status_reason: BLOCKED_BY_IP_FILTER`. Proxy logs also provide client IP in `client_ip` field.