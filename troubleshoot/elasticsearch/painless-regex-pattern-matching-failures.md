---
navigation_title: Regex pattern matching failures
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Troubleshoot regex pattern matching failures in Painless

Follow these guidelines to avoid [regex](elasticsearch://reference/scripting-languages/painless/painless-regexes.md) operation errors in your Painless script.

## Regex compilation and usage errors in Painless scripts

Regex operations in Painless can fail for several reasons: the regex feature is disabled, there is incorrect matcher usage, or there are malformed regex patterns. These errors are common when developers assume that standard Java regex behavior applies directly to Painless.

### Sample error

```json
{
  "error": {
    "root_cause": [
      {
        "type": "script_exception",
        "reason": "runtime error",
        "script_stack": [
          "java.base/java.util.regex.Matcher.checkMatch(Matcher.java:1850)",
          "java.base/java.util.regex.Matcher.group(Matcher.java:685)",
          """return /(?<=SHIPPER:).*?(?=\\n)/.matcher(orderLog).group(0);
    """,
          "                                                  ^---- HERE"
        ],
        "script": " ...",
        "lang": "painless",
        "position": {
          "offset": 176,
          "start": 126,
          "end": 191
        }
      }
    ],
    "type": "script_exception",
    "reason": "runtime error",
    "script_stack": [
      "java.base/java.util.regex.Matcher.checkMatch(Matcher.java:1850)",
      "java.base/java.util.regex.Matcher.group(Matcher.java:685)",
      """return /(?<=SHIPPER:).*?(?=\\n)/.matcher(orderLog).group(0);
    """,
      "                                                  ^---- HERE"
    ],
    "script": " ...",
    "lang": "painless",
    "position": {
      "offset": 176,
      "start": 126,
      "end": 191
    },
    "caused_by": {
      "type": "illegal_state_exception",
      "reason": "No match found"
    }
  },
  "status": 400
}
```

### Problematic code

```json
{
  "script": {
    "lang": "painless",
    "source": """
      String orderLog = "Order processing initiated\\nSHIPPER: SHIP-EX EXPRESS DELIVERY\\nTracking number generated";

      return /(?<=SHIPPER:).*?(?=\\n)/.matcher(orderLog).group(0);
    """
  }
}
```

### Root cause

The error occurs because the `group()` method is called on a Matcher before calling `find()`. You must explicitly search for matches before accessing groups. This is a common mistake when developers expect the matcher to automatically find matches.

### Solution: Call find() before accessing groups

Always call `find()` before using `group()` methods:

```json
POST _scripts/painless/_execute
{
  "script": {
    "lang": "painless",
    "source": """
      String orderLog = "Order processing initiated\\nSHIPPER: SHIP-EX EXPRESS DELIVERY\\nTracking number generated";

      Matcher m = /(?<=SHIPPER:).*?(?=\\n)/.matcher(orderLog);
      boolean found = m.find();

      return found ? m.group(0).trim() : "No match";
    """
  }
}
```

### Results

```json
{
  "result": "SHIP-EX EXPRESS DELIVERY"
}
```

### Notes

* **Call find() first:** Always use `matcher.find()` before accessing groups.  
* **Enable regex:** Set `script.painless.regex.enabled=true` in the `elasticsearch.yml` settings file if regex is disabled.  
* **Group numbering:** Use `group(0)` for the entire match, `group(1)` for first capture group, etc.  
* **Performance impact:** Regex operations can be expensive, especially with complex patterns.




