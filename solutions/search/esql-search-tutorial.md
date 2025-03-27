---
navigation_title: "Search and filter with ES|QL"
---

# Tutorial: Search and filter with {{esql}}

:::{tip}
This tutorial presents examples in {{esql}} syntax. Refer to [the Query DSL version](querydsl-full-text-filter-tutorial.md) for the equivalent examples in Query DSL syntax.
:::

This is a hands-on introduction to the basics of full-text search and semantic search, using [{{esql}}](/explore-analyze/query-filter/languages/esql.md).

% TODO For an overview of all the search capabilities in {{esql}}, refer to [Search with {{esql}}](elasticsearch://reference/query-languages/esql/esql-for-search.md).

In this scenario, we're implementing search for a cooking blog. The blog contains recipes with various attributes including textual content, categorical data, and numerical ratings.

## Requirements

You'll need a running {{es}} cluster, together with {{kib}} to use the Dev Tools API Console. Refer to [choose your deployment type](/deploy-manage/deploy.md#choosing-your-deployment-type) for deployment options.

Want to get started quickly? Run the following command in your terminal to set up a [single-node local cluster in Docker](get-started.md):

```sh
curl -fsSL https://elastic.co/start-local | sh
```

## Running {{esql}} queries

In this tutorial, you'll see {{esql}} examples in the following format:

```esql
FROM cooking_blog
| WHERE description:"fluffy pancakes"
| LIMIT 1000
```

If you want to run these queries in the [Dev Tools Console](/explore-analyze/query-filter/languages/esql-rest.md#esql-kibana-console), you'll need to use the following syntax:

```console
POST /_query?format=txt
{
  "query": """
    FROM cooking_blog 
    | WHERE description:"fluffy pancakes"  
    | LIMIT 1000 
  """
}
```

If you'd prefer to use your favorite programming language, refer to [Client libraries](/solutions/search/site-or-app/clients.md) for a list of official and community-supported clients.

## Step 1: Create an index

Create the `cooking_blog` index to get started:

```console
PUT /cooking_blog
```

Now define the mappings for the index:

```console
PUT /cooking_blog/_mapping
{
  "properties": {
    "title": {
      "type": "text",
      "analyzer": "standard", <1>
      "fields": { <2>
        "keyword": {
          "type": "keyword",
          "ignore_above": 256 <3>
        }
      }
    },
    "description": {
      "type": "text",
      "fields": {
        "keyword": {
          "type": "keyword"
        }
      }
    },
    "author": {
      "type": "text",
      "fields": {
        "keyword": {
          "type": "keyword"
        }
      }
    },
    "date": {
      "type": "date",
      "format": "yyyy-MM-dd"
    },
    "category": {
      "type": "text",
      "fields": {
        "keyword": {
          "type": "keyword"
        }
      }
    },
    "tags": {
      "type": "text",
      "fields": {
        "keyword": {
          "type": "keyword"
        }
      }
    },
    "rating": {
      "type": "float"
    }
  }
}
```

1. The `standard` analyzer is used by default for `text` fields if an `analyzer` isn't specified. It's included here for demonstration purposes.
2. [Multi-fields](elasticsearch://reference/elasticsearch/mapping-reference/multi-fields.md) are used here to index `text` fields as both `text` and `keyword` [data types](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md). This enables both full-text search and exact matching/filtering on the same field. Note that if you used [dynamic mapping](../../manage-data/data-store/mapping/dynamic-field-mapping.md), these multi-fields would be created automatically.
3. The [`ignore_above` parameter](elasticsearch://reference/elasticsearch/mapping-reference/ignore-above.md) prevents indexing values longer than 256 characters in the `keyword` field. Again this is the default value, but it's included here for demonstration purposes. It helps to save disk space and avoid potential issues with Lucene's term byte-length limit.

::::{tip}
Full-text search is powered by [text analysis](full-text/text-analysis-during-search.md). Text analysis normalizes and standardizes text data so it can be efficiently stored in an inverted index and searched in near real-time. Analysis happens at both [index and search time](../../manage-data/data-store/text-analysis/index-search-analysis.md). This tutorial won't cover analysis in detail, but it's important to understand how text is processed to create effective search queries.
::::

## Step 2: Add sample blog posts to your index [full-text-filter-tutorial-index-data]

Now you’ll need to index some example blog posts using the [Bulk API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-settings). Note that `text` fields are analyzed and multi-fields are generated at index time.

```console
POST /cooking_blog/_bulk?refresh=wait_for
{"index":{"_id":"1"}}
{"title":"Perfect Pancakes: A Fluffy Breakfast Delight","description":"Learn the secrets to making the fluffiest pancakes, so amazing you won't believe your tastebuds. This recipe uses buttermilk and a special folding technique to create light, airy pancakes that are perfect for lazy Sunday mornings.","author":"Maria Rodriguez","date":"2023-05-01","category":"Breakfast","tags":["pancakes","breakfast","easy recipes"],"rating":4.8}
{"index":{"_id":"2"}}
{"title":"Spicy Thai Green Curry: A Vegetarian Adventure","description":"Dive into the flavors of Thailand with this vibrant green curry. Packed with vegetables and aromatic herbs, this dish is both healthy and satisfying. Don't worry about the heat - you can easily adjust the spice level to your liking.","author":"Liam Chen","date":"2023-05-05","category":"Main Course","tags":["thai","vegetarian","curry","spicy"],"rating":4.6}
{"index":{"_id":"3"}}
{"title":"Classic Beef Stroganoff: A Creamy Comfort Food","description":"Indulge in this rich and creamy beef stroganoff. Tender strips of beef in a savory mushroom sauce, served over a bed of egg noodles. It's the ultimate comfort food for chilly evenings.","author":"Emma Watson","date":"2023-05-10","category":"Main Course","tags":["beef","pasta","comfort food"],"rating":4.7}
{"index":{"_id":"4"}}
{"title":"Vegan Chocolate Avocado Mousse","description":"Discover the magic of avocado in this rich, vegan chocolate mousse. Creamy, indulgent, and secretly healthy, it's the perfect guilt-free dessert for chocolate lovers.","author":"Alex Green","date":"2023-05-15","category":"Dessert","tags":["vegan","chocolate","avocado","healthy dessert"],"rating":4.5}
{"index":{"_id":"5"}}
{"title":"Crispy Oven-Fried Chicken","description":"Get that perfect crunch without the deep fryer! This oven-fried chicken recipe delivers crispy, juicy results every time. A healthier take on the classic comfort food.","author":"Maria Rodriguez","date":"2023-05-20","category":"Main Course","tags":["chicken","oven-fried","healthy"],"rating":4.9}
```

## Step 3: Perform basic full-text searches

Full-text search involves executing text-based queries across one or more document fields. These queries calculate a relevance score for each matching document, based on how closely the document's content aligns with the search terms. Elasticsearch offers various query types, each with its own method for matching text and relevance scoring.

:::{tip}
{{esql}} provides two ways to perform full-text searches:

1. Full [match function](elasticsearch://reference/query-languages/esql/esql-functions-operators.md#esql-match) syntax: `match(field, "search terms")`
1. Compact syntax using the [match operator `:`](elasticsearch://reference/query-languages/esql/esql-functions-operators.md#esql-search-operators): `field:"search terms"`

Both are equivalent and can be used interchangeably. The compact syntax is more concise, while the function syntax allows for more configuration options. We'll use the compact syntax in most examples for brevity.

Refer to the [match function](elasticsearch://reference/query-languages/esql/esql-functions-operators.md#esql-match) reference docs for advanced parameters available with the function syntax.
:::

### Basic full-text query

Here's how to search the `description` field for "fluffy pancakes":

```esql
FROM cooking_blog  # Specify the index to search
| WHERE description:"fluffy pancakes"  # Full-text search with OR logic by default
| LIMIT 1000  # Return up to 1000 results
```

:::{note}
The results ordering isn't by relevance, as we haven't requested the `_score` metadata field. We'll cover relevance scoring in the next section.
:::

By default, like the Query DSL `match` query, {{esql}} uses `OR` logic between terms. This means it will match documents that contain either "fluffy" or "pancakes", or both, in the description field.

:::{tip}
You can control which fields to include in the response using the `KEEP` command:

```esql
FROM cooking_blog
| WHERE description:"fluffy pancakes"
| KEEP title, description, rating  # Select only specific fields to include in response
| LIMIT 1000
```
:::

### Require all terms in a match query

Sometimes you need to require that all search terms appear in the matching documents. Here's how to do that using the function syntax with the `operator` parameter:

```esql
FROM cooking_blog
| WHERE match(description, "fluffy pancakes", {"operator": "AND"})  # Require ALL terms to match
| LIMIT 1000
```

This stricter search returns *zero hits* on our sample data, as no document contains both "fluffy" and "pancakes" in the description.

### Specify a minimum number of terms to match

Sometimes requiring all terms is too strict, but the default OR behavior is too lenient. You can specify a minimum number of terms that must match:

```esql
FROM cooking_blog
| WHERE match(title, "fluffy pancakes breakfast", {"minimum_should_match": 2})
| LIMIT 1000
```

This query searches the title field to match at least 2 of the 3 terms: "fluffy", "pancakes", or "breakfast".

## Step 4: Semantic search and hybrid search

### Index semantic content

{{es}} allows you to semantically search for documents based on the meaning of the text, rather than just the presence of specific keywords. This is useful when you want to find documents that are conceptually similar to a given query, even if they don't contain the exact search terms.

ES|QL supports semantic search when your mappings include fields of the [`semantic_text`](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text.md) type. This example mapping update adds a new field called `semantic_description` with the type `semantic_text`:

```console
PUT /cooking_blog/_mapping
{
  "properties": {
    "semantic_description": {
      "type": "semantic_text"
    }
  }
}
```

Next, index a document with content into the new field:

```console
POST /cooking_blog/_doc
{
  "title": "Mediterranean Quinoa Bowl",
  "semantic_description": "A protein-rich bowl with quinoa, chickpeas, fresh vegetables, and herbs. This nutritious Mediterranean-inspired dish is easy to prepare and perfect for a quick, healthy dinner.",
  "author": "Jamie Oliver",
  "date": "2023-06-01",
  "category": "Main Course",
  "tags": ["vegetarian", "healthy", "mediterranean", "quinoa"],
  "rating": 4.7
}
```

### Perform semantic search

Once the document has been processed by the underlying model running on the inference endpoint, you can perform semantic searches. Here's an example natural language query against the `semantic_description` field:

```esql
FROM cooking_blog
| WHERE semantic_description:"What are some easy to prepare but nutritious plant-based meals?"
| LIMIT 5 
```

:::{tip}
Follow this [tutorial](/solutions/search/semantic-search/semantic-search-semantic-text.md) if you'd like to test out the semantic search workflow against a large dataset.
:::

### Perform hybrid search

You can combine full-text and semantic queries. In this example we combine full-text and semantic search with custom weights:

```esql
FROM cooking_blog METADATA _score
| WHERE match(semantic_description, "easy to prepare vegetarian meals", { "boost": 0.75 })
    OR match(tags, "vegetarian", { "boost": 0.25 })
| SORT _score DESC
| LIMIT 5
```

## Step 5: Search across multiple fields at once

When users enter a search query, they often don't know (or care) whether their search terms appear in a specific field. {{esql}} provides ways to search across multiple fields simultaneously:

```esql
FROM cooking_blog
| WHERE title:"vegetarian curry" OR description:"vegetarian curry" OR tags:"vegetarian curry"
| LIMIT 1000
```

This query searches for "vegetarian curry" across the title, description, and tags fields. Each field is treated with equal importance.

However, in many cases, matches in certain fields (like the title) might be more relevant than others. We can adjust the importance of each field using scoring:

```esql
FROM cooking_blog METADATA _score  # Request _score metadata for relevance-based results
| WHERE match(title, "vegetarian curry", {"boost": 2.0})  # Title matches are twice as important
    OR match(description, "vegetarian curry")
    OR match(tags, "vegetarian curry")
| KEEP title, description, tags, _score  # Include relevance score in results
| SORT _score DESC  # You must explicitly sort by `_score` to see relevance-based results
| LIMIT 1000
```

:::{tip}
When working with relevance scoring in ES|QL, it's important to understand `_score`. If you don't include `METADATA _score` in your query, you won't see relevance scores in your results. This means you won't be able to sort by relevance or filter based on relevance scores.

When you include `METADATA _score`, search functions included in WHERE conditions contribute to the relevance score. Filtering operations (like range conditions and exact matches) don't affect the score.

If you want the most relevant results first, you must sort by `_score`, by explicitly using `SORT _score DESC` or `SORT _score ASC`.
:::

## Step 6: Filter and find exact matches

Filtering allows you to narrow down your search results based on exact criteria. Unlike full-text searches, filters are binary (yes/no) and do not affect the relevance score. Filters execute faster than queries because excluded results don't need to be scored.

```esql
FROM cooking_blog
| WHERE category.keyword == "Breakfast"  # Exact match using keyword field(case-sensitive)
| KEEP title, author, rating, tags
| SORT rating DESC
| LIMIT 1000
```

Note the use of `category.keyword` here. This refers to the [`keyword`](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md) multi-field of the `category` field, ensuring an exact, case-sensitive match.

### Search for posts within a date range

Often users want to find content published within a specific time frame:

```esql
FROM cooking_blog
| WHERE date >= "2023-05-01" AND date <= "2023-05-31"  # Inclusive date range filter
| KEEP title, author, date, rating
| LIMIT 1000
```

### Find exact matches

Sometimes users want to search for exact terms to eliminate ambiguity in their search results:

```esql
FROM cooking_blog
| WHERE author.keyword == "Maria Rodriguez"  # Exact match on author
| KEEP title, author, rating, tags
| SORT rating DESC
| LIMIT 1000
```

Like the `term` query in Query DSL, this has zero flexibility and is case-sensitive.

## Step 7: Combine multiple search criteria

Complex searches often require combining multiple search criteria:

```esql
FROM cooking_blog METADATA _score
| WHERE rating >= 4.5  # Numerical filter
    AND NOT category.keyword == "Dessert"  # Exclusion filter
    AND (title:"curry spicy" OR description:"curry spicy")  # Full-text search in multiple fields
| SORT _score DESC
| KEEP title, author, rating, tags, description
| LIMIT 1000
```

### Combine relevance scoring with custom criteria

For more complex relevance scoring with combined criteria, you can use the `EVAL` command to calculate custom scores:

```esql
FROM cooking_blog METADATA _score
| WHERE NOT category.keyword == "Dessert"
| EVAL tags_concat = MV_CONCAT(tags.keyword, ",")  # Convert multi-value field to string
| WHERE tags_concat LIKE "*vegetarian*" AND rating >= 4.5  # Wildcard pattern matching
| WHERE match(title, "curry spicy", {"boost": 2.0}) OR match(description, "curry spicy") # Uses full text functions, will update _score metadata field
| EVAL category_boost = CASE(category.keyword == "Main Course", 1.0, 0.0)  # Conditional boost
| EVAL date_boost = CASE(DATE_DIFF("month", date, NOW()) <= 1, 0.5, 0.0)  # Boost recent content
| EVAL custom_score = _score + category_boost + date_boost  # Combine scores
| WHERE custom_score > 0  # Filter based on custom score
| SORT custom_score DESC
| LIMIT 1000
  
```

## Learn more

### Documentation

This tutorial introduced the basics of search and filtering in {{esql}}. Building a real-world search experience requires understanding many more advanced concepts and techniques. Here are some resources once you're ready to dive deeper:

% TODO [Search with {{esql}}](): Learn about all your options for search use cases with {{esql}}.
- [{{esql}} search functions](elasticsearch://reference/query-languages/esql/esql-functions-operators.md#esql-search-functions): Explore the full list of search functions available in {{esql}}.
- [Semantic search](/solutions/search/semantic-search.md): Understand your various options for semantic search in Elasticsearch.
  - [The `semantic_text` workflow](/solutions/search/semantic-search.md#_semantic_text_workflow): Learn how to use the `semantic_text` field type for semantic search. This is the recommended approach for most users looking to perform semantic search in {{es}}, because it abstracts away the complexity of setting up inference endpoints and models.

### Related blog posts

% TODO [[uncomment once blog is live]] - https://www.elastic.co/blog/esql-you-know-for-search-scoring-semantic-search[ES|QL, you know for Search]: Introducing scoring and semantic search
- [Introducing full text filtering in ES|QL](https://www.elastic.co/blog/introducing-full-text-filtering-with-esql): Overview of text filtering capabilities
