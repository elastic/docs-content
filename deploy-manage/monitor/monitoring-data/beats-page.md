---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/beats-page.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
products:
  - id: kibana
---



# Beats metrics [beats-page]


If you are monitoring Beats, the **Stack Monitoring** page in {{kib}} contains a panel for Beats in the cluster overview.

% Candidate for removal: low value. The sentence before it already says the page has a Beats panel, so the crop adds counts only. Used only on this page.
:::{image} /deploy-manage/images/kibana-monitoring-beats.png
:alt: Monitoring Beats
:screenshot:
:::

To view an overview of the Beats data in the cluster, click **Overview**. The overview page has a section for activity in the last day, which is a real-time sample of data. The summary bar and charts follow the typical paradigm of data in the Monitoring UI, which is bound to the span of the time filter. This overview page can therefore show up-to-date or historical information.

:::{image} /deploy-manage/images/kibana-monitoring-beats-detail.png
:alt: Beats overview page with the summary bar, the activity in the last day, and charts
:screenshot:
:::

To view a listing of the individual Beat instances in the cluster, click **Beats**. The table listing shows each Beat instance that reports data to the monitoring cluster. All columns are sortable. Clicking a Beat name takes you to the detail page.

The detail page contains a summary bar and charts. There are more charts on this page than the overview page and they are specific to a single Beat instance.

