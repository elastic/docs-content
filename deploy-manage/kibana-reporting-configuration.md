---
navigation_title: Configure {{kib}} reporting
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/secure-reporting.html
applies_to:
  deployment:
    self: all
    ece: all
    eck: all
    ess: all
products:
  - id: kibana
---

% this anchor belongs to `kibana reporting production considerations doc`
$$$reporting-chromium-sandbox$$$

# Configure {{kib}} reporting [secure-reporting]

{{kib}}'s reporting functionality offers multiple ways to share **Discover** sessions, dashboards, **Visualize Library** visualizations, and **Canvas** workpads.

This section covers the necessary configuration to ensure reporting works correctly in your deployment. For guidance on using {{report-features}} effectively, refer to [](/explore-analyze/report-and-share.md).

::::{admonition} Note for self-managed deployments
{{kib}} PNG/PDF reporting uses a custom binary of headless Chromium, and support comes with special caveats:

* The functionality requires special OS dependencies which may not be available for all distributions and configurations of Linux.
* It is subject to system resource configurations such as the limited number of file descriptors, allowed processes, and types of processes.
* Linux versions that are in end-of-life phase are not supported.
* Linux systems with `SELinux` or `fapolicyd` are not supported.

Before upgrading {{kib}} in a production environment, we encourage you to test your screenshotting use cases in a pre-production environment to make sure your hosts support our latest build of Chromium. For the most reliable configuration of PDF/PNG {{report-features}}, consider installing {{kib}} using [Docker](/deploy-manage/deploy/self-managed/install-kibana-with-docker.md), or using [{{ecloud}}](https://cloud.elastic.co).
::::

## Configuration overview

To secure {{report-features}}, you must grant users access to reporting functionality and protect the reporting endpoints with TLS/SSL encryption. Additionally, you can install graphical packages on the operating system to enable screenshot capabilities in the {{kib}} server.

:::{note}
:applies_to: {stack: ga, serverless: unavailable}
API keys are used to authenticate requests to generate reports. If you have a cross-cluster search environment and want to generate reports from remote clusters, you must have the appropriate cluster and index privileges on the remote cluster and local cluster. For example, if requests are authenticated with an API key, the API key requires certain privileges on the local cluster that contains the leader index, instead of the remote. For more information and examples, refer to [Configure roles and users for remote clusters](../deploy-manage/remote-clusters/remote-clusters-cert.md#remote-clusters-privileges-cert).
:::

Configuring reporting in your environment involves two main areas:

### Granting users access to {{report-features}}

Depending on your license, the type of users, and whether you prefer using the {{kib}} UI or API, there are multiple ways to [grant access to reporting functionality](#grant-user-access).

### Applying system configuration

The following configurations are required at {{es}}, {{kib}}, and OS levels to support {{report-features}}.

::::{important}
These steps apply only to **self-managed deployments**. Orchestrated deployments include this configuration by default. For more details on different deployment options, refer to [](/deploy-manage/deploy.md).
::::

* [Secure the reporting endpoints](#securing-reporting)
* [Install the dependencies for the headless browser](#install-reporting-packages)
* [Set the `server.host` for the headless browser](#set-reporting-server-host)
* [Ensure {{es}} allows built-in templates](#reporting-elasticsearch-configuration)

## Grant users access to reporting [grant-user-access]
```yaml {applies_to}
  deployment:
    self: all
    ece: all
    eck: all
    ess: all
```

Choose the method that best fits your use case.

:::::{tab-set}

::::{tab-item} Using {{kib}} UI

When security is enabled, you grant users access to {{report-features}} with [{{kib}} application privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md), which allow you to create custom roles that control the spaces and applications where users generate reports.

1. Create the reporting role.

    1. Go to the **Roles** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
    2. Click **Create role**.

2. Specify the role settings.

    1. Enter the **Role name**. For example, `custom_reporting_user`.
    2. Specify the **Indices** and **Privileges**.

        Access to data is an index-level privilege. For each index that contains the data you want to include in reports, add a line, then give each index `read` and `view_index_metadata` privileges.

        :::{note}
        If you use index aliases, you must also grant `read` and `view_index_metadata` privileges to underlying indices to generate CSV reports.
        :::

        For more information, refer to [Security privileges](elasticsearch://reference/elasticsearch/security-privileges.md).

3. Add the {{kib}} privileges.

    1. Click **Add {{kib}} privilege**.
    2. Select one or more **Spaces**.
    3. Click **Customize**, then click **Analytics**.
    4. For each application, select **All**, or to customize the privileges, select **Read** and **Customize sub-feature privileges**.

        :::{note}
        If you have a Basic license, sub-feature privileges are unavailable.
        :::

        :::{note}
        If the **Reporting** options for application features are unavailable, and the cluster license is higher than Basic, contact your administrator.
        :::

        :::{image} /deploy-manage/images/kibana-kibana-privileges-with-reporting.png
        :alt: {{kib}} privileges with Reporting options, Gold or higher license
        :screenshot:
        :::

    5. Click **Add {{kib}} privilege**.

4. Click **Create role**.
5. Assign the reporting role to a user.

    1. Go to the **Users** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
    2. Select the user you want to assign the reporting role to.
    3. From the **Roles** dropdown, select **custom_reporting_user**.
    4. Click **Update user**.


Granting the privilege to generate reports also grants the user the privilege to view their reports in **Reporting**. Users can only access their own reports.

To view reports, go to the **Reporting** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).


::::

::::{tab-item} Using role API

With [{{kib}} application privileges](#grant-user-access), you can use the [role APIs](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-roles) to grant access to the {{report-features}}, using **All** privileges, or sub-feature privileges.

:::{note}
This API request needs to be run against the [{{kib}} API endpoint](https://www.elastic.co/docs/api/doc/kibana/).
:::

```console
PUT <kibana host>:<port>/api/security/role/custom_reporting_user
{
  "elasticsearch": {
    "cluster": [],
    "indices": [],
    "run_as": []
  },
  "kibana": [{
    "spaces": ["*"],
    "base": [],
    "feature": {
      "dashboard_v2": ["generate_report",  <1>
      "download_csv_report"], <2>
      "discover_v2": ["generate_report"], <3>
      "canvas": ["generate_report"], <4>
      "visualize_v2": ["generate_report"] <5>
    }
  }]
}
```

1. Grants access to generate PNG and PDF reports in **Dashboard**.
2. Grants access to generate CSV reports from saved Discover session panels in **Dashboard**.
3. Grants access to generate CSV reports from saved Discover sessions in **Discover**.
4. Grants access to generate PDF reports in **Canvas**.
5. Grants access to generate PNG and PDF reports in **Visualize Library**.
::::

::::{tab-item} External providers

If you are using an external identity provider, such as LDAP or Active Directory, you can assign roles to individual users or groups of users. Role mappings are configured in [`config/role_mapping.yml`](/deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md).

For example, assign the `kibana_admin` and `custom_reporting_user` roles to the Bill Murray user:

```yaml
kibana_admin:
  - "cn=Bill Murray,dc=example,dc=com"
custom_reporting_user:
  - "cn=Bill Murray,dc=example,dc=com"
```

::::

::::{tab-item} Basic license

With a Basic license, sub-feature [application privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md) are unavailable, requiring you to select **All** privileges for the applications where users can create reports. You can grant users access through the {{kib}} UI or role API.

Example using {{kib}} UI:

:::{image} /deploy-manage/images/kibana-kibana-privileges-with-reporting-basic.png
:alt: {{kib}} privileges with Reporting options, Basic license
:screenshot:
:::

Example using [role API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-roles) to grant access to CSV {{report-features}}:

```console
PUT localhost:5601/api/security/role/custom_reporting_user
{
  "elasticsearch": { "cluster": [], "indices": [], "run_as": [] },
  "kibana": [
    {
      "base": [],
      "feature": {
        "dashboard_v2": [ "all" ], <1>
        "discover_v2": [ "all" ], <2>
      },
      "spaces": [ "*" ]
    }
  ],
  "metadata": {} <3>
}
```
1. Grants access to generate CSV reports from saved Discover sessions in **Discover**.
2. Grants access to generate CSV reports from saved Discover session panels in **Dashboard**.
3. Optional

::::

:::::

## System configuration
```yaml {applies_to}
  deployment:
    self: all
```
The following configurations are required at {{es}}, {{kib}}, and OS levels to support reporting features.

These steps apply only to **self-managed deployments**. Orchestrated deployments include this configuration by default. For more details on different deployment options, refer to [](/deploy-manage/deploy.md).

### Secure the reporting endpoints [securing-reporting]

To automatically generate reports with {{watcher}}, you must configure {{watcher}} to trust the {{kib}} server certificate.

1. Enable {{stack-security-features}} on your {{es}} cluster. For more information, see [](/deploy-manage/security.md).
2. Configure TLS/SSL encryption for the {{kib}} server. For more information, see [*Encrypt TLS communications in {{kib}}*](/deploy-manage/security/set-up-basic-security-plus-https.md#encrypt-kibana-http).
3. Specify the {{kib}} server CA certificate chain in [`elasticsearch.yml`](/deploy-manage/stack-settings.md):

    If you are using your own CA to sign the {{kib}} server certificate, then you need to specify the CA certificate chain in {{es}} to properly establish trust in TLS connections between {{watcher}} and {{kib}}. If your CA certificate chain is contained in a PKCS #12 trust store, specify it like so:

    ```yaml
    xpack.http.ssl.truststore.path: "/path/to/your/truststore.p12"
    xpack.http.ssl.truststore.type: "PKCS12"
    xpack.http.ssl.truststore.password: "optional decryption password"
    ```

    Otherwise, if your CA certificate chain is in PEM format, specify it like so:

    ```yaml
    xpack.http.ssl.certificate_authorities: ["/path/to/your/cacert1.pem", "/path/to/your/cacert2.pem"]
    ```

    For more information, see [the {{watcher}} HTTP TLS/SSL Settings](elasticsearch://reference/elasticsearch/configuration-reference/watcher-settings.md#ssl-notification-settings).

4. Add one or more users who have access to the {{report-features}}.

    Once you’ve enabled SSL for {{kib}}, all requests to the reporting endpoints must include valid credentials.


For more information on sharing reports, direct links, and more, refer to [Reporting and sharing](/explore-analyze/report-and-share.md).


### Install the dependencies for the headless browser [install-reporting-packages]

If using PNG/PDF {{report-features}}, make sure the {{kib}} server operating system has the appropriate packages installed for the distribution.

If you are using RHEL operating systems, install the following packages:

* `xorg-x11-fonts-100dpi`
* `xorg-x11-fonts-75dpi`
* `xorg-x11-utils`
* `xorg-x11-fonts-cyrillic`
* `xorg-x11-fonts-Type1`
* `xorg-x11-fonts-misc`
* `vlgothic-fonts`
* `fontconfig`
* `freetype`

If you are using Ubuntu/Debian systems, install the following packages:

* `fonts-liberation`
* `libfontconfig1`
* `libnss3`

The screenshotting plugin used for {{report-features}} has a built-in utility to check for common issues, such as missing dependencies. See [Reporting diagnostics](/explore-analyze/report-and-share/reporting-troubleshooting-pdf.md#reporting-diagnostics) for more information.


### Set the `server.host` for the headless browser [set-reporting-server-host]

If using PNG/PDF {{report-features}} in a production environment, it is preferred to use the setting of `server.host: 0.0.0.0` in the [`kibana.yml`](/deploy-manage/stack-settings.md) configuration file. This allows the headless browser used for PDF/PNG reporting to reach {{kib}} over a local interface, while also allowing the {{kib}} server to listen on outward-facing network interfaces, as it makes the {{kib}} server accessible from any network interface on the machine. Make sure that no firewall rules or other routing rules prevent local services from accessing this address.


### Ensure {{es}} allows built-in templates [reporting-elasticsearch-configuration]

Reporting relies on {{es}} to install a mapping template for the data stream that stores reports. Ensure that {{es}} allows built-in templates to be installed by keeping the `stack.templates.enabled` setting at the default value of `true`. For more information, see [Index management settings](elasticsearch://reference/elasticsearch/configuration-reference/index-management-settings.md#stack-templates-enabled).

