# Ingest third-party cloud security data [ingest-third-party-cloud-security-data]

This section describes how to ingest cloud security data from third-party tools into {{es}}. Once ingested, this data can provide additional context and enrich your {{elastic-sec}} workflows.

You can ingest both third-party cloud workload protection data and third-party security posture and vulnerability data.


## Ingest third-party workload protection data [_ingest_third_party_workload_protection_data] 

You can ingest third-party cloud security alerts into {{elastic-sec}} to view them on the [Alerts page](../../../solutions/security/detect-and-alert/manage-detection-alerts.md) and incorporate them into your triage and threat hunting workflows.

* Learn to [ingest alerts from Sysdig Falco](../../../solutions/security/cloud/ingest-cncf-falco-data.md).


## Ingest third-party security posture and vulnerability data [_ingest_third_party_security_posture_and_vulnerability_data] 

You can ingest third-party data into {{elastic-sec}} to review and investigate it alongside data collected by {{elastic-sec}}'s native cloud security integrations. Once ingested, cloud security posture and vulnerability data appears on the [Findings](../../../solutions/security/cloud/findings-page.md) page and in the entity details flyouts for [alerts](../../../solutions/security/detect-and-alert/view-detection-alert-details.md#insights-section), [users](../../../solutions/security/explore/users-page.md#security-users-page-user-details-flyout), and [hosts](../../../solutions/security/explore/hosts-page.md#security-hosts-overview-host-details-flyout) flyouts.

* Learn to [ingest cloud security posture data from AWS Security Hub](../../../solutions/security/cloud/ingest-aws-security-hub-data.md).
* Learn to [ingest cloud security posture and vulnerability data from Wiz](../../../solutions/security/cloud/ingest-wiz-data.md).




