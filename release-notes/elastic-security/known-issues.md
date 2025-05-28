---
navigation_title: Known issues
---

# {{elastic-sec}} known issues [elastic-security-known-issues]
Known issues are significant defects or limitations that may impact your implementation. These issues are actively being worked on and will be addressed in a future release. Review the {{elastic-sec}} known issues to help you make informed decisions, such as upgrading to a new version.

% Use the following template to add entries to this page.

% :::{dropdown} Title of known issue
% Applies to: Applicable versions for the known issue 
% Description of the known issue.
% For more information, check [Issue #](Issue link).
% **Impact**<br> Impact of the known issue.
% **Workaround**<br> Steps for a workaround until the known issue is fixed.

% :::

:::{dropdown} Installing an {{elastic-defend}} integration or a new agent policy upgrades installed prebuilt rules, reverting user customizations and overwriting user-added actions and exceptions

Applies to: {{stack}} 9.0.0

On April 10, 2025, it was discovered that when you install a new {{elastic-defend}} integration or agent policy, the installed prebuilt detection rules upgrade to their latest versions (if any new versions are available). The upgraded rules lose any user-added rule actions, exceptions, and customizations.  

**Workaround**

To resolve this issue, before you add an {{elastic-defend}} integration to a policy in {{fleet}}, apply any pending prebuilt rule updates. This will prevent rule actions, exceptions, and customizations from being overwritten.

**Resolved**<br> 

Resolved in {{stack}} 9.0.1

:::

:::{dropdown} The technical preview badge incorrectly displays on the alert suppression fields for event correlation rules

Applies to: {{stack}} 9.0.0 and 9.0.1

On April 8, 2025, it was discovered that alert suppression for event correlation rules is incorrectly shown as being in technical preview when you create a new rule. For more information, check [#1021](https://github.com/elastic/docs-content/issues/1021).

**Resolved**<br> 

Resolved in {{stack}} 9.0.1

:::


:::{dropdown} Interaction between Elastic Defend and Trellix Access Protection causes IRQL_NOT_LESS_EQUAL bugcheck

Applies to: {{elastic-defend}} 9.0.0

An `IRQL_NOT_LESS_EQUAL` [bugcheck](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/bug-checks--blue-screens-) in the {{elastic-defend}} driver happens due to an interaction with Trellix Access Protection (`mfehidk.sys`). This issue can occur when `elastic-endpoint-driver.sys` calls [`FwpmTransactionBegin0`](https://learn.microsoft.com/en-us/windows/win32/api/fwpmu/nf-fwpmu-fwpmtransactionbegin0) to initialize its network driver. `FwpmTransactionBegin0` performs a synchronous RPC call to the user-mode Base Filtering Engine service. Trellix's driver intercepts this service's operations, causing `FwpmTransactionBegin0` to hang or slow significantly. This delay prevents {{elastic-defend}} driver from properly initializing in a timely manner. Subsequent system activity can invoke {{elastic-defend}}'s driver before it has fully initialized, leading to a `IRQL_NOT_LESS_EQUAL` bugcheck. This issue affects {{elastic-defend}} versions 8.16.0-8.16.6, 8.17.0-8.17.5, 8.18.0, and 9.0.0.

**Workaround**<br> 

If you can't upgrade, either disable Trellix Access Protection or add a [Trellix Access Protection exclusion](https://docs.trellix.com/bundle/endpoint-security-10.6.0-threat-prevention-client-interface-reference-guide-windows/page/GUID-6AC245A1-5E5D-4BAF-93B0-FE7FD33571E6.html) for the Base Filtering Engine service (`C:\Windows\System32\svchost.exe`). 

**Resolved**<br> 

Resolved in {{elastic-defend}} 9.0.1

:::


:::{dropdown} Unbounded kernel non-paged memory growth issue in Elastic Defend's kernal driver causes slow down on Windows systems

Applies to: {{elastic-defend}} 9.0.0

An unbounded kernel non-paged memory growth issue in {{elastic-defend}}'s kernel driver occurs during extremely high event load situations on Windows. Systems affected by this issue will slow down or become unresponsive until the triggering event load (for example, network activity) subsides. We are only aware of this issue occurring on very busy Windows Server systems running {{elastic-defend}} versions 8.16.0-8.16.6, 8.17.0-8.17.5, 8.18.0, and 9.0.0

**Workaround**<br> 

If you can't upgrade, turn off the relevant event source at the kernel level using your {{elastic-defend}} [advanced policy settings (optional)](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#adv-policy-settings):

* Network Events - Set the `windows.advanced.kernel.network` advanced setting to `false`.
* Registry Events - Set the `windows.advanced.kernel.registry` advanced setting to `false`.

Note that clearing the corresponding checkbox under [event collection](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#event-collection) is insufficient, as {{elastic-defend}} may still process these event sources internally to support other features.

**Resolved**<br> 

Resolved in {{elastic-defend}} 9.0.1

:::
