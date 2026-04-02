---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Using Painless regular expressions [regular-expressions-tutorial]

## Prerequisites

This tutorial uses the `kibana_sample_data_ecommerce` dataset. Refer to [Context example data](elasticsearch://reference/scripting-languages/painless/painless-context-examples.md) to get started.

## Extract customer email domains for marketing segmentation

The goal is to extract and categorize email domains during document ingestion for marketing segmentation. We will use regular expression pattern matching to parse a set of email addresses and break them into their component parts. The expression `/([^@]+)@(.+)/` splits emails at the @ symbol, while domain-specific patterns like `(gmail|yahoo|hotmail|outlook|icloud|aol)\.com/` identify personal email providers for automated categorization. 

### Understanding email domain extraction

The ingest pipeline allows you to extract structured data from email addresses during indexing. Regular expressions parse email components and categorize domains, creating fields for targeted marketing campaigns and customer analysis.

### Writing the Painless script

Create an ingest pipeline that extracts email domains and categorizes them:

```json
PUT _ingest/pipeline/kibana_sample_data_ecommerce-extract_email_domains
{
  "description": "Extract and categorize email domains from customer emails",
  "processors": [
    {
      "script": {
        "lang": "painless",
        "source": """
          // Extract email domain using regex
          Pattern emailPattern = /([^@]+)@(.+)/;
          Matcher emailMatcher = emailPattern.matcher(ctx.email);
          
          if (emailMatcher.matches()) {
            String username = emailMatcher.group(1);
            String domain = emailMatcher.group(2);
            
            // Store extracted components
            ctx.email_username = username;
            ctx.email_domain = domain;
            
            // Categorize domain type using regex patterns
            Pattern personalDomains = /(gmail|yahoo|hotmail|outlook|icloud|aol)\.com/;
            Pattern businessDomains = /\.(co|corp|inc|ltd|org|edu|gov)$/;
            Pattern testDomains = /\.zzz$/;
            
            if (testDomains.matcher(domain).find()) {
              ctx.email_category = "test";
            } else if (personalDomains.matcher(domain).find()) {
              ctx.email_category = "personal";
            } else if (businessDomains.matcher(domain).find()) {
              ctx.email_category = "business";
            } else {
              ctx.email_category = "other";
            }
            
            // Extract top-level domain
            Pattern tldPattern = /\.([a-zA-Z]{2,})$/;
            Matcher tldMatcher = tldPattern.matcher(domain);
            if (tldMatcher.find()) {
              ctx.email_tld = tldMatcher.group(1);
            }
          }
        """
      }
    }
  ]
}
```

This script includes the following steps:

* **Pattern matching:** Uses regex `/([^@]+)@(.+)/` to split email into username and domain parts  
* **Domain categorization:** Classifies domains using specific patterns:  
  * Personal: [gmail.com](http://gmail.com), [yahoo.com](http://yahoo.com), [hotmail.com](http://hotmail.com)   
  * Business: domains ending in .co, .corp, .inc, .org, .edu, .gov  
  * Test: domains ending in .zzz  
  * Other: Any domain not matching the above patterns  
* **TLD extraction:** Extracts the top-level domain (com, org, edu, etc.) using `/\.([a-zA-Z]{2,})$/` regular expression  
* **Test domain detection:** Identifies sample data domains ending in `.zzz` (used in the Kibana ecommerce sample dataset)  
* **Fields addition:** Adds new fields (`email_username`, `email_domain`, `email_category`, `email_tld`) to the document for analytics and segmentation

For more details about Painless regular expressions, refer to [Painless regex documentation](elasticsearch://reference/scripting-languages/painless/painless-regexes.md).

### Test the pipeline

Simulate the pipeline with sample e-commerce customer data:

```json
POST _ingest/pipeline/kibana_sample_data_ecommerce-extract_email_domains/_simulate
{
  "docs": [
    {
      "_source": {
        "customer_full_name": "Eddie Underwood",
        "email": "eddie@underwood-family.zzz"
      }
    },
    {
      "_source": {
        "customer_full_name": "John Smith",
        "email": "john.smith@gmail.com"
      }
    },
    {
      "_source": {
        "customer_full_name": "Sarah Wilson",
        "email": "s.wilson@acme-corp.com"
      }
    }
  ]
}
```

:::{dropdown} Response

```json
{
  "docs": [
    {
      "doc": {
        ...,
        "_source": {
          "customer_full_name": "Eddie Underwood",
          "email_tld": "zzz",
          "email_username": "eddie",
          "email_domain": "underwood-family.zzz",
          "email_category": "test",
          "email": "eddie@underwood-family.zzz"
        },
        "_ingest": {
          "timestamp": "2025-08-27T16:58:19.746710068Z"
        }
      }
    },
    {
      "doc": {
        ...,
        "_source": {
          "customer_full_name": "John Smith",
          "email_tld": "com",
          "email_username": "john.smith",
          "email_domain": "gmail.com",
          "email_category": "personal",
          "email": "john.smith@gmail.com"
        },
        "_ingest": {
          "timestamp": "2025-08-27T16:58:19.746774486Z"
        }
      }
    },
    {
      "doc": {
        ...,
        "_source": {
          "customer_full_name": "Sarah Wilson",
          "email_tld": "com",
          "email_username": "s.wilson",
          "email_domain": "acme-corp.com",
          "email_category": "business",
          "email": "s.wilson@acme-corp.com"
        },
        "_ingest": {
          "timestamp": "2025-08-27T16:58:19.746786425Z"
        }
      }
    }
  ]
}
```

:::

## Analyze product SKU patterns with aggregations

The goal is to parse SKU codes using regular expressions to extract manufacturer identifiers, then group products by these patterns to reveal inventory distribution across clothing, accessories, and footwear categories without creating additional index fields.

### Understanding SKU pattern analysis with aggregations

Aggregations with runtime fields allow you to analyze SKU patterns across thousands of products. The regex patterns validate SKU formats and extract meaningful segments from codes like “ZO0549605496" to categorize products by manufacturer patterns.

### Writing the Painless script

Create aggregations that analyze SKU patterns:

```json
GET kibana_sample_data_ecommerce/_search
{
  "size": 0,
  "runtime_mappings": {
    "sku_category": {
      "type": "keyword",
      "script": {
        "lang": "painless",
        "source": """
          if (doc.containsKey('sku')) {
            String sku = doc['sku'].value;
            
            // Validate SKU format using regex
            Pattern skuPattern = /^ZO(\d{4})(\d{6})$/;
            Matcher skuMatcher = skuPattern.matcher(sku);
            
            if (skuMatcher.matches()) {
              String manufacturerCode = skuMatcher.group(1); // First 4 digits after ZO
              
              // Determine product category based on manufacturer code patterns
              if (manufacturerCode =~ /^0[1-3].*/) {
                emit("clothing");
              } else if (manufacturerCode =~ /^0[4-6].*/) {
                emit("accessories"); 
              } else if (manufacturerCode =~ /^0[0-9].*/) {
                emit("footwear");
              } else {
                emit("other");
              }
            } else {
              emit("invalid_or_unknown");
            }
          } else {
            emit("invalid_or_unknown");
          }
        """
      }
    }
  },
  "aggs": {
    "sku_category_breakdown": {
      "terms": {
        "field": "sku_category"
      }
    }
  }
}
```

This script includes the following steps:

* **Format validation:** Uses regex `/^ZO(\d{4})(\d{6})$/` to ensure the SKU formats follow the expected pattern (ZO \+ 4 digits \+ 6 digits)  
* **Component extraction:** Separates the manufacturer code product ID to enable category analysis  
* **Category classification:** Maps manufacturer patterns to product types for inventory reporting  
* **Aggregated analysis:** Counts products by category to show inventory distribution without storing new fields

For more details about Painless regular expressions, refer to [Painless regex documentation](elasticsearch://reference/scripting-languages/painless/painless-regexes.md).

The results provide comprehensive SKU format analysis across your product catalog:

:::{dropdown} Response

```json
{
  ...,
  "hits": {
    ...
  },
  "aggregations": {
    "sku_category_breakdown": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "clothing",
          "doc_count": 2337
        },
        {
          "key": "accessories",
          "doc_count": 1295
        },
        {
          "key": "footwear",
          "doc_count": 1043
        }
      ]
    }
  }
}
```

:::

## Convert custom date formats during data ingestion

The goal is to convert custom timestamp formats like “25-AUG-2025@14h30m” into ISO 8601 standard “2025-08-25T14:30:00Z” during data ingestion. This ensures consistent date fields across datasets from different source systems.

### Understanding custom date format conversion

Legacy manufacturing and ERP systems often use non-standard date formats that {{es}} cannot directly parse. Converting these during ingestion eliminates the need for repeated parsing at query time and ensures proper date range filtering and sorting.

### Writing the Painless script

Create an ingest pipeline that converts custom date formats:

```json
PUT _ingest/pipeline/kibana_sample_data_ecommerce-convert_custom_dates
{
  "description": "Convert custom date formats to ISO 8601 standard",
  "processors": [
    {
      "script": {
        "lang": "painless",
        "source": """
          // Format: "25-AUG-2025@14h30m" (DD-MMM-YYYY@HHhMMm)
          if (ctx.containsKey('manufacturing_date_custom')) {
            String customDate = ctx.manufacturing_date_custom;
            
            // Extract date components using regex
            Pattern customDatePattern = /(\d{1,2})-([A-Z]{3})-(\d{4})@(\d{2})h(\d{2})m/;
            Matcher customDateMatcher = customDatePattern.matcher(customDate);
            
            if (customDateMatcher.matches()) {
              String day = customDateMatcher.group(1);
              String monthAbbr = customDateMatcher.group(2);
              String year = customDateMatcher.group(3);
              String hour = customDateMatcher.group(4);
              String minute = customDateMatcher.group(5);
             
              Map monthMap = [
                'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04',
                'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08',
                'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'
              ];
              
              // Getting month based on month abbreviation
              String monthNum = monthMap.getOrDefault(monthAbbr, '01');
              
              // Format day with leading zero using regex pattern validation
              Pattern singleDigitPattern = /^\d$/;
              String dayFormatted = singleDigitPattern.matcher(day).matches() ? "0" + day : day;
              
              // Create ISO 8601 formatted date
              ctx.manufacturing_date = year + "-" + monthNum + "-" + dayFormatted + "T" + hour + ":" + minute + ":00Z";
              ctx.manufacturing_date_parsed = true;
              
              // Validate final ISO format using regex
              Pattern validDatePattern = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/;
              ctx.iso_format_valid = validDatePattern.matcher(ctx.manufacturing_date).matches();
              
            } else {
              ctx.manufacturing_date_parsed = false;
              ctx.parse_error = "Invalid custom date format";
            }
          }
        """
      }
    }
  ]
}
```

This script includes the following steps:

* **Pattern extraction:** Uses regex `/(\d{1,2})-([A-Z]{3})-(\d{4})@(\d{2})h(\d{2})m/` to parse the custom format "25-AUG-2025@14h30m"  
* **Month conversion:** Uses a Map lookup instead of multiple regex conditions for cleaner code  
* **Regex validation:** Uses the `/^\d$/` pattern to detect single-digit days that need zero-padding  
* **Format standardization:** Reconstructs date components into ISO 8601 format (YYYY-MM-DDTHH:mm:ssZ)  
* **ISO validation:** Additional regex `/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/` confirms the final format is valid


For more details about Painless scripting in the ingest context, refer to [Ingest processor context](elasticsearch://reference/scripting-languages/painless/painless-ingest-processor-context.md).

### Test the pipeline

Simulate the pipeline with sample custom date formats:

```json
POST _ingest/pipeline/kibana_sample_data_ecommerce-convert_custom_dates/_simulate
{
  "docs": [
    {
      "_source": {
        "product_name": "Winter Jacket",
        "manufacturing_date_custom": "25-AUG-2025@14h30m"
      }
    },
    {
      "_source": {
        "product_name": "Summer Shoes",
        "manufacturing_date_custom": "03-JUN-2025@09h15m"
      }
    }
  ]
}
```

The simulation shows successful conversion to ISO 8601 format:

:::{dropdown} Response

```json
{
  "docs": [
    {
      "doc": {
        ...,
        "_source": {
          "manufacturing_date_custom": "25-AUG-2025@14h30m",
          "manufacturing_date": "2025-08-25T14:30:00Z",
          "iso_format_valid": true,
          "product_name": "Winter Jacket",
          "manufacturing_date_parsed": true
        },
        "_ingest": {
          "timestamp": "2025-08-27T18:57:00.481410405Z"
        }
      }
    },
    {
      "doc": {
        ...,
        "_source": {
          "manufacturing_date_custom": "03-JUN-2025@09h15m",
          "manufacturing_date": "2025-06-03T09:15:00Z",
          "iso_format_valid": true,
          "product_name": "Summer Shoes",
          "manufacturing_date_parsed": true
        },
        "_ingest": {
          "timestamp": "2025-08-27T18:57:00.481449186Z"
        }
      }
    }
  ]
}
```

:::

## Learn more about regular expressions in Painless

This tutorial demonstrates practical regex applications across ingest, aggregation, and runtime field contexts. For comprehensive regex capabilities and advanced pattern techniques, explore these resources:

* [Painless regex documentation](elasticsearch://reference/scripting-languages/painless/painless-regexes.md): Complete syntax, operators, and pattern flags  
* [Painless syntax-context bridge](/explore-analyze/scripting/painless-syntax-context-bridge.md): How data access methods apply across different Painless contexts  
* [Painless Context](elasticsearch://reference/scripting-languages/painless/painless-contexts.md): General view for each context in Painless

