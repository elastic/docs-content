# SEO guidelines

Learn how to structure content for search visibility, craft clear and user-focused copy, and apply techniques that improve discoverability and usability. To deliver value to users, search engines and AI-powered tools—including large language models (LLMs), use the SEO guidelines to ensure your documentation is easy to find, understand, and maintain.

As AI-powered assistants and LLMs become more common, documentation is increasingly consumed by both humans and AI tools. Following these best practices ensures your content is discoverable, understandable, and actionable—not just for search engines and users, but also for AI-driven platforms that rely on clear structure and context to provide accurate answers and guidance.

Use these guidelines to ensure your documentation is easy to find, understand, and maintain—delivering value to users and search engines alike.

## Headings

Headings provide a clear structure to your documentation, making it easier to scan and understand. For SEO, headings (H1, H2, H3, and so on) signal the hierarchy and main topics of your content, helping search engines, LLMs (Large Language Models) determine the relevance of your page to specific queries. For users, well-structured headings improve readability, accessibility, and navigation, especially for long or complex pages.

Use headings in order, maintaining [W3C standards](https://www.w3.org/standards/). Accurately reflect the content that follows each heading. Avoid vague headings like "Introduction" or "Overview", and use specific headings like "Introduction to using Elasticsearch". Make heading text unique, especially for headings higher in the hierarchy.

### H1: Primary page title

The H1 is the main title of the page and should clearly state the primary topic or purpose. Search engines give significant weight to the H1. There should be only one H1 per page, and each H1 should be unique. When headings are not unique, search engines struggle to understand the differences between thematically related pages.

Best practices:

* Include the main topic.  
* Be concise and descriptive.  
* Reflect what the user will learn or accomplish.  
* Be specific. Add any modifiers that make clear what the purpose of the page is.  
* H1s should *always* be unique.  
* Incorporate any applicable primary keywords.

Examples:

✅Configure data views in Kibana

❌Data views

✅Elasticsearch documentation

❌Elasticsearch

⚠️**Note:** The primary H1 header tag, sometimes called the page title, is what is used to populate the meta title tag, which appears on the search engines results page and impacts the Click-Through Rate (CTR).

Example:  
![Screenshot of a documentation page showing the meta title field in a content management system. The meta title field is populated with Elasticsearch Documentation. The interface includes form fields and labels in a clean, minimal layout. The tone is neutral and instructional, focusing on how the meta title is set for a documentation page.](./images/metatitleexample.png)

The meta title, and in turn, the page title, is very broad. A more descriptive title could be "Data ingestion with Elasticsearch".

Best practices:

* The meta title should be concise, descriptive, and include the main keyword or topic of the page.  
* It's important that the H1 accurately reflects the page's content and purpose, as this will be shown in the search results.  
* Avoid duplicating meta titles across different pages. Each should be unique.  
* Keep the H1 to a recommended length of 50–60 characters, and make sure the most important information is at the beginning.  
* The meta title is not directly visible to users on the page itself, but it's critical for search visibility and user engagement in search results.

### H2: Secondary headings

H2s break the content into logical sections, outlining key steps, concepts, or features. H2s help search engines understand subtopics and improve page scannability. Given the volume of documentation content, and the similarity between certain topics, try to make secondary headings unique.

Best practices:

* Use H2s for major sections or steps.  
* Incorporate secondary keywords where relevant.  
* H2s are descriptive so users can quickly find the information they need.

Examples:

✅Configure output settings

❌Settings

✅Deploy Filebeat to Kubernetes

❌Deploy

### Subheadings

H3 and greater subheadings further divide section content into more specific topics or steps. These headings help organize detailed information and can target long-tail keywords.

Best practices:

* Use H3s and great subheadings for sub-steps, options, or detailed explanations within an H2 section.  
* Keep them short and relevant.  
* Maintain logical hierarchy and don’t skip heading levels.

Example:

H2: Troubleshoot common issues

H3: Resolve mapping conflicts

## Introductory paragraph

The introductory paragraph is the first section users and search engines encounter after the H1 page title. A well-crafted introduction sets clear expectations, provides essential context, and helps both readers and search engines quickly understand the page purpose. For SEO, it’s an opportunity to naturally include primary keywords and related terms, improving the page relevance for targeted queries. Sticking to any context that will help ground the visitor in the content they are about to ingest is a perfect introductory paragraph.

Best practices:

* **Be clear and concise**: Summarize what the page covers in 1–3 sentences. Avoid unnecessary background or filler.  
* **State the purpose**: Clearly explain what users will learn or accomplish by reading the page.  
* **Include keywords**: Use primary and secondary keywords naturally within the first 1–2 sentences to reinforce relevance.  
* **Address the audience needs**: Reflect the user’s intent, such as the problem they are trying to solve or what task are they performing. 
* **Avoid jargon**: Use plain language, or briefly define technical terms if needed.  
* **Keep it actionable**: If the page is a how-to or guide, indicate the action or outcome.

**⚠️Note:** Within the context of the "introductory paragraph", the first and/or second sentence is used in the meta description tag, up to the first 150-160 characters. This tag appears on the search engines results page and impacts CTR. It is not directly user-facing otherwise.

When a page starts with a note, image, table, or other component, the meta description is *not* impacted by the component content. Only the first paragraph content nested within the first lines of the opening paragraph tags \<p\>\</p\>) impact the meta description.

