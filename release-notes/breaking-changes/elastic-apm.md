---
navigation_title: "Elastic APM"
---

# Elastic APM breaking changes [elastic-apm-breaking-changes]
Before you upgrade, carefully review the Elastic APM breaking changes and take the necessary steps to mitigate any issues. 

To learn how to upgrade, check out <uprade docs>.

% ## Next version [elastic-apm-nextversion-breaking-changes]
% **Release date:** Month day, year

% ::::{dropdown} Title of breaking change 
% Description of the breaking change.
% For more information, check [PR #](PR link).
% **Impact**<br> Impact of the breaking change.
% **Action**<br> Steps for mitigating deprecation impact.
% ::::

## 9.0.0 [elastic-apm-9-0-0-breaking-changes]
**Release date:** March 25, 2025

% ::::{dropdown} Title of breaking change 
% Description of the breaking change.
% For more information, check [PR #](PR link).
% **Impact**<br> Impact of the breaking change.
% **Action**<br> Steps for mitigating deprecation impact.
% ::::

::::{dropdown} Change server information endpoint "/" to only accept GET and HEAD requests
This will surface any agent misconfiguration causing data to be sent to `/` instead of the correct endpoint (for example, `/v1/traces` for OTLP/HTTP).
For more information, check [PR #15976](https://github.com/elastic/apm-server/pull/15976).
**Impact**<br> Any methods other than `GET` and `HEAD` to `/` will return HTTP 405 Method Not Allowed.
**Action**<br> Update any existing usage, for example, update `POST /` to `GET /`.
::::
