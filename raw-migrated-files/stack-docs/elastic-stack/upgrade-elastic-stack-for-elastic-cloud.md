# Upgrade on Elastic Cloud [upgrade-elastic-stack-for-elastic-cloud]

Once you are [prepared to upgrade](../../../deploy-manage/upgrade/deployment-or-cluster.md), a single click in the Elastic Cloud console can upgrade a deployment to a newer version, add more processing capacity, change plugins, and enable or disable high availability, all at the same time. During the upgrade process, {{es}}, {{kib}}, and all of your deployment components are upgraded simultaneously.

Minor version upgrades, upgrades from 8.17 to 9.0.0-beta1, and cluster configuration changes can be performed with no downtime. Elastic Cloud only supports upgrades to released versions. Preview releases and master snapshots are not supported.

{{ech}} and {{ece}} do not support the ability to upgrade to or from release candidate builds, such as 8.0.0-rc1.

If you use a separate [monitoring deployment](../../../deploy-manage/monitor/stack-monitoring/elastic-cloud-stack-monitoring.md), you should upgrade the monitoring deployment before the production deployment. In general, the monitoring deployment and the deployments being monitored should be running the same version of the Elastic Stack. A monitoring deployment cannot monitor production deployments running newer versions of the stack. If necessary, the monitoring deployment can monitor production deployments running the latest release of the previous major version.

::::{important} 
Although it’s simple to upgrade an Elastic Cloud deployment, the new version might include breaking changes that affect your application. Make sure you review the deprecation logs, make any necessary changes, and test against the new version before upgrading your production deployment.
::::


