---
navigation_title: How IP filtering rules work in ECE
applies_to:
  deployment:
    ece: ga
---

# IP filtering rules in {{ece}}

By default, in {{ece}}, all your deployments are accessible to external networks through the orchestrator’s proxies without any traffic restrictions. In some cases, these proxies may also be accessible over the public internet.

IP filtering rules are created at the orchestrator level. Rules are grouped into rule sets, and then are associated with one or more deployments to take effect. After you associate at least one IP filtering rule set with a deployment, traffic that does not match any rules for the deployment is denied.

IP filtering rules apply to external traffic only. Internal traffic is managed by ECE. For example, {{kib}} can connect to {{es}}, as well as internal services which manage the deployment. Other deployments can’t connect to deployments protected by IP filters.

IP filters operate on the proxy. Requests rejected by the IP filters are not forwarded to the deployment. The proxy responds to the client with `403 Forbidden`.

## Logic

Rule sets work as follows:

- You can assign multiple rule sets to a single deployment. The rule sets can be of different types. In case of multiple rule sets, traffic can match ANY of them. If none of the rule sets match, the request is rejected with `403 Forbidden`.

- IP filtering rule sets, when associated with a deployment, will apply to all deployment endpoints, such as {{es}}, {{kib}}, APM Server, and others.

- Any IP filtering rule set assigned to a deployment overrides the default behavior of *allow all access over the public internet endpoint*. The implication is that if you make a mistake putting in the traffic source (for example, specified the wrong IP address) the deployment will be effectively locked down to any of your traffic. You can use the UI to adjust or remove the rule sets.

- You can mark a rule set as *default*. It is automatically attached to all new deployments that you create. You can detach default rule sets from deployments after they are created. Note that a *default* rule set is not automatically attached to existing deployments.

## Restrictions

- You can have a maximum of 512 rule sets, and 128 rules in each rule set.

- Domain-based filtering rules are not allowed for IP filtering rule sets, because the original IP is hidden behind the proxy. Only IP-based filtering rules are allowed.

## Review the rule sets associated with a deployment

1. Log in to the [Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.
3. Select the **Security** tab on the left-hand side menu bar.

IP filtering rule sets are listed under **Traffic filters**.

On this page, you can view and remove existing rule sets and attach new rule sets.

## Identify default rule sets

To identify which rule sets are automatically applied to new deployments in your account:

1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).

2. From the **Platform** menu, select **Security**.

3. Select each of the rule sets — **Include by default** is checked when this rule set is automatically applied to all new deployments.

## View rejected requests

Requests rejected by IP filters have status code `403 Forbidden` and one of the following in the response body:

```json
{"ok":false,"message":"Forbidden"}
```

```json
{"ok":false,"message":"Forbidden due to traffic filtering. Please see the Elastic documentation on Traffic Filtering for more information."}
```

Additionally, IP filter rejections are logged in ECE proxy logs as `status_reason: BLOCKED_BY_IP_FILTER`. Proxy logs also provide client IP in `client_ip` field.