---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/allowlist-endpoint-3rd-party-av-apps.html
  - https://www.elastic.co/guide/en/serverless/current/security-allowlist-endpoint.html
---



# Allowlist {{elastic-endpoint}} in third-party antivirus apps [allowlist-endpoint-3rd-party-av-apps]

::::{note} 
If you use other antivirus (AV) software along with {{elastic-defend}}, you may need to add the other system as a trusted application in the {{security-app}}. Refer to [*Trusted applications*](trusted-applications.md) for more information.
::::


Third-party antivirus (AV) applications may identify the expected behavior of {{elastic-endpoint}}—the installed component that performs {{elastic-defend}}'s threat monitoring and prevention—as a potential threat. Add {{elastic-endpoint}}'s digital signatures and file paths to your AV software’s allowlist to ensure {{elastic-endpoint}} continues to function as intended. We recommend you allowlist both the file paths and digital signatures, if applicable.

::::{note} 
Your AV software may refer to allowlisted processes as process exclusions, ignored processes, or trusted processes. It is important to note that file, folder, and path-based exclusions/exceptions are distinct from trusted applications and will not achieve the same result. This page explains how to ignore actions taken by processes, not how to ignore the files that spawned those processes.
::::



## Allowlist {{elastic-endpoint}} on Windows [allowlist-endpoint-on-windows] 

File paths:

* ELAM driver: `c:\Windows\system32\drivers\ElasticElam.sys`
* Driver: `c:\Windows\system32\drivers\elastic-endpoint-driver.sys`
* Executable: `c:\Program Files\Elastic\Endpoint\elastic-endpoint.exe`

    ::::{note} 
    The executable runs as `elastic-endpoint.exe`.
    ::::


Digital signatures:

* `Elasticsearch, Inc.`
* `Elasticsearch B.V.`

For additional information about allowlisting on Windows, refer to [Trusting Elastic Defend in other software](https://github.com/elastic/endpoint/blob/main/PerformanceIssues-Windows.md#trusting-elastic-defend-in-other-software).


## Allowlist {{elastic-endpoint}} on macOS [allowlist-endpoint-on-macos] 

File paths:

* System extension (recursive directory structure): `/Applications/ElasticEndpoint.app/`

    ::::{note} 
    The system extension runs as `co.elastic.systemextension`.
    ::::

* Executable: `/Library/Elastic/Endpoint/elastic-endpoint.app/Contents/MacOS/elastic-endpoint`

    ::::{note} 
    The executable runs as `elastic-endpoint`.
    ::::


Digital signatures:

* Authority/Developer ID Application: `Elasticsearch, Inc (2BT3HPN62Z)`
* Team ID: `2BT3HPN62Z`


## Allowlist {{elastic-endpoint}} on Linux [allowlist-endpoint-on-linux] 

File path:

* Executable: `/opt/Elastic/Endpoint/elastic-endpoint`

    ::::{note} 
    The executable runs as `elastic-endpoint`.
    ::::