Upgrade Assistant
:   Prior to upgrading, Elastic Cloud checks the deprecation API to retrieve information about the cluster, node, and index-level settings that need to be removed or changed. If there are any issues that would prevent a successful upgrade, the upgrade is blocked. Use the [Upgrade Assistant](https://www.elastic.co/guide/en/kibana/8.17/upgrade-assistant.html) in 8.17 to identify and resolve issues and reindex any indices created before 7.0.

Snapshots
:   To keep your data safe during the upgrade process, a snapshot is taken automatically before any changes are made to your cluster. After a major version upgrade is complete and a snapshot of the upgraded cluster is available, all snapshots taken with the previous major version of {{es}} are stored in the snapshot repository.

    From version 8.3, snapshots are generally available as simple archives. Use the [archive functionality](../../../deploy-manage/upgrade/deployment-or-cluster/reading-indices-from-older-elasticsearch-versions.md) to search snapshots as old as version 5.0 without the need of an old {{es}} cluster. This ensures that data you store in {{es}} doesn’t have an end of life and is still accessible when you upgrade, without requiring a reindex process.

    On {{ece}}, you need to [configure a snapshot repository](/deploy-manage/tools/snapshot-and-restore/cloud-enterprise.md) to enable snapshots.


Breaking changes
:   Major version upgrades can include breaking changes that require you to take additional steps to ensure that your applications behave as expected after the upgrade. Make sure you test against the new version before upgrading existing deployments.

    Review the [*Breaking changes*](https://www.elastic.co/guide/en/elastic-stack/current/elastic-stack-breaking-changes.html) and upgrade your code to work with 9.0.0-beta1.


Known issues
:   In {{es}} 7.8 and later, {{ilm}} ({{ilm-init}}) is always enabled, even if the cluster is still using deprecated index curation methods. If index curation and {{ilm-init}} are both configured to manage the same indices, the outcome can be unpredictable. Elastic solutions default to using {{ilm-init}}, and we strongly encourage you to [migrate all of your indices to {{ilm-init}}](../../../manage-data/lifecycle/index-lifecycle-management.md).

Security realm settings
:   During the upgrade process, you are prompted to update the security realm settings if your user settings include a `xpack.security.authc.realms` value.

    If the security realms are configured in `user_settings`, you’ll be prompted to modify the settings:

    1. On the **Update security realm settings** window, edit the settings.
    2. Click **Update settings**. If the security realm settings are located in `user_settings_override`, contact support to help you upgrade.



## Perform the upgrade [perform-cloud-upgrade] 

Log in to your Elastic Cloud environment:

<style>
.tabs {
  width: 100%;
}
[role="tablist"] {
  margin: 0 0 -0.1em;
  overflow: visible;
}
[role="tab"] {
  position: relative;
  padding: 0.3em 0.5em 0.4em;
  border: 1px solid hsl(219, 1%, 72%);
  border-radius: 0.2em 0.2em 0 0;
  overflow: visible;
  font-family: inherit;
  font-size: inherit;
  background: hsl(220, 20%, 94%);
}
[role="tab"]:hover::before,
[role="tab"]:focus::before,
[role="tab"][aria-selected="true"]::before {
  position: absolute;
  bottom: 100%;
  right: -1px;
  left: -1px;
  border-radius: 0.2em 0.2em 0 0;
  border-top: 3px solid hsl(219, 1%, 72%);
  content: '';
}
[role="tab"][aria-selected="true"] {
  border-radius: 0;
  background: hsl(220, 43%, 99%);
  outline: 0;
}
[role="tab"][aria-selected="true"]:not(:focus):not(:hover)::before {
  border-top: 5px solid hsl(218, 96%, 48%);
}
[role="tab"][aria-selected="true"]::after {
  position: absolute;
  z-index: 3;
  bottom: -1px;
  right: 0;
  left: 0;
  height: 0.3em;
  background: hsl(220, 43%, 99%);
  box-shadow: none;
  content: '';
}
[role="tab"]:hover,
[role="tab"]:focus,
[role="tab"]:active {
  outline: 0;
  border-radius: 0;
  color: inherit;
}
[role="tab"]:hover::before,
[role="tab"]:focus::before {
  border-color: hsl(218, 96%, 48%);
}
[role="tabpanel"] {
  position: relative;
  z-index: 2;
  padding: 1em;
  border: 1px solid hsl(219, 1%, 72%);
  border-radius: 0 0.2em 0.2em 0.2em;
  box-shadow: 0 0 0.2em hsl(219, 1%, 72%);
  background: hsl(220, 43%, 99%);
  margin-bottom: 1em;
}
[role="tabpanel"] p {
  margin: 0;
}
[role="tabpanel"] * + p {
  margin-top: 1em;
}
</style>
<script>
window.addEventListener("DOMContentLoaded", () => {
  const tabs = document.querySelectorAll('[role="tab"]');
  const tabList = document.querySelector('[role="tablist"]');
  // Add a click event handler to each tab
  tabs.forEach(tab => {
    tab.addEventListener("click", changeTabs);
  });
  // Enable arrow navigation between tabs in the tab list
  let tabFocus = 0;
  tabList.addEventListener("keydown", e => {
    // Move right
    if (e.keyCode === 39 || e.keyCode === 37) {
      tabs[tabFocus].setAttribute("tabindex", -1);
      if (e.keyCode === 39) {
        tabFocus++;
        // If we're at the end, go to the start
        if (tabFocus >= tabs.length) {
          tabFocus = 0;
        }
        // Move left
      } else if (e.keyCode === 37) {
        tabFocus--;
        // If we're at the start, move to the end
        if (tabFocus < 0) {
          tabFocus = tabs.length - 1;
        }
      }
      tabs[tabFocus].setAttribute("tabindex", 0);
      tabs[tabFocus].focus();
    }
  });
});
function setActiveTab(target) {
  const parent = target.parentNode;
  const grandparent = parent.parentNode;
  // console.log(grandparent);
  // Remove all current selected tabs
  parent
    .querySelectorAll('[aria-selected="true"]')
    .forEach(t => t.setAttribute("aria-selected", false));
  // Set this tab as selected
  target.setAttribute("aria-selected", true);
  // Hide all tab panels
  grandparent
    .querySelectorAll('[role="tabpanel"]')
    .forEach(p => p.setAttribute("hidden", true));
  // Show the selected panel
  grandparent.parentNode
    .querySelector(`#${target.getAttribute("aria-controls")}`)
    .removeAttribute("hidden");
}
function changeTabs(e) {
  // get the containing list of the tab that was just clicked
  const tabList = e.target.parentNode;

  // get all of the sibling tabs
  const buttons = Array.apply(null, tabList.querySelectorAll('button'));

  // loop over the siblings to discover which index thje clicked one was
  const { index } = buttons.reduce(({ found, index }, button) => {
    if (!found && buttons[index] === e.target) {
      return { found: true, index };
    } else if (!found) {
      return { found, index: index + 1 };
    } else {
      return { found, index };
    }
  }, { found: false, index: 0 });

  // get the tab container
  const container = tabList.parentNode;
  // read the data-tab-group value from the container, e.g. "os"
  const { tabGroup } = container.dataset;
  // get a list of all the tab groups that match this value on the page
  const groups = document.querySelectorAll('[data-tab-group=' + tabGroup + ']');

  // for each of the found tab groups, find the tab button at the previously discovered index and select it for each group
  groups.forEach((group) => {
    const target = group.querySelectorAll('button')[index];
    setActiveTab(target);
  });
}
</script>
:::::::{tab-set}

::::::{tab-item} {{ech}}
1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co/?page=docs&placement=docs-body).
2. Select your deployment on the home page in the **Hosted deployments** card or go to the **Deployments** page.

    Narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.
::::::

::::::{tab-item} Elastic Cloud Enterprise
1. [Log into the Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md)
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.
::::::

:::::::
To upgrade a deployment:

1. In the **Deployment version** section, click **Upgrade**.
2. Select version 9.0.0-beta1.
3. Click **Upgrade** and then **Confirm upgrade**. The new configuration takes a few minutes to create.

    ::::{note} 
    If any incompatibilities are detected when you attempt to upgrade to 9.0.0-beta1, the UI provides a link to the Upgrade Assistant, which checks for deprecated settings in your cluster and indices and helps you resolve them. After resolving the issues, return to the **Deployments** page and restart the upgrade.
    ::::



## Upgrading {{es}} clients and ingest components [upgrading-clients-ingest] 

Once you have upgraded from 8.17, you need to update your {{es}} clients and ingest components in the following order:

1. Java API Client: [dependency configuration](asciidocalypse://docs/elasticsearch-java/docs/reference/installation.md#maven)
2. Logstash: [upgrade instructions](asciidocalypse://docs/logstash/docs/reference/upgrading-logstash.md)
3. Beats: [upgrade instructions](asciidocalypse://docs/beats/docs/reference/libbeat/upgrading.md)
4. {{agent}}: [upgrade instructions](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/upgrade-elastic-agent.md)


## Reindex to upgrade [upgrading-reindex] 

If you are running a pre-8.x version, you might need to perform multiple upgrades or a full-cluster restart to get to 8.17 to prepare to upgrade to 9.0.0-beta1.

Alternatively, you can create a new 9.0.0-beta1 deployment and reindex from remote:

1. Provision an additional deployment running 9.0.0-beta1.
2. Reindex your data into the new {{es}} cluster using [reindex from remote](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) and temporarily send new index requests to both clusters.
3. Verify that the new cluster performs as expected, fix any problems, and then permanently swap in the new cluster.
4. Delete the old deployment. On Elastic Cloud, you are billed only for the time that the new deployment runs in parallel with your old deployment. Usage is billed on an hourly basis.

