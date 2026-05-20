:::::{note}
In {{ech}}, you can use dedicated {{ecloud}} APIs to expose the built-in snapshot repository (`found-snapshots`) from one deployment to another as read-only. This allows a deployment to access and restore snapshots from another deployment without manually configuring snapshot repositories:

- [Attach another deployment's built-in snapshot repository]({{cloud-apis}}operation/operation-create-deployment-es-resource-snapshot-repository)
- [List the attached snapshot repositories]({{cloud-apis}}operation/operation-get-deployment-es-resource-snapshot-repository)
- [Remove an attached snapshot repository]({{cloud-apis}}operation/operation-delete-deployment-es-resource-snapshot-repository)
:::::