Below is an example of a page with one sentence and no introductory paragraph.  
![Screenshot of a documentation page displaying only a single sentence without an introductory paragraph. The page shows a heading at the top, followed by the sentence: Pulse Connect Secure integration enables you to collect, monitor, and analyze VPN and remote access logs from Pulse Connect Secure appliances in Elastic. The layout is minimal and lacks additional context or descriptive content, creating a sparse and utilitarian tone.](./images/onesentence.png) 

If the page had more content, which is required, a good introductory paragraph within the context of this example could be something like "The Pulse Connect Secure integration enables you to collect, monitor, and analyze VPN and remote access logs from Pulse Connect Secure appliances in Elastic. Use this integration to gain visibility into user activity, detect security events, and streamline compliance reporting within Kibana. Compatible with Elastic Stack version 8.13.0 and higher, this integration supports both Security and Observability use cases".

In turn, the meta description would be more descriptive, for example, "The Pulse Connect Secure integration enables you to collect, monitor, and analyze VPN and remote access logs from Pulse Connect Secure appliances in Elastic".

Examples:  
**Overview**

Heartbeat is an Elastic Stack monitoring tool that enables you to track the availability and response time of services across your infrastructure. This overview explains how Heartbeat works, its key features, and how it integrates with other Elastic solutions to provide real-time uptime monitoring and alerting. Use Heartbeat to proactively detect outages, measure service performance, and ensure your systems remain reliable.

**How-to**

Learn how to configure index patterns in Kibana to manage and visualize your Elasticsearch data efficiently. This guide walks you through each step, from creating a new pattern to troubleshooting common issues.

**Troubleshooting**

If you’re experiencing issues with index patterns in Kibana, this page provides solutions to common problems and tips for resolving errors quickly.

## Body copy

The body copy is where you deliver the main content of your documentation page. Well-structured, clear, and concise body copy helps users accomplish their goals and enables search engines to understand the depth and relevance of your content. For technical documentation, body copy should be easy to scan, actionable, and accurate.

Best practices:

**Establish authority and credibility by relaying expertise**

* Using accurate technical terms demonstrates expertise and familiarity with the subject.  
* Define technical terms on first use, especially if your audience may include newcomers.  
* Proper terminology reassures users that the documentation is trustworthy and written by knowledgeable authors.  
* Technical terminology helps attract and serve users who are already familiar with your field or searching for in-depth information.

**Write clearly and concisely**

