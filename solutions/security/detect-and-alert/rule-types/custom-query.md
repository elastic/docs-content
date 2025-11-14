---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/rules-ui-create.html#create-custom-rule
  - https://www.elastic.co/guide/en/serverless/current/security-rules-create.html#create-custom-rule
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Create a custom query rule [create-custom-rule]

Custom query rules search for events matching a KQL or Lucene query and create alerts when matches are found. This is the most common rule type, suitable for approximately 90% of detection use cases.

**When to use**: Detect single events that match specific criteria (e.g., failed login, specific process execution, network connection to suspicious IP).

**Performance**: Fast execution (~50-100ms per run), suitable for 5-minute intervals.

## Create the rule

1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then click **Create new rule**.
2. To create a rule based on a KQL or Lucene query, select **Custom query** on the **Create new rule** page, then:

    1. Define which {{es}} indices or data view the rule searches for alerts.
    2. Use the filter and query fields to create the criteria used for detecting alerts.

        The following example (based on the prebuilt rule [Volume Shadow Copy Deleted or Resized via VssAdmin](https://www.elastic.co/guide/en/security/8.17/prebuilt-rule-0-14-2-volume-shadow-copy-deleted-or-resized-via-vssadmin.html)) detects when the `vssadmin delete shadows` Windows command is executed:

        * **Index patterns**: `winlogbeat-*`

            Winlogbeat ships Windows event logs to {{elastic-sec}}.

        * **Custom query**: `event.action:"Process Create (rule: ProcessCreate)" and process.name:"vssadmin.exe" and process.args:("delete" and "shadows")`

            Searches the `winlogbeat-*` indices for `vssadmin.exe` executions with the `delete` and `shadow` arguments, which are used to delete a volume's shadow copies.

            :::{image} /solutions/images/security-rule-query-example.png
            :alt: Rule query example
            :screenshot:
            :::

    3. You can use {{kib}} saved queries (![Saved query menu](/solutions/images/security-saved-query-menu.png "title =20x20")) and queries from saved Timelines (**Import query from saved Timeline**) as rule conditions.

        When you use a saved query, the **Load saved query "*query name*" dynamically on each rule execution** check box appears:

        * Select this to use the saved query every time the rule runs. This links the rule to the saved query, and you won't be able to modify the rule's **Custom query** field or filters because the rule will only use settings from the saved query. To make changes, modify the saved query itself.
        * Deselect this to load the saved query as a one-time way of populating the rule's **Custom query** field and filters. This copies the settings from the saved query to the rule, so you can then further adjust the rule's query and filters as needed. If the saved query is later changed, the rule will not inherit those changes.

3. (Optional) Use **Suppress alerts by** to reduce the number of repeated or duplicate alerts created by the rule. Refer to [Suppress detection alerts](/solutions/security/detect-and-alert/suppress-detection-alerts.md) for more information.
4. (Optional) Create a list of **Required fields** that the rule needs to function. This list is informational only, to help users understand the rule; it doesn't affect how the rule actually runs.

    1. Click **Add required field**, then select a field from the index patterns or data view you specified for the rule. You can also start typing a field's name to find it faster, or type in an entirely new custom field.
    2. Enter the field's data type.

5. (Optional) Add **Related integrations** to associate the rule with one or more [Elastic integrations](https://docs.elastic.co/en/integrations). This indicates the rule's dependency on specific integrations and the data they generate, and allows users to confirm each integration's [installation status](/solutions/security/detect-and-alert/manage-detection-rules.md#rule-prerequisites) when viewing the rule.

    1. Click **Add integration**, then select an integration from the list. You can also start typing an integration's name to find it faster.
    2. Enter the version of the integration you want to associate with the rule, using [semantic versioning](https://semver.org/). For version ranges, you must use tilde or caret syntax. For example, `~1.2.3` is from 1.2.3 to any patch version less than 1.3.0, and `^1.2.3` is from 1.2.3 to any minor and patch version less than 2.0.0.

6. Click **Continue** to [configure basic rule settings](/solutions/security/detect-and-alert/create-detection-rule.md#rule-ui-basic-params).

## Example: Detect failed SSH login attempts

**Use case**: Alert when an IP address attempts SSH authentication more than 10 times in 10 minutes.

**Prerequisites**:
* {{filebeat}} system module OR {{auditbeat}} installed and collecting auth logs
* Field `system.auth.ssh.event` must exist in your data

**Configuration**:
* **Index patterns**: `filebeat-*,auditbeat-*`
* **Custom query**: `system.auth.ssh.event: "Failed" AND source.ip: *`

**Testing**: Before creating the rule, verify the query returns results in **Discover**. If you get zero results, check that:
* {{filebeat}} system module is enabled: `filebeat modules list`
* Auth logs are being collected (check `/var/log/auth.log` on Ubuntu or `/var/log/secure` on RHEL)
* Data is reaching {{es}}: Look for `system.auth` indices in **Index Management**

**Expected behavior**: Rule creates one alert per execution when matches are found. For threshold-based counting (e.g., "10+ failures from same IP"), use a Threshold rule instead.

**Tuning**:
* Add exceptions for known security scanners: `source.ip is not <scanner-ip>`
* If receiving too many alerts, increase threshold or add more specific filters

## Example: Detect unusual outbound network connections

**Use case**: Alert when servers in your DMZ or web tier make unexpected outbound connections to public IPs.

**Prerequisites**:
* {{packetbeat}} or {{filebeat}} with network logs
* Field `network.direction` must exist

**Configuration**:
* **Index patterns**: `packetbeat-*,logs-network-*`
* **Custom query**:
  ```kql
  host.name: (web-server-* OR dmz-*) AND network.direction: outbound AND NOT destination.ip: (10.0.0.0/8 OR 172.16.0.0/12 OR 192.168.0.0/16) AND NOT destination.port: (80 OR 443 OR 53 OR 123)
  ```

**Query explanation**:
* Matches servers with specific naming patterns (adjust `host.name` to match your environment)
* Only outbound connections
* Excludes private IP ranges (RFC1918)
* Excludes common legitimate services: HTTP (80), HTTPS (443), DNS (53), NTP (123)

**Expected alert volume**: 0-10 per day initially. Tune with exceptions as you identify legitimate outbound connections (package updates, monitoring agents, backup systems).

**Common false positives**:
* Package managers (apt, yum) connecting to update repositories: Add exception for specific `process.name`
* Monitoring agents: Add exception for known monitoring service destinations
* Time synchronization: Add exception for `destination.port: 123` if using public NTP servers

