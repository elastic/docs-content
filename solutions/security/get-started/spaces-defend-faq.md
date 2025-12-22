---
applies_to:
  stack: preview 9.1
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Spaces and {{elastic-defend}} FAQ [security-spaces-faq]

This page introduces {{elastic-sec}} space awareness and answers frequently asked questions about how {{elastic-defend}} integration policies, endpoint artifacts, and endpoint response actions function when using {{kib}} spaces.

::::{admonition} Key points
* Artifacts such as trusted applications, event filters, and response action history are scoped by space to provide granular control over access.
* Role-based access control (RBAC) defines who can manage global and space-specific resources. Users can view, edit, or manage artifacts based on their role privileges and the space context.
* You need the **Global artifact management** privilege to manage global artifacts (those not associated with specific policies).
::::

::::{note}
{{elastic-sec}}'s space awareness works in conjunction with {{fleet}}'s space awareness. Space awareness is enabled by default in both applications, but for {{stack}} deployments that existed prior to version 9.1, {{fleet}} requires you to manually “opt-in” so that existing data can become space aware. For instructions, refer to [Enable space awareness in {{fleet}}](/deploy-manage/manage-spaces-fleet.md#spaces-fleet-enable).

This is a one-time migration that copies your existing {{fleet}} data into a new, space-aware model. Previous data will be preserved in snapshots in case rollback is needed.
::::

## General FAQ [spaces-security-faq-general]
**What are spaces in {{kib}}, and how do they affect what I see?**

Spaces allow your organization to segment data and configurations within {{kib}}. If you're working in a specific space, you’ll only see the policies, {{agents}}, endpoints, and data that belong to that space.


**Does this matter to me if my organization doesn't use spaces?**

If your organization doesn't use spaces, the only thing you need to know is that to manage global artifacts, you need the **Global Artifact Management** privilege.

When you upgrade your {{stack}} deployment to 9.1.0, the **Global Artifact Management** privilege is automatically granted to any role that grants the **All** privilege to at least one artifact type.


**How do I use spaces with {{agent}} and {{elastic-defend}}?**

Spaces are defined at the {{kib}} level. Once a space is created, {{agent}} policies can be assigned to it. To do this, go to your list of agent policies in {{fleet}}, and select the policy you want to assign. Navigate to the **Settings** tab, find the **Spaces** section, and select the space(s) where you want the policy to appear.

Once assigned, the {{agents}}—and {{elastic-defend}} endpoints, if applicable—associated with this policy are visible and manageable only within the designated space(s).


**Can artifacts be assigned to multiple spaces?**

Yes, {{agent}} policies and all associated artifacts can be assigned to more than one space.


## {{elastic-defend}} policies [spaces-security-faq-defend-policies]
**How do spaces impact the visibility of endpoints in the {{security-app}}?**

The list of endpoints that you see depends on your current space. Only endpoints associated with policies in the space you're working in will appear.


**How do spaces impact the visibility of {{elastic-defend}} integration policies in {{elastic-sec}}?**

The **Policies** list displays only the policies associated with your current space. The endpoint agent count for each policy includes only the endpoints within that space.


## Endpoint artifacts [spaces-security-faq-endpoint-artifacts]

**What are endpoint artifacts?**

Endpoint artifacts are the various objects that can be associated with endpoints and {{elastic-defend}} policies. These include trusted applications, event filters, host isolation exceptions, and blocklist items. Artifacts can be global (shared across all policies) or per-policy (specific to individual policies). Per-policy configuration of artifacts is available only with an Enterprise license.


**How do global artifacts work across spaces?**

Global artifacts are space agnostic and appear in all spaces.


**How do policy-specific artifacts work across spaces?**

Users can assign artifacts to any policies they have access to within their assigned space.

When an artifact entry is created within a space, it is owned by that space. To edit or delete the artifact, you must either be in the owning space or have **Global artifact management** privileges.


**What happens if my policy uses an artifact owned by a space I don't have access to?**

When viewing a policy, you will still see all artifacts associated with it - regardless of which space they were created in. However, artifacts viewed outside of their owning space will appear as read-only.

If an artifact is associated with a policy that isn't visible in the current space, only the policy's UUID will appear in the "Applied to the following policies" pop-up. For policies accessible within the space, the full policy name will appear.


**Why is an endpoint artifact marked as “read-only”?**

An artifact may appear as read-only if:
- It is a global artifact, and you do not have **Global artifact management** privileges.
- The artifact was created in a different space.

In these situations, editing may be disabled, and tooltips will provide additional context.


**How can I tell which space “owns” a per-policy artifact?**

This information is not currently visible in the Kibana UI. It is, however, available on each artifact record returned by the API under the `tag` field. It will include a value that corresponds to the owner space's ID in the format of `ownerSpaceId:<space_id_here>`, for example: `ownerSpaceId:default`. By default, each artifact will have at least one such tag, but multiple tags are also supported and cause a per-policy artifact to be managed by multiple spaces.


## RBAC [spaces-security-faq-rbac]

**How does RBAC work for artifacts assigned to a particular space?**

Specific {{kib}} privileges for each artifact type—such as event filters or trusted applications—allow you to manage (create, edit, delete, and assign) those artifact types globally or per policy, but only for policies within the spaces you have access to. These artifact types include:

* Trusted applications
* Host isolation exceptions
* Blocklist items
* Event filters

The **Global Artifact Management** privilege grants full control over artifacts in any space. This privilege by itself does not enable you to manage the different artifact types, but rather grants additional privileged actions to users who also have the **All** privilege for a given artifact type. This includes the ability to:

* Create, edit, and delete global artifacts
* Manage per-policy artifacts, even if they were created in a different space
* Convert an artifact between global and per-policy scope

Endpoint exceptions are global-only, so you need the **Global Artifact Management** privilege to create, edit, or delete them.


**How do I change which space owns a per-policy artifact?**

Artifact `tags` enable you to change the owning space of per-policy artifacts (those not assigned globally). When an artifact is created, a tag for the space it was created in is automatically added. The format of this tag is `ownerSpaceId:<space_id_here>`, for example: `ownerSpaceId:default`. Artifacts can have multiple owner space tags, which enables the management of per-policy artifacts from multiple spaces.

Updates to owner space `tags` are supported via API. This type of update requires that you have the **Global Artifact Management** privilege. Refer to [Security endpoint management APIs]({{kib-apis}}/group/endpoint-security-endpoint-management-api) to learn how to use each artifact type's corresponding API.


**What happens if I delete a space that “owns” certain per-policy artifacts?**

When a space is deleted, artifacts that were previously created from the deleted space will continue to be manageable by users who have the **Global Artifact Management** privilege. Alternatively, you can update their owner space via API, as detailed above.



## Endpoint response actions [spaces-security-faq-endpoint-response-actions]

**How do spaces impact response actions?**

Response actions for both {{elastic-defend}} and third-party EDR solutions are associated with the {{fleet}} integration policy that's connected to the {{agent}} that executed the response action. A user authorized to view the response actions history log can only view items associated with integration policies that are accessible in the active space. If you share an integration policy with a new space, the associated response actions will automatically become visible in that space. There are some conditions that can result in response action history not being accessible by default—we call these ["orphan” response actions](#spaces-security-faq-orphan-response-actions).


**How are response actions visible across spaces?**

You can see the response action history for hosts whose {{fleet}} integration policies are visible in the current space. This includes actions initiated in other spaces; you can see all historical response actions associated with integration policies that are accessible in your current space.


**If a policy is deleted, how does that impact my response history?**

When an integration policy is deleted in {{fleet}}, response actions associated with that integration policy will become orphans and will no longer be accessible via the response action history log. You can force these actions to appear in the action history log (refer to [Orphan response actions](#spaces-security-faq-orphan-response-actions)).


**What happens if my {{agent}} moves to a new integration policy?**

When an {{agent}} moves to a new integration policy, its response actions history will continue to be visible as long as the prior integration policy is not deleted and remains accessible from the same spaces that the new integration policy is shared with.

If the new integration policy is not shared with the same spaces as the previous integration policy, then some history may be hidden; you can only view response action history for integration policies you have access to in the current space.


**How do spaces impact automated response actions?**

Automated response actions (currently supported only for {{elastic-defend}}) work similarly to regular response actions, with a few caveats:

* If you unenroll a host before the detection engine processes an event from that host, the response action will fail. The failed response action will not appear in the UI (either as part of the alert details, or in the response actions history log) because it won't be associated with the integration policy that was running on the host. These actions will become [orphans](#spaces-security-faq-orphan-response-actions).

* If a policy that triggered automated response actions moves to a new space or is shared with a new space, links to the detection engine rule that triggered the automated response actions will go to a “rule not found” page. This occurs because the rule is space-specific and not accessible in your current space.


**How do spaces impact third-party response actions?**

Response actions for third-party EDR systems behave the same as response actions for {{elastic-defend}}. However, each space must be configured to support the given third-party system. For example, each space must have its own connector to the third-party system.


**Will third-party response actions continue to work if I move (or share) the associated policy to a new space?**

Response actions will not work unless a connector for the given third-party EDR exists in the space where the policy was moved. Connectors are space-specific and cannot be shared or moved to a new space; a new instance of the connector must be created in the new space so that the policy in that space can send response actions to the third-party system.


### What are orphan response actions? [spaces-security-faq-orphan-response-actions]
“Orphan” response actions are those associated only with deleted integration policies. These response actions are not visible in the response action history log because it can't be determined whether your current space has visibility of the policy associated with the response actions.


**How can I access orphan response actions?**

To make orphan response actions visible in a given space, you can make an API call with the space ID where you want them to appear. Below are several examples:

::::{important}
To use this API, you need {{kib}}'s built-in `superuser` role.
::::

:::{dropdown} View current orphan response action's space ID:

API call:
`GET /internal/api/endpoint/action/_orphan_actions_space`

Response:
```
{
  "data": {
    "spaceId": "admin"
  }
}
```
:::

:::{dropdown} Update orphan response action space id:
API call:
```
POST /internal/api/endpoint/action/_orphan_actions_space
{
  "spaceId": "admin"
}
```

Response:
```
{
  "data": {
    "spaceId": "admin"
  }
}
```
:::

To remove the space ID where orphan response actions appear, call the API with an empty string for `spaceId`. Orphan response actions can only appear in a single space.


## Endpoint protection rules [spaces-security-faq-endpoint-protection-rules]

By default, [endpoint protection rules](/solutions/security/manage-elastic-defend/endpoint-protection-rules.md) use an index pattern that may be too broad for use in a particular space. In order to ensure that the space only shows the desired data in that space, you may need to customize the rule. For example, the Endpoint Security ({{elastic-defend}}) rule has an index pattern that picks up all data sent to `logs-endpoint.alerts-*`. This index pattern would pick up all events sent by {{elastic-defend}}, which may not be desirable.

One option in this situation is to add a rule exception that ensures that only data with a `data_stream.namespace` that matches the namespace defined in the {{fleet}} policy that contains the applicable {{elastic-defend}} integration policies. {{fleet}} allows you to configure a space to restrict which namespace values can apply to policies, which can help you manage rules when new {{fleet}} policies are created, or existing policies are updated. Existing rules would not have to be adjusted to keep the namespace values in sync.

**What happens to protection rules when a policy is shared with or moved to a new space?**

Sharing or moving a {{fleet}} agent policy or associating an {{elastic-defend}} integration policy with additional {{fleet}} agent policies may require you to configure the associated protection rules in the new space. Rules are space specific and will not be automatically created in the additional spaces that the policies were shared with.

## Osquery [spaces-security-faq-osquery]

Osquery artifacts are not yet space aware. They can only exist within a single space.