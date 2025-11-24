---
navigation_title: Grammar and spelling
description: Guidelines for using correct grammar and spelling in your writing.
---
 
# Grammar and spelling

## Pronouns do's and don'ts 

### Be unambiguous 

In order to make your sentences as clear as possible when using pronouns, they should always be unambiguous.

Pronouns provide a wonderful kind of shorthand so that we don't need to repeat lengthy terms over and over. But they can also cause confusion. In the first sentence, readers might be puzzled about whether the pronoun *they* refers to *your sentences* or to *pronouns*.

To remedy this, let's reorganize the sentence so that we don't need the *they* pronoun at all:

"In order to make your sentences as clear as possible, avoid using ambiguous pronouns".

And while we're at it, let's remove the *in order* since it doesn't really add anything:

"To make your sentences as clear as possible, avoid using ambiguous pronouns".

### Use second-person pronouns (*you*, *your*, *yours*)

In general, write in the second person to establish a friendly, casual tone with the reader as though you're speaking to them. Writing in the second person also helps you avoid using passive voice. However, don't overuse *your* when referring to user interaction. 

For example: *Your Elastic Agents* can feel overly familiar if used too many times. However, *your environment* as opposed to *the environment* sounds more casual. It can be tricky when deciding word choice, but when in doubt, try replacing the pronoun with *the* to see if it's an appropriate substitute.    

:::{dropdown} Examples
  * Log in to your account to display the settings. 
  * Verify that you have the correct permissions.
:::

### Use singular first-person pronouns sparingly (*I*, *me*, *my*, *mine*)

Typically, you should never write in the first person. You can, however, use first-person pronouns if they appear in the product UI. 

:::{dropdown} Example
Select the checkbox that says, "Confirm my selection." 
:::

### Use plural first-person pronouns wisely (*we*, *us*, *our*, *our*) 

First-person plural pronouns can sometimes convey a stuffy and serious tone—the opposite of Elastic's more casual tone. In some instances, however, it's okay to use these sparingly. For example, it's perfectly acceptable to say *we recommend*, and in fact is preferable over *it is recommended* since that uses passive voice. 

### Avoid gendered pronouns

Use gender-neutral pronouns as appropriate. Avoid using *he*, *him*, *his*, *she*, and *her*. Instead, try replacing it with a form of *user*. Also, avoid using combination pronouns such as *he/she* or *(s)he*. Use *they* or *them* instead.

## Verb tense 

Avoid temporal words like *currently*, *now*, or *will* and conditional words like *should* or *could*. Write in the present tense to describe the state of the product as it is now. You may need to use the past tense occasionally, but try to change it to the present tense to see if that's a better fit.

:::{dropdown} Example
  ❌ **Don't**: If you didn't select all the required permissions, an error message will appear.

  ✔️ **Do**: If you don't select all the required permissions, an error message appears. 
:::

## Contraction do's and dont's

Use contractions: they're (an acceptable contraction, by the way) conversational and don't require a lot of thought because we use them in everyday language. However, don't mix contractions and their spelled-out equivalents. For example, don't use *don't* and *do not* in the same context unless you absolutely need the latter for emphasis. 

Don't use Elastic references as a contraction to replace *Elastic is*. 

:::{dropdown} Example
  ❌ **Don't**: Elastic's excited to release this new feature.

  ✔️ **Do**: Elastic's new feature helps you find information fast. 
:::

Avoid ambiguous or awkward contractions, such as *there'd*, *it'll*, and *they'd*.

## Gerunds

A gerund is a verb form that ends in `-ing` and acts as a noun. Use gerunds or action verbs in titles that describe tasks. Use gerunds in top-level topic titles, but use action verbs in lower-level titles, especially in sections with many subtasks.

:::{dropdown} Example

Working with clusters

Change your cluster configuration

Keep your clusters healthy

Secure your cluster

:::

Avoid gerunds in prepositional phrases—this will make your instructions easier to understand. Also avoid gerunds in instructional/procedural sentences or headings. 

:::{dropdown} Example
  ❌ **Don't**: Refer to instructions on configuring the Elastic Agent.
  
  ✔️ **Do**: Refer to instructions on how to configure the Elastic Agent.
:::

## Punctuation 

### Colons

Use a colon at the end of a sentence or phrase that introduces a list. If a list item is followed by a description, use a colon to introduce the description.

:::{dropdown} Example
Select one of the following alert actions:
* **Close this alert**: Closes the alert when the exception is added. This option is only available when adding exceptions from the Alerts table.
* **Close all alerts that match this exception and were generated by this rule**: Closes all alerts that match the exception's conditions and were generated only by the current rule.
:::

### Commas

Use commas:

* Before the conjunction in a list of three or more items (also known as Oxford comma).

:::{dropdown} Examples
* Supported providers are OpenAI, Azure OpenAI Service, and Amazon Bedrock.
* Follow the onboarding instructions in the getting started guides for AWS, GCP, or Azure.
:::

* After an introductory word or phrase.

:::{dropdown} Examples
* Generally, the monitoring cluster and the clusters being monitored should be running the same version.
* For additional context, alert events are stored in hidden Elasticsearch indices.
:::