* Use plain language and define technical terms on first use.  
* Keep sentences and paragraphs short for readability.  
* Use active voice and direct instructions.  
* Avoid overusing jargon—balance technical accuracy with clarity to ensure content remains accessible.

**Thoughtfully use relevant keywords**

* Incorporate keywords that match the search intent of your target audience and the topic of the page.  
* Place keywords naturally throughout the content—especially in headings, the first paragraph, and where they fit contextually.  
* Include related terms and synonyms to improve semantic relevance.

**Organize with headings and subheadings**

* Break content into logical sections using descriptive headings (H2, H3, and so on).  
* Headings help users scan for relevant information and assist search engines in understanding content hierarchy.  
* Each heading should accurately reflect the content that follows.

**Ensure content quality, originality, and uniqueness**

* Avoid thin content—ensure each page provides substantial, unique value to the reader.  
* Do not duplicate content from other pages or sources; always tailor information for the specific context and audience.  
* Regularly review and update content to keep it accurate and relevant.

**Make content scannable**

* Use bullet points, numbered lists, and callouts for important information.  
* Highlight warnings, tips, or best practices using clear formatting.

**Provide examples and visuals**

* Include code snippets, sample commands, or screenshots to illustrate concepts.  
* Reference visuals in the text, but ensure all key information is also available in text for accessibility.

**Leverage structured data, where applicable**

