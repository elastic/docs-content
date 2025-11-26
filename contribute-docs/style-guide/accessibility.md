---
navigation_title: Accessibility and inclusivity
description: Guidelines for writing accessible and inclusive content.
---
 
# Accessibility

These guidelines are intended for all content authors and contains common tips and tricks for writing accessible content. It is not exhaustive and does not replace the official [WCAG 2.0 guidelines](https://www.w3.org/TR/2008/REC-WCAG20-20081211/#guidelines).

**Accessibility** for content means ensuring that all of our users can understand the content we publish—all of it—independently of how they choose or have to interact with it.

Our users and readers are diverse, with different abilities and disabilities. 
They also interact with our content in different ways, such as screen readers, mobile devices, and Braille. The list is long and constantly evolving. 

As content authors, it is our responsibility to provide them with [perceivable, operable, understandable, and robust content](https://www.w3.org/TR/UNDERSTANDING-WCAG20/intro.html#introduction-fourprincs-head).

## Guidelines [accessibility-guidelines]

✔️ **Make your content quickly scannable.** A clear structure and meaningful words will tell users if the content is relevant to them within seconds. Use unique headings, and put the most important information first.

✔️ **Add alt text for all images, icons, and media files.** Screen readers, Braille output devices, and search engines love concise, accurate alt text that describes what cannot always be displayed, viewed, or heard on screen. 

:::{dropdown} Examples
✔️ **Do:**

```md
![Signup page for Elastic Cloud](signup.png)
```

Note: Do not use special characters, such as backticks (`), in alt text. They are known to cause
  formatting issues when building pages.

  For audio and videos, add captions and create scripts that describe the visual content.
  Provide the script as a separate description track, either as timed text or recorded
  narration. There are many free, easy-to-use tools available that support the process of
  transcribing and captioning videos. For more information, refer to
  [Creating Accessible Videos](https://www.washington.edu/accessibility/videos/).

:::

✔️ **Use plain language.** Users read our content to perform their tasks. Jargon and complex sentences will confuse them or, at best, slow them down. Expand acronyms when first written. You can find helpful, detailed plain language guidance on the [plainlanguage.gov](https://www.plainlanguage.gov/guidelines/) website.

✔️ **Use parallel writing structures for similar things.** For example, don't use a combination of verbs and noun phrases to start each item in a list. Choose one or the other.

:::{dropdown} Examples
❌ **Don't:** 

* Navigate Elastic Security's various tools and interfaces.
* Use Elastic Security's detection engine with custom and prebuilt rules.
* System requirements, workspaces, configuration, and data ingestion.

✔️ **Do:** 

* Navigate Elastic Security's various tools and interfaces.
* Use Elastic Security's detection engine with custom and prebuilt rules.
* Learn about system requirements, workspaces, configuration, and data ingestion.

:::

✔️ **Use meaningful link text.** Descriptive text instead of "click here", "read more", or even a raw URL for a link makes it easier for users to understand what to expect when they open it. Screen
readers jump between links by generating a list of them, and spell out URLs.
:::{dropdown} Examples
❌ **Don't:** "[Click here](https://www.elastic.co) and make search your best ally."

✔️ **Do:** "Visit [Elastic.co](https://www.elastic.co) and make search your best ally."

:::

✔️ **Use device-agnostic language when possible.** Users can access content and products in many ways. We do not know if they use a mouse, keyboard, tablet, or another device. 
:::{dropdown} Examples
❌ **Don't:** "Enter a description and click the **Next** button."

✔️ **Do:** "Enter a description and select **Next**."

:::

✔️ **Avoid directional language.** *Above*, *below*, *left*, *right*, and so on. All these terms assume that the layout never varies, that users actually see it, and that they see it the way you think they do. What about disabilities or responsiveness?
:::{dropdown} Examples
  ❌ **Don't:** "Update your index mapping as you can see below to get the full benefit of
    aggregating and searching for feature importance."

  ✔️ **Do:** "To benefit from aggregating and searching for feature importance, update your
    index mapping as shown in this code example: [code example]"

:::

## Terms

| Avoid | Use instead |
| ----- | ----------- |
| Click, tap | Select, choose |
| Above | Preceding, previous |
| Below, under | Following, further, later |
| See | Check, refer to |
| Hear (hear about) | Learn |

## Testing content for accessibility

Test as early and often as possible. It is always a good exercise to spot improvements early and develop good habits. 
Here are a few methods that you can use to test content:

**Navigate a website or app with only a keyboard** to ensure all content is accessible and
that a skip navigation link exists.

**Test pages on mobile devices.** A growing number of users, including users with
disabilities, are accessing the web using phones, tablets, and other mobile devices. Test
your website using mobile devices, and when doing so, be sure to check for accessibility.

You don't need an actual phone to do this. The Chrome dev tools, for example, are a precious ally to test various layouts.

**Try a screen reader** to understand how users navigate websites using one of the screen
reader/browser combinations listed in the [Assistive technologies](#assistive-technologies) section.

**Turn off speakers and microphones** to ensure the website experience is the same with
or without sound.

## Assistive technologies

Assistive technology allows individuals with disabilities to access
information technology and perform functions that might be otherwise impossible, like
reading text, navigating websites, or listening to a video.

[Text-to-speech and screen readers](https://libguides.reading.ac.uk/inclusive-technology/text-to-speech)
read what's on your screen through the semantics placed in the content by developers.

[Screen magnification software](https://www.afb.org/blindness-and-low-vision/using-technology/using-computer/part-ii-experienced-computer-user-new-0)
enlarges the monitor and makes reading easy for vision-impaired users.

[The #NoMouse challenge](http://nomouse.org) provides guidance on navigating a
website using only the keyboard. Also, check out
[this list of special keyboards](https://bltt.org/keyboards-for-disabled-people/) made for
users with motor control difficulties.

## Inclusivity

These guidelines are intended for all content authors, whether you are a developer, designer, or writer. 
This page is not exhaustive but provides some guidelines to write inclusive content for product content and technical documentation.

**Inclusivity** for content means ensuring that the content we provide reflects the diversity of our community, respects it, and promotes positive change.

### Guidelines [inclusivity-guidelines]

### Write for an international audience

Our products and documentation use American English (en_US) as a standard for written content. 
Yet they are used and read by people all around the globe, for whom English is not always their primary language.
Our content must take that into account.

✔️ **Aim for simplicity.** We are a technical company that writes for 
  technically savvy users. However, keeping our writing as simple as possible benefits everyone.

  * **Short sentences**: They leave less space for interpretation. They are easier to scan, read, and translate.

  * **Plain language**: Active voice, present tense, using examples, and so on.
  Some of these guidelines might already look familiar. Several countries have [plain language initiatives](https://www.plainlanguage.gov/guidelines/) to promote clearer communication.
  Do your best to embrace these guidelines and focus on the message.
  We're not going for Scrabble high scores, and no one is carrying a thesaurus to read our docs.
  Well, maybe the writers...

  * **Negation**: It is generally easier for everyone to say what something IS versus what it is NOT.
  When you add a negative construction, it takes the reader longer to parse the meaning of the phrase.
  Instead of saying, "You cannot access the content without signing up", it's much easier to read, "Sign up to access the content."

  * **Words with multiple meanings**: 
  Don't skip helper words if they make the sentence clearer or easier to read.
  We try to be as literal and unambiguous as possible in our docs to ensure that our readers from around the globe can consume them.
  One way to achieve that is to choose words with fewer meanings, especially when a word's intended meaning is not its primary meaning.

:::{dropdown} Example
    You may have noticed the rather poetic use of _consume_ in the 
    previous paragraph. While the use here is correct, it's somewhat figurative. Someone 
    looking up the term in an English dictionary may wonder why on Earth they should 
    want to _eat, drink, or ingest_ our documentation.

    A more subtle example of a multi-meaning term that appears very often in 
    technical documentation is the word _once_. For example:

    "Once Luke, Leia, Han, and Chewie have entered the trash compactor, press Start."
    (_Death Star Reference Manual, V1.6, p.25_)

   The primary meaning of _once_ is _on one occasion_ or 
    _for one time only_. In this sentence, the term _after_ is preferable since it's unambiguous and, 
    therefore, easier for non-native English speakers and stormtroopers to 
    ~~consume~~ understand. 
:::

✔️ **Be aware of differences and diversity in content and examples.** 
Different people are used to different names, currencies, date and time formats, different measurement units (such as for temperature, distance, speed), and so much more.

* Avoid ambiguous values, like `04/05/06` for a date. Is it May 4 or April 5, and which year? `11/17/1987` leaves less room for interpretation if the exact format is not specified nearby. 
* If there is no obvious example standard (RFC) to follow, try to be diverse to represent our audience.

✔️ **Avoid idioms or expressions that are not commonly known, also known as regionalisms.**

In our Elastic documentation, we aim for a fun, friendly, and sometimes quirky tone.
To achieve that, it can help to use informal, playful language.
However, we also have to be careful that our text is as inclusive as possible, so we try to avoid expressions that might be unknown or opaque to some readers.
Here are a few examples of what to avoid:
  
* Idioms (for example, _It's a piece of cake_ or _So far so good_)
* Regional expressions (for example, _G'day!_, _Y'all_, or _eh_)
* Sports expressions (for example, _touched base_ or _threw a curve ball_)
* Pop culture references (for example, _Elvis has left the building_ or _Same bat-time, same bat-channel_)

We're all pretty good at avoiding these, but there's one problematic type of expression that shows up frequently in docs reviews.
Latin terms and abbreviations are a common source of confusion, particularly for people whose first language does not have Latin roots.

Here are some terms to avoid and suggested alternatives:

| Avoid | Use instead |
| ----- | ----------- |
| e.g. (exempli gratia) | For example |
| etc. (et cetera) | And more, and so on |
| i.e. (id est) | That is |
| via | By way of, by means of, through |

For more examples, refer to [](/contribute-docs/style-guide/word-choice.md)

✔️ **Aim for readability.** Tools like the Hemingway App can help you make content simpler. Be conversational, but prioritize clarity.

#### Use gender-neutral language

Writing gender-neutral mainly consists of avoiding gender bias and word choices implying that one gender is the norm.

✔️ **Pronouns.** In technical documentation, you can avoid this most of the time by addressing users directly.
When it's not possible, use *they*/*their*, even for singular. There's more than one gender, and it's not binary, either.

✔️ **Biased words and expressions.** Guys, mankind, policeman...these are all words we use and are used to hearing. But the default is not male.
Most expressions and words that perpetuate this bias (that exists in many cultures and languages!) can be replaced with neutral alternatives or synonyms: Folks, humanity, police officer...

#### Avoid violent, offensive, ableist terminology

Earlier in this page, we discussed avoiding ambiguous terms, especially when a word's intended meaning is 
not its primary meaning. Other types of words and phrases best avoided are:

* buzzwords (_incentivize_, _synergies_)
* superhero terms (_rockstar_, _wizard_, _ninja_)
* violent imagery (_crush the competition_)
* non-specific superlatives (_unrivaled_, _unparalleled_, _world class_)

Some words have nuances that fall into the above categories, which might cause 
them to be misinterpreted. For a full list, refer to [Word choice](word-choice.md).
