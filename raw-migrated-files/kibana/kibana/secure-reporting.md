---
navigation_title: "Configure reporting"
---

# Configure reporting in {{kib}} [secure-reporting]


::::{note}
Kibana PNG/PDF Reporting uses a custom binary of headless Chromium, and support comes with special caveats:

* The functionality requires special OS dependencies which may not be available for all distributions and configurations of Linux.
* It is subject to system resource configurations such as the limited number of file descriptors, allowed processes, and types of processes.
* Linux versions that are in end-of-life phase are not supported.
* Linux systems with SELinux or fapolicyd are not supported.

Before upgrading Kibana in a production environment, we encourage you to test your screenshotting use cases in a pre-production environment to make sure your hosts support our latest build of Chromium. For the most reliable configuration of PDF/PNG {{report-features}}, consider installing {{kib}} using [Docker](../../../deploy-manage/deploy/self-managed/install-with-docker.md), or using [Elastic Cloud](https://cloud.elastic.co).

::::


For security, you grant users access to the {{report-features}} and secure the reporting endpoints with TLS/SSL encryption. Additionally, you can install graphical packages into the operating system to enable the {{kib}} server to have screenshotting capabilities.

* [Grant users access to reporting](../../../explore-analyze/report-and-share.md#grant-user-access)
* [Grant access with the role API](../../../explore-analyze/report-and-share.md#reporting-roles-user-api)
* [Grant users access with a Basic license](../../../explore-analyze/report-and-share.md#grant-user-access-basic)
* [Grant access using an external provider](../../../explore-analyze/report-and-share.md#grant-user-access-external-provider)
* [Secure the reporting endpoints](../../../explore-analyze/report-and-share.md#securing-reporting)
* [Install the dependencies for the headless browser](../../../explore-analyze/report-and-share.md#install-reporting-packages)
* [Set the `server.host` for the headless browser](../../../explore-analyze/report-and-share.md#set-reporting-server-host)
* [Ensure {{es}} allows built-in templates](../../../explore-analyze/report-and-share.md#reporting-elasticsearch-configuration)


## Grant users access to reporting [grant-user-access]

When security is enabled, you grant users access to {{report-features}} with [{{kib}} application privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md), which allow you to create custom roles that control the spaces and applications where users generate reports.

1. Create the reporting role.

    1. Go to the **Roles** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
    2. Click **Create role**.

2. Specify the role settings.

    1. Enter the **Role name**. For example, `custom_reporting_user`.
    2. Specify the **Indices** and **Privileges**.

        Access to data is an index-level privilege. For each index that contains the data you want to include in reports, add a line, then give each index `read` and `view_index_metadata` privileges.

        ::::{note}
        If you use index aliases, you must also grant `read` and `view_index_metadata` privileges to underlying indices to generate CSV reports.
        ::::


        For more information, refer to [Security privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md).

3. Add the {{kib}} privileges.

    1. Click **Add Kibana privilege**.
    2. Select one or more **Spaces**.
    3. Click **Customize**, then click **Analytics**.
    4. For each application, select **All**, or to customize the privileges, select **Read** and **Customize sub-feature privileges**.

        ::::{note}
        If you have a Basic license, sub-feature privileges are unavailable. For details, check out [Grant users access with a Basic license](../../../explore-analyze/report-and-share.md#grant-user-access-basic).
        ::::


        :::{image} ../../../images/kibana-kibana-privileges-with-reporting.png
        :alt: Kibana privileges with Reporting options, Gold or higher license
        :class: screenshot
        :::

        ::::{note}
        If the **Reporting** options for application features are unavailable, and the cluster license is higher than Basic, contact your administrator.
        ::::

    5. Click **Add {{kib}} privilege**.

4. Click **Create role**.
5. Assign the reporting role to a user.

    1. Go to the **Users** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
    2. Select the user you want to assign the reporting role to.
    3. From the **Roles** dropdown, select **custom_reporting_user**.
    4. Click **Update user**.


Granting the privilege to generate reports also grants the user the privilege to view their reports in **Stack Management > Reporting**. Users can only access their own reports.


### Grant access with the role API [reporting-roles-user-api]

With [{{kib}} application privileges](../../../explore-analyze/report-and-share.md#grant-user-access), you can use the [role APIs](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-roles) to grant access to the {{report-features}}, using **All** privileges, or sub-feature privileges.

::::{note}
This API request needs to be run against the [Kibana API endpoint](https://www.elastic.co/guide/en/kibana/current/api.html).
::::


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



## Grant users access with a Basic license [grant-user-access-basic]

With a Basic license, you can grant users access with custom roles to {{report-features}} with [{{kib}} application privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md). However, with a Basic license, sub-feature privileges are unavailable. [Create a role](../../../explore-analyze/report-and-share.md#grant-user-access), then select **All** privileges for the applications where users can create reports.

:::{image} ../../../images/kibana-kibana-privileges-with-reporting-basic.png
:alt: Kibana privileges with Reporting options, Basic license
:class: screenshot
:::

With a Basic license, sub-feature application privileges are unavailable, but you can use the [role API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-role) to grant access to CSV {{report-features}}:

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



### Grant access using an external provider [grant-user-access-external-provider]

If you are using an external identity provider, such as LDAP or Active Directory, you can assign roles to individual users or groups of users. Role mappings are configured in [`config/role_mapping.yml`](../../../deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md).

For example, assign the `kibana_admin` and `reporting_user` roles to the Bill Murray user:

```yaml
kibana_admin:
  - "cn=Bill Murray,dc=example,dc=com"
reporting_user:
  - "cn=Bill Murray,dc=example,dc=com"
```


## Secure the reporting endpoints [securing-reporting]

To automatically generate reports with {{watcher}}, you must configure {{watcher}} to trust the {{kib}} server certificate.

1. Enable {{stack-security-features}} on your {{es}} cluster. For more information, see [Getting started with security](https://www.elastic.co/guide/en/elasticsearch/reference/current/secure-cluster.html).
2. Configure TLS/SSL encryption for the {{kib}} server. For more information, see [*Encrypt TLS communications in {{kib}}*](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-basic-setup-https.html#encrypt-kibana-http).
3. Specify the {{kib}} server CA certificate chain in `elasticsearch.yml`:

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

    For more information, see [the {{watcher}} HTTP TLS/SSL Settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/notification-settings.html#ssl-notification-settings).

4. Add one or more users who have access to the {{report-features}}.

    Once you’ve enabled SSL for {{kib}}, all requests to the reporting endpoints must include valid credentials.


For more information on sharing reports, direct links, and more, refer to [Reporting and sharing](../../../explore-analyze/report-and-share.md).


## Install the dependencies for the headless browser [install-reporting-packages]

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

The screenshotting plugin used for {{report-features}} has a built-in utility to check for common issues, such as missing dependencies. See [Reporting diagnostics](../../../explore-analyze/report-and-share/reporting-troubleshooting-pdf.md#reporting-diagnostics) for more information.


## Set the `server.host` for the headless browser [set-reporting-server-host]

If using PNG/PDF {{report-features}} in a production environment, it is preferred to use the setting of `server.host: 0.0.0.0` in the `kibana.yml` configuration file. This allows the headless browser used for PDF/PNG reporting to reach {{kib}} over a local interface, while also allowing the {{kib}} server to listen on outward-facing network interfaces, as it makes the {{kib}} server accessible from any network interface on the machine. Make sure that no firewall rules or other routing rules prevent local services from accessing this address.


## Ensure {{es}} allows built-in templates [reporting-elasticsearch-configuration]

Reporting relies on {{es}} to install a mapping template for the data stream that stores reports. Ensure that {{es}} allows built-in templates to be installed by keeping the `stack.templates.enabled` setting at the default value of `true`. For more information, see [Index management settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-management-settings.html#stack-templates-enabled).