Use structured data (for example, [schema.org](https://schema.org/) markup) to add semantic meaning.  
* Structured data can help search engines display your documentation in rich results, such as FAQs or How-To snippets.  
  Check with the documentation team for existing capabilities or implementation guidance.

### Content length

The ideal length for a body copy should not be focused on word count, but instead on whether the content is enough to be satisfying to a user and accomplish its goal.

Paragraph length is also important. Readers on the Internet are conditioned to skim, looking for emphasized words in short paragraphs. Using highlighted, pulled-out blockquote boxes, asides, call-out sections, section dividers, and other features help liven up a page.

These visual breaks help make sure a user’s attention span isn’t broken. They should also not be overused, and their frequency will depend upon the relationship to the topic.

Best practices:
**Focus on user needs, not word count**

* The ideal length for a documentation page is determined by how well it answers the user’s question or helps them accomplish their task.  
* Avoid padding content to meet arbitrary word counts; instead, ensure the page is comprehensive, accurate, and directly relevant.  
* If a topic is too broad, consider breaking it into multiple focused pages for easier navigation and better SEO.

**Keep paragraphs clear and scannable**

* Online readers tend to skim rather than read every word. Ensure that content is easy to digest.  
* Start paragraphs with key information and use plain language for clarity.  
* Use formatting tools (bold, italics, code formatting) to highlight important terms or actions.

### Lists

Lists are powerful tools for organizing information in a clear, scannable format. Lists help make your content easier to read and scan, they can increase user engagement and retention, improve your content’s structure and layout, and much more.

Best practices:
**Choose the right list type**

* Use bulleted lists for unordered items, features, or options.  
* Use numbered lists for sequential steps, processes, or instructions.

**Keep items concise and parallel**

* Write list items as short, clear phrases or sentences.  
* Avoid using too many or too few list items.  
* Avoid nesting lists within lists unless necessary.  
* Use parallel structure (start each item with the same part of speech).

**Introduce lists clearly**

* Use a lead-in sentence or phrase to explain what the list covers.

**Use lists to improve scannability**

* Break up long paragraphs with lists to make content easier to scan.  
* Limit lists to 5–7 items when possible; split longer lists into logical groups.

**Naturally incorporate keywords**

* Where appropriate, use relevant keywords in list items to reinforce page relevance.

**Maintain consistency**

* Use consistent punctuation and capitalization for all list items.  
* Avoid mixing full sentences and fragments within the same list.

**Accessibility considerations**

* Use semantic HTML (\<ul\>, \<ol\>, \<li\>) for lists.  
* Avoid using lists for layout or decorative purposes.

### Interlinking

Links are vital for both user navigation and SEO. They help users discover related content and signal content relationships to search engines. They also serve as a means for search engine crawlers to find and index pages.

Best practices:

**Use descriptive anchor text**

* Make link text meaningful (e.g., "Monitor Configuration Reference" instead of "click here").  
* Avoid vague phrases; anchor text should describe the destination or resource.

**Prioritize internal linking**

* Link to related documentation pages to guide users and strengthen site structure.  
* Use internal links to connect related documentation pages, guiding users to deeper or related topics.  
* Regularly audit and update links to avoid broken or outdated references.  
* Consider the user journey when linking, and link outside of Docs, like to the marketing site, or blog where appropriate and relevant.

**Use external links judiciously**

* Link to reputable, authoritative sources when necessary. E.g. https://www.python.org/doc/  
* Ensure external links open in a new tab/window.

**Maintain link accessibility**

* Ensure link text is distinguishable (for example, by using color and underline).  
* Avoid Overlinking  
* Don’t overload paragraphs with multiple links—prioritize the most relevant ones.


## Multimedia

Multimedia is important because it can improve user experience, site performance, and ranking signals. It can boost user engagement and retention by providing different ways to consume information.

By adding things like image alt tags, and structured data, search engines can also pick up assets to serve them within organic search results, or use them to enhance your listing within organic search results.

Multimedia content can include images, videos, podcasts, infographics, and more. Multimedia elements enhance understanding and engagement but must be used thoughtfully for accessibility and SEO.

Best practices:  
**Use relevant visuals**

* Include screenshots, diagrams, or videos to clarify complex concepts or steps.  
* Ensure visuals directly support the surrounding content.  
* Create unique images and videos that add value to your page and avoid using stock photos.

**Optimize images for SEO**

* Avoid embedding important text inside images or videos, as search engines cannot "read" images beyond their file name and alt tag text.  
* Use descriptive file names and add an alt tag with descriptive text for all images.  
* Alt text should convey the purpose or content of the image for screen readers and search engines.  
* Images should also be exported in the size in which they are intended to be viewed to reduce page resources.  
* Compress images to balance quality and page load speed; if available, consider using web optimized files like vectors or WebP to reduce size.


**Ensure accessibility**

* Avoid relying solely on images to convey critical information; always provide a text alternative.  
* For videos, include captions and, if possible, a transcript.

**Maintain quality and consistency**

* Use high-quality, clear images and consistent styling (e.g., borders, background).

**Reference visuals in text**

* Clearly reference images or videos in the body copy (e.g., "See Figure 1" or "Watch the setup video below").

**Cite sources when needed**

* If using third-party visuals, ensure you have permission and provide appropriate attribution.

**Consider structured data**

* Where applicable, use structured data (e.g., VideoObject, ImageObject) to help search engines understand and display multimedia in rich results.  
* Check with the documentation team for existing capabilities or implementation guidance. If you're an external contributor, open a GitHub issue to discuss implementation options.

## URLs

A URL (Uniform Resource Locator) is the web address of a page. Well-structured URLs benefit both SEO and user experience.

Having a URL that clearly reflects what the page is about, can increase click-through-rates within the search engine results page by matching the user query. The URL is also displayed to users in the top of a browser’s search bar. Allowing the URL to be clear, concise, and easy to read, supports a positive on-site experience.

URLs should not have special characters to ensure readability. They should also be lower-case to prevent issues with multiple URL versions that can signal duplicate content to search engines.

Best practices:
**Reflect the page topic**

* Use keywords that accurately describe the page’s subject.  
* Align the URL with the page title and H1 heading for consistency.

**Keep URLs short and readable**

* Avoid unnecessary words or parameters.  
* Use hyphens (-) to separate words for clarity.

**Use lowercase letters**

* Always use lowercase to prevent duplicate content issues (e.g., /Guide/ vs. /guide/).

**Avoid special characters**

* Stick to letters, numbers, and hyphens. Avoid spaces, underscores, or special symbols.

Ensure the Hierarchy is Reflected in the URL Structure

* Structure URLs to mirror the documentation’s content hierarchy, nesting child pages under their logical parent directories (e.g., /docs/solutions/security/ai/ai-assistant).  
* Ensure each child page has a valid parent URL that leads to a parent page.

## Meta keywords tag

Meta keywords are not important for SEO on Google and Bing, as they have stated that they ignore this meta tag. However, some other search engines like Yandex may still use them as a low weight ranking factor.

It’s not necessary to add, but if needed, keywords should be kept to 5 keywords, separated by commas, while avoiding repetition, and duplication.

## Content updates and maintenance

Keeping documentation accurate and up-to-date is critical for both users and SEO.

Best practices:

**Regular reviews**

* Schedule periodic audits to check for outdated information, broken links, and deprecated features.

**Versioning**

* Update or archive obsolete pages.

**Redirects**

* If removing or merging pages, set up appropriate redirects to preserve SEO value and user experience.  
  * If a page is being moved, submit a redirect request for the old URL to the new URL. For internal contributors, contact the documentation team. For external contributors, include redirect information in your pull request or open a GitHub issue.

**User feedback**

* Review user feedback to identify unclear or outdated sections.

## Mobile performance and usability

Search engines prioritize mobile usability, and "reference" the mobile viewport for all content on the web. Prior to publishing ensure that all elements on-page are visible to users and search engines. If content is visible on desktop and not mobile, search engines will ignore that content, which could cause it to miss out on critical information that can help the page get picked up, understood, and indexed within organic search.

Best practices:

**Test functionality**

* Review pages on various mobile devices to confirm all features, navigation, and media display correctly.

**Readable text**

* Use legible font sizes and sufficient line spacing for mobile screens.  
* Do not deviate from template styles.  
* If new functionality is needed, discuss with the documentation team before implementing. External contributors should open a GitHub issue to propose new functionality.

**Accessible interactions**

* Make sure buttons, links, and interactive elements are easy to tap.

**Optimize media**

* Compress images and avoid large files that can slow down mobile load times.

**Avoid horizontal scrolling**

* Content should fit within the screen width without requiring users to scroll sideways.

## Content localization and SEO

Localization is not currently in scope for all Documentation content. If localization is needed there are SEO considerations that should be followed.

Best practices:

**Write in clear, simple language**

* Avoid idioms, slang, or cultural references that may not translate well.  
* Ensure that content is translated by an expert of that language.

**Consistent terminology**

* Use consistent technical terms and product names throughout the documentation.

**Customize visuals**

* Use images that are culturally appropriate and relevant to the respective language and region.  
  * E.g., do not use English-USA language graphics if taking English-USA targeted content for a localization effort that does not use USA English.  
* Allow for text expansion in UI elements, lists, and tables, as some languages require more space.

**Link to localized resources**

* When linking or displaying resources, use those respective to the user’s region and language.

**Update HTML lang attribute**

* HTML Lang tag should be updated to reflect respective language and regional targeting.

**Use unicode characters**

* Ensure content and code samples support international character sets.

**Hreflang tag support required**

* Hreflang tags signal language and region to search engines in order to surface and index them within respective search results.  
* Consult with the documentation team for implementation guidance. External contributors should open a GitHub issue to discuss hreflang implementation.

## Elastic Docs SEO checklist

**Headings**

- [ ] H1 is unique, concise, & clearly states the page’s main topic or purpose  
- [ ] Only one H1 is used per page  
- [ ] H1 includes the primary keyword & matches the page focus  
- [ ] H2s break content into logical, descriptive sections  
- [ ] H2s & H3s are unique, not vague or duplicative  
- [ ] Headings use proper order & hierarchy  
- [ ] Headings reflect the content that follows  
- [ ] Headings are not used solely for styling

**Introductory paragraph**

- [ ] First paragraph summarizes the page in 1–3 sentences  
- [ ] States what users will learn or accomplish  
- [ ] Naturally includes primary & secondary keywords  
- [ ] Addresses user intent & context  
- [ ] Uses clear, plain language (defines jargon if needed)  
- [ ] First sentence is suitable for meta description (concise, relevant, actionable)

**Body copy**

- [ ] Uses accurate technical terminology; defines terms on first use  
- [ ] Written clearly & concisely  
- [ ] Uses active voice & direct instructions  
- [ ] Keywords & related terms are incorporated naturally  
- [ ] Content is organized with logical headings & subheadings  
- [ ] Provides unique value (not thin or duplicate content)  
- [ ] Includes examples, code snippets, or visuals where helpful  
- [ ] Uses bullet points, numbered lists, & callouts for scannability  
- [ ] Structured data is added where applicable (consult engineering if unsure)  
- [ ] Links to related documentation or authoritative external sources  
- [ ] Content is up-to-date & regularly reviewed

**Content length and structure**

- [ ] Content fully answers the user’s question or task (not padded or too brief)  
- [ ] Long topics are broken into focused, navigable pages  
- [ ] Paragraphs are short & easy to scan  
- [ ] Visual breaks (callouts, asides) are used for emphasis, but not overused

**Lists**

- [ ] Lists use the correct type (bulleted for unordered, numbered for steps)  
- [ ] List items are concise, parallel, & consistent  
- [ ] Lead-in sentence introduces each list  
- [ ] Lists are not excessively long or nested  
- [ ] Semantic HTML is used for lists  
- [ ] Keywords are included naturally

**Interlinking (internal and external links)**

- [ ] Anchor text is descriptive & meaningful  
- [ ] Internal links guide users to related or deeper documentation  
- [ ] External links point to reputable, relevant sources & open in a new tab  
- [ ] No broken or outdated links  
- [ ] Links are not excessive or distracting  
- [ ] Link text is visually distinguishable & accessible

**Multimedia (images and video)**

- [ ] Visuals (images, diagrams, videos) directly support the content  
- [ ] Images are unique, high-quality, & not stock photos  
- [ ] Image file names are descriptive, lowercase, & use hyphens  
- [ ] Images are compressed/optimized for web  
- [ ] Alt text accurately describes each image’s purpose  
- [ ] No important text is embedded in images  
- [ ] Videos are relevant, compressed, & include captions/transcripts  
- [ ] Visuals are referenced in the body copy  
- [ ] Third-party visuals are properly attributed  
- [ ] Structured data is used for multimedia where possible

**URLs**

- [ ] URL is short, descriptive, & reflects the page’s topic  
- [ ] Uses lowercase letters & hyphens (no spaces, underscores, or special characters)  
- [ ] URL structure mirrors the documentation hierarchy (`/docs/section/topic/`)  
- [ ] Each child page has a valid parent page  
- [ ] URL matches the H1 & page focus  
- [ ] Canonical tag is set to the preferred URL

**Meta keywords tag**

- [ ] No more than 5 unique, relevant keywords (comma-separated)  
- [ ] No repetition or duplication  
- [ ] Keywords are specific to the page topic

**Content updates and maintenance**

- [ ] Content is reviewed regularly for accuracy & relevance  
- [ ] Versioning is clearly indicated where applicable  
- [ ] Change log or last-updated date is included  
- [ ] Redirects are set up for removed or merged pages  
- [ ] User feedback is reviewed & acted on

**Mobile performance and usability**

- [ ] Pages are tested on various mobile devices  
- [ ] All features, navigation, & media are visible & functional on mobile  
- [ ] Text is readable & interactive elements are easy to tap  
- [ ] Images & media are optimized for fast mobile loading  
- [ ] No horizontal scrolling is required

**Final content review**

- [ ] Checklist items have been reviewed  
- [ ] Content is written with the user in mind  
- [ ] Content is enhanced for search engine "readability"
