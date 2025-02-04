---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-concepts.html
---

# Conventions and Terminology [sql-concepts]

For clarity, it is important to establish the meaning behind certain words as, the same wording might convey different meanings to different readers depending on one’s familiarity with SQL versus {{es}}.

::::{note} 
This documentation while trying to be complete, does assume the reader has *basic* understanding of {{es}} and/or SQL. If that is not the case, please continue reading the documentation however take notes and pursue the topics that are unclear either through the main {{es}} documentation or through the plethora of SQL material available in the open (there are simply too many excellent resources here to enumerate).
::::


As a general rule, Elasticsearch SQL as the name indicates provides a SQL interface to {{es}}. As such, it follows the SQL terminology and conventions first, whenever possible. However the backing engine itself is {{es}} for which Elasticsearch SQL was purposely created hence why features or concepts that are not available, or cannot be mapped correctly, in SQL appear in Elasticsearch SQL. Last but not least, Elasticsearch SQL tries to obey the [principle of least surprise](https://en.wikipedia.org/wiki/Principle_of_least_astonishment), though as all things in the world, everything is relative.


