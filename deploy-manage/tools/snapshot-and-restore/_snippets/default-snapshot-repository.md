The default snapshot repository is a repository that {{es}} features can use when they need to perform snapshot or restore operations without explicitly specifying a repository. Currently, only [data stream lifecycle management (DLM)](/manage-data/lifecycle/data-stream.md) uses it to create searchable snapshots when moving data to the frozen tier.

When you register your first repository in {{kib}}, the **Set as default repository** option is turned on by default, so that repository becomes the default unless you turn it off. You can change the default repository at any time.

To change the default repository from {{kib}}, you need the `cluster:admin/settings/update` [cluster privilege](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-cluster). The default repository is stored in the [`repositories.default_repository`](elasticsearch://reference/elasticsearch/configuration-reference/snapshot-restore-settings.md#repositories-default-repository) cluster setting.

Keep the following constraints in mind:

* The default repository cannot be removed. To remove it, first set another repository as the default.
* Read-only repositories cannot be set as the default.
* URL repositories cannot be set as the default.

To change the default repository, use one of the following methods:

* From the list of repositories:
   1. Open the actions menu for the repository you want to use as the default.
   2. Select **Set as default**.
   3. In the **Change default repository?** dialog, select **Change default** to confirm.
* When you edit a repository: Turn on the **Set as default repository** option, then save.
