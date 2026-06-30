---
navigation_title: Exception types and syntax
applies_to:
  stack: ga
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
description: Understand the differences in escaping rules for detection rule exceptions and Elastic Endpoint exceptions.
---

# Exception types and value syntax [exception-types-and-syntax]

Different exception types in {{elastic-sec}} require different escaping rules for file paths. This page clarifies the syntax differences between each exception type so you can create exceptions that work as expected.

## Value syntax [value-syntax-details]

[Detection rule exceptions](/solutions/security/detect-and-alert/add-manage-exceptions.md#detection-rule-exceptions) require escaping for special characters, while [{{elastic-endpoint}} exceptions](/solutions/security/detect-and-alert/add-manage-exceptions.md#endpoint-rule-exceptions) and [trusted applications](/solutions/security/manage-elastic-defend/trusted-applications.md) do not. The following sections explain the syntax for each type.

### Detection rule exceptions (escaping required) [detection-rule-escaping]

When you use the `matches` or `does not match` operator in a detection rule exception, you must escape special characters with a backslash:

* `\\` for a literal backslash
* `\*` for a literal asterisk
* `\?` for a literal question mark

Windows paths use backslashes as directory separators, so you must double each separator. Paths that already contain double backslashes (such as UNC paths) require four backslashes per separator.

**Examples:**

| What you want to match | Value to enter |
| --- | --- |
| `C:\Windows\explorer.exe` | `C:\\Windows\\explorer.exe` |
| `C:\Program Files\*\app.exe` (wildcard) | `C:\\Program Files\\*\\app.exe` |
| `\\server\share\file.txt` (UNC path) | `\\\\server\\share\\file.txt` |

### {{elastic-endpoint}} exceptions and trusted applications (no escaping) [endpoint-no-escaping]

{{elastic-endpoint}} exceptions and trusted applications interpret values literally. Enter file paths and other values exactly as they appear on the host operating system. Do **not** escape backslashes or other special characters.

**Examples:**

| What you want to match | Value to enter |
| --- | --- |
| `C:\Windows\explorer.exe` | `C:\Windows\explorer.exe` |
| `C:\Program Files\*\app.exe` (wildcard) | `C:\Program Files\*\app.exe` |
| `\\server\share\file.txt` (UNC path) | `\\server\share\file.txt` |

### Wildcard characters

The `?` and `*` wildcards work the same way across all exception types — `?` matches one character and `*` matches zero or more characters — but only the **detection rule** exception type requires escaping these characters when you want to match them literally.

## Troubleshoot exception values [troubleshooting-exception-values]

Because escaping rules differ between exception types, values that work in one context can silently fail in another. The following table describes symptoms and how to resolve them:

| Symptom | Likely cause | Resolution |
| --- | --- | --- |
| {{elastic-endpoint}} exception or trusted application does not match a Windows path | The value contains double backslashes (for example, `C:\\Windows\\explorer.exe`) copied from a detection rule exception | Remove the extra backslashes and enter the path as it appears on disk: `C:\Windows\explorer.exe` |
| Detection rule exception with the `matches` operator does not match a Windows path | The value contains single backslashes that are not escaped (for example, `C:\Windows\explorer.exe`) | Escape each backslash: `C:\\Windows\\explorer.exe` |
| Exception was copied from a working detection rule into an {{elastic-endpoint}} exception and no longer matches | Detection rule escaping syntax is not valid for {{elastic-endpoint}} exceptions | Re-enter the value without escaping, matching the path exactly as it appears on the host |

## Exception type comparison [exception-type-comparison]

The following table compares how detection rule exceptions and {{elastic-endpoint}} exceptions differ in behavior and risk:

| | Detection rule exception | {{elastic-endpoint}} exception |
| --- | --- | --- |
| **Where it operates** | Detection engine in {{kib}} | {{elastic-endpoint}} (on the host) |
| **Primary purpose** | Suppress alerts in {{kib}} | Exclude a process from blocking and monitoring on the endpoint |
| **Affects endpoint blocking?** | No — {{elastic-endpoint}} can still block or detect the activity | Yes — prevents blocking and detection on the host |
| **Affects alert generation?** | Yes — prevents alerts | Sometimes — if {{elastic-endpoint}} never generates an event, the detection engine has nothing to alert on |
| **Used for** | Reduce alert noise | Prevent endpoint interference with known-safe software |
| **Risk if used incorrectly** | Silent blocking on endpoints ({{elastic-endpoint}} still blocks the process, but generates no alert) | Blind spots — {{elastic-endpoint}} may never detect the activity |
| **Example use case** | Suppress alerts for a harmless administrative script | Allow a trusted installer so {{elastic-endpoint}} does not block it |

For a comparison of trusted applications, event filters, blocklists, and {{elastic-endpoint}} exceptions — including how each affects performance and visibility — refer to [Optimize {{elastic-defend}}](optimize-elastic-defend.md).

