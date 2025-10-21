---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Working with dates [datetime-tutorial]

In this tutorial you’ll learn how to use Painless scripts to work with dates in three scenarios:

* Add quarter and fiscal year fields during ingestion  
* Calculate delivery dates with runtime fields  
* Transform time data during reindex

## Prerequisites

This tutorial uses the `kibana_sample_data_ecommerce` dataset. Refer to [Context example data](elasticsearch://reference/scripting-languages/painless/painless-context-examples.md) to get started.

The examples work with the dataset’s `order_date` field, which contains ISO 8601-formatted datetime strings such as `2025-08-29T16:49:26+00:00`. For more details refer to [Date field type](elasticsearch://reference/elasticsearch/mapping-reference/date.md).

## Add quarter and fiscal year fields during ingestion (ingest context)

The [ingest pipeline](/manage-data/ingest/transform-enrich/ingest-pipelines.md) allows you to add standardized time period fields (like a fiscal quarter) during document ingestion. This is ideal when you need reporting fields such as quarters, fiscal years, and week classifications without calculating them repeatedly at query time. 

### Writing the Painless script

To achieve this, we create the ingest pipeline with a script processor that adds documents to the fields we want to use:

```json
PUT _ingest/pipeline/kibana_sample_data_ecommerce-add_reporting_fields
{
  "description": "Add reporting period fields from order_date",
  "processors": [
    {
      "script": {
        "lang": "painless",
        "source": """
          // Parse order_date string to Calendar object
          def calendar = Calendar.getInstance();
          calendar.setTime(Date.from(Instant.parse(ctx.order_date)));
          
          // Extract date components
          int year = calendar.get(Calendar.YEAR);
          int month = calendar.get(Calendar.MONTH) + 1; // Calendar.MONTH is 0-based
          int dayOfWeek = calendar.get(Calendar.DAY_OF_WEEK);
          
          // Calculate derived periods
          int quarter = (int)Math.ceil((double)month / 3.0);
          int fiscalYear = (month >= 4) ? year : year - 1; // Fiscal year starts in April
          boolean isWeekend = (dayOfWeek == 1 || dayOfWeek == 7); // Sunday=1, Saturday=7
          
          // Add reporting fields
          ctx.reporting_year = year;
          ctx.reporting_month = month;
          ctx.reporting_quarter = quarter;
          ctx.reporting_fiscal_year = fiscalYear;
          ctx.is_weekend_order = isWeekend;

          ctx.updated_timestamp = new Date();
        """
      }
    }
  ]
}
```

This script  includes the following steps:

* Parse the datetime string: Uses `Instant.parse()` to convert the ISO 8601 string into a `Date` object via `Calendar.getInstance()`  
* Extract date components: Retrieves the year, month, and day of the week, noting that `Calendar.MONTH` is zero-based (January \= 0\)  
* Calculate business periods: Computes quarter using `Math.ceil()`, fiscal year assuming April start, and weekend classification  
* Add new fields: Stores all calculated values in the document context (`ctx`)


For more details about Painless scripting in the ingest context, refer to [Ingest processor context](elasticsearch://reference/scripting-languages/painless/painless-ingest-processor-context.md) and Painless syntax-context bridge. 

### Test the pipeline

To confirm the pipeline works correctly, [simulate](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-simulate) it with `kibana_sample_data_ecommerce` sample documents:

```json
POST     _ingest/pipeline/kibana_sample_data_ecommerce-add_reporting_fields/_simulate
{
  "docs": [
    {
      "_source": {
        "updated_timestamp": "2025-08-20T18:21:30.943Z",
        "order_date": "2025-08-29T16:49:26+00:00"
      }
    },
    {
      "_source": {
        "updated_timestamp": "2025-08-20T18:21:30.943Z",
        "order_date": "2025-08-14T10:14:53+00:00"
      }
    }
  ]
}
```

The simulation confirms that your pipeline correctly adds the reporting fields to each document

:::{dropdown} Response

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_version": "-3",
        "_id": "_id",
        "_source": {
          "order_date": "2025-08-29T16:49:26+00:00",
          "reporting_quarter": 3,
          "reporting_year": 2025,
          "updated_timestamp": "2025-08-21T16:48:31.318Z",
          "reporting_fiscal_year": 2025,
          "is_weekend_order": false,
          "reporting_month": 8
        },
        "_ingest": {
          "timestamp": "2025-08-21T16:48:31.318150744Z"
        }
      }
    },
    {
      "doc": {
        "_index": "_index",
        "_version": "-3",
        "_id": "_id",
        "_source": {
          "order_date": "2025-08-14T10:14:53+00:00",
          "reporting_quarter": 3,
          "reporting_year": 2025,
          "updated_timestamp": "2025-08-21T16:48:31.318Z",
          "reporting_fiscal_year": 2025,
          "is_weekend_order": false,
          "reporting_month": 8
        },
        "_ingest": {
          "timestamp": "2025-08-21T16:48:31.318189178Z"
        }
      }
    }
  ]
}
```

:::

## Calculate delivery dates with runtime fields (runtime fields context)

In this script, we will calculate the delivery time of an order by projecting the order date a certain number of days into the future. If the resulting date falls on a weekend, it will automatically shift to the following Monday.

### Understanding runtime fields with date calculations

Runtime fields compute values at query time, which means you can embed scheduling rules directly in the calculation. In this case, we add a configurable number of delivery days to the order date, then check whether the resulting day falls on a weekend. If it does, the script automatically shifts the delivery date to the next Monday.

Create the runtime field:

```json
PUT kibana_sample_data_ecommerce/_mapping
{
  "runtime": {
    "delivery_timestamp": {
      "type": "date",
      "script": {
        "lang": "painless",
        "source": """
            if (doc.containsKey('order_date')) {
              long orderTime = doc['order_date'].value.millis;
              long deliveryDays = (long) params.delivery_days;
              
              // Add delivery days to order date
              long deliveryTime = orderTime + (deliveryDays * 24 * 60 * 60 * 1000L);
              
              // Check if delivery falls on weekend
              ZonedDateTime deliveryDateTime = Instant.ofEpochMilli(deliveryTime).atZone(ZoneId.of('UTC'));
              int dayOfWeek = deliveryDateTime.getDayOfWeek().getValue(); // 1=Monday, 7=Sunday
              
              // If weekend, move to next Monday
              if (dayOfWeek == 6 || dayOfWeek == 7) {
                int daysToAdd = (dayOfWeek == 6) ? 2 : 1;
                deliveryTime = deliveryTime + (daysToAdd * 24 * 60 * 60 * 1000L);
              }
              
              emit(deliveryTime);
            }
        """,
        "params": {
          "delivery_days": 3
        }
      }
    }
  }
}
```

This script includes the following steps:

* **Access order date**: Uses `doc['order_date'].value.millis` to retrieve the timestamp in milliseconds  
* **Add delivery days**: Converts days into milliseconds and adds them to the order date  
* **Check day of week**: Uses `ZonedDateTime` to extract the weekday from the calculated delivery time  
* **Skip weekends**: If Saturday or Sunday, moves the date to the following Monday  
* **Emit results**: Returns the adjusted delivery timestamp as a date

If everything works correctly, you should see:

```json
{
  "acknowledged": true
}
```

Now you can sort and display orders by their adjusted delivery timestamp:

```json
GET kibana_sample_data_ecommerce/_search
{
  "size": 5,
  "fields": [
    "delivery_timestamp"
  ],
  "_source": {
    "includes": [
      "order_id",
      "order_date",
      "customer_full_name"
    ]
  },
  "sort": [
    {
      "delivery_timestamp": {
        "order": "asc"
      }
    }
  ]
}
```

The results show delivery dates that avoid weekends. For example, orders placed on Thursday or Friday with 3 delivery days are shifted to Monday instead of falling on Saturday or Sunday:

:::{dropdown} Response

```json
{
  "hits": {
    "hits": [
      {
        "_source": {
          "customer_full_name": "Sultan Al Benson",
          "order_date": "2025-08-07T00:04:19+00:00",
          "order_id": 550375
        },
        "fields": {
          "delivery_timestamp": [
            "2025-08-11T00:04:19.000Z"
          ]
        }
      },
      {
        "_source": {
          "customer_full_name": "Pia Webb",
          "order_date": "2025-08-07T00:08:38+00:00",
          "order_id": 550385
        },
        "fields": {
          "delivery_timestamp": [
            "2025-08-11T00:08:38.000Z"
          ]
        }
      },
      {
        "_source": {
          "customer_full_name": "Jackson Bailey",
          "order_date": "2025-08-08T00:12:58+00:00",
          "order_id": 713287
        },
        "fields": {
          "delivery_timestamp": [
            "2025-08-11T00:12:58.000Z"
          ]
        }
      }
    ]
  }
}
```

:::

## Transform time data during reindex (reindex context)

In this example, we'll extract orders from a specific time window and add event-specific timing metadata for flash sale analysis. The script will calculate elapsed minutes from the event start, classify orders into time-based segments, and add fields for event analysis.

### Understanding the reindex scenario

Flash sale events generate concentrated purchasing activity within short time windows, making time-based analysis crucial for business intelligence. 

* **Rush periods:** Identifying peak demand moments for server capacity planning  
* **Conversion timing:** Analyzing whether early shoppers differ from late-decision customers  
* **Promotional effectiveness:** Measuring how purchasing behavior changes throughout the event duration

**Our 12 AM flash sale example:** E-commerce flash sales commonly start at midnight to capture global audiences and create urgency through limited-time offers. A 12:00 AM start maximizes reach across time zones and leverages the psychological impact of "new day" promotions. By categorizing orders into timing segments (`rush_start`, `peak_hour`, `final_rush`), we can analyze:

* **Rush\_start (0-30 min):** Early adopters who planned their purchase and stayed up for the launch  
* **Peak\_hour (30-60 min):** Customers drawn in by social sharing and notifications  
* **Final\_rush (60+ min):** Last-minute buyers motivated by scarcity

Event metadata to be added:

* `event_name`: Event identifier  
* `event_segment`: Time-based classification  
* `minutes_from_event_start`: Minutes elapsed since event start  
* `event_hour`: Hour classification

:::{important}    
Depending on when you added the dataset to {{es}}, the dates may vary. Make sure to use a recent date range to ensure that the reindex call processes documents.  
:::

### Writing the reindex script

The [reindex](elasticsearch://reference/elasticsearch/rest-apis/reindex-indices.md) operation will automatically generate the `flash_sale_event_analysis` index as it transfers and transforms documents from the source index. This destination index inherits the same field mappings as the source, with additional fields created by our script:

```json
POST _reindex
{
  "source": {
    "index": "kibana_sample_data_ecommerce",
    "query": {
      "range": {
        "order_date": {
          "gte": "2025-08-14T00:00:00",
          "lte": "2025-08-14T02:00:00"
        }
      }
    }
  },
  "dest": {
    "index": "flash_sale_event_analysis"
  },
  "script": {
    "lang": "painless",
    "source": """
      // Parse the order_date string using ZonedDateTime
      ZonedDateTime eventTime = ZonedDateTime.parse(ctx._source.order_date);
      
      int hour = eventTime.getHour();
      int minute = eventTime.getMinute();
      
      // Calculate minutes from event start (12 AM = 00:00)
      int minutesFromStart = hour * 60 + minute;
      
      // Classify by event timing
      String eventSegment;
      if (minutesFromStart <= 30) {
        eventSegment = 'rush_start';  // First 30 minutes
      } else if (minutesFromStart <= 60) {
        eventSegment = 'peak_hour';   // 30-60 minutes
      } else {
        eventSegment = 'final_rush';  // Last hour
      }
      
      // Add event analysis fields
      ctx._source.event_name = 'flash_sale';
      ctx._source.event_segment = eventSegment;
      ctx._source.minutes_from_event_start = minutesFromStart;
      ctx._source.event_hour = 'hour_' + (hour + 1); // hour_1, hour_2
    """
  }
}
```

This script includes the following steps:

* **Parse timestamps**: Converts ISO 8601 strings to ZonedDateTime objects  
* **Calculate event timing**: Determines minutes elapsed since 12:00 AM start  
* **Classify behavior periods**: Groups orders into `rush_start`/`peak_hour`/`final_rush` segments  
* **Add metadata**: Adds event analysis fields for business intelligence


For more details about Painless scripting in the reindex context, refer to the [Reindex context documentation](elasticsearch://reference/scripting-languages/painless/painless-reindex-context.md) or [Reindex API documentation](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex).

With the following request, we can see the final result in the `flash_sale_event_analysis` index:

```json
GET flash_sale_event_analysis/_search
```

:::{dropdown} Response

```json
"hits": [
  {
    "_index": "flash_sale_event_analysis",
    "_id": "c3acyJgBTbKqUnB55U8I",
    "_score": 1,
    "_source": {
      "minutes_from_event_start": 2,                
      ...
      "products": [...],
      "event_hour": "hour_1",                 
      ...
      "event_segment": "rush_start",          
      ...
      "order_date": "2025-08-25T00:23:02+00:00",
      "event_name": "flash_sale", 
      ...
      "order_id": 712908,
      ...
    }
  }
]
```

:::

## Learn more about datetime in Painless

This tutorial showed you practical datetime scripting across ingest, runtime fields, and reindex contexts. For deeper datetime capabilities and advanced patterns, explore the [Using datetime in Painless](elasticsearch://reference/scripting-languages/painless/using-datetime-in-painless.md) reference documentation.
