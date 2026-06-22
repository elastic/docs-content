To manage repositories in {{kib}}:

1. Go to the **Snapshot and Restore** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select the **Repositories** tab.
3. To register a snapshot repository, select **Register repository**.

    In the registration form, you can define:

    * The repository name and type
    * Type-specific connection settings, such as the storage location and credentials
    * Repository behavior, such as whether the repository is read-only
    * {applies_to}`stack: ga 9.5` Whether to set the repository as the [default snapshot repository](#snapshot-repo-default). When you register your first repository, this option is turned on by default.

    Select **Register** to save the repository.

You can also register a repository using the {{es}} [create snapshot repository API]({{es-apis}}operation/operation-snapshot-create-repository).
