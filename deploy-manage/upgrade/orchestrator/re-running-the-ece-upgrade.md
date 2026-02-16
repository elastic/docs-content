---
applies_to:
  deployment:
    ece: ga
products:
  - id: cloud-enterprise
---
    
# Re-running the ECE upgrade [re-running-ece-upgrade]

By default, re-running the `elastic-cloud-enterprise.sh upgrade` command resumes the previous ECE upgrade process. However, if your previous ECE upgrade attempt got stuck (for example, due to infrastructure problems, a host going offline, or similar) and re-attempting the upgrade still results in the upgrade process being blocked, run `elastic-cloud-enterprise.sh upgrade --force-upgrade` to ensure that any existing upgrade state gets cleared before starting the new ECE upgrade process.

The `--force-upgrade` parameter is also helpful in situations where the {{ece}} platform is already upgraded to the desired target version but there are containers still running at the old version. These rare situations can also be caused by infrastructure issues, for example, runners temporarily going offline and not being "seen" by the upgrade process. Running `elastic-cloud-enterprise.sh upgrade --force-upgrade` with the same target version makes the {{ece}} upgrader perform the upgrade procedure anyway, thereby covering any containers that failed to upgrade previously.

If the {{ece}} platform was upgraded successfully and yet one or more system deployments were not upgraded to a higher {{stack}} version during the very last phase of the {{ece}} upgrade, we recommend running the {{ece}} upgrader again without the `--force-upgrade` parameter. The {{ece}} upgrader will recognize that the platform is already at the desired target version and will apply upgrade plans to system deployments.

Refer to [](/deploy-manage/deploy/cloud-enterprise/default-system-deployment-versions.md) for details on the system deployment versions associated with each {{ece}} version.