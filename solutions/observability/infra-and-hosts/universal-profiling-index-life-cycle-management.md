---
navigation_title: Index lifecycle management
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/profiling-index-lifecycle-management.html
applies_to:
  stack: ga
products:
  - id: observability
---



# Universal Profiling index life cycle management [profiling-index-lifecycle-management]


Index lifecycle policies allow you to automate the lifecycle of your profiling indices as they grow and age. A default policy is applied, but you can customize it based on your business needs.


## Default policy [profiling-ilm-default-policy]

The default Universal Profiling index lifecycle policy includes the following rollover and delete definitions:

* **Rollover**: Rollover prevents a single index from growing too large and optimizes indexing and search performance. After an age or size metric threshold is met, a new index is created and all subsequent updates are written to the new index.
* **Delete**: The delete phase permanently removes the index after a time threshold is met.

The following table lists the default thresholds for rollover and delete:

| Rollover | Warm tier | Delete |
| --- | --- | --- |
| after 30 days or 50 GB | after 30 days | after 60 days |

::::{note}
The [rollover condition blocks phase transitions](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-rollover.md#_rollover_condition_blocks_phase_transition) which means that indices are kept 30 days **after** rollover on the hot tier.
::::


To view the Universal Profiling index lifecycle policy in {{kib}}, open **Index Lifecycle Management** from the navigation menu or using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), and search for `profiling`.

::::{tip}
Default {{ilm-init}} policies can change between minor versions. This is not considered a breaking change as index management should continually improve and adapt to new features.
::::



## Configure a custom index lifecycle policy [profiling-ilm-custom-policy]

Complete the following steps to configure a custom index lifecycle policy.


### Step 1: Create an index lifecycle policy [profiling-ilm-custom-policy-create-policy]

1. Open the **Index Lifecycle Policies** management page from the navigation menu or using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Create policy**.
3. Name your new policy, for example `custom-profiling-policy`.
4. Customize the policy to your liking.
5. Click **Save policy**.

::::{tip}
See [Manage the index lifecycle](/manage-data/lifecycle/index-lifecycle-management.md) to learn more about {{ilm-init}} policies.
::::



### Step 2: Apply the index lifecycle policy [profiling-ilm-custom-policy-apply-policy]

To apply your new index lifecycle policy for Universal Profiling, create a new component template named `profiling-ilm@custom`.

::::{note}
To apply a custom {{ilm-init}} policy, you must name the component template `profiling-ilm@custom`. Other names are not supported.
::::


1. From the **Index Management** page, select the **Component Template** tab and click **Create component template**.
2. Enter `profiling-ilm@custom` as the name and click **Next**.
3. In **Index settings**, set the {{ilm-init}} policy name created in the previous step:

    ```json
    {
      "lifecycle": {
        "name": "custom-profiling-policy"
      }
    }
    ```

4. Continue to the **Review** step, and select the **Request** tab. Your request should look similar to the following image.

    If it does, click **Create component template**.

    :::{image} /solutions/images/observability-profiling-create-component-template.png
    :alt: Create component template
    :screenshot:
    :::



### Step 3: Rollover indices [profiling-ilm-custom-policy-rollover]

Confirm that Universal Profiling is now using the new index template and {{ilm-init}} policy:

1. Open **Console** by finding `Dev Tools` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Run the following:

    ```bash
    GET _ilm/policy/custom-profiling-policy <1>
    ```

    1. The name of the custom {{ilm-init}} policy chosen in [Step 1](#profiling-ilm-custom-policy-create-policy).


If the custom policy is already applied, the result should include the following:

```json
{
    "in_use_by": {
      "indices": [
        ...
      ],
      "data_streams": [
        ...
        "profiling-events-all",
        ...
      ],
      "composable_templates": [
        "profiling-stackframes",
        "profiling-symbols-global",
        "profiling-metrics",
        "profiling-stacktraces",
        "profiling-executables",
        "profiling-hosts",
        "profiling-events"
      ]
    }
}
```

If the result is empty, the custom {{ilm-init}} policy is not yet in use. New {{ilm-init}} policies only take effect when new indices are created, so either wait for a rollover to occur (usually after 30 days or when the index size reaches 50 GB), or force a rollover using the [{{es}} rollover API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-rollover):

```bash
POST /profiling-events-5pow01/_rollover/
POST /profiling-events-5pow02/_rollover/
POST /profiling-events-5pow03/_rollover/
POST /profiling-events-5pow04/_rollover/
POST /profiling-events-5pow05/_rollover/
POST /profiling-events-5pow06/_rollover/
POST /profiling-events-5pow07/_rollover/
POST /profiling-events-5pow08/_rollover/
POST /profiling-events-5pow09/_rollover/
POST /profiling-events-5pow10/_rollover/
POST /profiling-events-5pow11/_rollover/
POST /profiling-events-all/_rollover/
POST /profiling-executables/_rollover/
POST /profiling-hosts/_rollover/
POST /profiling-metrics/_rollover/
POST /profiling-stackframes/_rollover/
POST /profiling-stacktraces/_rollover/
POST /profiling-symbols-global/_rollover/
```

After the rollover, the custom {{ilm-init}} policy will be applied to new indices and data streams.
