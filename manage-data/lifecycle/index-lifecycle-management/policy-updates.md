---
navigation_title: "Update a policy"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/update-lifecycle-policy.html
applies_to:
  stack: ga
  serverless: ga
---

# Update a lifecycle policy


You can change how the lifecycle of an index or collection of rolling indices is managed by modifying the current policy or switching to a different policy.

To ensure that policy updates don’t put an index into a state where it can’t exit the current phase, the phase definition is cached in the index metadata when it enters the phase. If changes can be safely applied, {{ilm-init}} updates the cached phase definition. If they cannot, phase execution continues using the cached definition.

When the index advances to the next phase, it uses the phase definition from the updated policy.


## How changes are applied [ilm-apply-changes]

When a policy is initially applied to an index, the index gets the latest version of the policy. If you update the policy, the policy version is bumped and {{ilm-init}} can detect that the index is using an earlier version that needs to be updated.

Changes to `min_age` are not propagated to the cached definition. Changing a phase’s `min_age` does not affect indices that are currently executing that phase.

For example, if you create a policy that has a hot phase that does not specify a `min_age`, indices immediately enter the hot phase when the policy is applied. If you then update the policy to specify a `min_age` of 1 day for the hot phase, that has no effect on indices that are already in the hot phase. Indices created *after* the policy update won’t enter the hot phase until they are a day old.


## How new policies are applied [ilm-apply-new-policy]

When you apply a different policy to a managed index, the index completes the current phase using the cached definition from the previous policy. The index starts using the new policy when it moves to the next phase.

