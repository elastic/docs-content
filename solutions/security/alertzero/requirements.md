---
navigation_title: Requirements
description: "The settings, privileges, and dependencies AlertZero needs before you set it up."
applies_to:
  stack: preview 9.6
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# AlertZero requirements

Check that these settings, privileges, and dependencies are in place before you set up AlertZero.

% Verified Worker prerequisites to document here (moved off the Worker pages, which are for analysts):
% - Every Worker: an AI model available in the space (Feature settings). Without one, the Worker can't be turned on.
% - Alert Triage: the Alert analysis setting turned on in the space.
% - Attack Discovery: the Attack Discovery workflows turned on. Context Engine on to hand attacks to the Forensics Watch.
% - Rule Coverage: Context Engine on; it reads Continuous Threat Hunt's detection gaps from it.
% - Continuous Threat Hunt: threat reports set up; AlertZero turns on the Threat Intel Supply workflows when you turn it on.
% - Endpoint Analysis: Elastic Defend set up and Context Engine on.
