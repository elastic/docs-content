---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-basic-setup-https.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-tls-certificates.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-custom-http-certificate.html
  - https://www.elastic.co/guide/en/kibana/current/Security-production-considerations.html
---

# Secure HTTP communications

% What needs to be done: Refine

% GitHub issue: https://github.com/elastic/docs-projects/issues/346

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/security-basic-setup-https.md
%      Notes: just the relevant section + concepts
% - [ ] ./raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-tls-certificates.md
% - [ ] ./raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-custom-http-certificate.md
% - [ ] ./raw-migrated-files/kibana/kibana/Security-production-considerations.md

% EEDUGON NOTE: security section might miss a section to secure the transport layer (not the HTTP).
% There we should integrate the content of https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-transport-settings.html which is currently in ECK (/deploy-manage) doc.

% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):

$$$encrypt-kibana-browser$$$

$$$encrypt-kibana-http$$$

$$$configure-beats-security$$$

$$$configuring-tls-browser-kib$$$

$$$beats-setup-role$$$

$$$beats-monitoring-role$$$

$$$beats-writer-role$$$

$$$beats-reader-role$$$

$$$configure-metricbeat-tls$$$

$$$encrypt-http-communication$$$

$$$csp-strict-mode$$$

$$$k8s-setting-up-your-own-certificate$$$

$$$k8s-static-ip-custom-domain$$$

$$$k8s-disable-tls$$$