---
applies_to:
  stack: preview 9.1
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Spaces and {{elastic-sec}} FAQ [security-spaces-faq]

This page introduces {{elastic-sec}} Space awareness and answers frequently asked questions about how {{elastic-defend}} integration policies, {{elastic-endpoint}} artifacts, and {{elastic-endpoint}} response actions function when utilizing {{kib}} Spaces.

::::{admonition} Key points
* Artifacts such as trusted applications, event filters, and response action history are scoped by Space to provide granular control over access.
* Role-Based Access Control (RBAC) defines who can manage global and space-specific resources. Users can view, edit, or manage artifacts based on their role privileges and the Space context. 
* You need the global management privilege to manage global artifacts (those not associated with specific policies).
:::: 

::::{note}
{{elastic-sec}}'s Space awareness works in conjunction with {{fleet}}'s space awareness. Space awareness is enabled by default in both applications, but for {{stack}} deployments that existed prior to version 9.1, {{fleet}} requires you to manually “opt-in” so that existing data can become space aware. To learn more, refer to [Fleet roles and privileges](/reference/fleet/fleet-roles-privileges.md).
::::

## General FAQ [spaces-security-faq-general]
**What are Spaces in {{kib}}, and how do they affect what I see?**

Spaces allow your organization to segment data and configurations within {{kib}}. If you're working in a specific space, you’ll only see the policies, {{elastic-agent}}s, {{elastic-endpoint}}s, and data that belong to that space. 

**Does this matter to me if my organization doesn't use spaces?**
If your organization doesn't use Spaces, the only thing you need to know is that to manage Global Artifacts you need the Global Artifact management privilege.

When you upgrade your {{stack}} deployment to 9.1.0, the Global Artifact Management privilege will be automatically granted to any role that grants the “All” privilege to at least one artifact type.

**How do I use Spaces with {{elastic-agent}} and {{elastic-defend}}?**

Spaces are defined at the {{kib}} level. Once a space is created, {{elastic-agent}} policies can be assigned to it. To do this, go to your list of agent policies in {{fleet}} and select the policy you want to assign. Navigate to the **Settings** tab, find the **Spaces** section, and select the space(s) where you want the policy to appear.

Once assigned, the {{elastic-agents}} — and {{elastic-defend}} endpoints, if applicable - associated with this policy are visible and manageable only within the designated Space(s). 


**Can artifacts be assigned to multiple Spaces?**

Yes, {{elastic-agent}} policies and all associated artifacts can be assigned to more than one Space.


## {{elastic-defend}} policies [spaces-security-faq-defend-policies]
**How do Spaces impact the visibility of Endpoints in the security app?**
The list of {{elastic-endpoint}}s that you see depends on your current Space. Only {{elastic-endpoint}}s associated with policies in the Space you're working in will appear.


**How do Spaces impact the visibility of {{elastic-defend}} integration policies in {{elastic-sec}}?**

The **Policies** list displays only the policies associated with your current Space. The {{elastic-endpoint}} count for each policy includes only the endpoints within that Space. 


## {{elastic-endpoint}} artifacts [spaces-security-faq-endpoint-artifacts]

**What are Endpoint artifacts?**
Endpoint artifacts are the various configurations that can be associated with {{elastic-endpoint}}s and {{elastic-defend}} policies. These include Trusted Applications, Event Filters, Host Isolation Exceptions, and Blocklist items. Artifacts can be global (shared across all policies) or per-policy (specific to individual policies). Per-policy configuration of artifacts is available only with an Enterprise license.


**How do global artifacts work across spaces?**
Global artifacts are Space agnostic and thus eppear in all spaces.


**How do policy-specific artifacts work across spaces?**
Users can assign artifacts to any policies they have access to within their assigned Space.

When an artifact entry is created within a Space, it is owned by that Space. To edit or delete the artifact, you must either be in the owning Space or have Global management privileges. 


**What happens if my policy uses an artifact owned by a Space I don't have access to?**
When viewing a policy, you will still see all artifacts associated with it - regardless of which Space they were created in. However, artifacts viewed outside of their owning Space will appear as read-only.

If an artifact is associated with a policy that isn't visible in the current Space, only the policy's UUID will appear in the "Applied to the following policies" pop-up. For policies accessible within the Space, the full policy name will appear.