* To join independent clauses with a coordinating conjunction (*and*, *but*, *or*, *nor*, *fo*r, *so*, or *yet*).

:::{dropdown} Examples
* A case can have multiple connectors, but only one connector can be selected at a time.
* Click **Add events**, and follow the links for the types of data you want to collect.
:::

* When an adverbial dependent clause comes before an independent clause.

:::{dropdown} Examples
* When creating exceptions, you can assign them to individual rules or to multiple rules.
      * After rules have started running, you can monitor their executions to verify they are functioning correctly.
:::

* To set off non-defining relative clauses (also known as non-restrictive or parenthetical clauses).

:::{dropdown} Examples
    * Missing fields get a `null` value, which is used to group and suppress alerts.
    * The risk scoring engine calculates the user risk score for `User_A`, whose asset criticality level is **Extreme impact**.
:::

❌ Don't use commas:

* When an independent clause and a dependent clause are separated by a coordinating conjunction (*and*, *but*, *or*, *nor*, *fo*r, *so*, or *yet*).

:::{dropdown} Examples
    ❌ **Don't**: The rule runs every 5 minutes, but analyzes the documents added to indices during the last 6 minutes.

    ✔️ **Do**: The rule runs every 5 minutes but analyzes the documents added to indices during the last 6 minutes.

    ❌ **Don't**: A custom query rule searches the defined indices, and creates an alert when a document matches the rule's KQL query.

    ✔️ **Do**: A custom query rule searches the defined indices and creates an alert when a document matches the rule's KQL query.
:::

* To set off defining relative clauses.

:::{dropdown} Examples
    ❌ **Don't**: You must use a data view, whose index pattern matches `servers-europe-*`.

    ✔️ **Do**: You must use a data view whose index pattern matches `servers-europe-*`.

    ❌ **Don't**: To roll back, you must have a backup snapshot, that includes the `kibana` feature state.

    ✔️ **Do**: To roll back, you must have a backup snapshot that includes the `kibana` feature state.
:::

### Dashes and hyphens

#### Hyphens

Hyphens compound words, word elements, or numbers to change their meaning.

Use a hyphen:

* When a prefixed word has two vowels together.

:::{dropdown} Examples
    * Re-enable
    * Pre-approve
:::

* When two or more words modify the following noun, making a compound adjective.

:::{dropdown} Examples
    * Real-time results
    * AI-generated text
    * User-defined values
    * Up-to-date environment
:::

* Whenever the prefix is `self-`, `ex-`, or `all-`.

:::{dropdown} Example
  Self-managed deployment
:::

* For a minus sign and to indicate negative numbers. In formulas and equations, add spacing between the numbers and arithmetic operators. For negative numbers, don't add spacing between the minus and the number.

:::{dropdown} Examples
    * 12 - 3 = 9
* -79
:::

❌ Don't use a hyphen:

* For predicate adjectives (compound modifiers that come after the word they modify).

:::{dropdown} Examples
    ❌ **Don't**: Ensure your environment is up-to-date.

    ✔️ **Do**: Ensure your environment is up to date.

    ❌ **Don't**: The values are user-defined.

    ✔️ **Do**: The values are user defined.
:::

* For compounds with an adverb ending in `-ly`.

:::{dropdown} Examples
    ❌ **Don't**: Newly-installed Agent

    ✔️ **Do**: Newly installed Agent

    ❌ **Don't**: Publicly-exposed storage buckets

    ✔️ **Do**: Publicly exposed storage buckets
:::

#### En dashes

Use an en dash:

* When one of the elements in a compound adjective is an open compound (made up of two words with a space between them).

:::{dropdown} Examples
* Windows 10–compatible products
* AI Assistant–generated content 
:::

* To indicate a range of numbers, such as inclusive values or dates.

:::{dropdown} Examples
* The field must contain 1–3 values.
* Upgrade from v. 7.17 to v. 8.5–8.10.
:::

#### Em dashes

Use em dashes to indicate a break in the flow of a sentence. Don't add spaces around an em dash.

:::{dropdown} Examples
  * Consider adding exceptions—preferably with a combination of user agent and IP address conditions.
  * Filter out endpoint events that you don't want to store—for example, high-volume events.
:::

### Parentheses

Before using parentheses, consider if you can replace them with dashes, semicolons, or other punctuation marks. If you need to include parentheses, keep the text inside them short.

Use parentheses for abbreviations and acronyms after spelling them out.

:::{dropdown} Examples
  * Monitor the security posture of your cloud assets using the Cloud Security Posture Management (CSPM) feature.
  * Expand a risk level group (for example, **High**) or an asset criticality group (for example, **high_impact**).
:::

### Semicolons

In general, try to simplify complex sentences to avoid using semicolons.

Where necessary, use a semicolon to join two closely related independent clauses where a period or a comma is not as effective.

:::{dropdown} Examples
  * The endpoint is idempotent; therefore, it can safely be used to poll a given migration and, upon completion, finalize it.
  * Multiple consecutive dashes in the value must be escaped; single dashes do not need to be escaped.
:::

## Spelling

