---
navigation_title: Migrate to {{ilm-init}} (self-managed and ECK)
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-with-existing-indices.html
applies_to:
  deployment:
    self: ga
    eck: ga
products:
  - id: elasticsearch
---

# Migrate to {{ilm-init}} on self-managed and {{eck}} deployments [ilm-with-existing-indices]

If you’ve been using [](/manage-data/lifecycle/curator.md) or some other mechanism to manage periodic indices, you have a couple of options when [migrating to {{ilm-init}}](./migrate-index-management.md):

* Set up your index templates to use an {{ilm-init}} policy to manage your new indices. Once {{ilm-init}} is managing your current write index, you can apply an appropriate policy to your old indices.
* Reindex into an {{ilm-init}}-managed index.

::::{note}
* Starting in Curator version 5.7, Curator ignores {{ilm-init}}-managed indices.
* This document is specifically about setting up {{ilm-init}} for managed indices. To manage the lifecycle of a [data stream](/manage-data/data-store/data-streams.md) you can opt to use either {{ilm-init}} or data stream lifecycle. Refer to [](/manage-data/lifecycle.md) for a comparison.
::::



## Apply policies to existing time series indices [ilm-existing-indices-apply]

The simplest way to transition to managing your periodic indices with {{ilm-init}} is to [configure an index template](configure-lifecycle-policy.md#apply-policy-template) to apply a lifecycle policy to new indices. A number of [example {{ilm-init}} polices](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-rollover.md#ilm-rollover-ex) are available, showing how index rollover can be initiated based on different criteria.

Once the index you are writing to is being managed by {{ilm-init}}, you can manually [apply a policy to your older indices](/manage-data/lifecycle/index-lifecycle-management/policy-apply.md). Define a separate policy for your older indices that omits the rollover action. Rollover is used to manage where new data goes, so isn’t applicable.

Keep in mind that policies applied to existing indices compare the `min_age` for each phase to the original creation date of the index, and might proceed through multiple phases immediately. If your policy performs resource-intensive operations like force merge, you don’t want to have a lot of indices performing those operations all at once when you switch over to {{ilm-init}}.

You can specify different `min_age` values in the policy you use for existing indices, or set [`index.lifecycle.origination_date`](elasticsearch://reference/elasticsearch/configuration-reference/index-lifecycle-management-settings.md#index-lifecycle-origination-date) to control how the index age is calculated.

Once all pre-{{ilm-init}} indices have been aged out and removed, you can delete the policy you used to manage them.

::::{note}
If you are using {{beats}} or {{ls}}, enabling {{ilm-init}} in version 7.0 and onward sets up {{ilm-init}} to manage new indices automatically. If you are using {{beats}} through {{ls}}, you might need to change your {{ls}} output configuration and invoke the {{beats}} setup to use {{ilm-init}} for new data.
::::



## Reindex into a managed index [ilm-existing-indices-reindex]

An alternative to [applying policies to existing indices](#ilm-existing-indices-apply) is to reindex your data into an {{ilm-init}}-managed index. You might want to do this if creating periodic indices with very small amounts of data has led to excessive shard counts, or if continually indexing into the same index has led to large shards and performance issues.

First, you need to set up the new {{ilm-init}}-managed index:

1. Update your index template to include the necessary {{ilm-init}} settings.
2. Bootstrap an initial index as the write index.
3. Stop writing to the old indices and index new documents using the alias that points to bootstrapped index.

To reindex into the managed index:

1. Pause indexing new documents if you do not want to mix new and old data in the {{ilm-init}}-managed index. Mixing old and new data in one index is safe, but a combined index needs to be retained until you are ready to delete the new data.
2. Reduce the {{ilm-init}} poll interval to ensure that the index doesn’t grow too large while waiting for the rollover check. By default, {{ilm-init}} checks to see what actions need to be taken every 10 minutes.

    ```console
    PUT _cluster/settings
    {
      "persistent": {
        "indices.lifecycle.poll_interval": "1m" <1>
      }
    }
    ```

    1. Check once a minute to see if {{ilm-init}} actions such as rollover need to be performed.

3. Reindex your data using the [reindex API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex). If you want to partition the data in the order in which it was originally indexed, you can run separate reindex requests.

    ::::{important}
    Documents retain their original IDs. If you don’t use automatically generated document IDs, and are reindexing from multiple source indices, you might need to do additional processing to ensure that document IDs don’t conflict. One way to do this is to use a [script](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) in the reindex call to append the original index name to the document ID.
    ::::


    ```console
    POST _reindex
    {
      "source": {
        "index": "mylogs-*" <1>
      },
      "dest": {
        "index": "mylogs", <2>
        "op_type": "create" <3>
      }
    }
    ```

    1. Matches your existing indices. Using the prefix for the new indices makes using this index pattern much easier.
    2. The alias that points to your bootstrapped index.
    3. Halts reindexing if multiple documents have the same ID. This is recommended to prevent accidentally overwriting documents if documents in different source indices have the same ID.

4. When reindexing is complete, set the {{ilm-init}} poll interval back to its default value to prevent unnecessary load on the master node:

    ```console
    PUT _cluster/settings
    {
      "persistent": {
        "indices.lifecycle.poll_interval": null
      }
    }
    ```

5. Resume indexing new data using the same alias.

    Querying using this alias will now search your new data and all of the reindexed data.

6. Once you have verified that all of the reindexed data is available in the new managed indices, you can safely remove the old indices.