**Why is an endpoint artifact marked as “read-only”?**
An artifact may appear as read-only if:
- It is a global artifact, and you do not have Global management privileges.
- The artifact was created in a different Space.

In these situations, editing may be disabled, and tooltips will provide additional context.


**How can I tell which Space “owns” a per-policy artifact?**
Each artifact has a `tag` field, whose value corresponds to the owner space's ID. The format of this tag is `ownerSpaceId:<space_id_here>`, for example: `ownerSpaceId:default`.


## RBAC  [spaces-security-faq-rbac]

**How does RBAC work for artifacts assigned to a particular Space?**
Specific {{kib}} privileges for each artifact type (such as Event Filters or Trusted Applications) allow you to manage (create, edit, delete, and assign) those artifacts types globally or per policy, but only for policies within the Spaces you have access to. These artifact types include 

* Trusted applications
* Host isolation exceptions
* Blocklist items
* Event filters

The `Global Artifact Management` privilege grants full control over artifacts in any Space. This privilege by itself does not enable you to manage the different artifact types, but rather grants additional privileged actions to those users that have the “All” privilege to a given artifact type. This includes the ability to:

* Create, edit, and delete global artifacts of any type
* Manage per-policy artifacts, even if they were created in a different Space
* Convert an artifact between global and per-policy scope

Endpoint Exceptions are global only, so you need the `Global Artifact Management` privilege to create, edit, or delete them.

**How do I change which Space owns a per-policy artifact?**
Artifact tags enable you to change the owning Space of per-policy artifacts (those not assigned globally). When an artifact is created, a tag for the Space it was created in is automatically added. The format of this tag is `ownerSpaceId:<space_id_here>`, for example: `ownerSpaceId:default`. Artifacts can have multiple owner space tags, which enables you to have multiple Spaces where you can manage per-policy artifacts.

Updates to owner Space tags are supported via API. This type of update requires that you have the `Global Artifact Management` privilege. Refer to the [Security API docs](/solutions/security/apis.md) to learn how to use each artifact type's corresponding API.

**What happens if I delete a Space that “owns” certain per-policy artifacts?**
When a Space is deleted, artifacts that were previously created from the deleted space will continue to be manageable by  users who have the `Global Artifact Management` privilege. Alternatively, you can update their owner space via API, as detailed above.



## Endpoint response actions [spaces-security-faq-endpoint-response-actions]

**How do Spaces impact Response Actions**
Response actions for both {{elastic-defend}} and third-party EDR solutions are associated with the {{fleet}} integration policy that's connected to the {{elastic-agent}} that executed the response action. A user authorized to view the response actions history Log can only view items associated with integration policies that are accessible in the active Space. If you share an integration policy with a new space, the associated response actions will automatically become visible in that Space. There are some conditions that can result in response action history not being accessible by default-we call these “ophan” response actions (refer to [What are orphan response actions and how can I access them?](#spaces-security-faq-orphan-response-actions)).

**How are response actions visible across spaces?**
You can see the response action history for hosts whose Fleet integration policies are visible in the the current space. This includes actions initiated in other spaces; you can see all historical response actions associated with integration policies that are accessible in your current space.

**If a policy is deleted, how does that impact my response history?**
When an integration policy is deleted in {{fleet}}, response actions associated with that integration policy will become orphans and will no longer be accessible via the response action history log. You can force these actions to appear in the action history log—refer to [What are orphan response actions and how can I access them?](#spaces-security-faq-orphan-response-actions).

**What happens if my {{agent}} moves to a new integration policy?**
When an {{agent}} moves to a new integration policy, its response actions history will continue to be visible as long as the prior integration policy is not deleted and continues remains accessible from the same Spaces that the new integration policy is shared with.

If the new integration policy is not shared with the same spaces as the prior integration policy, then some history may be hidden; you can only view response action history for integration policies you have access to in the current space.

**What are orphan response actions and how can I access them?** [spaces-security-faq-orphan-response-actions]
“Orphan” response actions are those associated only with deleted integration policies. These response actions are not visible in the response action history log because it can't be determined whether your current space has visibility of the policy associated with the response actions.

To make orphan response actions visible in a given space, you can make an API call with the space ID where you want them to appear. Below are several examples:

::::{important}
in order to use this API, you need {{kib}}'s built-in `superuser` role.
::::

:::{dropdown} View current orphan response actions space id:

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

To remove the space ID used to display the orphan response actions, this update API can be called with an empty string for spaceId.