We use [American English](#american-english) unless referring to a product, feature, API, or UI element that uses a different flavor of English, like British English.

:::::{note}
You might notice variations in our older docs. In the past, we used all variations of English freely throughout our docs. Now, we strive for consistency to reduce uncertainty among readers and contributors.
:::::

Outside of technical writing, Elastic has used variations of English in product, feature, and API names. Always use the spelling as it appears in the product when writing documentation.

Similarly, if you are referencing a non-Elastic product that uses a different flavor of English, including in the UI text, use the spelling as it appears in the product.

For example, in the [CI/CD observability guide](https://www.elastic.co/guide/en/observability/current/ci-cd-observability.html), we use the word "Visualisation" because that's how it appears in the Jenkins UI. Typically we would use the American spelling, "Visualization", instead.

### American English

American English is a version of the English language used in the United States. It's sometimes called United States English or U.S. English.

Certain words are spelled differently in American English and British English. You'll find some of these key spelling differences in the following sections.  

#### Verbs that end with `-ize` or `-yze`

In American English, verbs that end with `-ize` usually end with `-ise` in British English. Similarly, verbs that end with `-yze` in American English usually end with `-yse` in British English. 

| American English | British English | 
| ------------- |:-------------:|
| organize | organise | 
| authorize | authorise |  
| analyze | analyse | 

#### Nouns that end with `-or`

In American English, nouns that end with `-or` usually end with `-our` in British English.

| American English | British English | 
| ------------- |:-------------:|
| flavor | flavour | 
| color | colour |  
| behavior | behaviour | 

#### Nouns that end with `-ense` 

In American English, nouns that end with `-ense` usually end with `-ence` in British English.

| American English | British English | 
| ------------- |:-------------:|
| license | licence | 
| defense | defence |  
| pretense | pretence | 

#### Nouns that end with `-og` 

In American English, nouns that end with `-og` usually end with `-ogue` in British English.

| American English | British English | 
| ------------- |:-------------:|
| dialog | dialogue | 
| catalog | catalogue |  
| epilog | epilogue | 

## Capitalization

Follow the standard capitalization rules for American English. In general, use sentence-style capitalization and follow these rules:

* Capitalize the first word of a sentence, heading, title, or standalone phrase.
* Capitalize proper nouns and product names.
* Use lowercase for everything else.
* Match the capitalization as it appears in the UI.

❌ Don't capitalize the spelled-out form of an acronym unless it's a proper noun or is conventionally capitalized.

:::{dropdown} Examples
  ❌ **Don't**: This tab shows anomalies discovered by Machine Learning (ML) jobs.

  ✔️ **Do**: This tab shows anomalies discovered by machine learning (ML) jobs.
:::

❌ Don't capitalize API names.

:::{dropdown} Examples
  ❌ **Don't**: The Bulk API makes it possible to perform many index/delete operations in a single API call.

  ✔️ **Do**: The bulk API makes it possible to perform many index/delete operations in a single API call.
:::

## Abbreviations and acronyms

In general, spell out abbreviations when a term is unlikely to be familiar to the audience, or may be familiar only to a specific group of readers. Spell them out the first time you use them in body text—avoid using them in titles. Use the abbreviation rather than the full term for later mentions on the same page.

### Abbreviations in titles

Avoid using an abbreviation for the first time in a title or heading, unless you need to match the UI, for example. If the first use of the abbreviation is in a title or heading, introduce the abbreviation (in parentheses, following the spelled-out term) in the following body text.

:::{dropdown} Examples
  ❌ **Don't**: ECS field reference

  ✔️ **Do**: Elastic Common Schema field reference

  ✔️ **Do**: Create an ES|QL rule (OK to use abbreviation since this is how the rule type appears in the UI)
:::

### Capitalization of abbreviations

Capitalize the spelled-out version of the abbreviation only if it's a proper noun or is conventionally capitalized. That is, don't capitalize it only because the abbreviation includes capital letters.

:::{dropdown} Examples
  ❌ **Don't**: This setting determines whether Cross-Cluster Search (CCS) privilege warnings are displayed.

  ✔️ **Do**: This setting determines whether cross-cluster search (CCS) privilege warnings are displayed.
:::

### Making abbreviations plural

When making them plural, treat abbreviations as regular words. Do not use an apostrophe before the `-s` suffix.

If the abbreviation ends in `-s`, `-sh`, `-ch`, or `-x`, then add `-es`.

:::{dropdown} Examples
 ❌ **Don't**: API's, SDK's, OS'es

 ✔️ **Do**: APIs, SDKs, OSes
:::

### Using the right article

The article (*a* or *an*) you use in front of an abbreviation depends on how the abbreviation is pronounced, not how it's spelled.

:::{dropdown} Examples
 ❌ **Don't**: a HTML file, a SQL database

 ✔️ **Do**: an HTML file,  an SQL database
:::

### Latin abbreviations

Avoid Latin abbreviations for common English phrases, unless space is limited.

:::{dropdown} Examples
  ❌ **Don't**: e.g.
  
  ✔️ **Do**: for example
:::

## Glossary

For a list of terms and abbreviations commonly used in our docs, refer to the [Glossary](/reference/glossary/index.md).